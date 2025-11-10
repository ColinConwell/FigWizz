"""
Tests for GenAI functions
"""

import os
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from figwizz.workflows.genai import (
    convert_response_to_dict,
    gather_image_from_generative_ai,
    _recursive_convert_to_dict,
    _recursive_keep_keys,
)


class TestResponseConversion:
    """Tests for response conversion utilities."""
    
    def test_recursive_convert_to_dict_primitive(self):
        """Test converting primitive types."""
        assert _recursive_convert_to_dict(42) == 42
        assert _recursive_convert_to_dict("hello") == "hello"
        assert _recursive_convert_to_dict(3.14) == 3.14
        assert _recursive_convert_to_dict(True) is True
        assert _recursive_convert_to_dict(None) is None
    
    def test_recursive_convert_to_dict_list(self):
        """Test converting lists."""
        result = _recursive_convert_to_dict([1, 2, "three", [4, 5]])
        assert result == [1, 2, "three", [4, 5]]
    
    def test_recursive_convert_to_dict_dict(self):
        """Test converting dictionaries."""
        input_dict = {"a": 1, "b": {"c": 2, "d": [3, 4]}}
        result = _recursive_convert_to_dict(input_dict)
        assert result == {"a": 1, "b": {"c": 2, "d": [3, 4]}}
    
    def test_recursive_convert_to_dict_object(self):
        """Test converting objects with __dict__."""
        class MockResponse:
            def __init__(self):
                self.status = "success"
                self.code = 200
                self.data = {"key": "value"}
        
        response = MockResponse()
        result = _recursive_convert_to_dict(response)
        assert result == {
            "status": "success",
            "code": 200,
            "data": {"key": "value"}
        }
    
    def test_recursive_convert_to_dict_bytes(self):
        """Test converting bytes to string."""
        result = _recursive_convert_to_dict(b"hello world")
        assert result == "hello world"
    
    def test_recursive_convert_to_dict_nested_objects(self):
        """Test converting nested objects."""
        class InnerObject:
            def __init__(self):
                self.inner_value = "nested"
        
        class OuterObject:
            def __init__(self):
                self.outer_value = "outer"
                self.inner = InnerObject()
                self.list_of_objects = [InnerObject(), InnerObject()]
        
        result = _recursive_convert_to_dict(OuterObject())
        assert result["outer_value"] == "outer"
        assert result["inner"]["inner_value"] == "nested"
        assert len(result["list_of_objects"]) == 2
        assert result["list_of_objects"][0]["inner_value"] == "nested"
    
    def test_recursive_keep_keys_dict(self):
        """Test filtering dictionary keys."""
        input_dict = {"a": 1, "b": 2, "c": 3, "d": 4}
        result = _recursive_keep_keys(input_dict, ["a", "c"])
        assert result == {"a": 1, "c": 3}
    
    def test_recursive_keep_keys_nested(self):
        """Test filtering nested dictionary keys."""
        input_dict = {
            "keep_me": {"also_keep": 1, "remove": 2},
            "remove_me": {"also_keep": 3}
        }
        result = _recursive_keep_keys(input_dict, ["keep_me", "also_keep"])
        assert "keep_me" in result
        assert "remove_me" not in result
        assert "also_keep" in result["keep_me"]
        assert "remove" not in result["keep_me"]
    
    def test_recursive_keep_keys_object(self):
        """Test filtering object attributes."""
        class MockResponse:
            def __init__(self):
                self.keep_this = "value1"
                self.remove_this = "value2"
                self.also_keep = "value3"
        
        response = MockResponse()
        result = _recursive_keep_keys(response, ["keep_this", "also_keep"])
        assert "keep_this" in result
        assert "also_keep" in result
        assert "remove_this" not in result
    
    def test_convert_response_to_dict_no_filter(self):
        """Test converting response without filtering keys."""
        class MockResponse:
            def __init__(self):
                self.status = "success"
                self.data = {"image": "url"}
        
        response = MockResponse()
        result = convert_response_to_dict(response)
        assert result == {"status": "success", "data": {"image": "url"}}
    
    def test_convert_response_to_dict_with_filter(self):
        """Test converting response with key filtering."""
        class MockResponse:
            def __init__(self):
                self.status = "success"
                self.data = {"image": "url"}
                self.metadata = {"unwanted": "info"}
        
        response = MockResponse()
        result = convert_response_to_dict(response, keep_keys=["status", "data"])
        assert "status" in result
        assert "data" in result
        assert "metadata" not in result


class TestGatherImage:
    """Tests for gather_image_from_generative_ai function."""
    
    def test_gather_image_not_implemented(self):
        """Test that gather_image_from_generative_ai raises NotImplementedError."""
        with pytest.raises(NotImplementedError, match="not yet implemented"):
            gather_image_from_generative_ai({"data": "test"})


class TestGenerateImages:
    """Tests for image generation functionality."""
    
    def test_generate_images_missing_litellm(self):
        """Test error when litellm is not installed."""
        from figwizz.generate import generate_images
        
        with patch('figwizz.generate.check_optional_import', return_value=False):
            with pytest.raises(ImportError, match="litellm is required"):
                generate_images("test prompt", "output")
    
    def test_generate_images_missing_api_key(self, monkeypatch):
        """Test error when API key is missing."""
        from figwizz.generate import generate_images
        
        monkeypatch.delenv('OPENAI_API_KEY', raising=False)
        
        with patch('figwizz.generate.check_optional_import', return_value=True):
            with pytest.raises(ValueError, match="OPENAI_API_KEY required"):
                generate_images("test prompt", "output", api_key=None)
    
    @patch('figwizz.generate.check_optional_import')
    @patch('litellm.image_generation')
    def test_generate_images_single_prompt_mock(self, mock_image_gen, mock_check_import, temp_dir):
        """Test generating a single image with mocked API."""
        # Setup mocks
        mock_check_import.return_value = True
        
        # Mock the response with base64 encoded image data
        import base64
        from PIL import Image
        from io import BytesIO
        
        # Create a simple test image
        test_img = Image.new('RGB', (10, 10), color='red')
        img_buffer = BytesIO()
        test_img.save(img_buffer, format='PNG')
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        
        mock_response = {
            'data': [{'b64_json': img_base64}]
        }
        mock_image_gen.return_value = mock_response
        
        from figwizz.generate import generate_images
        
        # Generate images
        result = generate_images(
            "a red apple",
            str(temp_dir),
            n_images=1,
            api_key='test_key',
            return_images=False
        )
        
        # Verify image_generation was called
        mock_image_gen.assert_called_once()
        call_args = mock_image_gen.call_args
        assert call_args[1]['prompt'] == "a red apple"
        assert call_args[1]['model'] == 'gpt-image-1'
        assert call_args[1]['api_key'] == 'test_key'
    
    @patch('figwizz.generate.check_optional_import')
    @patch('litellm.image_generation')
    def test_generate_images_multiple_prompts_mock(self, mock_image_gen, mock_check_import, temp_dir):
        """Test generating images from multiple prompts."""
        # Setup mocks
        mock_check_import.return_value = True
        
        import base64
        from PIL import Image
        from io import BytesIO
        
        test_img = Image.new('RGB', (10, 10), color='blue')
        img_buffer = BytesIO()
        test_img.save(img_buffer, format='PNG')
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        
        mock_response = {
            'data': [{'b64_json': img_base64}]
        }
        mock_image_gen.return_value = mock_response
        
        from figwizz.generate import generate_images
        
        prompts = ["a red apple", "a blue ocean"]
        generate_images(
            prompts,
            str(temp_dir),
            n_images=1,
            api_key='test_key',
            return_images=False
        )
        
        # Should be called once per prompt
        assert mock_image_gen.call_count == 2
    
    @patch('figwizz.generate.check_optional_import')
    @patch('litellm.image_generation')
    def test_generate_images_error_handling_mock(self, mock_image_gen, mock_check_import, temp_dir, capsys):
        """Test error handling when image generation fails."""
        mock_check_import.return_value = True
        mock_image_gen.side_effect = Exception("API Error")
        
        from figwizz.generate import generate_images
        
        # Should not raise, but print error
        generate_images(
            "test prompt",
            str(temp_dir),
            n_images=1,
            api_key='test_key',
            return_images=False
        )
        
        captured = capsys.readouterr()
        assert "Error generating image" in captured.out
        assert "API Error" in captured.out
    
    @patch('figwizz.generate.check_optional_import')
    @patch('litellm.image_generation')
    def test_generate_images_custom_model_mock(self, mock_image_gen, mock_check_import, temp_dir):
        """Test using a custom model."""
        mock_check_import.return_value = True
        
        import base64
        from PIL import Image
        from io import BytesIO
        
        test_img = Image.new('RGB', (10, 10), color='green')
        img_buffer = BytesIO()
        test_img.save(img_buffer, format='PNG')
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        
        mock_response = {
            'data': [{'b64_json': img_base64}]
        }
        mock_image_gen.return_value = mock_response
        
        from figwizz.generate import generate_images
        
        generate_images(
            "test prompt",
            str(temp_dir),
            n_images=1,
            model='dall-e-3',
            api_key='test_key',
            return_images=False
        )
        
        call_args = mock_image_gen.call_args
        assert call_args[1]['model'] == 'dall-e-3'


# Integration tests - make actual API calls
@pytest.mark.requires_litellm
@pytest.mark.requires_network
@pytest.mark.skipif(
    not os.getenv('OPENAI_API_KEY'),
    reason="OPENAI_API_KEY not available in environment"
)
class TestGenerateImagesIntegration:
    """Integration tests that make actual API calls."""
    
    def test_generate_single_image_integration(self, temp_dir):
        """Test generating a real image from OpenAI."""
        try:
            import litellm
        except ImportError:
            pytest.skip("litellm not installed")
        
        from figwizz.generate import generate_images
        
        api_key = os.getenv('OPENAI_API_KEY')
        
        # Generate a simple image
        generate_images(
            "a simple red circle",
            str(temp_dir),
            n_images=1,
            model='dall-e-2',  # Use dall-e-2 as it's cheaper for testing
            api_key=api_key,
            return_images=False
        )
        
        # Check that image was created
        generated_files = list(Path(temp_dir).glob("*.png"))
        assert len(generated_files) > 0
        
        # Verify it's a valid image
        from PIL import Image
        img = Image.open(generated_files[0])
        assert img.size[0] > 0
        assert img.size[1] > 0
    
    def test_generate_multiple_images_integration(self, temp_dir):
        """Test generating multiple images."""
        try:
            import litellm
        except ImportError:
            pytest.skip("litellm not installed")
        
        from figwizz.generate import generate_images
        
        api_key = os.getenv('OPENAI_API_KEY')
        
        # Generate multiple images
        generate_images(
            "a simple geometric shape",
            str(temp_dir),
            n_images=2,
            model='dall-e-2',
            api_key=api_key,
            return_images=False
        )
        
        # Check that images were created
        generated_files = list(Path(temp_dir).glob("*.png"))
        assert len(generated_files) >= 2

