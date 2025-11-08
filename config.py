import os
import re
from dotenv import load_dotenv
from typing import Dict, Any

# Import centralized constants
from common.constants import (
    # Time constants
    SECONDS_PER_MINUTE,
    MINUTES_PER_HOUR,
    CHECK_INTERVAL_MINUTES,
    DEFAULT_CHECK_INTERVAL,

    # Ethereum constants
    WALLET_ADDRESS_LENGTH,
    ETH_ADDRESS_PREFIX,
    WEI_TO_ETH_DIVISOR,

    # API URLs
    HYPERLIQUID_API_URL,
    ETHERSCAN_API_URL,

    # Default values
    DEFAULT_BALANCE_CHANGE_THRESHOLD,
    DEFAULT_POSITION_CHANGE_THRESHOLD,
    DEFAULT_SMTP_SERVER,
    DEFAULT_SMTP_PORT,

    # Configuration
    CONFIG_FILE,
    ENV_FILE,

    # Validation patterns
    ETH_ADDRESS_PATTERN
)

# Load environment variables from .env file
load_dotenv()

class ConfigurationError(Exception):
    """Configuration related errors"""
    pass

def validate_ethereum_address(address: str) -> bool:
    """Validate Ethereum address format using centralized pattern"""
    if not address:
        return False
    # Use the centralized validation pattern
    return bool(re.match(ETH_ADDRESS_PATTERN, address))

def validate_required_env_var(key: str, value: str, allow_default: bool = False) -> str:
    """Validate required environment variable"""
    if not value:
        raise ConfigurationError(f"Required environment variable {key} is not set")

    if allow_default and value.startswith("YOUR_"):
        raise ConfigurationError(f"Environment variable {key} must be set to a real value, not the default placeholder")

    return value

def load_wallets_config() -> Dict[str, Dict[str, Any]]:
    """Load wallet configuration from JSON or individual environment variables"""
    wallets = {}

    # Try to load from JSON configuration first
    wallets_json = os.getenv("WALLETS_JSON", "")
    if wallets_json:
        try:
            import json
            raw_wallets = json.loads(wallets_json)

            for wallet_id, wallet_data in raw_wallets.items():
                if not isinstance(wallet_data, dict):
                    continue

                address = wallet_data.get("address", "")
                if not validate_ethereum_address(address):
                    raise ConfigurationError(f"Invalid Ethereum address in WALLETS_JSON: {address}")

                wallets[wallet_id] = {
                    "address": address,
                    "name": wallet_data.get("name", f"Wallet {wallet_id}"),
                    "enabled": wallet_data.get("enabled", True),
                    "telegram_chat_id": wallet_data.get("telegram_chat_id"),
                    "email_recipient": wallet_data.get("email_recipient")
                }
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Invalid JSON in WALLETS_JSON: {e}")

    # Fallback to individual wallet environment variables
    if not wallets:
        # Check for wallets from WALLET_1 to WALLET_100 to support gaps
        for i in range(1, 101):
            address_key = f"WALLET_{i}_ADDRESS"
            name_key = f"WALLET_{i}_NAME"
            enabled_key = f"WALLET_{i}_ENABLED"

            address = os.getenv(address_key, "")
            if not address:
                continue  # Skip if no address, but don't break - allow gaps

            if not validate_ethereum_address(address):
                raise ConfigurationError(f"Invalid Ethereum address in {address_key}: {address}")

            wallet_id = f"wallet_{i}"
            wallets[wallet_id] = {
                "address": address,
                "name": os.getenv(name_key, f"Wallet {i}"),
                "enabled": os.getenv(enabled_key, "true").lower() == "true",
                "telegram_chat_id": os.getenv(f"WALLET_{i}_TELEGRAM_CHAT_ID"),
                "email_recipient": os.getenv(f"WALLET_{i}_EMAIL_RECIPIENT")
            }

    return wallets

def load_secure_config() -> Dict[str, Any]:
    """Load and validate configuration securely"""
    config = {}

    try:
        # Load multiple wallets
        wallets = load_wallets_config()
        config["wallets"] = wallets

        # If no wallets defined, fallback to single wallet for backward compatibility
        if not wallets:
            wallet_address = os.getenv("WALLET_ADDRESS", "")
            if wallet_address:
                wallet_address = validate_required_env_var("WALLET_ADDRESS", wallet_address)
                if not validate_ethereum_address(wallet_address):
                    raise ConfigurationError(f"Invalid Ethereum address format: {wallet_address}")

                wallets = {
                    "default": {
                        "address": wallet_address,
                        "name": "Default Wallet",
                        "enabled": True
                    }
                }
                config["wallets"] = wallets
            else:
                raise ConfigurationError("No wallet addresses configured. Use WALLETS_JSON or WALLET_ADDRESS")

        # Validate Etherscan API key
        etherscan_key = os.getenv("ETHERSCAN_API_KEY", "")
        config["etherscan_api_key"] = validate_required_env_var("ETHERSCAN_API_KEY", etherscan_key)

        # Optional Telegram configuration
        telegram_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID", "")

        config["telegram"] = {
            "enabled": bool(telegram_token and telegram_chat_id),
            "bot_token": telegram_token,
            "chat_id": telegram_chat_id
        }

        # Optional Email configuration
        email_sender = os.getenv("EMAIL_SENDER", "")
        email_password = os.getenv("EMAIL_PASSWORD", "")
        email_recipient = os.getenv("EMAIL_RECIPIENT", "")
        email_enabled = os.getenv("EMAIL_ENABLED", "false").lower() == "true"

        # Email is only enabled if EMAIL_ENABLED=true is explicitly set
        # This prevents authentication errors when email is configured but not intended to be used
        config["email"] = {
            "enabled": email_enabled and bool(email_sender and email_password and email_recipient),
            "smtp_server": DEFAULT_SMTP_SERVER,
            "smtp_port": DEFAULT_SMTP_PORT,
            "sender_email": email_sender,
            "sender_password": email_password,
            "recipient_email": email_recipient
        }

        # Other configuration
        config["check_interval"] = int(os.getenv("CHECK_INTERVAL", str(DEFAULT_CHECK_INTERVAL)))
        config["balance_change_threshold"] = float(os.getenv("BALANCE_CHANGE_THRESHOLD", str(DEFAULT_BALANCE_CHANGE_THRESHOLD)))
        config["position_change_threshold"] = float(os.getenv("POSITION_CHANGE_THRESHOLD", str(DEFAULT_POSITION_CHANGE_THRESHOLD)))

        # Notification settings
        config["notification_settings"] = {
            "email": config["email"],
            "telegram": config["telegram"],
            "console": {"enabled": True}
        }

        return config

    except (ValueError, TypeError) as e:
        raise ConfigurationError(f"Configuration validation error: {e}")

def load_config():
    """Load and validate configuration"""
    return load_secure_config()

# Load configuration with validation
CONFIG = load_secure_config()

# Backward compatibility - export variables for existing code
if "wallets" in CONFIG and CONFIG["wallets"]:
    # Get first enabled wallet for backward compatibility
    first_wallet = next((w for w in CONFIG["wallets"].values() if w.get("enabled", True)), None)
    if first_wallet:
        WALLET_ADDRESS = first_wallet["address"]
    else:
        WALLET_ADDRESS = ""
else:
    WALLET_ADDRESS = ""

# Export configuration variables for backward compatibility
ETHERSCAN_API_KEY = CONFIG["etherscan_api_key"]
CHECK_INTERVAL = CONFIG["check_interval"]
BALANCE_CHANGE_THRESHOLD = CONFIG["balance_change_threshold"]
POSITION_CHANGE_THRESHOLD = CONFIG["position_change_threshold"]
NOTIFICATION_SETTINGS = CONFIG["notification_settings"]
TELEGRAM_BOT_TOKEN = CONFIG["telegram"]["bot_token"]
TELEGRAM_CHAT_ID = CONFIG["telegram"]["chat_id"]

