"""Image Selector Module

This module handles random image selection from the images folder
with fallback support for error cases.
"""

import os
import random
import logging
from typing import Optional


class ImageSelector:
    """Selects random images from the images folder.
    
    Provides functionality to randomly select images for photo messages
    with proper error handling and fallback support.
    """
    
    IMAGES_FOLDER = "images"
    
    def __init__(self):
        """Initialize the ImageSelector."""
        self.logger = logging.getLogger(__name__)
    
    def get_random_image_path(self) -> Optional[str]:
        """Get a random image path from the images folder.
        
        Returns:
            Full path to a random image file, or None if no images available
        """
        try:
            # Check if images folder exists
            if not os.path.exists(self.IMAGES_FOLDER):
                self.logger.warning(f"Images folder '{self.IMAGES_FOLDER}' does not exist")
                return None
            
            # Get list of files in images folder
            files = os.listdir(self.IMAGES_FOLDER)
            
            # Filter for image files (common extensions)
            image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
            image_files = [
                f for f in files 
                if os.path.isfile(os.path.join(self.IMAGES_FOLDER, f)) 
                and os.path.splitext(f.lower())[1] in image_extensions
            ]
            
            if not image_files:
                self.logger.warning(f"No image files found in '{self.IMAGES_FOLDER}' folder")
                return None
            
            # Select random image
            selected_file = random.choice(image_files)
            full_path = os.path.join(self.IMAGES_FOLDER, selected_file)
            
            self.logger.info(f"Selected image: {selected_file}")
            return full_path
            
        except Exception as e:
            self.logger.error(f"Error selecting random image: {str(e)}")
            return None
