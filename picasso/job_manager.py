

from dataclasses import dataclass
from time import sleep
from typing import cast

from kubernetes import client
from kubernetes.client import BatchV1Api
from kubernetes.client.models import (V1Affinity, V1EnvVar, V1Job, V1JobStatus,
                                      V1ResourceRequirements, V1Toleration)

from .config import JOB_CPU, JOB_GPU, JOB_MEMORY


@dataclass
class KubernetesConfig:

    # metadata information
    name: str
    namespace: str
    labels: dict[str, str]
    annotations: dict[str, str]

    service_account: str

    # pod information
    affinity: V1Affinity
    tolerations: list[V1Toleration]

    # container information
    image: str
    env: dict[str, str]


@dataclass
class JobConfig:
    k8s_config: KubernetesConfig
    parallelism: int
    completitions: int
    completion_mode: str


POLL_INTERVAL = 5
# twenty four hours
POLL_RETRY = 17280


class JobManager:

    def __init__(self, client: BatchV1Api, namespace: str):
        self.client = client
        self.namespace = namespace

    def create_job(self, job_config: JobConfig):
        definition = self._definition_from_config(job_config)
        self.client.create_namespaced_job(
            self.namespace, body=definition)
        return job_config.k8s_config.name

    def _pod_spec_from_config(self, k8s_config: KubernetesConfig):
        envs = []
        for key, value in k8s_config.env.items():
            envs.append(V1EnvVar(
                name=key,
                value=value,
            ),)

        return client.V1PodSpec(
            service_account=k8s_config.service_account,
            tolerations=k8s_config.tolerations,
            affinity=k8s_config.affinity,
            restart_policy="OnFailure",
            containers=[
                client.V1Container(
                    name=k8s_config.name,
                    image=k8s_config.image,
                    env=envs,
                    resources=V1ResourceRequirements(
                        requests={
                            'memory': JOB_MEMORY,
                            'cpu': JOB_CPU
                        },
                        limits={
                            'memory': JOB_MEMORY,
                            'cpu': JOB_CPU,
                            'nvidia.com/gpu': JOB_GPU
                        }
                    ),
                )
            ]
        )

    def _definition_from_config(self, job_config: JobConfig):
        k8s_config = job_config.k8s_config
        spec = self._pod_spec_from_config(k8s_config)
        return client.V1Job(
            metadata=client.V1ObjectMeta(
                name=k8s_config.name,
                namespace=self.namespace,
                labels=k8s_config.labels,
                annotations=k8s_config.annotations
            ),
            spec=client.V1JobSpec(
                template=client.V1PodTemplateSpec(
                    spec=spec
                ),
                completion_mode=job_config.completion_mode,
                completions=job_config.completitions,
                parallelism=job_config.parallelism
            ),
        )

    def get_job_status(self, name: str):
        job = cast(V1Job, self.client.read_namespaced_job_status(name, self.namespace))
        return cast(V1JobStatus, job.status)

    def delete_job(self, name: str):
        return self.client.delete_namespaced_job(
            name,
            self.namespace,
            propagation_policy="Background",
            grace_period_seconds=0
        )

    def wait_for_completition(self, job_id: str):
        for _ in range(POLL_RETRY):
            status = self.get_job_status(job_id)
            print(status)
            if status.completion_time:
                print(status.completion_time - status.start_time)
                return True
            elif status.conditions:
                print(status.conditions)
                return False
            else:
                sleep(POLL_INTERVAL)
        return False
