"""
Image generation with generative AI models.

This module provides functions for generating images using AI models
through the litellm library. Requires optional dependency: litellm.

Example:
    ```python
    from figwizz.generate import generate_images
    prompts = ["a red apple", "a blue ocean"]
    images = generate_images(prompts, output_dir="generated")
    ```
"""

import os, re,  base64
from copy import copy
from PIL import Image
from tqdm.auto import tqdm

from .utils import check_optional_import

def generate_images(prompts, output_dir, n_images=1, model='gpt-image-1', 
                    api_key=None, return_images=True):
    """
    Generate images from prompts using generative AI.
    
    Args:
        prompts: List of prompts to generate images from.
        output_dir: Directory to save the generated images.
        n_images: Number of images to generate for each prompt.
        model: Model to use for image generation.
        api_key: API key for the generative AI model.
        return_images: Whether to return the generated images as PIL Image objects.
        
    Returns:
        List of PIL Image objects if return_images is True, otherwise None.
    """
    
    if not check_optional_import('litellm'):
        raise ImportError("litellm is required for image generation. Install it with: pip install litellm or pip install 'figwizz[genai]'")
    
    from litellm import image_generation
    
    if api_key is None:
        api_key = os.getenv('OPENAI_API_KEY')
        
    if api_key is None:
        raise ValueError("OPENAI_API_KEY required for image generation. Set it in the .env file or pass it as an argument.")
    
    if not isinstance(prompts, list):
        prompts = [prompts]
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
        
    image_paths = [] # list to store the paths to the generated images
        
    for prompt in tqdm(prompts, desc="Processing Prompts"):
        prompt_for_filepath = copy(prompt).lower()
        
        # remove common english articles
        prompt_for_filepath = re.sub(r'\b(a|an|the)\b', '', prompt_for_filepath)
        
        # Remove all non-alphanumeric characters
        prompt_for_filepath = re.sub(r'[^a-z0-9\s]', '', prompt_for_filepath)
        
        # Replace whitespace with a single dash
        prompt_for_filepath = re.sub(r'\s+', '-', prompt_for_filepath)
        
        # Replace double dashes with single dash
        prompt_for_filepath = re.sub(r'--', '-', prompt_for_filepath)
        
        # Remove leading/trailing dashes
        prompt_for_filepath = prompt_for_filepath.strip('-')
        
        output_subdir = os.path.join(output_dir, prompt_for_filepath)
        os.makedirs(output_subdir, exist_ok=True)
        
        for image_index in tqdm(range(n_images), desc="Generating Images"):
            try: # to generate and parse the image
                response = image_generation(
                    prompt=prompt, 
                    size='1024x1024', 
                    model=model,
                    api_key=api_key,
                )
                
                image_data = response['data'][0]['b64_json']
                image_path = os.path.join(output_subdir, f"image_{image_index + 1}.png")
                
                if os.path.exists(image_path):
                    last_index = int(image_path.split('_')[-1].split('.')[0])
                    image_path = os.path.join(output_subdir, f"image_{last_index + 1}.png")
                
                with open(image_path, "wb") as filepath:
                    filepath.write(base64.b64decode(image_data))
                
                image_paths.append(image_path)
                    
            except Exception as error:
                print(f"Error generating image for prompt: {prompt}")
                print(f"   Error: {error}")
                continue
            
    if return_images:
        return [Image.open(image_path) for image_path in image_paths]