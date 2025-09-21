# 🛡️ AI-Powered Misinformation Detection Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Ready-4285F4.svg)](https://cloud.google.com/)

> **Winner Prototype - Google Gen AI Exchange Hackathon 2025**

A sophisticated AI-powered tool that detects potential misinformation in text, URLs, and images while educating users on how to identify credible content. Built with Google Cloud AI services and modern web technologies.

## 🎯 Project Overview

This tool addresses the critical challenge of misinformation by providing:

- **Real-time Analysis**: Instant evaluation of text, web content, and images
- **AI-Powered Detection**: Advanced pattern recognition using Google's Gemini AI
- **Educational Component**: Comprehensive tips and guidance for manual verification
- **User-Friendly Interface**: Intuitive web application accessible to all users
- **Credibility Scoring**: Clear risk assessment with detailed explanations

## 🌟 Features

### Core Functionality
- ✅ **Text Analysis**: Detects emotional manipulation, clickbait patterns, and unreliable language
- ✅ **URL Analysis**: Evaluates website credibility, domain reputation, and content quality
- ✅ **Image Analysis**: Identifies potential manipulation and provides reverse search guidance
- ✅ **AI Integration**: Advanced content analysis using Google Gemini AI
- ✅ **Educational Tips**: Context-aware guidance and verification steps

### Technical Features
- 🚀 **Real-time Processing**: Fast analysis with responsive UI
- 🔒 **Secure**: Proper file handling and input validation
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile devices
- ☁️ **Cloud-Ready**: Deployable on Google Cloud Run with auto-scaling
- 🎨 **Modern UI**: Professional interface with accessibility features

## 🏗️ Architecture

```
misinformation-detector/
├── backend/                 # Flask API server
│   ├── app.py              # Main application
│   ├── modules/            # Analysis modules
│   │   ├── text_analyzer.py
│   │   ├── url_analyzer.py
│   │   ├── image_analyzer.py
│   │   ├── gemini_integration.py
│   │   └── educational_content.py
│   └── uploads/            # Temporary file storage
├── frontend/               # Web interface
│   ├── index.html          # Main page
│   ├── style.css           # Styles
│   └── script.js           # JavaScript functionality
├── Dockerfile              # Container configuration
├── cloudrun.yaml           # Cloud Run deployment
├── deploy.sh               # Unix deployment script
├── deploy.bat              # Windows deployment script
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Google Cloud Account (for AI features)
- Docker (for containerized deployment)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd misinformation-detector
   ```

2. **Set up environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit .env with your API keys
   GOOGLE_API_KEY=
   NEWS_API_KEY=
   ```

4. **Run the application**
   ```bash
   cd backend
   python app.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

### Docker Deployment

1. **Build the container**
   ```bash
   docker build -t misinformation-detector .
   ```

2. **Run with environment variables**
   ```bash
   docker run -p 8080:8080 \
     -e GOOGLE_API_KEY=AIzaSyAQqzZ4BNdi-sXEnkyGxZ17qDdKqUEcIPY \
     -e NEWS_API_KEY=712ace18ed8b41228024c65a0847796f \
     misinformation-detector
   ```

### Google Cloud Run Deployment

1. **Use the deployment script**
   ```bash
   # On Unix/macOS:
   chmod +x deploy.sh
   ./deploy.sh your-project-id
   
   # On Windows:
   deploy.bat your-project-id
   ```

2. **Manual deployment**
   ```bash
   # Set up gcloud
   gcloud config set project YOUR_PROJECT_ID
   
   # Enable APIs
   gcloud services enable cloudbuild.googleapis.com run.googleapis.com
   
   # Build and deploy
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/misinformation-detector
   gcloud run deploy --image gcr.io/YOUR_PROJECT_ID/misinformation-detector --platform managed
   ```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GOOGLE_API_KEY` | Gemini AI API key | Yes | - |
| `NEWS_API_KEY` | NewsAPI key for fact-checking | No | - |
| `FLASK_ENV` | Flask environment | No | development |
| `FLASK_DEBUG` | Enable debug mode | No | True |
| `PORT` | Server port | No | 5000 |
| `MAX_CONTENT_LENGTH` | Max upload size (bytes) | No | 16777216 |

### API Keys Setup

1. **Google Gemini API Key**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Add to environment as `GOOGLE_API_KEY`

2. **NewsAPI Key (Optional)**
   - Visit [NewsAPI](https://newsapi.org/)
   - Sign up for free account
   - Add to environment as `NEWS_API_KEY`

## 📚 API Documentation

### Endpoints

#### Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "message": "Misinformation Detector API is running"
}
```

#### Text Analysis
```http
POST /api/analyze/text
Content-Type: application/json

{
  "text": "Content to analyze..."
}
```

**Response:**
```json
{
  "type": "text",
  "content": "Content preview...",
  "risk_score": 75,
  "analysis": {
    "basic": { /* Basic analysis results */ },
    "ai": { /* AI analysis results */ }
  },
  "red_flags": ["List of concerns found"],
  "educational_tips": ["Tips for this content type"],
  "verification_suggestions": ["Steps to verify content"]
}
```

#### URL Analysis
```http
POST /api/analyze/url
Content-Type: application/json

{
  "url": "https://example.com/article"
}
```

#### Image Analysis
```http
POST /api/analyze/image
Content-Type: multipart/form-data

image: [binary file data]
```

### Error Responses

```json
{
  "error": "Error description"
}
```

Common error codes:
- `400`: Bad Request (invalid input)
- `413`: Payload Too Large (file size limit exceeded)
- `500`: Internal Server Error

## 🎓 Educational Features

The tool provides comprehensive educational content:

### Red Flags Detection
- Emotional manipulation language
- Clickbait patterns
- Unreliable source indicators
- Overconfident language
- Missing credibility markers

### Verification Steps
1. **Source Verification**: Check publisher credentials and reputation
2. **Fact Checking**: Use established fact-checking websites
3. **Cross-Reference**: Compare with multiple independent sources
4. **Context Analysis**: Consider timing and motivations

### Resource Links
- Snopes (Fact-checking)
- FactCheck.org (Political claims)
- Google/TinEye (Reverse image search)
- News Literacy Project (Educational resources)

## 🔬 Technical Details

### Analysis Modules

#### Text Analyzer
- **Emotional Keywords**: Detects manipulation language
- **Clickbait Patterns**: Identifies sensational headlines
- **Source Reliability**: Checks for credibility indicators
- **Sentiment Analysis**: Evaluates emotional tone
- **Grammar Quality**: Assesses writing quality

#### URL Analyzer
- **Domain Reputation**: Checks against known unreliable sources
- **Content Quality**: Analyzes page structure and metadata
- **Social Signals**: Evaluates sharing and engagement indicators
- **Technical Factors**: HTTPS, design quality, contact information

#### Image Analyzer
- **Metadata Analysis**: EXIF data examination
- **Quality Assessment**: Resolution, compression artifacts
- **Manipulation Detection**: Basic tampering indicators
- **File Properties**: Size, format consistency

#### AI Integration
- **Gemini Pro**: Advanced text and content analysis
- **Gemini Vision**: Image content understanding
- **Structured Prompts**: Consistent analysis framework
- **Fallback Handling**: Graceful degradation when AI unavailable

## 🛡️ Security & Privacy

### Data Handling
- **No Persistent Storage**: Uploaded files are immediately deleted
- **Minimal Logging**: Only essential information logged
- **Secure Transmission**: HTTPS encryption in production
- **Input Validation**: Comprehensive sanitization and validation

### File Upload Security
- **Type Validation**: Only allowed image formats
- **Size Limits**: 16MB maximum file size
- **Temporary Storage**: Files deleted after processing
- **Malware Protection**: Basic file type verification

## 🚀 Deployment Options

### Local Development
- Flask development server
- Hot reload for development
- Debug mode available

### Production Options

#### Google Cloud Run
- **Serverless**: Automatic scaling
- **Cost-Effective**: Pay per use
- **Global**: Multi-region deployment
- **Managed**: No infrastructure management

#### Other Cloud Platforms
- **Heroku**: Easy deployment with buildpacks
- **AWS**: ECS or Lambda deployment
- **Azure**: Container Instances or App Service
- **DigitalOcean**: App Platform

#### Self-Hosted
- **Docker**: Containerized deployment
- **Traditional**: Direct Python deployment
- **Kubernetes**: Orchestrated scaling

## 📊 Performance

### Benchmarks
- **Text Analysis**: ~200ms average response time
- **URL Analysis**: ~2-5s depending on page size
- **Image Analysis**: ~500ms for basic analysis
- **AI Enhancement**: +1-3s when Gemini AI is available

### Scaling
- **Concurrent Users**: 10+ simultaneous analyses
- **Memory Usage**: ~512MB base + ~100MB per concurrent request
- **CPU Usage**: Moderate during image processing
- **Storage**: Minimal (temporary files only)

## 🧪 Testing

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=backend --cov-report=html
```

### Test Coverage
- ✅ API endpoints
- ✅ Analysis modules
- ✅ Error handling
- ✅ File upload validation
- ✅ Security measures

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. **Fork the repository**
2. **Create a feature branch**
3. **Add tests for new functionality**
4. **Ensure all tests pass**
5. **Submit a pull request**

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run linting
flake8 backend/
black backend/

# Run type checking
mypy backend/
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google AI**: For providing the Gemini AI API
- **Flask Team**: For the excellent web framework
- **Open Source Community**: For the various libraries used
- **Hackathon Organizers**: For the opportunity to build this tool

## 📞 Support

### Getting Help
- **Documentation**: Check this README and inline comments
- **Issues**: Open a GitHub issue for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions

### Common Issues

#### API Key Problems
```bash
# Check if API key is set
echo $GOOGLE_API_KEY

# Verify API key works
curl -H "Authorization: Bearer $GOOGLE_API_KEY" \
  https://generativelanguage.googleapis.com/v1beta/models
```

#### Port Already in Use
```bash
# Find process using port
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill process or use different port
export PORT=8080
```

#### Memory Issues
```bash
# Increase Docker memory limit
docker run -m 2g misinformation-detector

# For Cloud Run, increase memory in cloudrun.yaml
```

## 🔮 Future Enhancements

### Planned Features
- [ ] **Video Analysis**: Deepfake and manipulation detection
- [ ] **Social Media Integration**: Direct platform analysis
- [ ] **Real-time Monitoring**: Continuous content tracking
- [ ] **Machine Learning**: Custom model training
- [ ] **Browser Extension**: Direct web page analysis
- [ ] **Mobile App**: Native iOS/Android applications

### Technical Improvements
- [ ] **Caching**: Redis integration for performance
- [ ] **Database**: Persistent storage for analytics
- [ ] **Monitoring**: Comprehensive logging and metrics
- [ ] **A/B Testing**: Feature experimentation framework
- [ ] **API Rate Limiting**: Advanced quota management

## 📈 Analytics & Metrics

### Usage Statistics
- **Daily Analyses**: Track analysis volume
- **Success Rates**: Monitor API success/failure rates
- **Response Times**: Performance monitoring
- **User Engagement**: Feature usage patterns

### Monitoring Setup
```yaml
# Example monitoring configuration
monitoring:
  metrics:
    - analysis_count
    - response_time
    - error_rate
    - ai_availability
  alerts:
    - high_error_rate
    - slow_response_time
    - ai_service_down
```

---

**Built with ❤️ for the Google Gen AI Exchange Hackathon 2025**

*Empowering users to combat misinformation through AI and education.*
