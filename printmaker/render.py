

import subprocess
from dataclasses import dataclass
from enum import Enum
from os import mkdir, path

BLEND_MY_NFT_PATH = "./addon/__init__.py"


class Operation(Enum):
    CREATE_DNA = "create-dna"
    GENERATE_NFT = "generate-nfts"
    REFACTOR_BATCHES = "refactor-batches"


@dataclass
class RenderConfig:
    blend_file_path: str
    config_file_path: str
    save_path: str
    operation: Operation

    batch_data: str
    batch_number: int = 1
    logic_file_path: str = ""


def render(config: RenderConfig):
    args = []

    if config.logic_file_path:
        args.extend(["--logic-file", config.logic_file_path])

    if not path.exists(config.batch_data):
        mkdir(config.batch_data)

    if path.isfile(config.batch_data):
        raise KeyError("Batch data is not a folder")
    cmd = ["blender",
           "--background",
           config.blend_file_path,
           "-E",
           "CYCLES",
           "--python",
           BLEND_MY_NFT_PATH,
           "--",
           "--config-file",
           config.config_file_path,
           "--save-path",
           config.save_path,
           "--operation",
           config.operation.value,
           "--batch-data",
           config.batch_data,
           "--batch-number",
           str(config.batch_number),
           ]
    cmd.extend(args)

    result = subprocess.run(cmd)
    return result.returncode
