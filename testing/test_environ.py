"""
Tests for environment variable loading
"""

import pytest
import os
from pathlib import Path
from figwizz.utils.environ import (
    search_for_env_file, 
    load_env_variables,
    check_capabilities,
    auto_load_env,
)


def test_search_for_env_file(mock_env_file, temp_dir, monkeypatch):
    """Test searching for .env files."""
    monkeypatch.chdir(temp_dir)
    result = search_for_env_file()
    assert result is not None
    assert Path(result).exists()


def test_search_for_env_file_not_found(temp_dir, monkeypatch):
    """Test handling of missing .env file."""
    monkeypatch.chdir(temp_dir)
    # Remove any .env files
    for env_file in temp_dir.glob(".env*"):
        env_file.unlink()
    result = search_for_env_file()
    assert result is None


def test_load_env_variables(mock_env_file, monkeypatch):
    """Test loading environment variables from file."""
    # Clear existing env vars
    for key in ['PIXABAY_API_KEY', 'UNSPLASH_ACCESS_KEY', 'OPENAI_API_KEY']:
        monkeypatch.delenv(key, raising=False)
    
    load_env_variables(mock_env_file, update_environ=True)
    
    assert os.getenv('PIXABAY_API_KEY') == 'test_pixabay_key'
    assert os.getenv('UNSPLASH_ACCESS_KEY') == 'test_unsplash_key'
    assert os.getenv('OPENAI_API_KEY') == 'test_openai_key'


def test_load_env_variables_quoted_values(mock_env_file):
    """Test loading quoted values."""
    env_vars = load_env_variables(mock_env_file, update_environ=False)
    assert env_vars['TEST_VAR'] == 'quoted value'


def test_load_env_variables_inline_comments(mock_env_file):
    """Test handling inline comments."""
    env_vars = load_env_variables(mock_env_file, update_environ=False)
    assert env_vars['TEST_VAR_WITH_COMMENT'] == 'value'


def test_load_env_variables_malformed_line(temp_dir):
    """Test handling of malformed lines."""
    malformed_env = temp_dir / ".env.malformed"
    malformed_env.write_text("VALID_KEY=value\nMALFORMED LINE\nANOTHER_KEY=value2")
    
    env_vars = load_env_variables(str(malformed_env), update_environ=False)
    assert 'VALID_KEY' in env_vars
    assert 'ANOTHER_KEY' in env_vars
    assert 'MALFORMED LINE' not in str(env_vars)


def test_load_env_variables_file_not_found():
    """Test error handling for missing file."""
    with pytest.raises(FileNotFoundError):
        load_env_variables('nonexistent_file.env')


def test_check_capabilities_with_api_keys(monkeypatch):
    """Test capability detection with API keys present."""
    # Set up environment with some API keys
    monkeypatch.setenv('PIXABAY_API_KEY', 'test_key')
    monkeypatch.setenv('OPENAI_API_KEY', 'test_key')
    
    capabilities = check_capabilities(verbose=False)
    
    assert 'stock_image_download' in capabilities
    assert 'pixabay' in capabilities['stock_image_download']
    assert 'genai_image_generation' in capabilities
    assert 'openai' in capabilities['genai_image_generation']


def test_check_capabilities_no_api_keys(monkeypatch):
    """Test capability detection with no API keys."""
    # Clear all relevant API keys
    api_keys = [
        'PIXABAY_API_KEY', 'UNSPLASH_ACCESS_KEY', 
        'OPENAI_API_KEY', 'GOOGLE_API_KEY', 'OPENROUTER_API_KEY'
    ]
    for key in api_keys:
        monkeypatch.delenv(key, raising=False)
    
    capabilities = check_capabilities(verbose=False)
    
    assert capabilities == {}


def test_check_capabilities_multiple_providers(monkeypatch):
    """Test capability detection with multiple providers."""
    # Set up multiple API keys
    monkeypatch.setenv('PIXABAY_API_KEY', 'test_key')
    monkeypatch.setenv('UNSPLASH_ACCESS_KEY', 'test_key')
    monkeypatch.setenv('OPENAI_API_KEY', 'test_key')
    monkeypatch.setenv('GOOGLE_API_KEY', 'test_key')
    
    capabilities = check_capabilities(verbose=False)
    
    assert 'stock_image_download' in capabilities
    assert len(capabilities['stock_image_download']) == 2
    assert 'pixabay' in capabilities['stock_image_download']
    assert 'unsplash' in capabilities['stock_image_download']
    
    assert 'genai_image_generation' in capabilities
    assert len(capabilities['genai_image_generation']) == 2
    assert 'openai' in capabilities['genai_image_generation']
    assert 'google' in capabilities['genai_image_generation']


def test_check_capabilities_verbose(monkeypatch, capsys):
    """Test verbose output of capability detection."""
    monkeypatch.setenv('PIXABAY_API_KEY', 'test_key')
    
    check_capabilities(verbose=True)
    
    captured = capsys.readouterr()
    assert 'Available capabilities:' in captured.out
    assert 'Stock Image Download' in captured.out
    assert 'pixabay' in captured.out


def test_check_capabilities_verbose_no_keys(monkeypatch, capsys):
    """Test verbose output when no API keys present."""
    # Clear all API keys
    api_keys = [
        'PIXABAY_API_KEY', 'UNSPLASH_ACCESS_KEY', 
        'OPENAI_API_KEY', 'GOOGLE_API_KEY', 'OPENROUTER_API_KEY'
    ]
    for key in api_keys:
        monkeypatch.delenv(key, raising=False)
    
    check_capabilities(verbose=True)
    
    captured = capsys.readouterr()
    assert 'No API keys found' in captured.out
    assert 'Basic functionality available' in captured.out


def test_auto_load_env_with_file(mock_env_file, temp_dir, monkeypatch):
    """Test auto_load_env with .env file present."""
    monkeypatch.chdir(temp_dir)
    
    # Clear existing env vars
    for key in ['PIXABAY_API_KEY', 'UNSPLASH_ACCESS_KEY', 'OPENAI_API_KEY']:
        monkeypatch.delenv(key, raising=False)
    
    capabilities = auto_load_env(verbose=False, silent_on_missing=True)
    
    # Verify env vars were loaded
    assert os.getenv('PIXABAY_API_KEY') == 'test_pixabay_key'
    assert os.getenv('OPENAI_API_KEY') == 'test_openai_key'
    
    # Verify capabilities were detected
    assert 'stock_image_download' in capabilities
    assert 'genai_image_generation' in capabilities


def test_auto_load_env_without_file(temp_dir, monkeypatch):
    """Test auto_load_env without .env file."""
    monkeypatch.chdir(temp_dir)
    
    # Remove any .env files
    for env_file in temp_dir.glob(".env*"):
        env_file.unlink()
    
    # Clear all API keys
    api_keys = [
        'PIXABAY_API_KEY', 'UNSPLASH_ACCESS_KEY', 
        'OPENAI_API_KEY', 'GOOGLE_API_KEY', 'OPENROUTER_API_KEY'
    ]
    for key in api_keys:
        monkeypatch.delenv(key, raising=False)
    
    # Should not raise error with silent_on_missing=True
    capabilities = auto_load_env(verbose=False, silent_on_missing=True)
    
    assert capabilities == {}


def test_auto_load_env_verbose(mock_env_file, temp_dir, monkeypatch, capsys):
    """Test auto_load_env with verbose output."""
    monkeypatch.chdir(temp_dir)
    
    auto_load_env(verbose=True, silent_on_missing=True)
    
    captured = capsys.readouterr()
    assert 'Available capabilities:' in captured.out or 'Found .env file' in captured.out

