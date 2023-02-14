from printmaker.config import *
from printmaker.render import Operation, RenderConfig, render
from printmaker.storage import download_from_bucket, upload_to_bucket

folder = "./"

assets_path = f"{folder}/assets"

batch_name = "batch-data"
output_name = "Blend_My_NFTs Output"

batch_path = f"{folder}/{batch_name}"
output_path = f"{folder}/{output_name}"

bucket_batch = "/".join([BUCKET_PATH, batch_name])
bucket_output = "/".join([BUCKET_PATH, "output"])

if BUCKET_SOURCE:
    download_from_bucket(BUCKET_PATH, assets_path)

    if OPERATION == Operation.GENERATE_NFT:
        download_from_bucket(bucket_batch, batch_path)
    elif OPERATION == Operation.REFACTOR_BATCHES:
        download_from_bucket("/".join([bucket_output, "Generated NFT Batches"]),
                            "/".join([output_path, "Generated NFT Batches"]), True)

config = RenderConfig(
    blend_file_path="/".join([assets_path, BLEND_FILE]),
    operation=OPERATION,
    config_file_path="/".join([assets_path, CONFIG_FILE]),
    save_path=folder,
    batch_data=batch_path,
    batch_number=INDEX
)

code = render(config)
if code != 0:
    exit(code)

if BUCKET_SOURCE:
    if OPERATION == Operation.CREATE_DNA:
        upload_to_bucket(f"./{batch_path}", bucket_batch)

        nft_data = f"NFT_Data"
        upload_to_bucket(f"{output_path}/{nft_data}",
                        "/".join([bucket_output, nft_data]))

    elif OPERATION == Operation.GENERATE_NFT:
        batch = f"Generated NFT Batches/Batch{INDEX}"
        upload_to_bucket(f"{output_path}/{batch}",
                        "/".join([bucket_output, batch]))
    else:
        collection = f"Complete_Collection"
        upload_to_bucket(f"{output_path}/{collection}",
                        "/".join([bucket_output, collection]))
