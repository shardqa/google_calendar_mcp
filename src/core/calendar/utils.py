def ensure_timezone(datetime_str: str) -> str:
    """Ensure datetime string has timezone information."""
    if datetime_str.endswith('Z') or '+' in datetime_str[-6:] or '-' in datetime_str[-6:]:
        return datetime_str
    
    return f"{datetime_str}-03:00" 