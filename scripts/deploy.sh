#!/bin/bash
# WealthAlloc Deployment Script

set -e

echo "================================"
echo "WealthAlloc Deployment"
echo "================================"

# Build Docker image
echo "Building Docker image..."
docker build -t wealthalloc/api:latest .

# Push to registry
echo "Pushing to Docker registry..."
docker push wealthalloc/api:latest

# Apply Kubernetes configs
echo "Deploying to Kubernetes..."
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/configmap.yaml
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/ingress.yaml
kubectl apply -f kubernetes/hpa.yaml

# Wait for rollout
echo "Waiting for deployment rollout..."
kubectl rollout status deployment/wealthalloc-api -n wealthalloc

# Verify deployment
echo "Verifying deployment..."
kubectl get pods -n wealthalloc
kubectl get svc -n wealthalloc
kubectl get ingress -n wealthalloc

echo "================================"
echo "Deployment Complete!"
echo "================================"
echo "API Endpoint: https://api.wealthalloc.com"
echo "Health Check: https://api.wealthalloc.com/health"
echo "API Docs: https://api.wealthalloc.com/api/docs"
