#!/bin/bash

set -e

# Define variables
APP_NAME="my_web_app"
DOCKER_IMAGE="my_web_app_image"
DOCKER_CONTAINER="my_web_app_container"
DATABASE_URL="postgresql://user:password@localhost:5432/mydatabase"
NEXT_PUBLIC_API_URL="http://localhost:8000"
AWS_REGION="us-east-1"
S3_BUCKET="my-web-app-bucket"
ECR_REPO="my_web_app_repo"

# Function to build and push Docker image
build_and_push_docker_image() {
    echo "Building Docker image..."
    docker build -t $DOCKER_IMAGE .

    echo "Logging in to AWS ECR..."
    aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO

    echo "Tagging Docker image..."
    docker tag $DOCKER_IMAGE:latest $ECR_REPO:latest

    echo "Pushing Docker image to ECR..."
    docker push $ECR_REPO:latest
}

# Function to deploy the application
deploy_application() {
    echo "Deploying application..."
    docker run -d --name $DOCKER_CONTAINER -e DATABASE_URL=$DATABASE_URL -e NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL $DOCKER_IMAGE
}

# Function to set up S3 bucket
setup_s3_bucket() {
    echo "Setting up S3 bucket..."
    aws s3api create-bucket --bucket $S3_BUCKET --region $AWS_REGION --create-bucket-configuration LocationConstraint=$AWS_REGION || echo "Bucket may already exist."
}

# Function to run database migrations
run_migrations() {
    echo "Running database migrations..."
    # Assuming migrations are handled by Alembic
    alembic upgrade head
}

# Main script execution
echo "Starting deployment setup..."

setup_s3_bucket
build_and_push_docker_image
run_migrations
deploy_application

echo "Deployment setup completed successfully."