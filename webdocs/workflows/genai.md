# AI Image Generation

Generate images from text prompts using AI models.

## Installation

Install with AI support:

```bash
pip install figwizz[genai]
```

This installs the `litellm` library for AI model access.

## Basic Generation

Generate images from prompts:

```python
from figwizz.generate import generate_images
import os

# Set API key
os.environ['OPENAI_API_KEY'] = 'your_openai_key'

# Generate single image
images = generate_images(
    prompts=['a serene mountain landscape at sunset'],
    output_dir='generated',
    n_images=1
)
```

## Batch Generation

Generate multiple images from multiple prompts:

```python
prompts = [
    'a futuristic city skyline',
    'abstract geometric patterns in blue',
    'minimalist line art of a tree',
    'vibrant coral reef underwater scene'
]

images = generate_images(
    prompts=prompts,
    output_dir='ai_images',
    n_images=3,  # 3 variations per prompt
    model='dall-e-3'
)
```

## Using Environment Files

Store your API key securely:

```bash
# .env
OPENAI_API_KEY=your_key_here
```

Load and generate:

```python
from figwizz.utils import load_env_variables
from figwizz.generate import generate_images

# Load environment
load_env_variables()

# Generate images
images = generate_images(
    prompts=['cosmic nebula in deep space'],
    output_dir='space_images'
)
```

## Supported Models

FigWizz uses litellm which supports multiple AI models:

```python
# DALL-E 3 (OpenAI)
images = generate_images(
    prompts=['artwork'],
    output_dir='output',
    model='dall-e-3',
    api_key='openai_key'
)

# DALL-E 2 (OpenAI)
images = generate_images(
    prompts=['artwork'],
    output_dir='output',
    model='dall-e-2',
    api_key='openai_key'
)

# Stable Diffusion (via API providers)
images = generate_images(
    prompts=['artwork'],
    output_dir='output',
    model='stabilityai/stable-diffusion',
    api_key='stability_key'
)
```

## Return PIL Images

Get PIL Images directly for further processing:

```python
images = generate_images(
    prompts=['abstract art'],
    output_dir='temp',
    return_images=True
)

# images is now a list of PIL Image objects
for i, img in enumerate(images):
    # Process image
    img = img.resize((512, 512))
    img.save(f'processed_{i}.png')
```

## Error Handling

Handle generation errors gracefully:

```python
from figwizz.generate import generate_images

prompts = [
    'valid prompt 1',
    'valid prompt 2',
    'potentially problematic prompt'
]

try:
    images = generate_images(
        prompts=prompts,
        output_dir='output',
        n_images=2
    )
    print(f"Successfully generated {len(images)} images")
except Exception as e:
    print(f"Generation failed: {e}")
```

## Post-Processing

Process generated images:

```python
from figwizz.generate import generate_images
from figwizz import make_hexicon, convert_image

# Generate
images = generate_images(
    prompts=['logo concept'],
    output_dir='generated',
    return_images=True
)

# Post-process
for i, img in enumerate(images):
    # Create hexicon version
    hexicon = make_hexicon(img, border_size=10, border_color='auto')
    hexicon.save(f'hexicon_{i}.png')
    
    # Convert to JPEG
    convert_image(img, 'jpg')
```

## Progress Tracking

Generation includes progress bars via tqdm:

```python
from figwizz.generate import generate_images

# Progress bars show automatically
images = generate_images(
    prompts=['prompt1', 'prompt2', 'prompt3'],
    output_dir='output',
    n_images=5  # Shows progress for both prompts and images
)
```

## Workflow Example

Complete workflow from generation to hexicon:

```python
from figwizz.utils import load_env_variables
from figwizz.generate import generate_images
from figwizz import make_hexicon
from pathlib import Path

# Setup
load_env_variables()
output_dir = Path('project_icons')
output_dir.mkdir(exist_ok=True)

# Define prompts
prompts = [
    'minimalist python snake logo',
    'abstract data visualization icon',
    'geometric mountain peak symbol'
]

# Generate
print("Generating images...")
images = generate_images(
    prompts=prompts,
    output_dir=str(output_dir / 'raw'),
    n_images=3,
    return_images=True
)

# Create hexicons
print("Creating hexicons...")
hexicon_dir = output_dir / 'hexicons'
hexicon_dir.mkdir(exist_ok=True)

for i, img in enumerate(images):
    hexicon = make_hexicon(
        img,
        size=(500, 500),
        border_size=15,
        border_color='auto',
        padding=40
    )
    hexicon.save(hexicon_dir / f'hexicon_{i:02d}.png')

print(f"Created {len(images)} hexicons!")
```

## API Costs

Be mindful of API costs:

- DALL-E 3: ~$0.04 per image
- DALL-E 2: ~$0.02 per image
- Costs vary by model and provider

Use `n_images` carefully to control costs.

## Troubleshooting

### API Key Not Found

```python
ValueError: OPENAI_API_KEY required for image generation
```

Solution: Set the environment variable:
```bash
export OPENAI_API_KEY="your_key"
```

### litellm Not Installed

```python
ImportError: litellm is required for image generation
```

Solution: Install genai extras:
```bash
pip install figwizz[genai]
```

### Rate Limiting

If you hit rate limits, add delays:

```python
import time
from figwizz.generate import generate_images

for prompt in prompts:
    images = generate_images([prompt], 'output', n_images=1)
    time.sleep(2)  # Wait 2 seconds between requests
```

## See Also

- [Installation](../installation.md) - Setting up API keys
- [Icon Workflows](icons.md) - Creating hexicons from generated images
- [API Reference](../api/reference.md) - Complete API documentation

