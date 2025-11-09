"""
Common Constants for Balina2Droid
Centralized constants to avoid duplication across the codebase
"""

# =============================================================================
# 🔗 ETHEREUM BLOCKCHAIN CONSTANTS
# =============================================================================

# Ethereum conversions
WEI_TO_ETH_DIVISOR = 10**18

# Address validation
WALLET_ADDRESS_LENGTH = 42
ETH_ADDRESS_PREFIX = "0x"

# =============================================================================
# ⏰ TIME CONSTANTS
# =============================================================================

SECONDS_PER_MINUTE = 60
MINUTES_PER_HOUR = 60
SECONDS_PER_HOUR = MINUTES_PER_HOUR * SECONDS_PER_MINUTE
HOURS_PER_DAY = 24
SECONDS_PER_DAY = HOURS_PER_DAY * SECONDS_PER_HOUR

# Default intervals (in seconds)
CHECK_INTERVAL_MINUTES = 10
DEFAULT_CHECK_INTERVAL = CHECK_INTERVAL_MINUTES * SECONDS_PER_MINUTE

# =============================================================================
# 🔧 DEFAULT VALUES
# =============================================================================

# Balance and position change thresholds
DEFAULT_BALANCE_CHANGE_THRESHOLD = 0.1  # ETH
DEFAULT_POSITION_CHANGE_THRESHOLD = 1000  # USD

# API query limits
DEFAULT_LIMIT = 10
DEFAULT_RETRIES = 3

# Rate limiting
DEFAULT_RATE_LIMIT_ETHERSCAN = 2  # requests per second (more conservative)
DEFAULT_RATE_LIMIT_HYPERLIQUID = 10  # requests per second
DEFAULT_RATE_LIMIT_PERIOD = 1  # seconds

# Timeouts
DEFAULT_TIMEOUT_SECONDS = 30
DEFAULT_REQUEST_TIMEOUT = 30

# =============================================================================
# 🌐 API ENDPOINTS
# =============================================================================

# Blockchain APIs
ETHERSCAN_API_URL_V1 = "https://api.etherscan.io/api"  # Fallback for V2 issues
ETHERSCAN_API_URL = "https://api.etherscan.io/v2/api"  # V2 API
ETHERSCAN_CHAIN_ID = 1  # Ethereum mainnet
HYPERLIQUID_API_URL = "https://api.hyperliquid.xyz/info"

# =============================================================================
# 📧 EMAIL CONFIGURATION
# =============================================================================

# SMTP settings
DEFAULT_SMTP_SERVER = "smtp.gmail.com"
DEFAULT_SMTP_PORT = 587
DEFAULT_SMTP_USE_TLS = True

# =============================================================================
# 🎨 FORMATTING CONSTANTS
# =============================================================================

# Address and transaction formatting
ADDRESS_TRUNCATE_LENGTH = 10  # Gerçek sistemde kullanılan değer
TRANSACTION_HASH_TRUNCATE_LENGTH = 20  # Gerçek sistemde kullanılan değer

# Token formatting
DEFAULT_TOKEN_DECIMALS = 18

# Display defaults
DEFAULT_NUMERIC_VALUE = 0
DEFAULT_STRING_VALUE = "Unknown"
DEFAULT_CURRENCY = "USD"

# Scaling factors
PERCENTAGE_MULTIPLIER = 100

# =============================================================================
# 📊 POSITION STATUS MAPPINGS
# =============================================================================

# Position status emojis
POSITION_STATUS_EMOJIS = {
    "open": "🟢",
    "closed": "🔴",
    "liquidated": "💥",
    "partial": "🟡",
    "unknown": "❓"
}

# Position side emojis
POSITION_SIDE_EMOJIS = {
    "long": "🟢",
    "short": "🔴",
    "unknown": "❓"
}

# PnL emojis
PNL_EMOJIS = {
    "profit": "💰",
    "loss": "📉",
    "neutral": "➡️"
}

# Direction emojis
DIRECTION_EMOJIS = {
    "up": "⬆️",
    "down": "⬇️",
    "neutral": "➡️"
}

# Funding emojis
FUNDING_EMOJI = "💰"

# Highlight emoji
HIGHLIGHT_EMOJI = "🆕"

# =============================================================================
# 📊 DISPLAY FORMATTING
# =============================================================================

# Console formatting
CONSOLE_LINE_LENGTH = 60  # Gerçek sistemde kullanılan değer
CONSOLE_SEPARATOR = "=" * CONSOLE_LINE_LENGTH

# Status indicators
STATUS_ACTIVE = "✅"
STATUS_INACTIVE = "❌"
STATUS_WARNING = "⚠️"
STATUS_ERROR = "🚨"
STATUS_PENDING = "⏳"

# HTTP status codes
HTTP_SUCCESS_CODE = 200
HTTP_CREATED_CODE = 201
HTTP_BAD_REQUEST_CODE = 400
HTTP_UNAUTHORIZED_CODE = 401
HTTP_FORBIDDEN_CODE = 403
HTTP_NOT_FOUND_CODE = 404
HTTP_RATE_LIMIT_CODE = 429
HTTP_SERVER_ERROR_CODE = 500

# =============================================================================
# 🎨 CONSOLE COLOR CODES
# =============================================================================

# Console color codes for terminal output
COLOR_CODES = {
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'magenta': '\033[95m',
    'cyan': '\033[96m',
    'white': '\033[97m',
    'bold': '\033[1m',
    'end': '\033[0m'
}

# =============================================================================
# 🔍 LOGGING LEVELS
# =============================================================================

LOG_LEVEL_DEBUG = "DEBUG"
LOG_LEVEL_INFO = "INFO"
LOG_LEVEL_WARNING = "WARNING"
LOG_LEVEL_ERROR = "ERROR"
LOG_LEVEL_CRITICAL = "CRITICAL"

# =============================================================================
# 📊 PERFORMANCE METRICS
# =============================================================================

# Performance benchmarks
PERFORMANCE_TARGET_WALLET_CHECK_TIME = 15  # seconds
PERFORMANCE_TARGET_API_RESPONSE_TIME = 5   # seconds
PERFORMANCE_TARGET_CONCURRENT_WALLETS = 10   # number of wallets

# Memory limits
MEMORY_MAX_CONNECTIONS = 100
MEMORY_MAX_CONNECTIONS_PER_HOST = 20
MEMORY_CONNECTION_TTL = 300
MEMORY_DNS_CACHE_TTL = 300
MEMORY_KEEPALIVE_TIMEOUT = 60

# =============================================================================
# 🛡️ SECURITY CONSTANTS
# =============================================================================

# Validation patterns
ETH_ADDRESS_PATTERN = r'^0x[a-fA-F0-9]{40}$'

# Maximum values
MAX_WALLET_COUNT = 1000
MAX_RETRY_ATTEMPTS = 10
MAX_TIMEOUT_SECONDS = 300

# Safety checks
MIN_CHECK_INTERVAL = 30  # seconds
MAX_CHECK_INTERVAL = 3600  # 1 hour
MIN_RATE_LIMIT = 1  # requests per second
MAX_RATE_LIMIT = 100  # requests per second

# =============================================================================
# 📱 NOTIFICATION CONSTANTS
# =============================================================================

# Notification types
NOTIFICATION_TYPE_BALANCE = "BALANCE CHANGE"
NOTIFICATION_TYPE_POSITION = "POSITION"
NOTIFICATION_TYPE_TRANSACTION = "TRANSACTION"
NOTIFICATION_TYPE_ERROR = "ERROR"
NOTIFICATION_TYPE_SUMMARY = "SUMMARY"

# Notification channels
NOTIFICATION_CHANNEL_CONSOLE = "console"
NOTIFICATION_CHANNEL_TELEGRAM = "telegram"
NOTIFICATION_CHANNEL_EMAIL = "email"

# Message templates
MESSAGE_TEMPLATE_WALLET_STARTED = "🚀 WALLET TRACKER STARTED"
MESSAGE_TEMPLATE_CHECK_COMPLETED = "✅ Check completed"
MESSAGE_TEMPLATE_NO_CHANGES = "✅ No important changes detected"

# =============================================================================
# 🔧 DEVELOPMENT CONSTANTS
# =============================================================================

# Development mode
DEVELOPMENT_MODE = False
DEBUG_MODE = False

# Testing settings
TEST_MODE = False
MOCK_APIS = False

# Environment detection
ENVIRONMENT_DEV = "development"
ENVIRONMENT_STAGING = "staging"
ENVIRONMENT_PRODUCTION = "production"

# =============================================================================
# 📋 FILE PATHS
# =============================================================================

# Log files
DEFAULT_LOG_FILE = "wallet_tracker.log"
TRANSACTION_LOG_FILE = "transactions.log"
ERROR_LOG_FILE = "wallet_tracker_errors.log"

# Configuration files
CONFIG_FILE = "config.py"
ENV_FILE = ".env"
ENV_EXAMPLE_FILE = ".env.example"

# Data files
CACHE_DIR = ".cache"
TEMP_DIR = ".temp"
BACKUP_DIR = ".backups"

# =============================================================================
# 🎯 VERSION AND METADATA
# =============================================================================

# Application info
APP_NAME = "Balina2Droid"
APP_VERSION = "2.1.1"
APP_DESCRIPTION = "Multi-Wallet Crypto Tracker"
APP_AUTHOR = "Crypto Wallet Tracker Team"

# Protocol versions
TELEGRAM_BOT_API_VERSION = "13.7"
PYTHON_MIN_VERSION = "3.7"
WEB3_VERSION = "5.28.0"

# =============================================================================
# 📊 BUSINESS RULES
# =============================================================================

# Business thresholds
SIGNIFICANT_BALANCE_CHANGE = 0.1
SIGNIFICANT_POSITION_CHANGE_PERCENTAGE = 0.05
POSITION_CHANGE_PERCENTAGE = 0.05

# Alert thresholds
ALERT_THRESHOLD_HIGH_VALUE_TRANSACTION = 10000  # USD
ALERT_THRESHOLD_MULTIPLE_TRANSACTIONS = 5
ALERT_THRESHOLD_RARE_TOKEN = True

# =============================================================================
# 🔄 INTEGRATION CONSTANTS
# =============================================================================

# External service settings
ETHERSCAN_MAX_REQUESTS_PER_SECOND = 5
TELEGRAM_MESSAGE_MAX_LENGTH = 4096
EMAIL_SUBJECT_MAX_LENGTH = 200

# Batch processing
BATCH_SIZE_DEFAULT = 5
MAX_CONCURRENT_REQUESTS = 20
MAX_ASYNC_CONCURRENT_TASKS = 100

# =============================================================================
# 📦 PACKAGE EXPORTS
# =============================================================================

# Export all constants for easy import
__all__ = [
    # Ethereum constants
    "WEI_TO_ETH_DIVISOR",
    "WALLET_ADDRESS_LENGTH",
    "ETH_ADDRESS_PREFIX",

    # Time constants
    "SECONDS_PER_MINUTE",
    "MINUTES_PER_HOUR",
    "HOURS_PER_DAY",
    "SECONDS_PER_HOUR",
    "SECONDS_PER_DAY",
    "CHECK_INTERVAL_MINUTES",
    "DEFAULT_CHECK_INTERVAL",

    # Default values
    "DEFAULT_BALANCE_CHANGE_THRESHOLD",
    "DEFAULT_POSITION_CHANGE_THRESHOLD",
    "DEFAULT_LIMIT",
    "DEFAULT_RETRIES",
    "DEFAULT_TIMEOUT_SECONDS",
    "DEFAULT_REQUEST_TIMEOUT",

    # Rate limiting
    "DEFAULT_RATE_LIMIT_ETHERSCAN",
    "DEFAULT_RATE_LIMIT_HYPERLIQUID",
    "DEFAULT_RATE_LIMIT_PERIOD",

    # API endpoints
    "ETHERSCAN_API_URL_V1",
    "ETHERSCAN_API_URL",
    "ETHERSCAN_CHAIN_ID",
    "HYPERLIQUID_API_URL",

    # Email configuration
    "DEFAULT_SMTP_SERVER",
    "DEFAULT_SMTP_PORT",
    "DEFAULT_SMTP_USE_TLS",

    # Formatting constants
    "ADDRESS_TRUNCATE_LENGTH",
    "TRANSACTION_HASH_TRUNCATE_LENGTH",
    "DEFAULT_TOKEN_DECIMALS",
    "DEFAULT_NUMERIC_VALUE",
    "DEFAULT_STRING_VALUE",
    "DEFAULT_CURRENCY",
    "PERCENTAGE_MULTIPLIER",

    # Position mappings
    "POSITION_STATUS_EMOJIS",
    "POSITION_SIDE_EMOJIS",
    "PNL_EMOJIS",
    "DIRECTION_EMOJIS",
    "FUNDING_EMOJI",
    "HIGHLIGHT_EMOJI",

    # Display formatting
    "CONSOLE_LINE_LENGTH",
    "CONSOLE_SEPARATOR",
    "COLOR_CODES",

    # Status indicators
    "STATUS_ACTIVE",
    "STATUS_INACTIVE",
    "STATUS_WARNING",
    "STATUS_ERROR",
    "STATUS_PENDING",

    # HTTP status codes
    "HTTP_SUCCESS_CODE",
    "HTTP_CREATED_CODE",
    "HTTP_BAD_REQUEST_CODE",
    "HTTP_UNAUTHORIZED_CODE",
    "HTTP_FORBIDDEN_CODE",
    "HTTP_NOT_FOUND_CODE",
    "HTTP_RATE_LIMIT_CODE",
    "HTTP_SERVER_ERROR_CODE",

    # Logging levels
    "LOG_LEVEL_DEBUG",
    "LOG_LEVEL_INFO",
    "LOG_LEVEL_WARNING",
    "LOG_LEVEL_ERROR",
    "LOG_LEVEL_CRITICAL",

    # Performance metrics
    "PERFORMANCE_TARGET_WALLET_CHECK_TIME",
    "PERFORMANCE_TARGET_API_RESPONSE_TIME",
    "PERFORMANCE_TARGET_CONCURRENT_WALLETS",

    # Memory limits
    "MEMORY_MAX_CONNECTIONS",
    "MEMORY_MAX_CONNECTIONS_PER_HOST",
    "MEMORY_CONNECTION_TTL",
    "MEMORY_DNS_CACHE_TTL",
    "MEMORY_KEEPALIVE_TIMEOUT",

    # Security constants
    "ETH_ADDRESS_PATTERN",
    "MAX_WALLET_COUNT",
    "MAX_RETRY_ATTEMPTS",
    "MAX_TIMEOUT_SECONDS",
    "MIN_CHECK_INTERVAL",
    "MAX_CHECK_INTERVAL",
    "MIN_RATE_LIMIT",
    "MAX_RATE_LIMIT",

    # Notification constants
    "NOTIFICATION_TYPE_BALANCE",
    "NOTIFICATION_TYPE_POSITION",
    "NOTIFICATION_TYPE_TRANSACTION",
    "NOTIFICATION_TYPE_ERROR",
    "NOTIFICATION_TYPE_SUMMARY",
    "NOTIFICATION_CHANNEL_CONSOLE",
    "NOTIFICATION_CHANNEL_TELEGRAM",
    "NOTIFICATION_CHANNEL_EMAIL",

    # Message templates
    "MESSAGE_TEMPLATE_WALLET_STARTED",
    "MESSAGE_TEMPLATE_CHECK_COMPLETED",
    "MESSAGE_TEMPLATE_NO_CHANGES",

    # Development constants
    "DEVELOPMENT_MODE",
    "DEBUG_MODE",
    "TEST_MODE",
    "MOCK_APIS",

    # Environment detection
    "ENVIRONMENT_DEV",
    "ENVIRONMENT_STAGING",
    "ENVIRONMENT_PRODUCTION",

    # File paths
    "DEFAULT_LOG_FILE",
    "TRANSACTION_LOG_FILE",
    "ERROR_LOG_FILE",
    "CONFIG_FILE",
    "ENV_FILE",
    "ENV_EXAMPLE_FILE",
    "CACHE_DIR",
    "TEMP_DIR",
    "BACKUP_DIR",

    # Application info
    "APP_NAME",
    "APP_VERSION",
    "APP_DESCRIPTION",
    "APP_AUTHOR",

    # Protocol versions
    "TELEGRAM_BOT_API_VERSION",
    "PYTHON_MIN_VERSION",
    "WEB3_VERSION",

    # Business rules
    "SIGNIFICANT_BALANCE_CHANGE",
    "SIGNIFICANT_POSITION_CHANGE_PERCENTAGE",
    "POSITION_CHANGE_PERCENTAGE",

    # Alert thresholds
    "ALERT_THRESHOLD_HIGH_VALUE_TRANSACTION",
    "ALERT_THRESHOLD_MULTIPLE_TRANSACTIONS",
    "ALERT_THRESHOLD_RARE_TOKEN",

    # Integration constants
    "ETHERSCAN_MAX_REQUESTS_PER_SECOND",
    "TELEGRAM_MESSAGE_MAX_LENGTH",
    "EMAIL_SUBJECT_MAX_LENGTH",

    # Batch processing
    "BATCH_SIZE_DEFAULT",
    "MAX_CONCURRENT_REQUESTS",
    "MAX_ASYNC_CONCURRENT_TASKS"
]