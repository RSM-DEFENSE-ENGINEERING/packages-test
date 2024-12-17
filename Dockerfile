# Use the official AWS Lambda Python base image
FROM public.ecr.aws/lambda/python:3.9

# Install system dependencies for Poetry and Git
RUN yum install -y git gcc python3-devel libffi-devel make && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/bin/poetry

# Set environment variables for Poetry
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# Set the working directory for the application
WORKDIR /var/task

# Copy the Poetry configuration files
COPY pyproject.toml poetry.lock ./

# Install Python dependencies using Poetry
RUN poetry install --no-dev

# Copy the source code
COPY src/ ./

# Copy the function handler (if `lambda_function.py` is in `src/`, adjust the path accordingly)
COPY src/lambda_function.py ./lambda_function.py

# Optional: Set up SSH for Git (if needed)
RUN mkdir -p /root/.ssh && chmod 700 /root/.ssh
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

# Set the Lambda function handler path
CMD ["lambda_function.lambda_handler"]

