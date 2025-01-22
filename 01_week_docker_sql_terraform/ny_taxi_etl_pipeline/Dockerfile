FROM continuumio/miniconda3

WORKDIR /app

# Copy the Conda environment file into the container
COPY environment.yml /app/

# Install Conda dependencies
RUN conda env update --name base --file /app/environment.yml && conda clean --all -y

# Ensure Conda is initialized in the shell
RUN conda init bash

COPY . /app

# # Set environment variables
# ENV PATH /opt/conda/envs/my_env/bin:$PATH

# Run the ETL script
# CMD ["python", "script.py", "--user", "postgres" "--password", "postgres", "--host", "localhost", "--port", "5433", "--db", "ny_taxi"]