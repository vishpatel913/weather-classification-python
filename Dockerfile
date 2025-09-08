# FROM python:3.11-slim
FROM public.ecr.aws/lambda/python:3.11

# ENV PYTHONDONTWRITEBYTECODE=1 \
#     PYTHONUNBUFFERED=1 \
#     PYTHONPATH=/

# Copy requirements first for better caching
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}" -U --no-cache-dir

# Copy application code
COPY ./app ${LAMBDA_TASK_ROOT}/app
# COPY .env.docker ${LAMBDA_TASK_ROOT}/.env

# EXPOSE 8080
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
CMD ["app.main.handler"]