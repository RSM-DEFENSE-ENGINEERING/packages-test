aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 216570687663.dkr.ecr.us-east-1.amazonaws.com
docker build -t prod/agent-uploader .
docker tag prod/agent-uploader:latest 216570687663.dkr.ecr.us-east-1.amazonaws.com/prod/agent-uploader:latest
docker push 216570687663.dkr.ecr.us-east-1.amazonaws.com/prod/agent-uploader:latest
