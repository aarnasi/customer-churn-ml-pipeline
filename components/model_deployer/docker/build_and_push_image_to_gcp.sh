# Set environment variables
PROJECT_ID=<PROJECT_ID>
REGION=us-central1

# Enable required services
gcloud services enable run artifactregistry.googleapis.com

# Create Artifact Registry repo (if not already done)
gcloud artifacts repositories create customer-churn-ml-pipeline \
  --repository-format=docker \
  --location=$REGION

# Build Docker image
gcloud builds submit --tag $REGION-docker.pkg.dev/$PROJECT_ID/customer-churn-ml-pipeline/deployer-comp