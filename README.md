# 🎮 Antakshari Game Bot

An advanced Telegram bot for playing the classic Antakshari word game with countries and cities theme.

## 🌟 Features

### 🎯 Game Features
- **Country & City Theme**: Play with names of countries and cities from around the world
- **Multi-Group Support**: Each group has independent games
- **Smart Word Validation**: Comprehensive database of valid countries and cities
- **Scoring System**: Earn points for correct answers with bonus for rare words
- **Streak System**: Get bonus points for consecutive correct answers
- **Turn Timer**: 30 seconds per turn to keep the game moving
- **Join Timer**: 60 seconds for players to join before game starts

### 📊 Advanced Features
- **Player Statistics**: Track games played, won, points, accuracy, and more
- **Global Leaderboard**: See top players across all groups
- **Game History**: View past games and statistics
- **Rare Word Bonuses**: Extra points for difficult/uncommon words
- **Admin Controls**: Group admins can end games
- **Comprehensive Logging**: Full game logging and error handling

### 🎮 Game Rules
- Players take turns saying country or city names
- Next word must start with the last letter of previous word
- No repetition of words allowed
- 30 seconds per turn
- Minimum 2 players, maximum 20 players
- Game ends at 100 points or 50 rounds

## 🚀 Setup

### Prerequisites
- Python 3.8+
- MongoDB database
- Telegram Bot Token

### Installation

1. **Clone Repository**
\`\`\`bash
git clone <repository-url>
cd antakshari-game-bot
\`\`\`

2. **Install Dependencies**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

3. **Configure Environment**
\`\`\`bash
cp .env.example .env
# Edit .env with your credentials
\`\`\`

4. **Run Bot**
\`\`\`bash
python main.py
\`\`\`

### Environment Variables

\`\`\`env
TELEGRAM_TOKEN=your_bot_token
API_ID=your_api_id
API_HASH=your_api_hash
MONGO_URI=your_mongodb_uri
DB_NAME=antakshari_bot_db
OWNER_ID=your_user_id
BOT_NAME=Antakshari Game Bot
\`\`\`

## 🎯 Commands

### Game Commands
- `/antakshari` - Start new game
- `/join` - Join current game
- `/leave` - Leave current game
- `/endgame` - End game (admin only)
- `/gamestats` - Current game status

### Player Commands
- `/start` - Bot introduction
- `/help` - Show help message
- `/stats` - Your game statistics
- `/leaderboard` - Top 10 players
- `/countries` - List valid countries
- `/cities` - List valid cities

## 🏗️ Architecture

### File Structure
\`\`\`
├── main.py                    # Entry point
├── config.py                  # Configuration
├── requirements.txt           # Dependencies
├── Procfile                   # Deployment
├── AntakshariBot/
│   ├── __init__.py
│   ├── bot.py                 # Main bot logic
│   ├── game_manager.py        # Game state management
│   ├── word_validator.py      # Word validation logic
│   ├── database.py            # Database operations
│   ├── utils.py               # Utility functions
│   └── data/
│       ├── __init__.py
│       └── countries_cities.py # Word database
\`\`\`

### Database Schema

**Games Collection**
- chat_id, status, players, current_player
- last_word, next_letter, used_words
- round, start_time, creator

**Player Stats Collection**
- user_id, user_name, games_played, games_won
- total_points, best_score, best_streak
- correct_words, wrong_words, accuracy

**Game History Collection**
- Completed games with full details
- Winner information and final scores

## 🎮 How to Play

1. **Start Game**: Use `/antakshari` in a group
2. **Join**: Players use `/join` within 60 seconds
3. **Play**: Say country or city names in turn
4. **Rules**: Next word starts with last letter of previous word
5. **Win**: First to 100 points or highest score after 50 rounds

### Example Game Flow
\`\`\`
Player 1: "India"
Player 2: "Australia" (starts with 'A', last letter of India)
Player 3: "Argentina" (starts with 'A', last letter of Australia)
Player 1: "Albania" (starts with 'A', last letter of Argentina)
\`\`\`

## 🏆 Scoring System

- **Correct Answer**: 10 points
- **Rare Word Bonus**: +5 points
- **Streak Bonus**: +1 point per consecutive turn
- **Win Condition**: First to 100 points or highest score after 50 rounds

## 🌍 Word Database

### Countries (200+)
- All UN recognized countries
- Major territories and regions
- Alternative spellings supported

### Cities (500+)
- Major world cities
- Indian cities and towns
- State capitals and important centers
- International metropolitan areas

### Rare Words
- Bonus points for difficult countries like "Kyrgyzstan", "Liechtenstein"
- Uncommon cities like "Thiruvananthapuram", "Tiruchirappalli"
- Special recognition for challenging spellings

## 🔧 Advanced Features

### Game Management
- **Multi-threading**: Handle multiple games simultaneously
- **Auto-cleanup**: Remove inactive games and expired timers
- **Error Recovery**: Robust error handling and game state recovery
- **Performance**: Optimized database queries and caching

### Security & Moderation
- **Admin Controls**: Group admins can manage games
- **Spam Protection**: Rate limiting and flood control
- **Data Privacy**: Secure handling of user information
- **Logging**: Comprehensive audit trail

### Deployment Options
- **Heroku**: Ready-to-deploy with Procfile
- **Docker**: Containerized deployment
- **VPS**: Traditional server deployment
- **Cloud**: AWS/GCP/Azure compatible

## 📈 Statistics & Analytics

### Player Metrics
- Games played and won
- Total points earned
- Best single game score
- Longest winning streak
- Word accuracy percentage
- Favorite starting letters

### Group Analytics
- Most active groups
- Average game duration
- Popular words used
- Player engagement metrics

## 🛠️ Development

### Contributing
1. Fork the repository
2. Create feature branch
3. Add tests for new features
4. Submit pull request

### Testing
\`\`\`bash
# Run tests
python -m pytest tests/

# Test word validation
python -m pytest tests/test_word_validator.py

# Test game logic
python -m pytest tests/test_game_manager.py
\`\`\`

### Adding New Words
Edit `AntakshariBot/data/countries_cities.py`:
\`\`\`python
# Add to COUNTRIES list
COUNTRIES.append("NewCountry")

# Add to CITIES list
CITIES.append("NewCity")

# Add rare words for bonus points
RARE_WORDS.append("DifficultPlace")
\`\`\`

## 🐛 Troubleshooting

### Common Issues
- **Bot not responding**: Check token and permissions
- **Database errors**: Verify MongoDB connection
- **Game stuck**: Use `/endgame` command
- **Word not accepted**: Check spelling and validity

### Logs
Check `antakshari_bot.log` for detailed error information.

## 📄 License

This project is for educational purposes. Please comply with Telegram's Terms of Service.

## 🤝 Support

For issues and feature requests, please create an issue in the repository.

---

**Made with ❤️ by TEAMZYRO**
