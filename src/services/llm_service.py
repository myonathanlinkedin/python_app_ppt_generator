import openai
import json
from typing import Optional, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self, api_key: str = "NO_NEED_IF_USING_LMSTUDIO", base_url: str = "http://127.0.0.1:1234/v1"):
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        
    def _extract_json_from_text(self, text: str) -> Optional[Dict]:
        """Safely extract JSON from text response."""
        try:
            # Try direct JSON parsing first
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to find JSON between curly braces
            try:
                start_idx = text.find('{')
                end_idx = text.rfind('}') + 1
                if start_idx != -1 and end_idx > 0:
                    json_str = text[start_idx:end_idx]
                    return json.loads(json_str)
            except Exception as e:
                logger.error(f"Error extracting JSON: {e}")
                logger.debug(f"Raw text: {text}")
                return None
        return None

    def generate_presentation_content(self, topic: str) -> Optional[Dict]:
        """Generate presentation content using the LLM."""
        system_prompt = """
        You are a professional presentation designer. Create a comprehensive presentation outline following this exact structure:
        {
            "title": "Main presentation title",
            "subtitle": "A compelling subtitle",
            "theme": {
                "primary_color": "#0072C6",
                "secondary_color": "#404040",
                "accent_color": "#00B294"
            },
            "slides": [
                {
                    "title": "Slide title",
                    "type": "title|content|table",
                    "layout": "centered|split|table",
                    "content": ["Point 1", "Point 2", "Point 3"],
                    "table_data": {
                        "headers": ["Column 1", "Column 2", "Column 3"],
                        "rows": [
                            ["Row 1 Col 1", "Row 1 Col 2", "Row 1 Col 3"],
                            ["Row 2 Col 1", "Row 2 Col 2", "Row 2 Col 3"]
                        ]
                    },
                    "visual_notes": "Visual suggestion",
                    "notes": "Speaker notes"
                }
            ]
        }

        IMPORTANT GUIDELINES:
        1. Return ONLY valid JSON
        2. Always use lists for slide content
        3. Create as many slides as needed to cover the topic comprehensively
        4. Each content slide should have 2-5 bullet points
        5. Keep titles clear and descriptive
        6. For complex topics:
           - Start with an overview/agenda slide
           - Group related concepts into separate slides
           - Include comparison slides where relevant
           - End with summary/conclusion slides
        7. Use visual_notes field to suggest diagrams, charts, or images
        8. Include detailed speaker notes for complex points
        9. For comparison or data-heavy content:
           - Use table_data structure for tabular information
           - Set type to "table" and layout to "table" for table slides
           - Keep tables clear and well-structured
           - Use headers that clearly describe the columns
        """

        try:
            response = self.client.chat.completions.create(
                model="qwen2.5-7b-instruct-1m",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Create a detailed and comprehensive presentation about: {topic}. Include all necessary sections and explanations."}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            content = response.choices[0].message.content.strip()
            logger.info("Received response from LLM")
            logger.debug(f"Raw response: {content}")
            
            # Extract and validate JSON
            presentation_data = self._extract_json_from_text(content)
            if not presentation_data:
                logger.error("Failed to extract valid JSON from LLM response")
                return None
                
            return presentation_data
            
        except Exception as e:
            logger.error(f"Error generating content: {e}")
            return None 