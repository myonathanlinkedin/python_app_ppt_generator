import json
import os
import logging
from typing import Any, Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContextManager:
    _instance = None
    _context = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ContextManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._context is None:
            self.load_context()

    def load_context(self, context_file: str = "context.json") -> None:
        """Load context from the JSON file."""
        try:
            context_path = os.path.join(os.getcwd(), context_file)
            if os.path.exists(context_path):
                with open(context_path, 'r') as f:
                    self._context = json.load(f)
                logger.info("Context loaded successfully")
            else:
                logger.warning(f"Context file not found: {context_path}")
                self._context = {}
        except Exception as e:
            logger.error(f"Error loading context: {e}")
            self._context = {}

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get a value from context using dot notation.
        Example: context.get("presentation_defaults.colors.primary")
        """
        try:
            value = self._context
            for key in key_path.split('.'):
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default

    def get_all(self) -> Dict:
        """Get the entire context dictionary."""
        return self._context or {}

    def get_presentation_defaults(self) -> Dict:
        """Get presentation default settings."""
        return self.get('presentation_defaults', {})

    def get_colors(self) -> Dict:
        """Get color scheme."""
        return self.get('presentation_defaults.colors', {})

    def get_fonts(self) -> Dict:
        """Get font settings."""
        return self.get('presentation_defaults.fonts', {})

    def get_slide_type_info(self, slide_type: str) -> Optional[Dict]:
        """Get information about a specific slide type."""
        return self.get(f'slide_types.{slide_type}')

    def get_llm_settings(self) -> Dict:
        """Get LLM configuration."""
        return self.get('llm_settings', {})

    def get_file_paths(self) -> Dict:
        """Get file path configurations."""
        return self.get('file_paths', {})

# Create a singleton instance
context = ContextManager() 