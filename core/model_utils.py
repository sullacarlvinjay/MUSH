import logging
from PIL import Image
from typing import Dict, Any
import random

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def analyze_mushroom(image: Image.Image) -> Dict[str, Any]:
    """Mockup mushroom analysis function for testing.
    
    Returns realistic-looking results without requiring ML models.
    This will be replaced with actual ML functionality later.
    """
    try:
        logger.info("Running mockup mushroom analysis...")
        
        # Simulate mushroom detection with high confidence
        mushroom_confidence = random.uniform(75, 95)
        
        # Randomly determine if edible (70% chance for demo)
        is_edible = random.random() > 0.3
        edibility_confidence = random.uniform(70, 90)
        
        result = {
            'preliminary_passed': True,
            'confidence': mushroom_confidence,
            'is_edible': is_edible,
            'edibility_confidence': edibility_confidence,
            'edibility_probability': 0.8 if is_edible else 0.2,
            'note': 'This is a mockup result for testing. ML analysis will be added later.',
            'image_info': {
                'size': image.size,
                'mode': image.mode,
                'format': image.format
            }
        }
        
        # If edible, add mock species information
        if is_edible:
            species_options = [
                'Apioperdon_pyriforme',
                'Cerioporus_squamosus', 
                'Coprinellus_micaceus',
                'Coprinus_comatus'
            ]
            species = random.choice(species_options)
            species_confidence = random.uniform(65, 85)
            
            species_info = {
                'Apioperdon_pyriforme': {
                    'lifespan': 'Room temp. 12hours after harvest. The mushroom is edible when its interior is completely white.',
                    'preservation': 'refrigerated 3-5 days.'
                },
                'Cerioporus_squamosus': {
                    'lifespan': '4hours room temp after harvest',
                    'preservation': '1 week refrigerated. Can be frozen after cooking.'
                },
                'Coprinellus_micaceus': {
                    'lifespan': '1-2 days room temp after harvest',
                    'preservation': 'refrigerated 3-5 days.'
                },
                'Coprinus_comatus': {
                    'lifespan': '24 hours (dissolves quickly)',
                    'preservation': '10 days refrigerated, 18 days with treatment.'
                }
            }
            
            info = species_info.get(species, {})
            
            result.update({
                'species': species,
                'species_confidence': species_confidence,
                'species_probability': species_confidence / 100,
                'lifespan': info.get('lifespan', 'Unknown'),
                'preservation': info.get('preservation', 'Unknown')
            })
        else:
            result.update({
                'warning': 'This mushroom appears to be poisonous or inedible. Do not consume!',
                'safety_note': 'Always consult with expert mycologists before consuming wild mushrooms.'
            })
        
        logger.info(f"Mockup analysis completed: {'Edible' if is_edible else 'Not edible'}")
        return result
        
    except Exception as e:
        logger.error(f"Error in mockup analysis: {str(e)}")
        return {'error': str(e)}