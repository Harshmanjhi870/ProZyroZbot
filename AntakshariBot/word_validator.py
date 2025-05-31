import logging
from typing import Set
from AntakshariBot.data.data_loader import data_loader

logger = logging.getLogger(__name__)

class WordValidator:
    def __init__(self):
        self.valid_words = set()
        self.data_ready = False
    
    async def ensure_data_loaded(self):
        """Ensure data is loaded before validation"""
        if not data_loader.data_loaded:
            logger.info("Loading word data from JSON file...")
            success = await data_loader.load_all_data()
            if not success:
                logger.error("Failed to load word data from JSON file")
                # Fallback to basic words if data loading fails
                self.valid_words = {
                    "india", "america", "china", "japan", "france", "germany", "italy", "spain",
                    "london", "paris", "tokyo", "delhi", "mumbai", "sydney", "berlin", "rome"
                }
                return False
            
        self.valid_words = data_loader.get_all_words()
        self.data_ready = True
        logger.info(f"Word validator ready with {len(self.valid_words)} words")
        return True
    
    async def validate_word(self, word: str, required_letter: str, used_words: Set[str]) -> dict:
        """Validate a submitted word"""
        try:
            # Ensure data is loaded
            if not self.data_ready:
                await self.ensure_data_loaded()
            
            word_clean = word.lower().strip()
            
            # Check if word is empty
            if not word_clean:
                return {"valid": False, "reason": "Please enter a word!"}
            
            # Check if word contains only letters and spaces/hyphens/apostrophes
            if not all(c.isalpha() or c in [' ', '-', "'"] for c in word_clean):
                return {"valid": False, "reason": "Word must contain only letters!"}
            
            # Check minimum length
            if len(word_clean.replace(' ', '').replace('-', '').replace("'", '')) < 2:
                return {"valid": False, "reason": "Word must be at least 2 letters long!"}
            
            # Check if word starts with required letter
            if required_letter and word_clean[0] != required_letter.lower():
                return {"valid": False, "reason": f"Word must start with '{required_letter.upper()}'!"}
            
            # Check if word was already used
            if word_clean in used_words:
                return {"valid": False, "reason": "This word has already been used!"}
            
            # Check alternative names
            alternative_word = data_loader.get_alternative_name(word_clean)
            if alternative_word != word_clean and alternative_word in used_words:
                return {"valid": False, "reason": f"This word has already been used as '{alternative_word.title()}'!"}
            
            # Check if word is valid (country or city)
            if word_clean not in self.valid_words and alternative_word not in self.valid_words:
                return {"valid": False, "reason": "Invalid word! Only country and city names are allowed."}
            
            # Check if it's a rare word (bonus points)
            is_rare = data_loader.is_rare_word(word_clean) or data_loader.is_rare_word(alternative_word)
            
            return {"valid": True, "rare": is_rare}
            
        except Exception as e:
            logger.error(f"Error validating word: {e}")
            return {"valid": False, "reason": "An error occurred while validating the word."}
    
    async def get_word_count(self) -> dict:
        """Get statistics about loaded words"""
        if not self.data_ready:
            await self.ensure_data_loaded()
        
        return data_loader.get_stats()
    
    async def refresh_data(self) -> bool:
        """Refresh word data from JSON file"""
        try:
            # Clear current data
            data_loader.data_loaded = False
            
            # Reload from JSON
            success = await data_loader.load_all_data()
            if success:
                self.valid_words = data_loader.get_all_words()
                self.data_ready = True
            return success
        except Exception as e:
            logger.error(f"Error refreshing word data: {e}")
            return False
