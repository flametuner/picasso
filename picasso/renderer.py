
from .config import PARALLELISM, RENDERER_IMAGE, WORKER_NAME, NAMESPACE, BUCKET_PATH_INPUT
from .job_manager import JobConfig, JobManager, KubernetesConfig
from kubernetes.client import BatchV1Api
from kubernetes.client.models import V1Toleration, V1Affinity, V1NodeAffinity, V1NodeSelector, V1NodeSelectorTerm, V1NodeSelectorRequirement



class Renderer():

    def __init__(self, client: BatchV1Api, batches: int, name: str) -> None:
        self.manager = JobManager(client, NAMESPACE)
        self.name = name.replace("_", "-")
        self.batches = batches
        self.config = KubernetesConfig(
            name=self.name,
            namespace=NAMESPACE,
            labels={"app": "renderer"},
            annotations={"app": "renderer"},
            service_account="picasso-account",
            affinity=V1Affinity(
                node_affinity=V1NodeAffinity(
                    required_during_scheduling_ignored_during_execution=V1NodeSelector(
                        node_selector_terms=[
                            V1NodeSelectorTerm(
                                match_expressions=[
                                    V1NodeSelectorRequirement(
                                        key="name",
                                        operator="In",
                                        values=[WORKER_NAME]
                                    )
                                ]
                            )
                        ]
                    )
                )
            ),
            tolerations=[
                V1Toleration(
                    key="gpu",
                    value="true",
                    effect="NoSchedule"
                ),
                V1Toleration(
                    key="nvidia.com/gpu",
                    value="present",
                    effect="NoSchedule"
                )
            ],
            image=RENDERER_IMAGE,
            env={
                'BLEND_FILE': 'asset.blend',
                'CONFIG_FILE': 'config.cfg',
                'BUCKET_PATH_INPUT': f'{BUCKET_PATH_INPUT}/{name}'
            },
        )
        self.job_config = JobConfig(
            completion_mode="Indexed",
            completitions=batches,
            parallelism=PARALLELISM,
            k8s_config=self.config
        )

    def create_dna(self):
        self.config.env['OPERATION'] = 'CREATE_DNA'
        self.config.name = self.name + "-create-dna"
        job_config = JobConfig(
            completion_mode="NonIndexed",
            completitions=1,
            parallelism=1,
            k8s_config=self.config
        )
        id = self.manager.create_job(job_config)
        if not self.manager.wait_for_completition(id):
            raise Exception("The created DNA stage failed")
        self.manager.delete_job(id)

    def generate_nft(self):
        self.config.env['OPERATION'] = 'GENERATE_NFT'
        self.config.name = self.name + "-generate-nft"
        parallelism = PARALLELISM
        if parallelism > self.batches:
            parallelism = self.batches
        job_config = JobConfig(
            completion_mode="Indexed",
            completitions=self.batches,
            parallelism=parallelism,
            k8s_config=self.config
        )
        id = self.manager.create_job(job_config)
        if not self.manager.wait_for_completition(id):
            raise Exception("The Generate NFT stage failed")
        self.manager.delete_job(id)

    def refactor_batches(self):
        self.config.env['OPERATION'] = 'REFACTOR_BATCHES'
        self.config.name = self.name + "-refactor-batches"
        job_config = JobConfig(
            completion_mode="NonIndexed",
            completitions=1,
            parallelism=1,
            k8s_config=self.config
        )
        id = self.manager.create_job(job_config)
        if not self.manager.wait_for_completition(id):
            raise Exception("The Refactor Batches stage failed")
        self.manager.delete_job(id)
