import re

def validate_link(link: str) -> str:
    # Simple YouTube URL pattern
    yt_pattern = r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$"
    
    if re.match(yt_pattern, link.strip()):
        return link.strip()
    else:
        return "Error"