# Picasso

Create NFTs from Blender files using Blend My NFT addon and Kubernetes.

## Prerequisites
- Kubernetes
- Python 3
- Blender 3.0


## Installing Kubernetes Resources

First of all you need to create the Kubernetes Resources. You can do this by executing the following command:

```bash
kubectl apply -f kubernetes/
```

It will create the following resources:
-   A namespace called `picasso`
-   A service account called `picasso-account` with the `cluster-admin` role

The service account will be used by the Python script to create the Kubernetes Jobs.

## How it works

The `Picasso` script will create a Kubernetes Job in `Indexed` mode. The Kubernetes Job is important because it will allow us to scale the number of workers that will be used to render the NFTs. It also have failover capabilities in case one of the workers fails.

The Kubernetes Job will use `printmaker` as the image. This image is a custom image that contains Blender 3.0 and the Blend My NFT addon. It also have a custom script for spawning the addon and managing the Blender file, the configuration file and the logic from a GCP bucket.


## Environment variables 

The following environment variables are required to run the script:

| Name | Description | Required | Default |
| --- | --- | --- | --- |
| `BUCKET_PATH_INPUT` | The GCP bucket URL | Yes | - |
| `JOB_BATCHES` | The number of batches to be created | Yes | - |
| `PARALLELISM` | The number of parallel jobs to be created | Yes | - |
| `JOB_ASSET_FOLDER` | The folder where the asset, cfg and logic is located | No | `"assets"` |
| `NAMESPACE` | The namespace where the job will be created | No | `"picasso"` |
| `JOB_MEMORY` | The memory that will be allocated to the job | No | `"4Gi"` |
| `JOB_CPU` | The CPU that will be allocated to the job | No | `"3"` |
| `JOB_GPU` | The GPU that will be allocated to the job | No | `"1"` |
| `WORKER_NAME` | The name of the worker | No | `"picasso-worker"` |
| `RENDERER_IMAGE` | The image that will be used to render the NFTs | No | `"gustainacio/printmaker"` |

### Upload the asset to GCP

First of all, create a folder (`JOB_ASSET_FOLDER`) in the GCP bucket. This folder will be used to store the asset(`asset.blend`), the configuration file (`config.cfg`) and the logic (`logic.json`). The folder name will be used as the asset name. Use the exact name as described.

## Running local

### Building the printmaker image locally
```bash
docker build -t printmaker -f blender.Dockerfile .
```

### Execute docker local

Note: if you have a GPU, you need to install the [Nvidia Docker](#resources) and use the `--gpus all` flag.

```bash
docker run -it --gpus all -v $(pwd)/assets:/nft/assets printmaker assets/<asset name> <create-dna | generate-nfts>
```


## Resources
- [Blender image](https://hub.docker.com/layers/nytimes/blender)
- [Nvidia Docker](https://github.com/NVIDIA/nvidia-docker)
- [How to install addons via Python](https://blender.stackexchange.com/questions/73759/install-addons-in-headless-blender)
- [Blend My NFT addon](https://github.com/torrinworx/Blend_My_NFTs)
- [Kubernetes Client](https://github.com/kubernetes-client/python)
- Render command
    ```bash
    ./blender --background <path to your .blend file> --python <Path to Blend_My_NFTs __init__.py> -- --config-file <path to the generated config.cfg> --operation create-dna
    ```