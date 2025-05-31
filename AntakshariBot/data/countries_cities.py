"""
Legacy file - now using dynamic data from GitHub repository
This file is kept for backward compatibility
"""

# These are fallback lists in case the dynamic data loading fails
FALLBACK_COUNTRIES = [
    "Afghanistan", "Albania", "Algeria", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan",
    "Bahrain", "Bangladesh", "Belarus", "Belgium", "Bolivia", "Brazil", "Bulgaria",
    "Cambodia", "Canada", "Chile", "China", "Colombia", "Croatia", "Cuba", "Cyprus",
    "Denmark", "Ecuador", "Egypt", "England", "Estonia", "Ethiopia",
    "Finland", "France", "Georgia", "Germany", "Ghana", "Greece",
    "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy",
    "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kuwait",
    "Latvia", "Lebanon", "Libya", "Lithuania", "Luxembourg",
    "Malaysia", "Mexico", "Mongolia", "Morocco", "Myanmar",
    "Nepal", "Netherlands", "Norway", "Pakistan", "Peru", "Philippines", "Poland", "Portugal",
    "Qatar", "Romania", "Russia", "Singapore", "Spain", "Sweden", "Switzerland", "Syria",
    "Thailand", "Turkey", "Ukraine", "Uruguay", "Vietnam", "Yemen", "Zimbabwe"
]

FALLBACK_CITIES = [
    "Amsterdam", "Athens", "Bangkok", "Barcelona", "Beijing", "Berlin", "Boston", "Brussels",
    "Cairo", "Chicago", "Copenhagen", "Delhi", "Dubai", "Dublin", "Edinburgh",
    "Florence", "Geneva", "Hamburg", "Helsinki", "Istanbul", "Jakarta", "Jerusalem",
    "London", "Madrid", "Manila", "Melbourne", "Mexico", "Milan", "Montreal", "Moscow", "Mumbai",
    "Naples", "Paris", "Prague", "Rome", "Seoul", "Shanghai", "Singapore", "Stockholm", "Sydney",
    "Tokyo", "Toronto", "Vienna", "Warsaw", "Zurich"
]

# Legacy exports for backward compatibility
COUNTRIES = FALLBACK_COUNTRIES
CITIES = FALLBACK_CITIES
RARE_WORDS = []
ALTERNATIVE_NAMES = {}
