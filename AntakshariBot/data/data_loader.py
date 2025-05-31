import json
import logging
import os
from typing import Set, Dict, List

logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self):
        self.countries: Set[str] = set()
        self.cities: Set[str] = set()
        self.rare_words: Set[str] = set()
        self.alternative_names: Dict[str, str] = {}
        self.data_loaded = False
        
        # Local JSON file path - YOU NEED TO UPLOAD YOUR JSON FILE HERE
        self.json_file = "AntakshariBot/data/countries_cities.json"
    
    async def load_data_from_json(self) -> bool:
        """Load countries and cities data from local JSON file"""
        try:
            # Check if file exists
            if not os.path.exists(self.json_file):
                logger.error(f"JSON file not found: {self.json_file}")
                logger.error("Please upload your countries_cities.json file to AntakshariBot/data/ folder")
                return False
            
            # Load JSON data
            with open(self.json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Clear existing data
            self.countries.clear()
            self.cities.clear()
            self.rare_words.clear()
            
            # Process each country
            for country_data in data:
                country_name = country_data.get('name', '').strip()
                cities_list = country_data.get('cities', [])
                
                # Add country name
                if country_name and len(country_name) >= 2:
                    self.countries.add(country_name.lower())
                    
                    # Mark long country names as rare
                    if len(country_name) > 8:
                        self.rare_words.add(country_name.lower())
                
                # Add cities for this country
                for city in cities_list:
                    city_name = city.strip()
                    if city_name and len(city_name) >= 2:
                        # Clean city name - remove special characters at start
                        clean_city = city_name.lstrip("'\"").strip()
                        
                        # Only add if it contains mostly letters
                        if clean_city and len(clean_city.replace(' ', '').replace('-', '').replace("'", '')) >= 2:
                            # Check if it's mostly alphabetic
                            alpha_chars = sum(1 for c in clean_city if c.isalpha())
                            total_chars = len(clean_city.replace(' ', '').replace('-', '').replace("'", ''))
                            
                            if total_chars > 0 and (alpha_chars / total_chars) >= 0.8:
                                self.cities.add(clean_city.lower())
                                
                                # Mark long city names as rare
                                if len(clean_city) > 12:
                                    self.rare_words.add(clean_city.lower())
            
            # Add manual alternative names
            self.alternative_names.update({
                "mumbai": "bombay",
                "bombay": "mumbai",
                "kolkata": "calcutta", 
                "calcutta": "kolkata",
                "chennai": "madras",
                "madras": "chennai",
                "beijing": "peking",
                "peking": "beijing",
                "new york": "new york city",
                "new york city": "new york",
                "usa": "united states",
                "united states": "usa",
                "uk": "united kingdom", 
                "united kingdom": "uk",
                "uae": "united arab emirates",
                "united arab emirates": "uae"
            })
            
            self.data_loaded = True
            logger.info(f"Data loaded successfully: {len(self.countries)} countries, {len(self.cities)} cities, {len(self.rare_words)} rare words")
            return True
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON format in {self.json_file}: {e}")
            return False
        except Exception as e:
            logger.error(f"Error loading data from JSON: {e}")
            return False
    
    async def load_all_data(self) -> bool:
        """Load all data from local JSON file"""
        return await self.load_data_from_json()
    
    def get_all_words(self) -> Set[str]:
        """Get all valid words (countries + cities)"""
        return self.countries.union(self.cities)
    
    def is_rare_word(self, word: str) -> bool:
        """Check if a word is considered rare"""
        return word.lower() in self.rare_words
    
    def get_alternative_name(self, word: str) -> str:
        """Get alternative name for a word if exists"""
        return self.alternative_names.get(word.lower(), word)
    
    def get_stats(self) -> dict:
        """Get statistics about loaded data"""
        return {
            "countries": len(self.countries),
            "cities": len(self.cities), 
            "rare_words": len(self.rare_words),
            "total_words": len(self.get_all_words())
        }

# Global data loader instance
data_loader = DataLoader()

async def init_data_loader():
    """Initialize the data loader"""
    return await data_loader.load_all_data()
