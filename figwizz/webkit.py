import requests

def is_url_a_pdf(url):
    """
    Check if a URL points to a PDF file.
    
    Args:
        url: URL to check
    
    Returns:
        True if the URL likely points to a PDF
    """
    # Check URL extension
    if url.lower().endswith('.pdf'):
        return True
    
    # Check Content-Type header
    try:
        response = requests.head(url, headers={'User-Agent': 'Mozilla/5.0'}, allow_redirects=True, timeout=10)
        content_type = response.headers.get('Content-Type', '')
        if 'pdf' in content_type.lower():
            return True
    except:
        pass
    
    return False