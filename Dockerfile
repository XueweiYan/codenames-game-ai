# 1) choose base container
# base notebook, contains Jupyter and relevant tools
ARG BASE_CONTAINER=ucsdets/datahub-base-notebook:2021.2-stable

FROM $BASE_CONTAINER

LABEL maintainer="UC San Diego ITS/ETS <ets-consult@ucsd.edu>"


USER root

RUN echo 'jupyter notebook "$@"' > /run_jupyter.sh && chmod 755 /run_jupyter.sh


USER jovyan

RUN pip install --no-cache-dir numpy termcolor argparse tqdm nltk gensim bs4 lxml



