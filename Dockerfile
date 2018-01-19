FROM node_env
COPY dist/*.js ./
COPY run-docker.sh ./
CMD ./run-docker.sh
