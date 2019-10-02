# Use a build image first to build the project with dev dependencies
FROM continuumio/miniconda3:4.7.10-alpine AS build

USER root
RUN apk add --update bash
SHELL [ "/bin/bash", "-c" ]

COPY environment.yml /environment.yml

RUN /opt/conda/bin/conda init bash && \
    /opt/conda/bin/conda update -n base -c defaults conda && \
    /opt/conda/bin/conda env create -f /environment.yml && \
    /opt/conda/bin/conda shell.bash activate stayapp && \
    /opt/conda/bin/conda clean -afy

ENV PATH "/opt/conda/envs/stayapp/bin:$PATH"

COPY app /app
WORKDIR /app

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0" ]