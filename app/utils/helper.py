from urllib.parse import urlparse


def check_valid_url(url: str) -> bool:
    """
    Check if the URL is valid and not a file URL.
    """
    if not urlparse(url).scheme:
        return False
    return True

def check_valid_num_tries(num_tries: int) -> bool:
    """
    Check if the number of tries is a positive integer.
    """
    if num_tries <= 0:
        return False
    return True