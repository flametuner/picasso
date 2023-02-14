from kubernetes import client as kubeclient, config
from .config import JOB_ASSET_FOLDER, JOB_BATCHES

from .renderer import Renderer

# Configs can be set in Configuration class directly or using helper utility
try:
    config.load_incluster_config()
except:
    config.load_kube_config()

client = kubeclient.BatchV1Api()


def execute_printmaker():
    print("Starting script...")
    renderer = Renderer(client, JOB_BATCHES, JOB_ASSET_FOLDER)

    print("Generating DNA")
    renderer.create_dna()
    print("DNA generated.")


    print("Begin rendering process...")
    renderer.generate_nft()
    print("Successfully rendered.")

    print("Refactoring nft folder...")

    renderer.refactor_batches()

    print("Refactored the NFT folder")

    print("Nfts generated with success!")


