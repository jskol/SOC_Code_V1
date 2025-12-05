# syntax=docker/dockerfile:1


FROM ubuntu:latest

WORKDIR /app

ARG UID=10001
RUN apt-get update &&\
	apt-get install -y adduser &&\
	apt-get install -y \
	python3 \
	python3-pip \
    python3-venv \
	build-essential && \
	rm -rf /var/lib/apt/lists/*

RUN python3 -m venv .venv
ENV PATH="/app/.venv/bin:$PATH"
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt


COPY app ./app/
COPY out ./out/

# Run the application.
ENTRYPOINT [ "python3", "app/main.py"]
CMD ["-h"]
#CMD ["/bin/bash"]

