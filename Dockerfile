FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml .
COPY uv.lock .

RUN uv pip install --system --no-cache -r pyproject.toml

COPY app.py .
COPY model.pkl .

EXPOSE 8080

CMD ["python", "app.py"]
