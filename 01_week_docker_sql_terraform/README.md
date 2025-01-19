### HOMEWORK 1 Answers & Explanations

## Q1. Understanding Docker first run

- Command used: `docker run -i --entrypoint /bin/bash python:3.12.8`
- Docker downloads the python:3.12.8 image from Docker Hub and runs the container on my local machine. The entrypoint is set to the default bash shell, so that I can find out the version of pip being used.
- Find the version of pip inside this image: `pip --version`
- For our case, the result is `pip 24.3.1`
