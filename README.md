# Telegram Userbot Setup Guide

## Requirements
```
telethon
google-generativeai
python-dotenv
```

## Setup Steps

### 1. Install Dependencies
```bash
pip install telethon google-generativeai python-dotenv
```

### 2. Create .env file
Create a `.env` file in your project directory:
```
API_ID=your_api_id
API_HASH=your_api_hash
PHONE=your_phone_number
GEMINI_API_KEY=your_gemini_api_key
```

### 3. Get Telegram API Credentials
1. Go to https://my.telegram.org
2. Login with your phone number
3. Go to "API Development Tools"
4. Create a new application
5. Note down your `API_ID` and `API_HASH`

### 4. Get Gemini API Key
1. Go to https://makersuite.google.com/app/apikey
2. Create a new API key
3. Copy the key

### 5. Run the Bot
```bash
python userbot.py
```

## Features
- ✅ Responds to private messages automatically using AI
- ✅ Simple commands (!help, !status, !stop)
- ✅ Ignores group messages (configurable)
- ✅ Human-like delays
- ✅ Error handling

## Important Notes
- **Use responsibly**: This automates your personal Telegram account
- **Rate limits**: OpenAI API has rate limits
- **Telegram ToS**: Make sure you comply with Telegram's terms of service
- **Privacy**: Be careful about what messages you auto-respond to

## Customization
- Modify `SYSTEM_PROMPT` to change AI personality
- Adjust `max_tokens` and `temperature` for different response styles
- Add more commands in the event handlers
- Change group message handling behavior