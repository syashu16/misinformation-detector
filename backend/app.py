from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import logging
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

# Import our analysis modules
from modules.text_analyzer import TextAnalyzer
from modules.url_analyzer import URLAnalyzer
from modules.image_analyzer import ImageAnalyzer
from modules.gemini_integration import GeminiAnalyzer
from modules.educational_content import EducationalContent
from modules.advanced_ai_analyzer import AdvancedAIAnalyzer
from modules.realtime_fact_checker import RealTimeFactChecker
from modules.indian_context_detector import IndianMisinfoDetector

# Load environment variables
load_dotenv()

app = Flask(__name__, 
           static_folder='../frontend',
           template_folder='../frontend')
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Configuration
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize analyzers
text_analyzer = TextAnalyzer()
url_analyzer = URLAnalyzer()
image_analyzer = ImageAnalyzer()
gemini_analyzer = GeminiAnalyzer()
educational_content = EducationalContent()
advanced_analyzer = AdvancedAIAnalyzer()
fact_checker = RealTimeFactChecker()
indian_context = IndianMisinfoDetector()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Allowed file extensions for images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/style.css')
def serve_css():
    """Serve CSS file"""
    return send_from_directory('../frontend', 'style.css')

@app.route('/script.js')
def serve_js():
    """Serve JavaScript file"""
    return send_from_directory('../frontend', 'script.js')

@app.route('/demo-enhancements.css')
def serve_demo_css():
    """Serve demo CSS file"""
    return send_from_directory('../frontend', 'demo-enhancements.css')

@app.route('/demo-script.js')
def serve_demo_js():
    """Serve demo JavaScript file"""
    return send_from_directory('../frontend', 'demo-script.js')

@app.route('/advanced-visualization.js')
def serve_advanced_js():
    """Serve advanced visualization JavaScript file"""
    return send_from_directory('../frontend', 'advanced-visualization.js')

@app.route('/health')
def root_health_check():
    """Root health check endpoint for container health checks"""
    return jsonify({'status': 'healthy', 'message': 'Misinformation Detector API is running'})

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Misinformation Detector API is running'})

@app.route('/api/analyze/text', methods=['POST', 'OPTIONS'])
def analyze_text():
    """Advanced text analysis with multi-layered AI and fact-checking"""
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response
    
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text']
        if len(text.strip()) == 0:
            return jsonify({'error': 'Empty text provided'}), 400
        
        logger.info(f"Analyzing text content: {text[:100]}...")
        
        # Perform basic text analysis
        basic_analysis = text_analyzer.analyze(text)
        
        # Advanced AI analysis
        try:
            advanced_analysis = advanced_analyzer.analyze_comprehensive(text, 'text')
        except Exception as ai_error:
            logger.warning(f"Advanced AI analysis failed: {str(ai_error)}")
            advanced_analysis = {'error': 'Advanced analysis unavailable'}
        
        # Real-time fact checking
        try:
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            fact_check_results = loop.run_until_complete(
                fact_checker.check_claims_comprehensive(text, 'text')
            )
            loop.close()
        except Exception as fact_error:
            logger.warning(f"Fact-checking failed: {str(fact_error)}")
            fact_check_results = {'error': 'Fact-checking unavailable'}
        
        # Try Gemini AI analysis with fallback
        ai_analysis = {'risk_score': 0, 'red_flags': [], 'ai_confidence': 'Not available'}
        try:
            ai_analysis = gemini_analyzer.analyze_text(text)
        except Exception as ai_error:
            logger.warning(f"Gemini AI analysis failed: {str(ai_error)}")
            ai_analysis['explanation'] = "AI analysis temporarily unavailable"
        
        # Indian context analysis
        indian_analysis = {}
        try:
            indian_analysis = indian_context.analyze_indian_context(text)
        except Exception as indian_error:
            logger.warning(f"Indian context analysis failed: {str(indian_error)}")
            indian_analysis = {'error': 'Indian context analysis unavailable'}
        
        # Calculate composite risk score
        basic_risk = basic_analysis['risk_score']
        advanced_risk = advanced_analysis.get('risk_assessment', {}).get('overall_risk_score', 0)
        fact_check_risk = 100 - fact_check_results.get('overall_credibility', 50)
        ai_risk = ai_analysis.get('risk_score', 0)
        indian_risk = indian_analysis.get('india_specific_risk', 0)
        
        # Weighted average of all risk scores (including Indian context)
        final_risk_score = int(
            (basic_risk * 0.15) + 
            (advanced_risk * 0.3) + 
            (fact_check_risk * 0.25) + 
            (ai_risk * 0.15) +
            (indian_risk * 0.15)
        )
        
        # Combine all red flags
        all_red_flags = basic_analysis['red_flags'] + ai_analysis.get('red_flags', [])
        if advanced_analysis.get('detailed_analysis', {}).get('linguistic', {}).get('detected_patterns'):
            all_red_flags.extend(advanced_analysis['detailed_analysis']['linguistic']['detected_patterns'][:3])
        if indian_analysis.get('regional_patterns'):
            all_red_flags.extend(indian_analysis['regional_patterns'][:2])
        
        # Build comprehensive result
        result = {
            'type': 'text',
            'content': text[:200] + '...' if len(text) > 200 else text,
            'risk_score': final_risk_score,
            'analysis': {
                'basic': basic_analysis,
                'advanced': advanced_analysis,
                'fact_checking': fact_check_results,
                'ai': ai_analysis
            },
            'indian_context': indian_analysis,
            'red_flags': list(set(all_red_flags))[:10],  # Remove duplicates, limit to 10
            'educational_tips': educational_content.get_tips_for_text()[:5],
            'verification_suggestions': educational_content.get_verification_suggestions('text', final_risk_score),
            'confidence_score': advanced_analysis.get('confidence_score', 0.7),
            'processing_summary': {
                'total_processing_time': (
                    advanced_analysis.get('processing_time', 0) + 
                    fact_check_results.get('processing_time', 0)
                ),
                'fact_checks_performed': fact_check_results.get('total_claims', 0),
                'analysis_layers': 5  # Increased to include Indian context
            }
        }
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error analyzing text: {str(e)}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@app.route('/api/analyze/url', methods=['POST'])
def analyze_url():
    """Analyze URL content for misinformation"""
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'No URL provided'}), 400
        
        url = data['url']
        logger.info(f"Analyzing URL: {url}")
        
        # Analyze URL and extract content
        url_analysis = url_analyzer.analyze(url)
        
        if url_analysis.get('error'):
            return jsonify({'error': url_analysis['error']}), 400
        
        # Get AI analysis of the extracted content
        ai_analysis = gemini_analyzer.analyze_text(url_analysis.get('content', ''))
        
        # Combine results
        result = {
            'type': 'url',
            'url': url,
            'title': url_analysis.get('title', 'Unknown'),
            'risk_score': max(url_analysis['risk_score'], ai_analysis.get('risk_score', 0)),
            'analysis': {
                'url': url_analysis,
                'ai': ai_analysis
            },
            'red_flags': url_analysis['red_flags'] + ai_analysis.get('red_flags', []),
            'educational_tips': educational_content.get_tips_for_urls(),
            'verification_suggestions': educational_content.get_verification_suggestions()
        }
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error analyzing URL: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/analyze/image', methods=['POST'])
def analyze_image():
    """Analyze image for potential misinformation"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload PNG, JPG, JPEG, GIF, or WebP files'}), 400
        
        # Save the uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        logger.info(f"Analyzing image: {filename}")
        
        # Analyze image
        image_analysis = image_analyzer.analyze(filepath)
        
        # Get AI analysis
        ai_analysis = gemini_analyzer.analyze_image(filepath)
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except:
            pass
        
        # Combine results
        result = {
            'type': 'image',
            'filename': filename,
            'risk_score': max(image_analysis['risk_score'], ai_analysis.get('risk_score', 0)),
            'analysis': {
                'technical': image_analysis,
                'ai': ai_analysis
            },
            'red_flags': image_analysis['red_flags'] + ai_analysis.get('red_flags', []),
            'educational_tips': educational_content.get_tips_for_images(),
            'verification_suggestions': educational_content.get_verification_suggestions()
        }
        
        return jsonify(result)
        
    except RequestEntityTooLarge:
        return jsonify({'error': 'File too large. Maximum size is 16MB'}), 413
    except Exception as e:
        logger.error(f"Error analyzing image: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/educational/tips')
def get_educational_tips():
    """Get general educational tips about misinformation"""
    return jsonify({
        'general_tips': educational_content.get_general_tips(),
        'red_flags': educational_content.get_common_red_flags(),
        'verification_steps': educational_content.get_verification_steps()
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true')
