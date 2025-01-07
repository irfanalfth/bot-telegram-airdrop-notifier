import os
from telethon import TelegramClient, events
from generateImage import generateImgAirdrop
from dotenv import load_dotenv # type: ignore
import os

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
channelName = os.getenv("CHANNEL_NAME")
numberTelegram = os.getenv("NUMBER_TELEGRAM")

with open('airdrop.txt', 'r') as file:
    airdrop = [line.strip() for line in file]

client = TelegramClient(numberTelegram, api_id, api_hash)

def checkWords(words, text):
    for word in words:
        if word in text:
            return True
    return False

def format_message(chat_name, text, message_link):
    formatted_message = (
        f"[{chat_name}]\n\n"
        f"{text}\n\n\n"
        f"• {message_link}\n"
    )
    return formatted_message

@client.on(events.NewMessage)
async def handler(event):
    if event.is_channel:
        chat = await event.get_chat()
        if getattr(chat, 'broadcast', False): 
            chat_name = chat.title if hasattr(chat, 'title') else "Unknown Channel"
            chat_username = "@" + chat.username if hasattr(chat, 'username') and chat.username else "Unknown"

            if chat_username != channelName:
                airdrop_status = checkWords(airdrop, event.text.lower())

                generateImgAirdrop(chat_name, chat_username)

                if airdrop_status:
                    if hasattr(chat, 'username') and chat.username:
                        message_link = f"https://t.me/{chat.username}/{event.message.id}"
                    else:
                        message_link = "Cannot generate link for private channels"

                    formatted_message = format_message(chat_name, event.text, message_link)

                    image_path = os.path.join("img", f"{chat_username}.jpg")
                    
                    if os.path.exists(image_path):
                        await client.send_file(channelName, image_path, caption=formatted_message)
                    else:
                        await client.send_message(channelName, formatted_message)
                else:
                    print("No matching words found.")
                    return
            return

async def main():
    await client.start()
    print("Bot running...")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
