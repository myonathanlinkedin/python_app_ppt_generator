from dataclasses import dataclass
from typing import Optional

@dataclass
class Theme:
    """Theme configuration for presentations."""
    primary_color: str = "#0072C6"    # Microsoft Blue
    secondary_color: str = "#404040"  # Dark Gray
    accent_color: str = "#00B294"     # Teal
    background_color: str = "#011640" # Dark Navy
    text_color: str = "#FFFFFF"       # White
    font_family: str = "Segoe UI"
    title_font_size: int = 44
    subtitle_font_size: int = 32
    body_font_size: int = 24 