# src/utils/domain.py
from typing import Optional
import tldextract

def normalize_domain(url_or_domain: str) -> Optional[str]:
    """Return the registrable domain (eTLD+1) or None."""
    if not url_or_domain:
        return None
    ext = tldextract.extract(url_or_domain)
    reg = ext.registered_domain.lower()
    return reg or None  # empty string -> None

def domain_matches(url: str, target_domain: str) -> bool:
    """True if the URL's registrable domain equals the target registrable domain."""
    try:
        got = normalize_domain(url)
        target = normalize_domain(target_domain)
        return bool(got and target) and (got == target)
    except Exception:
        return False
