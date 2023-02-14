from os import environ

from dotenv import load_dotenv

from printmaker.render import Operation

load_dotenv()

BLEND_FILE = "asset.blend"
CONFIG_FILE = "config.cfg"
INDEX = int(environ.get("JOB_COMPLETION_INDEX", 0)) + 1
BUCKET_PATH = environ.get("BUCKET_PATH_INPUT", "")
OPERATION = Operation[environ.get("OPERATION", "CREATE_DNA")]
BUCKET_SOURCE = environ.get("BUCKET_SOURCE", "True") == "True"