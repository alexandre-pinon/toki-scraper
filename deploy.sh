#!/bin/bash

PROJECT_ID=$(gcloud config get project)
REGION="europe-west9" 
SERVICE_NAME="toki-scraper"
GIT_SHA=$(git rev-parse --short HEAD)

gcloud functions deploy ${SERVICE_NAME} \
  --region=${REGION} \
  --project=${PROJECT_ID} \
  --allow-unauthenticated \
  --memory=256Mi \
  --cpu=0.25 \
  --min-instances=0 \
  --max-instances=2 \
  --update-labels="git-sha=${GIT_SHA},app=${SERVICE_NAME}" \
  --service-account="${SERVICE_NAME}-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
  --runtime python312 \
  --trigger-http \
  --entry-point scrape_recipe \

# Verify deployment
echo "Verifying deployment..."
gcloud functions describe ${SERVICE_NAME} \
  --region=${REGION} \
  --format='get(status.url)'