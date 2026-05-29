FROM python:3.13-slim
WORKDIR /app
COPY apps/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY apps/api/fonts/ ./fonts/
COPY . /workspace
ENV PYTHONPATH=/workspace
EXPOSE 8000
CMD ["uvicorn", "apps.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
