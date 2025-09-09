import hashlib

def generate_etag(data) -> str:
    """Generate a hash for ETag."""
    return hashlib.md5(data).hexdigest()  # simple checksum

def check_etag_present(etag, if_none_match):
    if if_none_match == etag:
        return False
    headers = {
        "Cache-Control": f"public, max-age=0 must-revalidate",
        "ETag": etag
    }   
    return headers
