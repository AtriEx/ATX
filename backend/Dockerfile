FROM python:3.12

EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=15s --start-period=5s --retries=2 CMD ["curl", "-sfo", "/dev/null", "http://localhost:8000/health"]

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
