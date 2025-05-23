#!/bin/sh

echo "authenticating with aws"
aws configure

echo "Pre-Build Steps:"
echo "authenticating with AWS ECR"
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 514832027284.dkr.ecr.us-east-1.amazonaws.com

echo "Build Steps:"
echo "building image..."
docker build -t 514832027284.dkr.ecr.us-east-1.amazonaws.com/paradocx:latest --platform linux/amd64 .

echo "Post-Build steps:"
echo "pushing image to AWS ECR"
docker push 514832027284.dkr.ecr.us-east-1.amazonaws.com/paradocx:latest

echo "updating AWS ECS service..."
aws ecs update-service --cluster rag-cluster --service paradocx-service --force-new-deployment
