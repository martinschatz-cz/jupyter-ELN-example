FROM condaforge/miniforge3:latest

WORKDIR /home/jovyan/work
COPY environment.yml .

# Install environment and the RISE extension
RUN conda env create -f environment.yml && \
    conda clean -afy

# Standardize path
ENV PATH /opt/conda/envs/jp_eln_env/bin:$PATH

# Register kernel
RUN python -m ipykernel install --user --name jp_eln_env --display-name "Python (ELN Env)"

COPY . .
EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]