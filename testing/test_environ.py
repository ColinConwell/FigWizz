"""
Tests for environment variable loading
"""

import pytest
import os
from pathlib import Path
from figwizz.utils.environ import search_for_env_file, load_env_variables


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

