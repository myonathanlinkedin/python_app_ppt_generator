import openai
import json
from typing import Optional, Dict, List, Union
import logging
import re
from html import unescape
import os
import traceback
import httpx

# Configure logging
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, 'llm_service.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self, api_key: str = "NO_NEED_IF_USING_LMSTUDIO", base_url: str = "http://127.0.0.1:1234/v1"):
        self.api_key = api_key
        self.base_url = base_url
        logger.info(f"LLMService initialized with base_url: {base_url}")

    def _get_client(self):
        """Create a fresh client for each request to avoid state retention."""
        try:
            client = openai.OpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
                http_client=httpx.Client(timeout=60.0)
            )
            logger.debug("OpenAI client created successfully")
            return client
        except Exception as e:
            logger.error(f"Error creating OpenAI client: {str(e)}")
            logger.error(f"Stack trace: {traceback.format_exc()}")
            raise

    def _clean_text(self, text: str) -> str:
        """Clean text by removing HTML and special characters."""
        try:
            # Remove HTML tags
            text = re.sub(r'<[^>]+>', '', text)
            # Convert HTML entities
            text = unescape(text)
            # Remove asterisks
            text = text.replace('*', '')
            # Remove multiple spaces
            text = ' '.join(text.split())
            # Remove leading/trailing whitespace
            text = text.strip()
            return text
        except Exception as e:
            logger.error(f"Error cleaning text: {str(e)}")
            logger.error(f"Original text: {text}")
            logger.error(f"Stack trace: {traceback.format_exc()}")
            return text

    def _clean_content(self, content: Union[str, List, Dict]) -> Union[str, List, Dict]:
        """Recursively clean content in all text fields."""
        try:
            if isinstance(content, str):
                return self._clean_text(content)
            elif isinstance(content, list):
                return [self._clean_content(item) for item in content]
            elif isinstance(content, dict):
                return {k: self._clean_content(v) for k, v in content.items()}
            return content
        except Exception as e:
            logger.error(f"Error cleaning content: {str(e)}")
            logger.error(f"Content type: {type(content)}")
            logger.error(f"Stack trace: {traceback.format_exc()}")
            return content

    def _extract_json_from_text(self, text: str) -> Optional[Dict]:
        """Safely extract JSON from text response."""
        logger.debug("Starting JSON extraction from text")
        logger.debug(f"Raw text input:\n{text}")
        
        try:
            # Try direct JSON parsing first
            logger.debug("Attempting direct JSON parsing")
            data = json.loads(text)
            if self._validate_presentation_data(data):
                logger.info("Successfully parsed JSON directly")
                return data
        except json.JSONDecodeError as e:
            logger.debug(f"Direct JSON parsing failed: {str(e)}")
        
        try:
            # Find JSON between curly braces
            matches = re.findall(r'\{(?:[^{}]|\{[^{}]*\})*\}', text)
            logger.debug(f"Found {len(matches)} potential JSON matches")
            
            for i, match in enumerate(matches):
                try:
                    json_str = self._clean_json_string(match)
                    logger.debug(f"Attempting to parse match {i + 1}:\n{json_str}")
                    
                    data = json.loads(json_str)
                    if self._validate_presentation_data(data):
                        logger.info("Successfully extracted valid JSON from match")
                        return data
                except json.JSONDecodeError as e:
                    logger.debug(f"Failed to parse match {i + 1}: {str(e)}")
                    continue
            
            logger.error("No valid JSON structure found in any matches")
            return None
            
        except Exception as e:
            logger.error(f"Error during JSON extraction: {str(e)}")
            logger.error(f"Stack trace: {traceback.format_exc()}")
            return None

    def _clean_json_string(self, json_str: str) -> str:
        """Clean and prepare JSON string for parsing."""
        try:
            # Remove any markdown code block markers
            json_str = re.sub(r'```json\s*|\s*```', '', json_str)
            # Clean up the JSON string
            json_str = json_str.strip()
            # Remove any trailing commas before closing braces or brackets
            json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
            return json_str
        except Exception as e:
            logger.error(f"Error cleaning JSON string: {str(e)}")
            logger.error(f"Original string: {json_str}")
            return json_str

    def _validate_presentation_data(self, data: Dict) -> bool:
        """Validate that the presentation data has all required fields."""
        try:
            required_fields = ['title', 'subtitle', 'slides']
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                logger.error(f"Missing required fields: {missing_fields}")
                logger.error(f"Found keys: {list(data.keys())}")
                return False
            
            # Validate title and subtitle are non-empty strings
            if not isinstance(data['title'], str) or not data['title'].strip():
                logger.error("Title must be a non-empty string")
                return False
                
            if not isinstance(data['subtitle'], str) or not data['subtitle'].strip():
                logger.error("Subtitle must be a non-empty string")
                return False
            
            # Validate slides array
            if not isinstance(data['slides'], list) or not data['slides']:
                logger.error("Slides must be a non-empty array")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error during validation: {str(e)}")
            return False

    def generate_presentation_content(self, topic: str) -> Optional[Dict]:
        """Generate presentation content using the LLM."""
        logger.info(f"Starting presentation generation for topic: {topic}")
        
        try:
            # Get a fresh client
            client = self._get_client()
            
            # Check if topic is too vague
            if len(topic.split()) < 2:
                logger.error(f"Topic '{topic}' is too vague")
                raise ValueError("Please provide a more specific topic with at least 2-3 words for better results")
            
            system_prompt = """You are a presentation designer. Create a presentation outline about the given topic.
            Return ONLY a JSON object with this structure, no other text. The JSON MUST contain ALL of these fields:
            {
                "title": "Main presentation title (REQUIRED)",
                "subtitle": "A descriptive subtitle that complements the title (REQUIRED - DO NOT OMIT)",
                "theme": {
                    "primary_color": "#0072C6",
                    "secondary_color": "#404040",
                    "accent_color": "#00B294",
                    "background_color": "#FFFFFF"
                },
                "slides": [
                    {
                        "title": "Single string title only",
                        "type": "title|content|table",
                        "layout": "centered|split|table",
                        "content": ["Point 1", "Point 2"] or [["Header 1", "Header 2"], ["Row 1 Col 1", "Row 1 Col 2"]]
                    }
                ]
            }

            CRITICAL REQUIREMENTS:
            1. title: The main presentation title (REQUIRED)
            2. subtitle: A descriptive subtitle that complements the title (REQUIRED)
            3. slides: Array of slide objects (REQUIRED)
            4. First slide MUST be a title slide containing both the title and subtitle

            Rules for slides:
            1. Each slide must have exactly one "title" field as a string
            2. For table slides, content must be a 2D array where first row is headers
            3. For content slides, content must be an array of strings
            4. No additional fields are allowed in slide objects
            5. First slide should be a title slide with the main presentation title and subtitle

            Example for a specific topic like "Machine Learning in Healthcare":
            {
                "title": "Machine Learning in Healthcare",
                "subtitle": "Revolutionizing Patient Care Through AI Innovation",
                "slides": [
                    {
                        "title": "Machine Learning in Healthcare",
                        "type": "title",
                        "layout": "centered",
                        "content": ["Revolutionizing Patient Care Through AI Innovation"]
                    },
                    ...
                ]
            }
            """

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Create a detailed presentation about: {topic}. Focus on providing comprehensive and specific content. Return only the JSON."}
            ]
            
            logger.debug("Sending request to LLM")
            try:
                response = client.chat.completions.create(
                    model="qwen2.5-7b-instruct-1m",
                    messages=messages,
                    temperature=0.7,
                    max_tokens=2000
                )
            except Exception as e:
                logger.error(f"LLM API error: {str(e)}")
                raise ConnectionError("Failed to connect to the LLM service. Please ensure the service is running and try again.")
            
            content = response.choices[0].message.content.strip()
            logger.debug(f"Received raw response:\n{content}")
            
            if not content:
                logger.error("LLM returned empty response")
                raise ValueError("The AI service returned an empty response. Please try again with a more specific topic.")
            
            # Clean and parse the response
            content = self._clean_json_string(content)
            
            try:
                presentation_data = json.loads(content)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse LLM response as JSON: {str(e)}")
                logger.error(f"Raw content: {content}")
                raise ValueError("The AI service returned an invalid response format. Please try again.")
            
            if not self._validate_presentation_data(presentation_data):
                logger.error("Generated content failed validation")
                raise ValueError("The generated presentation content was incomplete. Please try again with a more specific topic.")
            
            # Additional validation for slide structure
            for i, slide in enumerate(presentation_data.get('slides', [])):
                if not isinstance(slide.get('title'), str):
                    logger.error(f"Invalid slide {i+1} title: {slide.get('title')}")
                    raise ValueError(f"Invalid title in slide {i+1}. Please try again.")
                
                if slide.get('type') not in ['title', 'content', 'table']:
                    logger.error(f"Invalid slide {i+1} type: {slide.get('type')}")
                    raise ValueError(f"Invalid type in slide {i+1}. Please try again.")
                
                if slide.get('layout') not in ['centered', 'split', 'table']:
                    logger.error(f"Invalid slide {i+1} layout: {slide.get('layout')}")
                    raise ValueError(f"Invalid layout in slide {i+1}. Please try again.")
                
                content = slide.get('content', [])
                if slide.get('type') == 'table':
                    if not isinstance(content, list) or not all(isinstance(row, list) for row in content):
                        logger.error(f"Invalid table content structure in slide {i+1}: {content}")
                        raise ValueError(f"Invalid table content in slide {i+1}. Please try again.")
                else:
                    if not isinstance(content, list) or not all(isinstance(item, str) for item in content):
                        logger.error(f"Invalid content structure in slide {i+1}: {content}")
                        raise ValueError(f"Invalid content in slide {i+1}. Please try again.")
            
            logger.info("Successfully generated and validated presentation content")
            return self._clean_content(presentation_data)
            
        except ValueError as e:
            logger.error(f"Validation error: {str(e)}")
            raise
        except ConnectionError as e:
            logger.error(f"Connection error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            logger.error(f"Stack trace: {traceback.format_exc()}")
            raise ValueError("An unexpected error occurred. Please try again with a different topic.") 