# Telegram Protection Bot

A comprehensive Telegram bot system with protection features and automated cleanup.

## Features

### Bot Protection
- 🛡️ Auto-delete PDF files immediately
- 📸 Auto-delete media files (photos, videos) after 60 seconds
- ✏️ Prevent message editing (deletes edited messages)
- 👮 Admin authorization system (`/auth` and `/unauth` commands)
- 📊 Comprehensive logging

### UserBot Cleanup
- 🧹 Auto-cleanup media files every 240 seconds
- 📱 Automated group maintenance
- 🔄 Continuous background operation

## Setup

### 1. Clone Repository
\`\`\`bash
git clone <repository-url>
cd telegram-protection-bot
\`\`\`

### 2. Install Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 3. Configure Environment
1. Copy `.env.example` to `.env`
2. Fill in your actual credentials:
   - `TELEGRAM_TOKEN`: Your bot token from @BotFather
   - `API_ID` & `API_HASH`: From https://my.telegram.org
   - `SESSION`: Userbot session string
   - `MONGO_URI`: MongoDB connection string
   - Other configuration values

### 4. Deploy

#### Local Development
\`\`\`bash
python main.py
\`\`\`

#### Heroku Deployment
1. Create new Heroku app
2. Set environment variables in Heroku dashboard
3. Connect GitHub repository
4. Deploy

## Commands

### Admin Commands
- `/auth` - Authorize a user (reply to their message)
- `/unauth` - Remove user authorization (reply to their message)
- `/start` - Show bot information
- `/help` - Show help message

## Security Features

- ✅ Environment variables for sensitive data
- ✅ Authorization system for trusted users
- ✅ Comprehensive error handling
- ✅ Logging and monitoring
- ✅ Database persistence

## File Structure

\`\`\`
├── main.py                 # Entry point
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── Procfile              # Heroku process file
├── .env.example          # Environment template
├── TEAMZYRO/
│   ├── __init__.py
│   ├── bot.py            # Main bot class
│   ├── userbot.py        # Userbot class
│   ├── database.py       # Database operations
│   ├── Bot_modules/      # Bot protection modules
│   │   ├── auth.py       # Authorization system
│   │   ├── media_protection.py
│   │   └── message_protection.py
│   └── Userbot_modules/  # Userbot cleanup modules
│       └── cleanup.py    # Media cleanup
\`\`\`

## Important Notes

⚠️ **Security Warning**: Never commit actual API keys or tokens to version control.

📝 **Configuration**: Always use environment variables for sensitive data.

🔐 **Permissions**: Ensure your bot has appropriate admin permissions in target groups.

## License

This project is for educational purposes. Please comply with Telegram's Terms of Service.
