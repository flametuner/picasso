from os import environ

from dotenv import load_dotenv

load_dotenv()

JOB_BATCHES = int(environ.get("JOB_BATCHES", 10))
PARALLELISM = int(environ.get("PARALLELISM", 64))


JOB_ASSET_FOLDER = environ.get("JOB_ASSET_FOLDER", "assets")
NAMESPACE = environ.get("NAMESPACE", "picasso")

BUCKET_PATH_INPUT = environ.get("BUCKET_PATH_INPUT", "")
RENDERER_IMAGE = environ.get("RENDERER_IMAGE", "gustainacio/printmaker")
WORKER_NAME = environ.get("WORKER_NAME", "picasso-worker")
JOB_MEMORY = environ.get("JOB_MEMORY","4G")
JOB_CPU = environ.get("JOB_CPU","3")
JOB_GPU = environ.get("JOB_GPU","1")