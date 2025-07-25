import asyncio
import logging
from telethon import TelegramClient, events
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE = os.getenv('PHONE')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash-lite')
client = TelegramClient('userbot_session', API_ID, API_HASH)

SYSTEM_PROMPT = """You are a helpful assistant responding to Telegram messages. 
Keep responses short, friendly, and conversational. 
Respond naturally as if you're chatting with a friend."""

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_ai_response(message_text, sender_name="User"):
    try:
        prompt = f"{SYSTEM_PROMPT}\n\n{sender_name}: {message_text}"
        response = await model.generate_content_async(prompt)
        return response.text.strip()
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return "Sorry, I'm having trouble responding right now."

@client.on(events.NewMessage(incoming=True))
async def handle_message(event):
    if event.message.out:
        return
    
    message = event.message
    sender = await event.get_sender()
    chat = await event.get_chat()
    
    if hasattr(chat, 'participants_count'):
        return
    
    sender_name = getattr(sender, 'first_name', 'User')
    if hasattr(sender, 'last_name') and sender.last_name:
        sender_name += f" {sender.last_name}"
    
    if not message.text or message.text.startswith('/') or message.text.startswith('!'):
        return
    
    try:
        ai_response = await get_ai_response(message.text, sender_name)
        await asyncio.sleep(2)
        await client.send_read_acknowledge(event.chat_id)
        async with client.action(event.chat_id, 'typing'):
            await asyncio.sleep(1)
        await event.reply(ai_response)
        logger.info(f"Replied to {sender_name}")
    except Exception as e:
        logger.error(f"Error: {e}")

@client.on(events.NewMessage(pattern=r'!help'))
async def help_command(event):
    help_text = "🤖 Commands: !help, !status, !stop"
    await event.reply(help_text)

@client.on(events.NewMessage(pattern=r'!status'))
async def status_command(event):
    await event.reply("✅ Bot is running!")

@client.on(events.NewMessage(pattern=r'!stop'))
async def stop_command(event):
    if event.message.out:
        await event.reply("🛑 Stopping...")
        await client.disconnect()

async def main():
    await client.start(phone=PHONE)
    print("✅ Userbot started!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Stopped")