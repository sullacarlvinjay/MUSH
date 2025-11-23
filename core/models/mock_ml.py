"""
Mock ML modules for deployment without heavy dependencies
"""
import logging
from typing import Dict, Any, Optional
from PIL import Image

logger = logging.getLogger(__name__)

class MockTensorFlow:
    """Mock TensorFlow module"""
    __version__ = "2.13.0"
    
    class keras:
        """Mock Keras module"""
        __version__ = "2.13.0"
        
        class models:
            @staticmethod
            def load_model(path):
                logger.warning(f"Mock: Loading model from {path}")
                return MockModel()
        
        class Model:
            pass
        
        class layers:
            class InputLayer:
                pass

class MockModel:
    """Mock ML model"""
    def predict(self, data):
        logger.warning("Mock: Making prediction")
        return [0.5, 0.5]  # Mock prediction
    
    def summary(self):
        logger.warning("Mock: Model summary")

class MockClassifier:
    """Mock Mushroom Classifier"""
    def __init__(self):
        logger.warning("Mock: Initializing MushroomClassifier")
        self.edibility_model = MockModel()
        self.species_model = MockModel()
    
    def predict_edibility(self, image_path):
        logger.warning(f"Mock: Predicting edibility for {image_path}")
        return {
            'is_edible': True,
            'confidence': 0.8,
            'prediction': 'edible'
        }
    
    def predict_species(self, image_path):
        logger.warning(f"Mock: Predicting species for {image_path}")
        return {
            'species': 'Agaricus bisporus',
            'confidence': 0.7,
            'prediction': 'common_mushroom'
        }

def mock_analyze_mushroom(image_path: str) -> Dict[str, Any]:
    """Mock mushroom analysis function"""
    logger.warning(f"Mock: Analyzing mushroom at {image_path}")
    
    try:
        # Mock image processing
        with Image.open(image_path) as img:
            width, height = img.size
        
        return {
            'is_mushroom': True,
            'mushroom_confidence': 0.9,
            'edibility': {
                'is_edible': True,
                'confidence': 0.8,
                'prediction': 'edible',
                'class_name': 'Edible'
            },
            'species': {
                'species': 'Agaricus bisporus',
                'confidence': 0.7,
                'prediction': 'common_mushroom',
                'class_name': 'Common Mushroom'
            },
            'image_info': {
                'width': width,
                'height': height,
                'format': img.format
            }
        }
    except Exception as e:
        logger.error(f"Mock analysis failed: {e}")
        return {
            'error': str(e),
            'is_mushroom': False,
            'mushroom_confidence': 0.0
        }

# Mock numpy for basic operations
class MockNumpy:
    """Mock NumPy for basic operations"""
    
    # Add ndarray class for type hints
    class ndarray:
        pass
    
    @staticmethod
    def array(data):
        return data
    
    @staticmethod
    def zeros(shape):
        if isinstance(shape, tuple) and len(shape) == 2:
            return [[0] * shape[1] for _ in range(shape[0])]
        return [0] * shape if isinstance(shape, int) else shape
    
    @staticmethod
    def ones(shape):
        if isinstance(shape, tuple) and len(shape) == 2:
            return [[1] * shape[1] for _ in range(shape[0])]
        return [1] * shape if isinstance(shape, int) else shape
    
    @staticmethod
    def reshape(data, shape):
        return data
    
    @staticmethod
    def expand_dims(data, axis):
        return [data]
    
    @staticmethod
    def float32():
        return "float32"
    
    @staticmethod
    def argmax(data):
        if isinstance(data, list) and len(data) > 0:
            return 0  # Return first index as mock
        return 0
    
    @staticmethod
    def max(data):
        return 0.9  # Mock max value

# Export mock modules
tf = MockTensorFlow()
np = MockNumpy()

# Additional mock classes for TFLite model functions
class MockTFLiteModel:
    """Mock TFLite model for deployment"""
    def __init__(self, model_path):
        self.input_shape = (224, 224)  # Mock input shape
        self.input_details = [{'shape': [1, 224, 224, 3], 'dtype': 'float32', 'name': 'input'}]
        self.output_details = [{'shape': [1, 2], 'dtype': 'float32', 'name': 'output'}]
    
    def predict(self, input_data):
        return [[0.5, 0.5]]  # Mock prediction

def mock_get_mushroom_detector_model():
    return MockTFLiteModel("mock_mushroom_model")

def mock_get_edibility_model():
    return MockTFLiteModel("mock_edibility_model")

def mock_get_species_model():
    return MockTFLiteModel("mock_species_model")
