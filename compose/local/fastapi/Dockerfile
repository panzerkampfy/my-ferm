FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

WORKDIR /app/

# Requirements are installed here to ensure they will be cached.
COPY requirements.txt /requirements
RUN pip install -r /requirements

COPY ./compose/local/fastapi/entrypoint /entrypoint
RUN chmod +x /entrypoint

ENTRYPOINT ["/entrypoint"]
