FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

# RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN pip install langchain_nvidia_ai_endpoints
RUN pip install llama_index
RUN pip install langchain_core
RUN pip install dotenv-python
RUN pip install fastapi
RUN pip install pydantic
RUN pip install llama-index-embeddings-huggingface
RUN pip install llama-index-llms-langchain

RUN useradd -m -u 1000 appuser

USER appuser

ENV HOME=/home/appuser \
    PATH=/home/appuser/.local/bin:$PATH

# Set the working directory to the user's home directory
WORKDIR $HOME/app

# Copy the current directory contents into the container at the working directory
COPY --chown=appuser . $HOME/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]

    