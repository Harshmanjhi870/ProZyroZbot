import logging
from typing import Set
from AntakshariBot.data.countries_cities import COUNTRIES, CITIES, RARE_WORDS

logger = logging.getLogger(__name__)

class WordValidator:
    def __init__(self):
        self.valid_words = set()
        self.load_words()
    
    def load_words(self):
        """Load all valid words (countries and cities)"""
        try:
            # Add countries
            for country in COUNTRIES:
                self.valid_words.add(country.lower())
            
            # Add cities
            for city in CITIES:
                self.valid_words.add(city.lower())
            
            logger.info(f"Loaded {len(self.valid_words)} valid words")
            
        except Exception as e:
            logger.error(f"Error loading words: {e}")
    
    async def validate_word(self, word: str, required_letter: str, used_words: Set[str]) -> dict:
        """Validate a submitted word"""
        try:
            word_clean = word.lower().strip()
            
            # Check if word is empty
            if not word_clean:
                return {"valid": False, "reason": "Please enter a word!"}
            
            # Check if word contains only letters
            if not word_clean.isalpha():
                return {"valid": False, "reason": "Word must contain only letters!"}
            
            # Check minimum length
            if len(word_clean) < 2:
                return {"valid": False, "reason": "Word must be at least 2 letters long!"}
            
            # Check if word starts with required letter
            if required_letter and word_clean[0] != required_letter.lower():
                return {"valid": False, "reason": f"Word must start with '{required_letter.upper()}'!"}
            
            # Check if word was already used
            if word_clean in used_words:
                return {"valid": False, "reason": "This word has already been used!"}
            
            # Check if word is valid (country or city)
            if word_clean not in self.valid_words:
                return {"valid": False, "reason": "Invalid word! Only country and city names are allowed."}
            
            # Check if it's a rare word (bonus points)
            is_rare = word_clean in [w.lower() for w in RARE_WORDS]
            
            return {"valid": True, "rare": is_rare}
            
        except Exception as e:
            logger.error(f"Error validating word: {e}")
            return {"valid": False, "reason": "An error occurred while validating the word."}
