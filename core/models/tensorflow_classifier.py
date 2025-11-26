import os
import logging
import numpy as np
from PIL import Image
import tensorflow as tf
from pathlib import Path
from typing import Dict, Any, Tuple

# Configure TensorFlow for CPU-only to avoid GPU warnings
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow logging

logger = logging.getLogger(__name__)

class TensorFlowLiteMushroomClassifier:
    """TensorFlow Lite-based mushroom classifier for edibility and species detection."""
    
    def __init__(self):
        """Initialize the TensorFlow Lite classifier."""
        try:
            # Get model paths
            base_path = Path('core/models/keras_models')
            edibility_model_path = base_path / 'edibility_model.tflite'
            species_model_path = base_path / 'species_model.tflite'
            
            if not edibility_model_path.exists():
                raise FileNotFoundError(f"Edibility model not found: {edibility_model_path}")
            if not species_model_path.exists():
                raise FileNotFoundError(f"Species model not found: {species_model_path}")
            
            logger.info(f"TensorFlow version: {tf.__version__}")
            
            # Load TensorFlow Lite models
            logger.info("Loading TensorFlow Lite models...")
            
            # Load edibility model
            self.edibility_interpreter = tf.lite.Interpreter(
                model_path=str(edibility_model_path)
            )
            self.edibility_interpreter.allocate_tensors()
            
            # Load species model
            self.species_interpreter = tf.lite.Interpreter(
                model_path=str(species_model_path)
            )
            self.species_interpreter.allocate_tensors()
            
            # Get input/output details
            self.edibility_input_details = self.edibility_interpreter.get_input_details()
            self.edibility_output_details = self.edibility_interpreter.get_output_details()
            
            self.species_input_details = self.species_interpreter.get_input_details()
            self.species_output_details = self.species_interpreter.get_output_details()
            
            logger.info("✓ TensorFlow Lite models loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading TensorFlow Lite models: {str(e)}")
            self.edibility_interpreter = None
            self.species_interpreter = None
    
    def preprocess_image(self, image: Image.Image, target_size: Tuple[int, int] = (224, 224)) -> np.ndarray:
        """Preprocess PIL image for model input."""
        try:
            # Resize image
            img = image.resize(target_size)
            
            # Convert to array and normalize
            img_array = np.array(img, dtype=np.float32) / 255.0
            
            # Add batch dimension
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            raise
    
    def predict_edibility(self, img_array: np.ndarray) -> Dict[str, Any]:
        """Predict edibility using TensorFlow Lite model."""
        try:
            if not self.edibility_interpreter:
                raise Exception("Edibility model not loaded")
            
            # Set input tensor
            self.edibility_interpreter.set_tensor(self.edibility_input_details[0]['index'], img_array)
            
            # Run inference
            self.edibility_interpreter.invoke()
            
            # Get output
            edibility_pred = self.edibility_interpreter.get_tensor(self.edibility_output_details[0]['index'])[0]
            
            # Determine edibility (assuming [poisonous, edible] classes)
            is_edible = edibility_pred[1] > edibility_pred[0]
            confidence = float(max(edibility_pred) * 100)
            
            return {
                'is_edible': bool(is_edible),
                'confidence': confidence,
                'probabilities': {
                    'poisonous': float(edibility_pred[0] * 100),
                    'edible': float(edibility_pred[1] * 100)
                }
            }
            
        except Exception as e:
            logger.error(f"Error in edibility prediction: {str(e)}")
            return {'error': str(e)}
    
    def predict_species(self, img_array: np.ndarray) -> Dict[str, Any]:
        """Predict species using TensorFlow Lite model."""
        try:
            if not self.species_interpreter:
                raise Exception("Species model not loaded")
            
            # Set input tensor
            self.species_interpreter.set_tensor(self.species_input_details[0]['index'], img_array)
            
            # Run inference
            self.species_interpreter.invoke()
            
            # Get output
            species_pred = self.species_interpreter.get_tensor(self.species_output_details[0]['index'])[0]
            
            # Get top prediction
            top_idx = int(np.argmax(species_pred))
            top_conf = float(species_pred[top_idx] * 100)
            
            # Species information mapping
            species_info = {
                0: {
                    'name': 'Apioperdon_pyriforme',
                    'lifespan': 'Room temp. 12hours after harvest. The mushroom is edible when its interior is completely white.',
                    'preservation': 'refrigerated 3-5 days.'
                },
                1: {
                    'name': 'Cerioporus_squamosus',
                    'lifespan': '4hours room temp after harvest',
                    'preservation': '1 week refrigerated. Can be frozen after cooking.'
                },
                2: {
                    'name': 'Coprinellus_micaceus',
                    'lifespan': '1-2 days room temp after harvest',
                    'preservation': 'refrigerated 3-5 days.'
                },
                3: {
                    'name': 'Coprinus_comatus',
                    'lifespan': '24 hours (dissolves quickly)',
                    'preservation': '10 days refrigerated, 18 days with treatment.'
                }
            }
            
            info = species_info.get(top_idx, {
                'name': f'Unknown Species {top_idx}',
                'lifespan': 'Unknown',
                'preservation': 'Unknown'
            })
            
            return {
                'species': info['name'],
                'confidence': top_conf,
                'class_index': top_idx,
                'lifespan': info['lifespan'],
                'preservation': info['preservation'],
                'all_probabilities': [float(p * 100) for p in species_pred]
            }
            
        except Exception as e:
            logger.error(f"Error in species prediction: {str(e)}")
            return {'error': str(e)}
    
    def analyze_mushroom(self, image: Image.Image) -> Dict[str, Any]:
        """Complete mushroom analysis using TensorFlow Lite models."""
        try:
            if image is None:
                return {'error': 'No image provided'}
            
            # Preprocess image
            img_array = self.preprocess_image(image)
            
            # Get predictions
            edibility_result = self.predict_edibility(img_array)
            species_result = self.predict_species(img_array)
            
            if 'error' in edibility_result or 'error' in species_result:
                return {'error': 'Model prediction failed'}
            
            # Combine results
            result = {
                'preliminary_passed': True,
                'is_edible': edibility_result['is_edible'],
                'edibility_confidence': edibility_result['confidence'],
                'edibility_probability': edibility_result['confidence'] / 100,
                'species': species_result['species'],
                'species_confidence': species_result['confidence'],
                'species_probability': species_result['confidence'] / 100,
                'lifespan': species_result['lifespan'],
                'preservation': species_result['preservation'],
                'analysis_method': 'TensorFlow Lite Models',
                'image_info': {
                    'size': image.size,
                    'mode': image.mode,
                    'format': image.format
                },
                'model_details': {
                    'edibility_probabilities': edibility_result['probabilities'],
                    'species_class_index': species_result['class_index']
                }
            }
            
            # Add safety warnings if not edible
            if not edibility_result['is_edible']:
                result.update({
                    'warning': 'This mushroom appears to be poisonous or inedible. Do not consume!',
                    'safety_note': 'Always consult with expert mycologists before consuming wild mushrooms.'
                })
            
            logger.info(f"TensorFlow Lite analysis completed: {'Edible' if result['is_edible'] else 'Not edible'}")
            return result
            
        except Exception as e:
            logger.error(f"Error in TensorFlow Lite analysis: {str(e)}")
            return {'error': str(e)}

# Global classifier instance
_mushroom_classifier = None

def get_mushroom_classifier():
    """Get or create the mushroom classifier instance."""
    global _mushroom_classifier
    if _mushroom_classifier is None:
        _mushroom_classifier = TensorFlowLiteMushroomClassifier()
    return _mushroom_classifier

def analyze_mushroom_with_tensorflow(image: Image.Image) -> Dict[str, Any]:
    """Analyze mushroom image using TensorFlow Lite models."""
    try:
        classifier = get_mushroom_classifier()
        return classifier.analyze_mushroom(image)
    except Exception as e:
        logger.error(f"Error in TensorFlow Lite analysis: {str(e)}")
        return {'error': str(e)}
