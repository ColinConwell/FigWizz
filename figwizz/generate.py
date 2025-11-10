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

import os, re, json
import base64
import requests
from copy import copy
from datetime import datetime
from typing import Any, Dict
from PIL import Image
from tqdm.auto import tqdm

from .utils import check_optional_import
from .workflows.genai import convert_response_to_dict


def _make_json_serializable(obj: Any) -> Any:
    """
    Convert an object to a JSON-serializable format.
    
    Handles various non-serializable types including litellm response objects,
    datetime objects, and custom classes with __dict__.
    """
    return convert_response_to_dict(obj)


def _extract_image_data(response: Any) -> tuple[bytes, Dict[str, Any]]:
    """
    Extract image data from various response formats.
    
    Supports multiple response structures:
    - response['data'][0] with 'b64_json' or 'url'
    - response['data'][0] with 'image' key containing base64
    - response with direct 'b64_json', 'url', or 'image' keys
    - response['choices'][0]['image'] (for some API formats)
    
    Returns:
        tuple: (image_bytes, metadata_dict) where metadata contains info about the response
    """
    metadata = {'extraction_method': None, 'original_format': None}
    
    # Try to convert response to dict if it's an object
    if hasattr(response, '__dict__') and not isinstance(response, dict):
        response_dict = _make_json_serializable(response)
    else:
        response_dict = response
    
    # Method 1: Standard format with data array
    if isinstance(response_dict, dict) and 'data' in response_dict:
        data = response_dict['data']
        if isinstance(data, list) and len(data) > 0:
            item = data[0]
        elif isinstance(data, dict):
            item = data
        else:
            raise ValueError(f"Unexpected 'data' format: {type(data)}")
        
        # Check for b64_json
        if isinstance(item, dict) and 'b64_json' in item and item['b64_json'] is not None:
            image_str = item['b64_json']
            metadata['extraction_method'] = 'data[0].b64_json'
            metadata['original_format'] = 'base64'
            
            # Handle data URI format
            if image_str.startswith('data:image/'):
                image_str = image_str.split(',', 1)[1]
            
            return base64.b64decode(image_str), metadata
        
        # Check for url
        elif isinstance(item, dict) and 'url' in item and item['url'] is not None:
            url = item['url']
            metadata['extraction_method'] = 'data[0].url'
            metadata['original_format'] = 'url'
            metadata['source_url'] = url
            
            response_obj = requests.get(url)
            response_obj.raise_for_status()
            return response_obj.content, metadata
        
        # Check for direct image key
        elif isinstance(item, dict) and 'image' in item and item['image'] is not None:
            image_str = item['image']
            metadata['extraction_method'] = 'data[0].image'
            metadata['original_format'] = 'base64'
            
            if image_str.startswith('data:image/'):
                image_str = image_str.split(',', 1)[1]
            
            return base64.b64decode(image_str), metadata
    
    # Method 2: Direct keys at top level
    if isinstance(response_dict, dict):
        if 'b64_json' in response_dict and response_dict['b64_json'] is not None:
            image_str = response_dict['b64_json']
            metadata['extraction_method'] = 'root.b64_json'
            metadata['original_format'] = 'base64'
            
            if image_str.startswith('data:image/'):
                image_str = image_str.split(',', 1)[1]
            
            return base64.b64decode(image_str), metadata
        
        elif 'url' in response_dict and response_dict['url'] is not None:
            url = response_dict['url']
            metadata['extraction_method'] = 'root.url'
            metadata['original_format'] = 'url'
            metadata['source_url'] = url
            
            response_obj = requests.get(url)
            response_obj.raise_for_status()
            return response_obj.content, metadata
        
        elif 'image' in response_dict and response_dict['image'] is not None:
            image_str = response_dict['image']
            metadata['extraction_method'] = 'root.image'
            metadata['original_format'] = 'base64'
            
            if image_str.startswith('data:image/'):
                image_str = image_str.split(',', 1)[1]
            
            return base64.b64decode(image_str), metadata
        
        # Method 3: Choices format (some APIs use this)
        elif 'choices' in response_dict:
            choices = response_dict['choices']
            if isinstance(choices, list) and len(choices) > 0:
                item = choices[0]
                if isinstance(item, dict) and 'image' in item and item['image'] is not None:
                    image_str = item['image']
                    metadata['extraction_method'] = 'choices[0].image'
                    metadata['original_format'] = 'base64'
                    
                    if image_str.startswith('data:image/'):
                        image_str = image_str.split(',', 1)[1]
                    
                    return base64.b64decode(image_str), metadata
    
    # If we got here, we couldn't parse the response
    if isinstance(response_dict, dict):
        # Build a helpful error message showing what keys were found
        found_keys = list(response_dict.keys())
        none_keys = [k for k in ['b64_json', 'url', 'image', 'data', 'choices'] if k in response_dict and response_dict[k] is None]
        
        error_msg = f"Unable to extract image data from response. Found keys: {found_keys}"
        if none_keys:
            error_msg += f"\nNote: These image-related keys were present but had None values: {none_keys}"
        
        if 'data' in response_dict:
            data = response_dict['data']
            if isinstance(data, list) and len(data) > 0:
                error_msg += f"\nFirst data item keys: {list(data[0].keys()) if isinstance(data[0], dict) else type(data[0])}"
            elif isinstance(data, dict):
                error_msg += f"\nData keys: {list(data.keys())}"
        
        raise ValueError(error_msg)
    else:
        raise ValueError(f"Unable to extract image data. Response type: {type(response_dict)}")

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
            response = None
            response_path = None
            
            try:
                # Generate the image
                response = image_generation(
                    prompt=prompt, 
                    size='1024x1024', 
                    model=model,
                    api_key=api_key,
                )
                
            except Exception as error:
                print(f"Error generating image for prompt: {prompt}")
                print(f"   Error: {error}")
                continue
            
            # Prepare file paths
            image_path = os.path.join(output_subdir, f"image_{image_index + 1}.png")
            response_path = os.path.join(output_subdir, f"image_{image_index + 1}_response.json")
            metadata_path = os.path.join(output_subdir, f"image_{image_index + 1}_metadata.json")
            
            # Handle existing files by incrementing index
            if os.path.exists(image_path):
                last_index = int(image_path.split('_')[-1].split('.')[0])
                image_path = os.path.join(output_subdir, f"image_{last_index + 1}.png")
                response_path = os.path.join(output_subdir, f"image_{last_index + 1}_response.json")
                metadata_path = os.path.join(output_subdir, f"image_{last_index + 1}_metadata.json")
            
            try:
                # Convert response to JSON-serializable format and save
                serializable_response = _make_json_serializable(response)
                
                with open(response_path, 'w') as json_file:
                    json.dump(serializable_response, json_file, indent=2)
                
            except Exception as error:
                print(f"Warning: Could not save full response to JSON: {error}")
                print(f"   Attempting to save string representation instead")
                try:
                    with open(response_path, 'w') as json_file:
                        json.dump({'response_str': str(response), 'error': str(error)}, json_file, indent=2)
                except Exception as nested_error:
                    print(f"   Failed to save response: {nested_error}")
            
            try:
                # Extract image data using the helper function
                image_bytes, extraction_metadata = _extract_image_data(response)
                
                # Save the image
                with open(image_path, "wb") as filepath:
                    filepath.write(image_bytes)
                
                # Create and save comprehensive metadata
                metadata = {
                    'prompt': prompt,
                    'model': model,
                    'timestamp': datetime.now().isoformat(),
                    'image_path': image_path,
                    'response_path': response_path,
                    'extraction_info': extraction_metadata
                }
                
                with open(metadata_path, 'w') as json_file:
                    json.dump(metadata, json_file, indent=2)
                
                image_paths.append(image_path)
                    
            except ValueError as error:
                print(f"Error: Unable to parse image from response for prompt: {prompt}")
                print(f"   {error}")
                if response_path and os.path.exists(response_path):
                    print(f"   Full response saved to: {response_path}")
                continue
                
            except Exception as error:
                print(f"Error processing generated image for prompt: {prompt}")
                print(f"   Error type: {type(error).__name__}")
                print(f"   Error: {error}")
                if response_path and os.path.exists(response_path):
                    print(f"   Full response saved to: {response_path}")
                continue
            
    if return_images:
        return [Image.open(image_path) for image_path in image_paths]