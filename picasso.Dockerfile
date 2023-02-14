FROM python:3.10

# Install dependencies

WORKDIR /app

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

COPY ./picasso/ ./picasso/

CMD ["python3.10", "-m", "picasso"]