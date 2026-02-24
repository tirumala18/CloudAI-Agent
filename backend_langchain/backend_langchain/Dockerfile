FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
# Install PyTorch CPU specifically so it doesn't pull a 3GB CUDA package
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
