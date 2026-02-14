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
from io import BytesIO
from datetime import datetime
from typing import Any, Dict
from PIL import Image
from tqdm.auto import tqdm

from .utils import check_optional_import
from .utils.images import normalize_image_input

from .workflows.genai import (
    make_json_serializable,
    extract_image_from_genai_response,
)

def extract_image_data(response: Any) -> tuple[bytes, Dict[str, Any]]:
    """
    Extract image data from a generative AI response.
    
    This is a convenience wrapper around extract_image_from_genai_response.
    It handles various response formats from different AI providers.
    
    Args:
        response (Any): The response object from a generative AI model (e.g., OpenAI,
            Google, OpenRouter). Can be a dictionary or custom response object.
        
    Returns:
        tuple[bytes, dict]: A tuple containing:
            - bytes: Raw image data ready to be saved
            - dict: Metadata about the extraction method and format
    
    Examples:
        ```python
        from figwizz.generate import extract_image_data
        from litellm import image_generation
        
        # Generate image
        response = image_generation(prompt="a sunset", model="gpt-image-1.5")
        
        # Extract image bytes
        image_bytes, metadata = extract_image_data(response)
        
        # Save to file
        with open('sunset.png', 'wb') as f:
            f.write(image_bytes)
        ```
    
    Note:
        - Supports base64 and URL-based image responses
        - Automatically handles various AI provider response formats
        - See extract_image_from_genai_response for detailed format support
    """
    return extract_image_from_genai_response(response)

def _sanitize_for_path(text):
    """Sanitize a string for safe use as a directory/file name."""
    text = text.lower()
    text = re.sub(r'\b(a|an|the)\b', '', text)
    text = re.sub(r'[^a-z0-9\s_-]', '', text)
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'-{2,}', '-', text)
    return text.strip('-') or 'unnamed'


def _get_seed_label(seed_input, index):
    """Derive a filesystem-safe label for a seed image."""
    if isinstance(seed_input, (str, os.PathLike)):
        s = str(seed_input)
        if not s.startswith(('http://', 'https://')) and len(s) < 500:
            name = os.path.splitext(os.path.basename(s))[0]
            if name:
                return _sanitize_for_path(name)
    return f"seed_{index + 1}"


def _prepare_seed_image(seed_input):
    """Normalize a seed image to a seekable BytesIO file-like object."""
    pil_seed = normalize_image_input(seed_input, return_type='pil')
    seed_buffer = BytesIO()
    pil_seed.save(seed_buffer, format='PNG')
    seed_buffer.seek(0)
    seed_buffer.name = 'seed_image.png'
    return seed_buffer


def generate_images(prompts, output_dir, n_images=1, model='gpt-image-1.5', 
                    seed_image=None, api_key=None, return_images=True,
                    disable_seed_warning=False):
    """
    Generate images from text prompts using generative AI models.
    
    Uses the litellm library to generate images from various AI providers including
    OpenAI, Google, and OpenRouter. Each generated image is saved with comprehensive
    metadata including the prompt, model, timestamp, and API response details.
    
    When a seed_image is provided, the function uses the image editing endpoint
    (litellm.image_edit) to generate images that reference the seed image. This
    is useful for style transfer, modifications, or using an existing image as a
    starting point. The seed_image is normalized via figwizz's image handlers,
    so it can be a file path, URL, PIL Image, bytes, numpy array, or base64 string.
    
    A list of seed images can also be provided; in that case, each prompt is applied
    to every seed image, producing n_images per (prompt, seed_image) pair. The user
    is warned about the total image count and asked for confirmation before proceeding
    (this can be suppressed with disable_seed_warning=True). When seed images are
    used, outputs are organized into per-seed subfolders within each prompt directory.
    
    Args:
        prompts (str or list[str]): Text prompt(s) describing the desired image(s).
            Can be a single string or a list of strings for batch generation.
        output_dir (str): Directory where generated images and metadata will be saved.
            Created automatically if it doesn't exist.
        n_images (int, optional): Number of images to generate per (prompt, seed_image)
            pair. Defaults to 1.
        model (str, optional): Model identifier for image generation. Common options:
            - 'gpt-image-1.5' (OpenAI GPT Image 1.5, latest)
            - 'gpt-image-1' (OpenAI GPT Image 1)
            - 'dall-e-3' (OpenAI DALL-E 3)
            - 'dall-e-2' (OpenAI DALL-E 2)
            Defaults to 'gpt-image-1.5'.
        seed_image (optional): A reference image (or list of reference images) to use
            as a starting point for generation. Each element accepts any format
            supported by normalize_image_input: file path, URL, PIL Image, bytes,
            numpy array, base64 string, or file-like object. When provided, the
            image editing endpoint is used instead of the generation endpoint.
            If a list is provided, each prompt is applied to every seed image,
            and outputs are organized into per-seed subfolders. Defaults to None.
        api_key (str, optional): API key for the AI service. If None, reads from
            OPENAI_API_KEY environment variable. Defaults to None.
        return_images (bool, optional): If True, returns list of PIL Image objects.
            If False, only saves images and returns None. Defaults to True.
        disable_seed_warning (bool, optional): If True, suppresses the confirmation
            prompt that appears when multiple seed images would multiply the total
            image count. Defaults to False.
        
    Returns:
        list[PIL.Image.Image] or None: List of PIL Image objects if return_images=True,
            otherwise None
    
    Raises:
        ImportError: If litellm is not installed
        ValueError: If OPENAI_API_KEY is not set and api_key is None
    
    Examples:
        ```python
        from figwizz import generate_images
        
        # Generate a single image
        images = generate_images(
            "a serene mountain landscape at sunset",
            output_dir="generated_images"
        )
        images[0].show()
        
        # Generate multiple images from multiple prompts
        prompts = [
            "a red apple on a wooden table",
            "a blue ocean with white clouds",
            "a futuristic city at night"
        ]
        images = generate_images(
            prompts,
            output_dir="ai_art",
            n_images=2,  # 2 variations per prompt
            model="gpt-image-1"
        )
        
        # Generate with a single seed image (uses image editing endpoint)
        images = generate_images(
            "transform this into a watercolor painting",
            output_dir="edited_images",
            seed_image="reference_photo.png"
        )
        
        # Generate with multiple seed images
        # This will produce 3 prompts x 2 seeds x 1 image = 6 total images
        images = generate_images(
            prompts,
            output_dir="multi_seed",
            seed_image=["photo_a.png", "photo_b.png"]
        )
        
        # Suppress the confirmation prompt for batch seed generation
        images = generate_images(
            prompts,
            output_dir="multi_seed",
            seed_image=["photo_a.png", "photo_b.png"],
            disable_seed_warning=True
        )
        
        # Generate without returning images (saves memory)
        generate_images(
            prompts,
            output_dir="batch_output",
            return_images=False
        )
        ```
    
    Note:
        - Requires litellm: `pip install litellm` or `pip install 'figwizz[genai]'`
        - Each prompt creates a subdirectory named after the prompt (sanitized)
        - When seed images are used, an additional subfolder level is created per
          seed image (named after the source file, or seed_1, seed_2, etc.)
        - For each image, saves:
          * image_N.png - The generated image
          * image_N_response.json - Full API response
          * image_N_metadata.json - Curated metadata (prompt, model, timestamp, etc.)
        - Failed generations are skipped with error messages
        - Progress is displayed via tqdm progress bars
        - Image numbering continues from existing images in subdirectories
        - Prompt text is sanitized for use in directory names (removes special chars)
        - When seed_image is provided, litellm.image_edit() is used instead of
          litellm.image_generation(), routing through OpenAI's /images/edits endpoint
    """
    
    if not check_optional_import('litellm'):
        raise ImportError("litellm is required for image generation. Install it with: pip install litellm or pip install 'figwizz[genai]'")
    
    from litellm import image_generation, image_edit
    
    if api_key is None:
        api_key = os.getenv('OPENAI_API_KEY')
        
    if api_key is None:
        raise ValueError("OPENAI_API_KEY required for image generation. Set it in the .env file or pass it as an argument.")
    
    if not isinstance(prompts, list):
        prompts = [prompts]
    
    # ---------------------
    # Normalize seed images
    # ---------------------
    # Build a list of (label, BytesIO) tuples, or None if no seeds provided.
    seed_entries = None  # list of (label, BytesIO, original_input)
    if seed_image is not None:
        raw_seeds = seed_image if isinstance(seed_image, list) else [seed_image]
        
        seed_entries = []
        for idx, si in enumerate(raw_seeds):
            label = _get_seed_label(si, idx)
            seed_file = _prepare_seed_image(si)
            seed_entries.append((label, seed_file, si))
        
        # Warn about total image count when multiple seeds are provided
        if len(seed_entries) > 1 and not disable_seed_warning:
            n_prompts = len(prompts)
            n_seeds = len(seed_entries)
            total = n_prompts * n_seeds * n_images
            print(
                f"Warning: {n_seeds} seed images x {n_prompts} prompt(s) "
                f"x {n_images} image(s) = {total} total images to generate."
            )
            confirmation = input("Continue? [y/N]: ").strip().lower()
            if confirmation not in ('y', 'yes'):
                print("Generation aborted by user.")
                return [] if return_images else None
    
    # When seeds are present, iterate over them; otherwise use a single
    # pass with (None, None, None) so the loop body stays unified.
    generation_targets = seed_entries if seed_entries is not None else [(None, None, None)]
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
        
    image_paths = []  # list to store the paths to the generated images
        
    for prompt in tqdm(prompts, desc="Processing Prompts"):
        prompt_for_filepath = _sanitize_for_path(prompt)
        
        prompt_subdir = os.path.join(output_dir, prompt_for_filepath)
        os.makedirs(prompt_subdir, exist_ok=True)
        
        seed_iter = generation_targets
        if len(generation_targets) > 1:
            seed_iter = tqdm(generation_targets, desc="Seed Images")
        
        for seed_label, seed_file, seed_original in seed_iter:
            # Determine output directory for this (prompt, seed) pair
            if seed_label is not None:
                target_dir = os.path.join(prompt_subdir, seed_label)
                os.makedirs(target_dir, exist_ok=True)
            else:
                target_dir = prompt_subdir
            
            for image_index in tqdm(range(n_images), desc="Generating Images"):
                response = None
                response_path = None
                
                try:
                    if seed_file is not None:
                        # Use image editing endpoint with seed image as reference
                        seed_file.seek(0)
                        response = image_edit(
                            prompt=prompt,
                            image=seed_file,
                            size='1024x1024',
                            model=model,
                            api_key=api_key,
                        )
                    else:
                        # Standard image generation (no seed image)
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
                image_path = os.path.join(target_dir, f"image_{image_index + 1}.png")
                response_path = os.path.join(target_dir, f"image_{image_index + 1}_response.json")
                metadata_path = os.path.join(target_dir, f"image_{image_index + 1}_metadata.json")
                
                # Handle existing files by incrementing index
                if os.path.exists(image_path):
                    last_index = int(image_path.split('_')[-1].split('.')[0])
                    image_path = os.path.join(target_dir, f"image_{last_index + 1}.png")
                    response_path = os.path.join(target_dir, f"image_{last_index + 1}_response.json")
                    metadata_path = os.path.join(target_dir, f"image_{last_index + 1}_metadata.json")
                
                try:
                    # Convert response to JSON-serializable format and save
                    serializable_response = make_json_serializable(response)
                    
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
                    image_bytes, extraction_metadata = extract_image_data(response)
                    
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
                        'seed_image': seed_label,
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