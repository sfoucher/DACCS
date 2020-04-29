ARG BASE_CONTAINER=jupyter/scipy-notebook
FROM $BASE_CONTAINER

LABEL maintainer="Samuel Foucher"

USER root

# Install all OS dependencies for fully functional notebook server
RUN apt-get update && apt-get clean && rm -rf /var/lib/apt/lists/*

# Switch back to jovyan to avoid accidental container runs as root
USER $NB_UID

# Install eodag
RUN cd /home/$NB_USER/work && \
    git clone https://bitbucket.org/geostorm/eodag.git && \
    cd /home/$NB_USER/work/eodag && \
    python -m pip install -r requirements-dev.txt && \
    conda install --quiet --yes ipyleaflet && \
    jupyter labextension install @jupyter-widgets/jupyterlab-manager jupyter-leaflet && \
    conda clean --all -f -y && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

