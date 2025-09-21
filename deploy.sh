#!/bin/bash
# Deployment script for MisInfo Detector on Google Cloud Run

# Set project configuration
PROJECT_ID="your-project-id"
SERVICE_NAME="misinformation-detector"
REGION="us-central1"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "🚀 Deploying MisInfo Detector to Google Cloud Run..."

# Step 1: Authenticate with Google Cloud (if not already done)
echo "📝 Please ensure you're authenticated with Google Cloud:"
echo "   gcloud auth login"
echo "   gcloud config set project $PROJECT_ID"
echo ""

# Step 2: Enable required APIs
echo "🔧 Enabling required Google Cloud APIs..."
gcloud services enable cloudbuild.googleapis.com
 gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Step 3: Build and push Docker image
echo "🏗️ Building Docker image..."
gcloud builds submit --tag $IMAGE_NAME

# Step 4: Create secret for API key
echo "� Creating secret for Gemini API key..."
echo "Please enter your Google Gemini API key:"
read -s GEMINI_API_KEY
echo $GEMINI_API_KEY | gcloud secrets create gemini-api-key --data-file=-

# Step 5: Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 8080 \
    --memory 2Gi \
    --cpu 1 \
    --timeout 300 \
    --concurrency 100 \
    --max-instances 10 \
    --set-env-vars="FLASK_ENV=production" \
    --set-secrets="GOOGLE_API_KEY=gemini-api-key:latest"

# Step 6: Get the service URL
echo "✅ Deployment complete!"
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)')
echo "🌐 Your application is live at: $SERVICE_URL"
echo ""
echo "� Use this URL for your hackathon submission!"
echo "🎯 Demo URL: $SERVICE_URL"
echo "🔍 Health Check: $SERVICE_URL/api/health"
echo ""
echo "� Next Steps:"
echo "1. Test your deployed application"
echo "2. Record your demo video"
echo "3. Submit to the hackathon!"
