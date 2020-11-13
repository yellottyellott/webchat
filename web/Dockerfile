FROM python:latest

ENV PYTHONDONTWRITEBYTECODE="1"

COPY requirements.txt /src/requirements.txt
RUN pip install --no-deps -r /src/requirements.txt

COPY . /src
WORKDIR /src
CMD ["/src/main.py"]
