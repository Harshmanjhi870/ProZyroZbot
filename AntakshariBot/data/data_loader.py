import json
import logging
import aiohttp
import asyncio
from typing import Set, Dict, List
import os

logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self):
        self.countries: Set[str] = set()
        self.cities: Set[str] = set()
        self.rare_words: Set[str] = set()
        self.alternative_names: Dict[str, str] = {}
        self.data_loaded = False
        
        # GitHub raw URLs for the JSON files
        self.countries_url = "https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/countries.json"
        self.cities_url = "https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/cities.json"
        
        # Local file paths
        self.data_dir = "AntakshariBot/data/json_data"
        self.countries_file = f"{self.data_dir}/countries.json"
        self.cities_file = f"{self.data_dir}/cities.json"
    
    async def ensure_data_directory(self):
        """Ensure the data directory exists"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    async def download_file(self, url: str, filename: str) -> bool:
        """Download a file from URL"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        content = await response.read()
                        with open(filename, 'wb') as f:
                            f.write(content)
                        logger.info(f"Downloaded {filename}")
                        return True
                    else:
                        logger.error(f"Failed to download {url}: {response.status}")
                        return False
        except Exception as e:
            logger.error(f"Error downloading {url}: {e}")
            return False
    
    async def load_countries_data(self) -> bool:
        """Load countries data from JSON"""
        try:
            # Try to load from local file first
            if not os.path.exists(self.countries_file):
                logger.info("Countries file not found, downloading...")
                await self.ensure_data_directory()
                if not await self.download_file(self.countries_url, self.countries_file):
                    return False
            
            with open(self.countries_file, 'r', encoding='utf-8') as f:
                countries_data = json.load(f)
            
            # Extract country names
            for country in countries_data:
                name = country.get('name', '').strip()
                if name and len(name) >= 2:
                    self.countries.add(name.lower())
                    
                    # Add alternative names if available
                    if len(name) > 8:  # Consider longer names as rare
                        self.rare_words.add(name.lower())
            
            # Add some manual alternative names
            self.alternative_names.update({
                "usa": "united states",
                "united states": "usa",
                "uk": "united kingdom",
                "united kingdom": "uk",
                "uae": "united arab emirates",
                "united arab emirates": "uae"
            })
            
            logger.info(f"Loaded {len(self.countries)} countries")
            return True
            
        except Exception as e:
            logger.error(f"Error loading countries data: {e}")
            return False
    
    async def load_cities_data(self) -> bool:
        """Load cities data from JSON"""
        try:
            # Try to load from local file first
            if not os.path.exists(self.cities_file):
                logger.info("Cities file not found, downloading...")
                await self.ensure_data_directory()
                if not await self.download_file(self.cities_url, self.cities_file):
                    return False
            
            with open(self.cities_file, 'r', encoding='utf-8') as f:
                cities_data = json.load(f)
            
            # Extract city names
            for city in cities_data:
                name = city.get('name', '').strip()
                if name and len(name) >= 2:
                    # Filter out cities with numbers or special characters
                    if name.replace(' ', '').replace('-', '').replace("'", '').isalpha():
                        self.cities.add(name.lower())
                        
                        # Consider longer city names as rare
                        if len(name) > 12:
                            self.rare_words.add(name.lower())
            
            # Add some manual alternative names for cities
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
                "new york city": "new york"
            })
            
            logger.info(f"Loaded {len(self.cities)} cities")
            return True
            
        except Exception as e:
            logger.error(f"Error loading cities data: {e}")
            return False
    
    async def load_all_data(self) -> bool:
        """Load all data (countries and cities)"""
        try:
            countries_loaded = await self.load_countries_data()
            cities_loaded = await self.load_cities_data()
            
            if countries_loaded and cities_loaded:
                self.data_loaded = True
                logger.info(f"Data loaded successfully: {len(self.countries)} countries, {len(self.cities)} cities, {len(self.rare_words)} rare words")
                return True
            else:
                logger.error("Failed to load some data files")
                return False
                
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return False
    
    def get_all_words(self) -> Set[str]:
        """Get all valid words (countries + cities)"""
        return self.countries.union(self.cities)
    
    def is_rare_word(self, word: str) -> bool:
        """Check if a word is considered rare"""
        return word.lower() in self.rare_words
    
    def get_alternative_name(self, word: str) -> str:
        """Get alternative name for a word if exists"""
        return self.alternative_names.get(word.lower(), word)
    
    async def refresh_data(self) -> bool:
        """Force refresh data by downloading latest files"""
        try:
            await self.ensure_data_directory()
            
            # Remove existing files
            if os.path.exists(self.countries_file):
                os.remove(self.countries_file)
            if os.path.exists(self.cities_file):
                os.remove(self.cities_file)
            
            # Clear existing data
            self.countries.clear()
            self.cities.clear()
            self.rare_words.clear()
            
            # Reload data
            return await self.load_all_data()
            
        except Exception as e:
            logger.error(f"Error refreshing data: {e}")
            return False

# Global data loader instance
data_loader = DataLoader()

async def init_data_loader():
    """Initialize the data loader"""
    return await data_loader.load_all_data()
