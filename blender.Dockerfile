FROM nytimes/blender as deps

# Install dependencies
# RUN apt-get update && apt-get install -y \
#     curl \
#     python3.10 \
#     python3-pip \
#     && rm -rf /var/lib/apt/lists/*

# Downloading gcloud package
RUN curl -sSL https://sdk.cloud.google.com | bash

ENV PATH $PATH:/root/google-cloud-sdk/bin

WORKDIR /nft

ENV BLEND_MY_NFT_VERSION=4.5.1
ENV BLEND_MY_NFT=Blend_My_NFT
ENV BLEND_MY_NFT_FILE=v$BLEND_MY_NFT_VERSION.tar.gz
ENV BLEND_MY_NFT_FOLDER=Blend_My_NFTs-$BLEND_MY_NFT_VERSION

RUN wget https://github.com/torrinworx/Blend_My_NFTs/archive/refs/tags/$BLEND_MY_NFT_FILE && \
    tar -xvf $BLEND_MY_NFT_FILE && \
    mv $BLEND_MY_NFT_FOLDER addon && \
    rm $BLEND_MY_NFT_FILE


ENTRYPOINT [ "python3.10", "-m"]

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

COPY ./printmaker/ ./printmaker/

CMD ["printmaker"]