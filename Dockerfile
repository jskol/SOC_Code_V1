# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7
FROM ubuntu:22.04

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN apt-get update &&\
	apt-get install -y adduser &&\
	apt-get install -y \
	python3 \
	python3-pip \
	build-essential && \
	rm -rf /var/lib/apt/lists/*

RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

#RUN chown -R appuser:appuser /app

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.


#RUN --mount=type=cache,target=/root/.cache/pip \
#    --mount=type=bind,source=requirements.txt,target=requirements.txt \
#RUN python3 -m venv /app/venv
#ENV PATH="/app/venv/bin:$PATH"
COPY requirements.txt .
RUN pip3 install -r requirements.txt


# Switch to the non-privileged user to run the application.
#USER appuser
WORKDIR /app

# Copy the source code into the container.
COPY app ./app
COPY out ./out

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
ENTRYPOINT [ "python3", "app/main.py"]
CMD ["-h"]
#CMD ["/bin/bash"]

