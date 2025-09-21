# 📡 API Documentation

## Overview

The Misinformation Detector API provides endpoints for analyzing text, URLs, and images for potential misinformation indicators. The API returns structured data including risk scores, red flags, and educational recommendations.

## Base URL

```
Production: https://your-service-url.run.app
Development: http://localhost:5000
```

## Authentication

Currently, no authentication is required for public endpoints. API keys are managed internally for Google Cloud services.

**Internal Configuration:**
- Google Gemini API: `AIzaSyAQqzZ4BNdi-sXEnkyGxZ17qDdKqUEcIPY`
- NewsAPI: `712ace18ed8b41228024c65a0847796f`

## Rate Limiting

- **Text Analysis**: 60 requests per minute per IP
- **URL Analysis**: 30 requests per minute per IP (due to external fetching)
- **Image Analysis**: 20 requests per minute per IP (due to processing overhead)

## Content Types

All endpoints accept and return JSON unless otherwise specified.

## Error Handling

All errors return a JSON object with an `error` field:

```json
{
  "error": "Description of the error"
}
```

### HTTP Status Codes

- `200`: Success
- `400`: Bad Request (invalid input)
- `413`: Payload Too Large
- `429`: Too Many Requests
- `500`: Internal Server Error

---

## Endpoints

### Health Check

Check if the API is running and healthy.

**Endpoint:** `GET /api/health`

**Response:**
```json
{
  "status": "healthy",
  "message": "Misinformation Detector API is running"
}
```

---

### Text Analysis

Analyze text content for misinformation indicators.

**Endpoint:** `POST /api/analyze/text`

**Request Body:**
```json
{
  "text": "Text content to analyze (max 5000 characters)"
}
```

**Response:**
```json
{
  "type": "text",
  "content": "Preview of analyzed text...",
  "risk_score": 75,
  "analysis": {
    "basic": {
      "risk_score": 70,
      "red_flags": ["Emotional manipulation detected"],
      "details": {
        "emotional_manipulation": 25,
        "clickbait_patterns": 15,
        "source_reliability": 20,
        "certainty_language": 10,
        "sentiment": 0,
        "grammar_quality": 0,
        "structure": 0
      },
      "word_count": 156,
      "sentiment": {
        "polarity": 0.8,
        "subjectivity": 0.9,
        "interpretation": "extremely positive, highly subjective"
      }
    },
    "ai": {
      "risk_score": 80,
      "red_flags": ["AI detected potential misleading content"],
      "explanation": "Detailed AI analysis explanation...",
      "verification_steps": ["Step 1", "Step 2"],
      "detailed_assessment": {
        "language_analysis": "Analysis of language patterns",
        "factual_consistency": "Assessment of claims",
        "source_reliability": "Evaluation of sources",
        "emotional_manipulation": "Assessment of tactics"
      },
      "ai_confidence": "high"
    }
  },
  "red_flags": [
    "Emotional manipulation detected",
    "AI detected potential misleading content"
  ],
  "educational_tips": [
    "Watch for emotional language designed to make you angry or afraid",
    "Be suspicious of articles with ALL CAPS or excessive exclamation points"
  ],
  "verification_suggestions": [
    {
      "step": "Source Verification",
      "description": "Research the publisher and author credentials"
    }
  ]
}
```

**Example cURL:**
```bash
curl -X POST https://your-api-url/api/analyze/text \
  -H "Content-Type: application/json" \
  -d '{"text": "SHOCKING! Scientists discover miracle cure!"}'
```

---

### URL Analysis

Analyze web content from a URL for misinformation indicators.

**Endpoint:** `POST /api/analyze/url`

**Request Body:**
```json
{
  "url": "https://example.com/article"
}
```

**Response:**
```json
{
  "type": "url",
  "url": "https://example.com/article",
  "title": "Article Title",
  "risk_score": 45,
  "analysis": {
    "url": {
      "risk_score": 40,
      "red_flags": ["Domain contains many numbers"],
      "domain": "example123.com",
      "scheme": "https",
      "title": "Article Title",
      "content": "First 1000 characters of content...",
      "meta_info": {
        "author": "John Doe",
        "published": "2025-01-01",
        "description": "Article description",
        "keywords": "keyword1, keyword2"
      },
      "external_links": [
        "https://external1.com",
        "https://external2.com"
      ],
      "social_signals": {
        "sharing_buttons": true,
        "social_meta": true,
        "embedded_social": false
      }
    },
    "ai": {
      "risk_score": 50,
      "red_flags": ["AI analysis findings"],
      "explanation": "AI assessment of the content...",
      "verification_steps": ["Verify claims", "Check sources"],
      "ai_confidence": "medium"
    }
  },
  "red_flags": [
    "Domain contains many numbers",
    "AI analysis findings"
  ],
  "educational_tips": [
    "Check the website's 'About' page to understand who runs it",
    "Look at the URL carefully - fake sites often mimic real news sources"
  ],
  "verification_suggestions": [
    {
      "step": "Source Verification",
      "description": "Research the publisher and check their credibility"
    }
  ]
}
```

**Example cURL:**
```bash
curl -X POST https://your-api-url/api/analyze/url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://suspicious-news-site.com/article"}'
```

---

### Image Analysis

Analyze an uploaded image for manipulation indicators.

**Endpoint:** `POST /api/analyze/image`

**Request:** Multipart form data with image file

**Form Fields:**
- `image`: Image file (PNG, JPG, JPEG, GIF, WebP, max 16MB)

**Response:**
```json
{
  "type": "image",
  "filename": "uploaded_image.jpg",
  "risk_score": 30,
  "analysis": {
    "technical": {
      "risk_score": 25,
      "red_flags": ["Missing camera information in EXIF data"],
      "technical_details": {
        "exif_score": 15,
        "quality_score": 5,
        "file_score": 0,
        "manipulation_score": 5
      }
    },
    "ai": {
      "risk_score": 35,
      "red_flags": ["AI detected potential inconsistencies"],
      "explanation": "AI analysis of image content and context...",
      "verification_steps": ["Use reverse image search", "Check image source"],
      "ai_confidence": "medium"
    }
  },
  "red_flags": [
    "Missing camera information in EXIF data",
    "AI detected potential inconsistencies"
  ],
  "image_info": {
    "format": "JPEG",
    "mode": "RGB",
    "size": [1920, 1080],
    "width": 1920,
    "height": 1080,
    "has_transparency": false
  },
  "file_hash": "a1b2c3d4e5f6...",
  "reverse_search_info": {
    "thumbnail_size": [150, 150],
    "original_size": [1920, 1080],
    "format": "JPEG",
    "suggestion": "Consider using Google Images, TinEye, or Bing Visual Search..."
  },
  "educational_tips": [
    "Use reverse image search to see if the image appears elsewhere online",
    "Look for inconsistencies in lighting, shadows, or image quality"
  ],
  "verification_suggestions": [
    {
      "step": "Reverse Image Search",
      "description": "Search for the image on Google Images or TinEye"
    }
  ]
}
```

**Example cURL:**
```bash
curl -X POST https://your-api-url/api/analyze/image \
  -F "image=@suspicious_image.jpg"
```

---

### Educational Tips

Get general educational content about misinformation detection.

**Endpoint:** `GET /api/educational/tips`

**Response:**
```json
{
  "general_tips": [
    "Check the source: Look for author credentials, publication date, and website reputation",
    "Cross-reference information: Verify claims with multiple reliable sources"
  ],
  "red_flags": [
    "No author byline or contact information",
    "Emotional, inflammatory language designed to provoke strong reactions"
  ],
  "verification_steps": [
    {
      "step": "Source Verification",
      "description": "Research the publisher, author, and publication",
      "actions": [
        "Look up the author's credentials and other published work",
        "Check the website's About page and contact information"
      ]
    }
  ]
}
```

---

## Response Schema

### Common Fields

All analysis responses include these fields:

- `type`: Analysis type ("text", "url", or "image")
- `risk_score`: Integer from 0-100 (higher = more risk)
- `red_flags`: Array of strings describing concerns found
- `educational_tips`: Array of content-specific tips
- `verification_suggestions`: Array of verification steps

### Risk Score Interpretation

- **0-19**: Minimal Risk - Content appears credible
- **20-39**: Low Risk - Minor concerns, verify if sharing widely
- **40-69**: Moderate Risk - Some concerning elements, verify before sharing
- **70-100**: High Risk - Multiple red flags, exercise extreme caution

### Red Flags Categories

#### Text Analysis
- Emotional manipulation language
- Clickbait patterns
- Unreliable source indicators
- Overconfident language
- Grammar and quality issues

#### URL Analysis
- Suspicious domain patterns
- Missing credibility indicators
- Poor content quality
- Technical issues (no HTTPS, poor design)

#### Image Analysis
- Missing or suspicious metadata
- Signs of digital manipulation
- Quality inconsistencies
- File property anomalies

---

## SDKs and Libraries

### JavaScript/Node.js

```javascript
class MisinfoDetector {
  constructor(baseUrl) {
    this.baseUrl = baseUrl;
  }

  async analyzeText(text) {
    const response = await fetch(`${this.baseUrl}/api/analyze/text`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    return response.json();
  }

  async analyzeUrl(url) {
    const response = await fetch(`${this.baseUrl}/api/analyze/url`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });
    return response.json();
  }

  async analyzeImage(imageFile) {
    const formData = new FormData();
    formData.append('image', imageFile);
    
    const response = await fetch(`${this.baseUrl}/api/analyze/image`, {
      method: 'POST',
      body: formData
    });
    return response.json();
  }
}

// Usage
const detector = new MisinfoDetector('https://your-api-url');
const result = await detector.analyzeText('Suspicious text content');
```

### Python

```python
import requests

class MisinfoDetector:
    def __init__(self, base_url):
        self.base_url = base_url
    
    def analyze_text(self, text):
        response = requests.post(
            f"{self.base_url}/api/analyze/text",
            json={"text": text}
        )
        return response.json()
    
    def analyze_url(self, url):
        response = requests.post(
            f"{self.base_url}/api/analyze/url",
            json={"url": url}
        )
        return response.json()
    
    def analyze_image(self, image_path):
        with open(image_path, 'rb') as f:
            files = {'image': f}
            response = requests.post(
                f"{self.base_url}/api/analyze/image",
                files=files
            )
        return response.json()

# Usage
detector = MisinfoDetector('https://your-api-url')
result = detector.analyze_text('Suspicious text content')
```

---

## Webhook Support (Future)

### Webhook Endpoints

For real-time notifications of analysis results:

```json
{
  "webhook_url": "https://your-app.com/webhook",
  "events": ["analysis_complete", "high_risk_detected"],
  "secret": "webhook_secret_key"
}
```

### Webhook Payload

```json
{
  "event": "analysis_complete",
  "timestamp": "2025-01-20T10:30:00Z",
  "analysis_id": "uuid-here",
  "content_type": "text",
  "risk_score": 85,
  "high_risk": true,
  "summary": "High-risk content detected with multiple red flags"
}
```

---

## Testing and Development

### Test Endpoints

Use these endpoints for testing (sandbox environment):

```
https://your-api-url/test/analyze/text
https://your-api-url/test/analyze/url
https://your-api-url/test/analyze/image
```

### Sample Test Data

```json
{
  "high_risk_text": "URGENT! Share this before they delete it! Doctors HATE this simple trick!",
  "moderate_risk_url": "https://suspicious-news.example.com/fake-story",
  "low_risk_text": "According to a peer-reviewed study published in Nature journal, researchers found..."
}
```

### Mock Responses

For development and testing, mock responses maintain the same schema but include a `mock: true` field.

---

## Support and Resources

### Documentation
- **OpenAPI Spec**: Available at `/api/docs` (when enabled)
- **Postman Collection**: [Download link]
- **Interactive API Explorer**: [Web interface URL]

### Support Channels
- **GitHub Issues**: For bug reports and feature requests
- **Documentation**: This file and inline code comments
- **Community Forum**: [Forum URL]

### Rate Limit Headers

All responses include rate limit information:

```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 59
X-RateLimit-Reset: 1642694400
```

---

*API Version: 1.0 | Last Updated: January 2025*
