"""
Tests for web utilities
"""

import pytest
from unittest.mock import Mock, patch
from figwizz.webkit import is_url_a_pdf, convert_response_to_dict


def test_is_url_a_pdf_extension():
    """Test PDF detection by file extension."""
    assert is_url_a_pdf('http://example.com/document.pdf')
    assert is_url_a_pdf('https://example.com/file.PDF')
    assert not is_url_a_pdf('http://example.com/image.jpg')


@patch('figwizz.webkit.requests.head')
def test_is_url_a_pdf_content_type(mock_head):
    """Test PDF detection by Content-Type header."""
    mock_response = Mock()
    mock_response.headers = {'Content-Type': 'application/pdf'}
    mock_head.return_value = mock_response
    
    assert is_url_a_pdf('http://example.com/document')


@patch('figwizz.webkit.requests.head')
def test_is_url_a_pdf_not_pdf(mock_head):
    """Test non-PDF URL detection."""
    mock_response = Mock()
    mock_response.headers = {'Content-Type': 'text/html'}
    mock_head.return_value = mock_response
    
    assert not is_url_a_pdf('http://example.com/page')


@patch('figwizz.webkit.requests.head')
def test_is_url_a_pdf_request_error(mock_head):
    """Test handling of request errors."""
    mock_head.side_effect = Exception("Network error")
    
    # Should return False on error
    assert not is_url_a_pdf('http://example.com/document')


def test_convert_response_to_dict_simple():
    """Test converting simple object to dict."""
    class SimpleObject:
        def __init__(self):
            self.key1 = 'value1'
            self.key2 = 'value2'
    
    obj = SimpleObject()
    result = convert_response_to_dict(obj)
    
    assert isinstance(result, dict)
    assert result['key1'] == 'value1'
    assert result['key2'] == 'value2'


def test_convert_response_to_dict_nested():
    """Test converting nested object to dict."""
    class NestedObject:
        def __init__(self):
            self.inner = SimpleInner()
    
    class SimpleInner:
        def __init__(self):
            self.value = 'nested_value'
    
    obj = NestedObject()
    result = convert_response_to_dict(obj)
    
    assert isinstance(result, dict)
    assert isinstance(result['inner'], dict)
    assert result['inner']['value'] == 'nested_value'


def test_convert_response_to_dict_with_list():
    """Test converting object with list to dict."""
    class ObjectWithList:
        def __init__(self):
            self.items = [1, 2, 3]
    
    obj = ObjectWithList()
    result = convert_response_to_dict(obj)
    
    assert result['items'] == [1, 2, 3]


def test_convert_response_to_dict_keep_keys():
    """Test filtering keys in conversion."""
    class MultiKeyObject:
        def __init__(self):
            self.key1 = 'value1'
            self.key2 = 'value2'
            self.key3 = 'value3'
    
    obj = MultiKeyObject()
    result = convert_response_to_dict(obj, keep_keys=['key1', 'key3'])
    
    assert 'key1' in result
    assert 'key3' in result
    assert 'key2' not in result

