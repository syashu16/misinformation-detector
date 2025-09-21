# 🚀 Quick Deploy to Railway (Free)

## Step 1: Install Railway CLI
```bash
npm install -g @railway/cli
```

## Step 2: Login to Railway
```bash
railway login
```

## Step 3: Deploy
```bash
cd "c:\Users\devel\OneDrive\Desktop\Projects\genai hackathon\misinformation-detector"
railway deploy
```

## Alternative: GitHub + Railway Auto-Deploy

1. **Create GitHub Repository:**
   - Go to https://github.com/new
   - Repository name: `misinformation-detector-hackathon`
   - Make it public
   - Don't initialize with README (we have files)

2. **Push Your Code:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Google Gen AI Hackathon submission"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/misinformation-detector-hackathon.git
   git push -u origin main
   ```

3. **Deploy on Railway:**
   - Go to https://railway.app
   - Click "Start a New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will auto-detect the Python app and deploy

## Step 4: Set Environment Variables
In Railway dashboard, add:
- `GOOGLE_API_KEY` = your Gemini API key
- `PORT` = 5000

## Alternative Free Platforms:

### Render.com (Also Free)
1. Go to https://render.com
2. Connect GitHub account
3. Select "Web Service"
4. Choose your repository
5. Build Command: `pip install -r requirements.txt`
6. Start Command: `python backend/app.py`

### Heroku (Limited Free)
```bash
# Install Heroku CLI first
heroku create misinformation-detector-hackathon
git push heroku main
heroku config:set GOOGLE_API_KEY=your_key_here
```

## Quick Deploy Option: GitHub Codespaces
1. Push to GitHub
2. Open in Codespaces
3. Run the app - gives you a public URL instantly

Let's start with Railway - it's the fastest!
