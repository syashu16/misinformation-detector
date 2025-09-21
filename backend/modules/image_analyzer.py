from PIL import Image, ExifTags
from PIL.ExifTags import TAGS
import hashlib
import os
from typing import Dict, List
import logging
import numpy as np

logger = logging.getLogger(__name__)

class ImageAnalyzer:
    """Analyzes images for potential manipulation or misinformation indicators"""
    
    def __init__(self):
        # Known manipulated image signatures (would be expanded with ML models)
        self.suspicious_patterns = [
            'heavy_compression',
            'missing_exif',
            'inconsistent_lighting',
            'unusual_artifacts'
        ]
    
    def analyze(self, image_path: str) -> Dict:
        """
        Analyze image for manipulation indicators
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            red_flags = []
            risk_score = 0
            
            # Load image
            with Image.open(image_path) as img:
                # Basic image information
                image_info = self._get_image_info(img)
                
                # EXIF data analysis
                exif_score = self._analyze_exif_data(img, red_flags)
                risk_score += exif_score
                
                # Quality and compression analysis
                quality_score = self._analyze_image_quality(img, red_flags)
                risk_score += quality_score
                
                # File properties analysis
                file_score = self._analyze_file_properties(image_path, red_flags)
                risk_score += file_score
                
                # Basic manipulation detection
                manipulation_score = self._detect_basic_manipulation(img, red_flags)
                risk_score += manipulation_score
                
                # Reverse image search indicators
                reverse_search_info = self._prepare_reverse_search_info(image_path)
                
            # Normalize risk score
            final_score = min(100, max(0, risk_score))
            
            result = {
                'risk_score': final_score,
                'red_flags': red_flags,
                'image_info': image_info,
                'file_hash': self._calculate_file_hash(image_path),
                'reverse_search_info': reverse_search_info,
                'technical_details': {
                    'exif_score': exif_score,
                    'quality_score': quality_score,
                    'file_score': file_score,
                    'manipulation_score': manipulation_score
                }
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing image {image_path}: {str(e)}")
            return {
                'risk_score': 50,  # Default moderate risk for analysis errors
                'red_flags': [f'Error analyzing image: {str(e)}'],
                'image_info': {},
                'file_hash': '',
                'reverse_search_info': {},
                'technical_details': {}
            }
    
    def _get_image_info(self, img: Image.Image) -> Dict:
        """Extract basic image information"""
        try:
            return {
                'format': img.format,
                'mode': img.mode,
                'size': img.size,
                'width': img.width,
                'height': img.height,
                'has_transparency': img.mode in ('RGBA', 'LA') or 'transparency' in img.info
            }
        except Exception as e:
            logger.error(f"Error getting image info: {str(e)}")
            return {}
    
    def _analyze_exif_data(self, img: Image.Image, red_flags: List[str]) -> int:
        """Analyze EXIF metadata for manipulation indicators"""
        try:
            score = 0
            exif_data = img._getexif()
            
            if not exif_data:
                red_flags.append("No EXIF metadata found (possible manipulation)")
                score += 20
                return score
            
            # Check for suspicious EXIF patterns
            exif_dict = {}
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                exif_dict[tag] = value
            
            # Check for missing camera information
            camera_tags = ['Make', 'Model', 'Software']
            missing_camera_info = sum(1 for tag in camera_tags if tag not in exif_dict)
            
            if missing_camera_info >= 2:
                red_flags.append("Missing camera information in EXIF data")
                score += 15
            
            # Check for suspicious software signatures
            software = exif_dict.get('Software', '')
            suspicious_software = ['photoshop', 'gimp', 'paint.net', 'canva']
            
            if any(soft in software.lower() for soft in suspicious_software):
                red_flags.append(f"Image processed with editing software: {software}")
                score += 25
            
            # Check for inconsistent timestamps
            datetime_tags = ['DateTime', 'DateTimeOriginal', 'DateTimeDigitized']
            timestamps = [exif_dict.get(tag) for tag in datetime_tags if tag in exif_dict]
            
            if len(set(timestamps)) > 1:
                red_flags.append("Inconsistent timestamps in EXIF data")
                score += 10
            
            return score
            
        except Exception as e:
            logger.error(f"Error analyzing EXIF data: {str(e)}")
            return 5  # Minor penalty for EXIF analysis errors
    
    def _analyze_image_quality(self, img: Image.Image, red_flags: List[str]) -> int:
        """Analyze image quality indicators"""
        try:
            score = 0
            
            # Convert to RGB for analysis
            if img.mode != 'RGB':
                img_rgb = img.convert('RGB')
            else:
                img_rgb = img
            
            # Check image dimensions
            width, height = img.size
            
            # Very small images might be suspicious
            if width < 100 or height < 100:
                red_flags.append("Very low resolution image")
                score += 15
            
            # Extremely large images might be suspicious
            if width * height > 10000000:  # > 10MP
                red_flags.append("Unusually high resolution image")
                score += 10
            
            # Check aspect ratio
            aspect_ratio = width / height
            if aspect_ratio > 5 or aspect_ratio < 0.2:
                red_flags.append("Unusual aspect ratio")
                score += 8
            
            # Basic compression artifacts detection
            # Convert to numpy array for analysis
            img_array = np.array(img_rgb)
            
            # Check for unusual color distribution
            if self._check_color_distribution(img_array):
                red_flags.append("Unusual color distribution detected")
                score += 12
            
            return score
            
        except Exception as e:
            logger.error(f"Error analyzing image quality: {str(e)}")
            return 0
    
    def _check_color_distribution(self, img_array: np.ndarray) -> bool:
        """Check for unusual color distributions that might indicate manipulation"""
        try:
            # Calculate histogram for each channel
            hist_r = np.histogram(img_array[:,:,0], bins=256, range=(0,256))[0]
            hist_g = np.histogram(img_array[:,:,1], bins=256, range=(0,256))[0]
            hist_b = np.histogram(img_array[:,:,2], bins=256, range=(0,256))[0]
            
            # Check for extremely peaked distributions (possible posterization)
            for hist in [hist_r, hist_g, hist_b]:
                max_bin = np.max(hist)
                total_pixels = np.sum(hist)
                if max_bin > total_pixels * 0.8:  # 80% of pixels in one bin
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking color distribution: {str(e)}")
            return False
    
    def _analyze_file_properties(self, image_path: str, red_flags: List[str]) -> int:
        """Analyze file system properties"""
        try:
            score = 0
            
            # Get file stats
            file_stats = os.stat(image_path)
            file_size = file_stats.st_size
            
            # Check file size
            if file_size < 1024:  # Less than 1KB
                red_flags.append("Suspiciously small file size")
                score += 20
            elif file_size > 50 * 1024 * 1024:  # Greater than 50MB
                red_flags.append("Unusually large file size")
                score += 10
            
            # Check file extension vs actual format
            file_extension = os.path.splitext(image_path)[1].lower()
            
            with Image.open(image_path) as img:
                actual_format = img.format.lower() if img.format else 'unknown'
                
                expected_extensions = {
                    'jpeg': ['.jpg', '.jpeg'],
                    'png': ['.png'],
                    'gif': ['.gif'],
                    'webp': ['.webp']
                }
                
                if actual_format in expected_extensions:
                    if file_extension not in expected_extensions[actual_format]:
                        red_flags.append(f"File extension mismatch: {file_extension} vs {actual_format}")
                        score += 15
            
            return score
            
        except Exception as e:
            logger.error(f"Error analyzing file properties: {str(e)}")
            return 0
    
    def _detect_basic_manipulation(self, img: Image.Image, red_flags: List[str]) -> int:
        """Detect basic signs of image manipulation"""
        try:
            score = 0
            
            # Convert to RGB for analysis
            if img.mode != 'RGB':
                img_rgb = img.convert('RGB')
            else:
                img_rgb = img
            
            img_array = np.array(img_rgb)
            
            # Check for copy-paste artifacts (simple duplicate region detection)
            if self._detect_duplicate_regions(img_array):
                red_flags.append("Possible duplicate regions detected")
                score += 30
            
            # Check for edge inconsistencies
            if self._check_edge_inconsistencies(img_array):
                red_flags.append("Edge inconsistencies detected")
                score += 20
            
            return score
            
        except Exception as e:
            logger.error(f"Error detecting manipulation: {str(e)}")
            return 0
    
    def _detect_duplicate_regions(self, img_array: np.ndarray) -> bool:
        """Simple duplicate region detection"""
        try:
            # This is a very basic implementation
            # In production, you'd use more sophisticated algorithms
            
            height, width = img_array.shape[:2]
            
            # Sample small regions and check for exact matches
            region_size = 20
            matches = 0
            samples = 0
            
            for y in range(0, height - region_size, region_size * 2):
                for x in range(0, width - region_size, region_size * 2):
                    region1 = img_array[y:y+region_size, x:x+region_size]
                    
                    # Check against other regions
                    for y2 in range(y + region_size, height - region_size, region_size):
                        for x2 in range(0, width - region_size, region_size):
                            if abs(y2 - y) < region_size and abs(x2 - x) < region_size:
                                continue  # Skip nearby regions
                            
                            region2 = img_array[y2:y2+region_size, x2:x2+region_size]
                            
                            if np.array_equal(region1, region2):
                                matches += 1
                            
                            samples += 1
                            
                            if samples > 100:  # Limit computation
                                break
                        if samples > 100:
                            break
                    if samples > 100:
                        break
                if samples > 100:
                    break
            
            # If more than 5% of sampled regions have exact duplicates
            return matches > samples * 0.05 if samples > 0 else False
            
        except Exception as e:
            logger.error(f"Error detecting duplicate regions: {str(e)}")
            return False
    
    def _check_edge_inconsistencies(self, img_array: np.ndarray) -> bool:
        """Check for inconsistent edges that might indicate manipulation"""
        try:
            # Very basic edge consistency check
            # In production, you'd use more sophisticated edge detection
            
            # Calculate simple gradient
            gray = np.mean(img_array, axis=2)
            
            # Simple edge detection using differences
            edges_x = np.abs(np.diff(gray, axis=1))
            edges_y = np.abs(np.diff(gray, axis=0))
            
            # Check for unusually sharp transitions
            threshold = np.percentile(edges_x, 95)  # 95th percentile
            sharp_edges = np.sum(edges_x > threshold * 2)
            
            # If too many extremely sharp edges, might indicate manipulation
            total_edges = edges_x.size
            return sharp_edges > total_edges * 0.001  # 0.1% threshold
            
        except Exception as e:
            logger.error(f"Error checking edge inconsistencies: {str(e)}")
            return False
    
    def _calculate_file_hash(self, image_path: str) -> str:
        """Calculate MD5 hash of the image file"""
        try:
            hash_md5 = hashlib.md5()
            with open(image_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            logger.error(f"Error calculating file hash: {str(e)}")
            return ""
    
    def _prepare_reverse_search_info(self, image_path: str) -> Dict:
        """Prepare information for reverse image searching"""
        try:
            # Get image properties that would be useful for reverse search
            with Image.open(image_path) as img:
                # Create thumbnail for potential reverse search
                thumbnail_size = (150, 150)
                img.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
                
                return {
                    'thumbnail_size': thumbnail_size,
                    'original_size': img.size,
                    'format': img.format,
                    'suggestion': "Consider using Google Images, TinEye, or Bing Visual Search to check if this image appears elsewhere online"
                }
                
        except Exception as e:
            logger.error(f"Error preparing reverse search info: {str(e)}")
            return {
                'suggestion': "Manual reverse image search recommended"
            }
