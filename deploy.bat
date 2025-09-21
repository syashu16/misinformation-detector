@echo off
REM Deployment script for Google Cloud Run (Windows)
REM Usage: deploy.bat [PROJECT_ID]

setlocal enabledelayedexpansion

REM Configuration
if "%1"=="" (
    set PROJECT_ID=your-project-id
) else (
    set PROJECT_ID=%1
)
set SERVICE_NAME=misinformation-detector
set REGION=us-central1
set IMAGE_NAME=gcr.io/%PROJECT_ID%/%SERVICE_NAME%

echo 🚀 Starting deployment to Google Cloud Run...
echo Project ID: %PROJECT_ID%
echo Service Name: %SERVICE_NAME%
echo Region: %REGION%

REM Check if gcloud is installed
where gcloud >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ❌ Google Cloud SDK (gcloud) is not installed. Please install it first.
    exit /b 1
)

REM Check if docker is installed
where docker >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ❌ Docker is not installed. Please install it first.
    exit /b 1
)

REM Set the project
echo 📋 Setting Google Cloud project...
gcloud config set project %PROJECT_ID%

REM Enable required APIs
echo 🔧 Enabling required Google Cloud APIs...
gcloud services enable cloudbuild.googleapis.com run.googleapis.com containerregistry.googleapis.com secretmanager.googleapis.com

REM Build and push the Docker image
echo 🐳 Building Docker image...
docker build -t %IMAGE_NAME% .

echo 📤 Pushing image to Google Container Registry...
docker push %IMAGE_NAME%

REM Create secrets if they don't exist
echo 🔐 Setting up secrets...

REM Check if Gemini API key secret exists
gcloud secrets describe gemini-api-key --quiet >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Creating Gemini API key secret...
    set /p GEMINI_API_KEY="Please enter your Gemini API key: "
    echo !GEMINI_API_KEY! | gcloud secrets create gemini-api-key --data-file=-
) else (
    echo Gemini API key secret already exists.
)

REM Check if News API key secret exists
gcloud secrets describe news-api-key --quiet >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Creating News API key secret...
    set /p NEWS_API_KEY="Please enter your News API key (or press Enter to skip): "
    if "!NEWS_API_KEY!"=="" (
        echo dummy | gcloud secrets create news-api-key --data-file=-
    ) else (
        echo !NEWS_API_KEY! | gcloud secrets create news-api-key --data-file=-
    )
) else (
    echo News API key secret already exists.
)

REM Replace PROJECT_ID in cloudrun.yaml and deploy
echo ☁️ Deploying to Cloud Run...
powershell -Command "(Get-Content cloudrun.yaml) -replace 'PROJECT_ID', '%PROJECT_ID%' | Set-Content cloudrun-deploy.yaml"

gcloud run services replace cloudrun-deploy.yaml --region=%REGION%

REM Get the service URL
for /f "delims=" %%i in ('gcloud run services describe %SERVICE_NAME% --region=%REGION% --format="value(status.url)"') do set SERVICE_URL=%%i

echo ✅ Deployment completed successfully!
echo 🌐 Service URL: %SERVICE_URL%
echo.
echo 📋 Next steps:
echo 1. Test the service at: %SERVICE_URL%
echo 2. Set up custom domain (optional)
echo 3. Configure additional monitoring and alerts
echo.
echo 🔧 Useful commands:
echo - View logs: gcloud logs tail "resource.type=cloud_run_revision AND resource.labels.service_name=%SERVICE_NAME%" --project=%PROJECT_ID%
echo - Update service: deploy.bat %PROJECT_ID%
echo - Delete service: gcloud run services delete %SERVICE_NAME% --region=%REGION%

REM Clean up temporary file
del cloudrun-deploy.yaml >nul 2>nul

echo.
echo 🎉 Happy misinformation detecting!

pause
