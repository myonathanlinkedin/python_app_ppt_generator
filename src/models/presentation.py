from dataclasses import dataclass
from typing import List, Dict, Optional, Union

@dataclass
class Slide:
    title: str
    type: str
    layout: str
    content: List[str]
    visual_notes: Optional[str] = None
    notes: Optional[str] = None
    table_data: Optional[Dict[str, Union[List[str], List[List[str]]]]] = None

@dataclass
class Theme:
    primary_color: str = "#0072C6"
    secondary_color: str = "#404040"
    accent_color: str = "#00B294"

@dataclass
class Presentation:
    title: str
    subtitle: str
    theme: Theme
    slides: List[Slide]

    @classmethod
    def from_dict(cls, data: Dict) -> 'Presentation':
        """Create a Presentation instance from a dictionary with validation."""
        if not isinstance(data, dict):
            raise ValueError("Input must be a dictionary")

        required_fields = ['title', 'subtitle', 'slides']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        # Process theme
        theme_data = data.get('theme', {})
        theme = Theme(
            primary_color=theme_data.get('primary_color', Theme().primary_color),
            secondary_color=theme_data.get('secondary_color', Theme().secondary_color),
            accent_color=theme_data.get('accent_color', Theme().accent_color)
        )

        # Process slides with validation
        slides = []
        for slide_data in data['slides']:
            if not isinstance(slide_data, dict):
                continue
            
            # Ensure content is always a list
            content = slide_data.get('content', [])
            if isinstance(content, str):
                content = [content]
            elif not isinstance(content, list):
                content = []

            # Process table data if present
            table_data = None
            if slide_data.get('type') == 'table' and 'table_data' in slide_data:
                table_data = {
                    'headers': slide_data['table_data'].get('headers', []),
                    'rows': slide_data['table_data'].get('rows', [])
                }

            # Create slide with validated data
            try:
                slide = Slide(
                    title=slide_data.get('title', 'Untitled Slide'),
                    type=slide_data.get('type', 'content'),
                    layout=slide_data.get('layout', 'centered'),
                    content=content,
                    visual_notes=slide_data.get('visual_notes'),
                    notes=slide_data.get('notes'),
                    table_data=table_data
                )
                slides.append(slide)
            except Exception as e:
                print(f"Error processing slide: {e}")
                continue

        return cls(
            title=data['title'],
            subtitle=data['subtitle'],
            theme=theme,
            slides=slides
        ) 