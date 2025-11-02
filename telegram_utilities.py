#!/usr/bin/env python3
"""
Telegram Utilities - Consolidated Telegram helper functions
Combines functionality from telegram_setup.py, telegram_helper.py, and check_telegram.py
"""

import requests
import os
from dotenv import load_dotenv

def get_bot_token_from_config():
    """Get bot token from environment configuration"""
    load_dotenv()
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        print("❌ TELEGRAM_BOT_TOKEN not found in .env file")
        return None
    return bot_token

def get_bot_info(bot_token):
    """Get bot information"""
    try:
        url = f"https://api.telegram.org/bot{bot_token}/getMe"
        response = requests.get(url)
        data = response.json()

        if data["ok"]:
            bot_info = data["result"]
            print(f"Bot Name: {bot_info['first_name']}")
            print(f"Bot Username: @{bot_info['username']}")
            print(f"Bot ID: {bot_info['id']}")
            return bot_info
        else:
            print(f"Error getting bot info: {data.get('description', 'Unknown error')}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def check_messages(bot_token):
    """Check for messages and get chat_id"""
    try:
        url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
        response = requests.get(url)
        data = response.json()

        if data["ok"]:
            if data["result"]:
                print("📬 Messages found:")
                for msg in data["result"]:
                    if "message" in msg:
                        chat_id = msg["message"]["chat"]["id"]
                        chat_info = msg["message"]["chat"]

                        # Display chat info
                        chat_type = chat_info.get("type", "unknown")
                        first_name = chat_info.get("first_name", "")
                        username = chat_info.get("username", "")

                        print(f"  Chat ID: {chat_id}")
                        print(f"  Type: {chat_type}")
                        if first_name:
                            print(f"  Name: {first_name}")
                        if username:
                            print(f"  Username: @{username}")
                        print()

                last_message = data["result"][-1]
                chat_id = last_message["message"]["chat"]["id"]

                return chat_id
            else:
                print("❌ No messages found. Please send a message to the bot first.")
                return None
        else:
            print(f"❌ API Error: {data.get('description', 'Unknown error')}")
            return None

    except Exception as e:
        print(f"❌ Error occurred: {e}")
        return None

def test_telegram_notification(bot_token: str, chat_id: str) -> bool:
    """Test sending a message"""
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": "✅ Telegram setup successful!\n\nYour crypto wallet tracker is now configured to send notifications to Telegram.",
            "parse_mode": "HTML"
        }

        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("\n✅ Test message sent successfully!")
            return True
        else:
            print(f"\n❌ Failed to send test message: {response.text}")
            return False
    except Exception as e:
        print(f"\n❌ Error sending test message: {e}")
        return False

def interactive_chat_id_setup():
    """Interactive setup for getting chat ID"""
    print("🤖 Telegram Bot Kurulum Yardımcısı")
    print("="*50)

    # Bot token'ı al
    bot_token = input("BotFather'dan aldığınız Bot Token'ı girin: ").strip()

    if not bot_token:
        print("❌ Bot Token boş olamaz!")
        return None

    print(f"1. Lütfen botunuza bir mesaj gönderin: https://t.me/{bot_token.split(':')[0]}")
    print("2. Herhangi bir mesaj gönderin (örn: /start)")
    input("Mesaj gönderdikten sonra Enter tuşuna basın...")

    # Chat ID al
    chat_id = check_messages(bot_token)

    if chat_id:
        print(f"✅ Chat ID'niz: {chat_id}")
        print("\n✅ Kurulum tamamlandı!")
        print(f"📝 .env dosyasına ekleyin:")
        print(f"TELEGRAM_BOT_TOKEN={bot_token}")
        print(f"TELEGRAM_CHAT_ID={chat_id}")

        # Test mesajı gönder
        print("\n3. Test mesajı gönderiliyor...")
        test_telegram_notification(bot_token, chat_id)

        return chat_id
    else:
        print("❌ Chat ID bulunamadı")
        return None

def check_existing_chat_id():
    """Check for existing chat ID from configuration"""
    bot_token = get_bot_token_from_config()
    if not bot_token:
        print("❌ Please configure TELEGRAM_BOT_TOKEN in your .env file first")
        return None

    print("🤖 Checking for Telegram messages...")
    print(f"Bot link: https://t.me/{bot_token.split(':')[0]}")

    chat_id = check_messages(bot_token)

    if chat_id:
        print(f"✅ Use this Chat ID: {chat_id}")
        return chat_id
    else:
        print("\n❌ No messages found.")
        print("Please:")
        print("1. Click the link above")
        print("2. Send a message to the bot")
        print("3. Run this script again")
        return None

def setup_telegram_config():
    """Setup telegram configuration with multiple methods"""
    print("🤖 Telegram Configuration Setup")
    print("="*40)
    print("Choose setup method:")
    print("1. Interactive setup (recommended)")
    print("2. Check existing configuration")
    print("3. Test existing configuration")

    choice = input("\nEnter your choice (1-3): ").strip()

    bot_token = get_bot_token_from_config()
    if not bot_token:
        print("❌ Please configure TELEGRAM_BOT_TOKEN in your .env file first")
        return False

    if choice == "1":
        # Interactive setup
        chat_id = interactive_chat_id_setup()
        return chat_id is not None

    elif choice == "2":
        # Check existing
        chat_id = check_existing_chat_id()
        if chat_id:
            print(f"\n✅ Found Chat ID: {chat_id}")
            return True
        return False

    elif choice == "3":
        # Test existing
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        if chat_id:
            print(f"🧪 Testing with Chat ID: {chat_id}")
            return test_telegram_notification(bot_token, chat_id)
        else:
            print("❌ No TELEGRAM_CHAT_ID found in configuration")
            return False

    else:
        print("❌ Invalid choice")
        return False

if __name__ == "__main__":
    setup_telegram_config()