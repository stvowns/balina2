"""
Constants and configuration values for balina2droid project
"""

# Console color codes
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

# Console formatting
CONSOLE_LINE_LENGTH = 60

# API timeouts
TELEGRAM_TIMEOUT_SECONDS = 30

# Ethereum constants
WEI_TO_ETH_DIVISOR = 10**18
DEFAULT_TOKEN_DECIMALS = 18

# Address formatting
ADDRESS_TRUNCATE_LENGTH = 10
TRANSACTION_HASH_TRUNCATE_LENGTH = 20

# PnL calculation constants
PERCENTAGE_MULTIPLIER = 100
SIGNIFICANT_BALANCE_CHANGE_THRESHOLD = 0.001

# Position status emojis
POSITION_STATUS_EMOJIS = {
    'profit': ' ⬆️ KARDA ⬆️ ',
    'loss': ' ⬇️ ZARARDA ⬇️ ',
    'neutral': '  NÖTR '
}

# Position side emojis
POSITION_SIDE_EMOJIS = {
    'long': '🟢',
    'short': '🔴'
}

# Status indicators
PNL_EMOJIS = {
    'profit': '✅',
    'loss': '❌',
    'neutral': '➖'
}

# Funding emoji
FUNDING_EMOJI = '💰'

# Highlight emoji for changed positions
HIGHLIGHT_EMOJI = '🔥'

# Direction indicators
DIRECTION_EMOJIS = {
    'up': '📈',
    'down': '📉'
}

# API response codes
HTTP_SUCCESS_CODE = 200

# Default API values
DEFAULT_NUMERIC_VALUE = 0
DEFAULT_STRING_VALUE = "Unknown"