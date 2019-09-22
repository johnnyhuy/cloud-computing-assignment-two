# Use a build image first to build the project with dev dependencies
FROM jfloff/alpine-python:3.7-slim AS build

# Setup virtual env to build
RUN python -m venv /opt/venv
COPY app /app
WORKDIR /app
ENV PATH="/opt/venv/bin:$PATH"
RUN apk add --update alpine-sdk freetype-dev
RUN pip install --requirement requirements.txt


# Then use a "skinny" image to deploy the application
FROM tiangolo/uwsgi-nginx-flask:python3.7-alpine3.8 AS runtime

RUN apk add --update libstdc++

# Copy over build artifacts from the previous image
COPY --from=build /opt/venv /opt/venv
ENV PYTHONPATH="/opt/venv/lib/python3.7/site-packages/:$PYTHONPATH"
ENV PATH="/opt/venv/bin:$PATH"
ENV FLASK_APP="app/main.py"

COPY app /app

CMD [ "flask", "run", "--host=0.0.0.0" , "--port=80" ]

