# 📚 Balina2Droid API Reference

> Comprehensive API documentation for developers and integrators

## 🏗️ Architecture Overview

Balina2Droid follows a modular architecture with clear separation of concerns:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Main App      │────│ MultiWalletTracker│────│  WalletTracker  │
│                 │    │                  │    │                 │
│ - CLI Interface │    │ - Coordination   │    │ - API Calls     │
│ - Configuration │    │ - Aggregation    │    │ - Data Processing│
│ - Logging       │    │ - Orchestration  │    │ - Validation    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │NotificationSystem│
                    │                  │
                    │ - Telegram       │
                    │ - Email          │
                    │ - Formatting     │
                    └──────────────────┘
```

## 📋 Core Components

### 1. `CryptoWalletMonitor` (main.py)

**Purpose**: Main application orchestrator and CLI interface

#### Methods

```python
def __init__(self) -> None
```
**Description**: Initialize the wallet monitor with logging and configuration.

**Raises**: `ConfigurationError` - If configuration fails to load

```python
def check_wallet_changes(self) -> None
```
**Description**: Execute one-time check for all configured wallets.

**Process**:
1. Check all enabled wallets for changes
2. Send notifications for detected changes
3. Log results and statistics

**Raises**: `WalletError` - If wallet checking fails

```python
def send_initial_summary(self) -> None
```
**Description**: Send startup summary notifications for all wallets.

**Raises**: `WalletError` - If summary sending fails

```python
def run_manual_check(self) -> None
```
**Description**: Run manual check with detailed console output.

**Output**: Comprehensive wallet status report

```python
def start_monitoring(self) -> None
```
**Description**: Start continuous monitoring with scheduled checks.

**Behavior**: Runs indefinitely until interrupted

---

### 2. `MultiWalletTracker` (multi_wallet_tracker.py)

**Purpose**: Coordinates multiple wallet trackers and notification systems.

#### Constructor

```python
def __init__(self, config: Dict[str, Any]) -> None
```

**Parameters**:
- `config` (Dict): Application configuration dictionary

**Initializes**:
- Individual wallet trackers
- Notification systems per wallet
- Error handling and logging

#### Methods

```python
def check_all_wallets(self) -> Dict[str, List[Dict]]
```
**Description**: Check all enabled wallets for changes.

**Returns**: Dictionary mapping wallet IDs to lists of change events

**Change Events**:
- `balance_change`: ETH balance variations
- `position_change`: Hyperliquid position updates
- `deposit_withdrawal`: Token transfers
- `error`: Check failures

```python
def get_all_wallets_summary(self) -> Dict[str, Dict]
```
**Description**: Get comprehensive status summary for all wallets.

**Returns**: Dictionary with wallet balances, positions, and metadata

```python
def send_initial_summary(self) -> None
```
**Description**: Send initial status notifications for all wallets.

**Process**:
1. Generate wallet summaries
2. Send startup notifications
3. Log initialization status

---

### 3. `WalletTracker` (wallet_tracker.py)

**Purpose**: Individual wallet monitoring and API interaction.

#### Constructor

```python
def __init__(self, wallet_address: str, etherscan_api_key: str) -> None
```

**Parameters**:
- `wallet_address` (str): Ethereum wallet address
- `etherscan_api_key` (str): Etherscan API key

#### Constants

```python
WEI_TO_ETH_DIVISOR = 10**18
DEFAULT_LIMIT = 10
SIGNIFICANT_BALANCE_CHANGE = 0.1
POSITION_CHANGE_PERCENTAGE = 0.05
CHECK_INTERVAL_SECONDS = 600
```

#### Methods

```python
def get_eth_balance(self) -> Optional[float]
```
**Description**: Get current ETH balance from Etherscan API.

**Returns**: ETH balance as float or None if API call fails

**Raises**: `APIError` - If API request fails

```python
def get_transactions(self, limit: int = None) -> List[Dict]
```
**Description**: Get recent wallet transactions.

**Parameters**:
- `limit` (int, optional): Maximum number of transactions (default: 10)

**Returns**: List of transaction dictionaries

```python
def check_balance_change(self) -> Tuple[bool, Optional[float], Optional[float]]
```
**Description**: Check if ETH balance has changed significantly.

**Returns**: Tuple of (changed, current_balance, change_amount)

**Logic**:
- Compare current balance with last known balance
- Return True if change exceeds `SIGNIFICANT_BALANCE_CHANGE`
- Update internal balance tracking

```python
def get_hyperliquid_positions(self) -> Optional[Dict]
```
**Description**: Get Hyperliquid trading positions for the wallet.

**Returns**: Position data dictionary or None if unavailable

**Data Includes**:
- Open positions and sizes
- PnL information
- Margin usage
- Account value

```python
def check_position_changes(self) -> Tuple[bool, Optional[Dict], str]
```
**Description**: Check for significant position changes.

**Returns**: Tuple of (changed, positions_data, change_type)

**Change Types**:
- `position_opened`: New position detected
- `position_closed`: Position liquidated
- `position_changed`: Significant size/value change

---

### 4. `NotificationSystem` (notification_system.py)

**Purpose**: Handle notification delivery across multiple channels.

#### Constructor

```python
def __init__(self, config: Dict[str, Any]) -> None
```

**Parameters**:
- `config` (Dict): Notification configuration including:
  - Telegram settings
  - Email settings
  - Wallet-specific preferences

#### Methods

```python
def send_notification(self, message: str, title: str) -> bool
```
**Description**: Send notification through all enabled channels.

**Parameters**:
- `message` (str): Notification message content
- `title` (str): Notification title/subject

**Returns**: True if at least one channel succeeds

**Channels**:
- Telegram Bot API
- Email SMTP
- Future: Discord, Slack, etc.

```python
def format_balance_change(self, old_balance: float, new_balance: float, change: float) -> str
```
**Description**: Format balance change notification message.

**Returns**: Formatted message with emojis and context

```python
def format_position_change(self, positions: Dict, change_type: str) -> str
```
**Description**: Format position change notification message.

**Parameters**:
- `positions` (Dict): Position data from Hyperliquid
- `change_type` (str): Type of position change

**Returns**: Formatted position notification

---

### 5. `APIClient` (api_client.py)

**Purpose**: Robust HTTP client with retry logic and error handling.

#### Constructor

```python
def __init__(self, base_url: str, api_key: str = None, config: APIConfig = None)
```

**Parameters**:
- `base_url` (str): Base URL for API endpoints
- `api_key` (str, optional): API authentication key
- `config` (APIConfig, optional): Request configuration

#### Methods

```python
def get(self, endpoint: str, params: Dict = None) -> Dict[str, Any]
```
**Description**: Make GET request with retry logic.

**Parameters**:
- `endpoint` (str): API endpoint path
- `params` (Dict, optional): Query parameters

**Returns**: JSON response data

**Features**:
- Automatic retries on failure
- Rate limiting support
- Timeout management
- Error context preservation

```python
def post(self, endpoint: str, json_data: Dict = None) -> Dict[str, Any]
```
**Description**: Make POST request with JSON payload.

**Parameters**:
- `endpoint` (str): API endpoint path
- `json_data` (Dict, optional): Request body data

**Returns**: JSON response data

---

## 🔧 Configuration System

### Environment Variables

#### Core Configuration
```bash
# Required
ETHERSCAN_API_KEY=your_etherscan_api_key
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# Optional
CHECK_INTERVAL=600
BALANCE_CHANGE_THRESHOLD=0.1
POSITION_CHANGE_THRESHOLD=1000
LOG_LEVEL=INFO
```

#### Multi-Wallet Configuration
```bash
# Individual wallets
WALLET_1_ADDRESS=0x742d35Cc6634C0532925a3b8D4C9db96C4b4Db45
WALLET_1_NAME=Trading Wallet
WALLET_1_ENABLED=true
WALLET_1_TELEGRAM_CHAT_ID=123456789
WALLET_1_EMAIL_RECIPIENT=trading@example.com

# JSON configuration alternative
WALLETS_JSON={"trading":{"address":"0x742d35Cc6634C0532925a3b8D4C9db96C4b4Db45","name":"Trading Wallet","enabled":true}}
```

#### Email Configuration
```bash
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECIPIENT=alerts@example.com
```

### Configuration Priority

1. **Individual Environment Variables** (highest priority)
2. **JSON Configuration** (medium priority)
3. **Legacy Single Wallet** (lowest priority)

---

## 🔍 Exception Hierarchy

```python
Balina2DroidError                    # Base exception
├── ConfigurationError              # Config loading/validation
├── APIError                        # API request failures
├── WalletError                     # Wallet operation failures
├── NetworkError                    # Network connectivity issues
├── NotificationError               # Notification delivery failures
├── ValidationError                 # Data validation failures
└── RetryExhaustedError            # Retry limit exceeded
```

### Error Context

All exceptions include contextual information:

```python
try:
    # Some operation
except APIError as e:
    print(f"API Error: {e.message}")
    print(f"API: {e.api_name}")
    print(f"Status: {e.status_code}")
    print(f"Context: {e.context}")
```

---

## 📊 Data Structures

### Transaction Record
```python
{
    "hash": "0x...",
    "from": "0x...",
    "to": "0x...",
    "value": 1000000000000000000,  # wei
    "timestamp": 1640995200,
    "block_number": 12345678,
    "gas_used": 21000,
    "gas_price": 20000000000
}
```

### Position Data
```python
{
    "positions": [
        {
            "coin": "ETH",
            "side": "long",
            "position": 1.5,
            "entry_price": 3000.0,
            "mark_price": 3100.0,
            "unrealized_pnl": 150.0,
            "leverage": 5.0
        }
    ],
    "margin_summary": {
        "account_value": 10000.0,
        "total_notion": 5000.0,
        "margin_usage": 0.3
    }
}
```

### Notification Event
```python
{
    "wallet_id": "trading",
    "type": "balance_change",
    "timestamp": "2024-01-01T12:00:00Z",
    "data": {
        "old_balance": 1.0,
        "new_balance": 1.5,
        "change": 0.5
    }
}
```

---

## 🔄 Event Flow

### Wallet Check Cycle

```
1. Start Check
   ↓
2. Get Wallet List
   ↓
3. For Each Enabled Wallet:
   ├─ Get ETH Balance
   ├─ Get Transactions
   ├─ Get Hyperliquid Positions
   ├─ Compare with Previous State
   └─ Generate Change Events
   ↓
4. Aggregate All Changes
   ↓
5. Send Notifications
   ↓
6. Log Results
   ↓
7. Wait for Next Interval
```

### Notification Flow

```
1. Change Event Detected
   ↓
2. Determine Event Type
   ↓
3. Format Message
   ├─ Choose Template
   ├─ Add Context
   └─ Add Emojis
   ↓
4. Determine Recipients
   ├─ Global Settings
   ├─ Wallet-Specific
   └─ Channel Preferences
   ↓
5. Send via Each Channel
   ├─ Telegram API
   ├─ Email SMTP
   └─ Log Delivery Status
   ↓
6. Handle Failures
   ├─ Retry Logic
   ├─ Fallback Channels
   └─ Error Logging
```

---

## 🧪 Testing Integration

### Test Components

- **Unit Tests**: Individual function testing
- **Integration Tests**: Component interaction testing
- **Mock Tests**: API response simulation
- **End-to-End Tests**: Full workflow validation

### Test Data

```python
# Mock wallet address
TEST_WALLET = "0x742d35Cc6634C0532925a3b8D4C9db96C4b4Db45"

# Mock API responses
MOCK_BALANCE_RESPONSE = {
    "status": "1",
    "result": "1000000000000000000"  # 1 ETH in wei
}

MOCK_POSITIONS_RESPONSE = {
    "marginSummary": {
        "accountValue": "10000.0",
        "totalNotion": "5000.0",
        "marginUsage": "0.3"
    }
}
```

---

## 🔒 Security Considerations

### API Key Management
- Never commit API keys to version control
- Use environment variables or secure storage
- Rotate keys regularly
- Monitor API usage and limits

### Data Privacy
- Wallet addresses are public blockchain data
- Transaction history is public
- Notification content may contain sensitive financial information
- Store logs securely and consider retention policies

### Network Security
- Use HTTPS for all API communications
- Validate API responses before processing
- Implement rate limiting to prevent abuse
- Monitor for suspicious activity

---

## 📈 Performance Metrics

### API Call Optimization
- **Batch Requests**: Combine multiple calls when possible
- **Caching**: Cache frequently accessed data
- **Rate Limiting**: Respect API rate limits
- **Timeouts**: Implement appropriate timeouts

### Resource Management
- **Connection Pooling**: Reuse HTTP connections
- **Memory Management**: Clean up unused resources
- **Async Operations**: Consider async for concurrent requests
- **Background Processing**: Use threading for non-blocking operations

### Monitoring
- **Success Rates**: Track API call success/failure rates
- **Response Times**: Monitor API response latency
- **Error Patterns**: Identify common failure modes
- **Resource Usage**: Track memory and CPU usage

---

## 🛠️ Extension Points

### Custom Notification Channels
```python
class CustomNotificationProvider:
    def send_notification(self, message: str, title: str) -> bool:
        # Custom notification logic
        pass

# Register with NotificationSystem
notification_system.add_provider('custom', CustomNotificationProvider())
```

### Custom Data Sources
```python
class CustomDataSource:
    def get_data(self, wallet_address: str) -> Dict:
        # Custom API integration
        pass

# Integrate with WalletTracker
tracker.add_data_source('custom', CustomDataSource())
```

### Custom Validation Rules
```python
class CustomValidator:
    def validate_transaction(self, tx: Dict) -> bool:
        # Custom validation logic
        return True

# Apply to transaction processing
tracker.add_validator(CustomValidator())
```

---

## 📝 API Usage Examples

### Basic Wallet Monitoring
```python
from multi_wallet_tracker import MultiWalletTracker

# Load configuration
config = {
    "wallets": {
        "trading": {
            "address": "0x742d35Cc6634C0532925a3b8D4C9db96C4b4Db45",
            "name": "Trading Wallet",
            "enabled": True
        }
    },
    "etherscan_api_key": "your_api_key"
}

# Initialize tracker
tracker = MultiWalletTracker(config)

# Check all wallets
results = tracker.check_all_wallets()

# Process results
for wallet_id, changes in results.items():
    for change in changes:
        print(f"Wallet {wallet_id}: {change['type']}")
```

### Custom Notification Handling
```python
from notification_system import NotificationSystem
from logger_config import get_logger

logger = get_logger('custom_notifications')

# Custom notification logic
def custom_notification_handler(change_event: Dict) -> None:
    if change_event['type'] == 'large_deposit':
        # Send high-priority notification
        message = f"🚨 LARGE DEPOSIT: {change_event['amount']} ETH"
        # Send to multiple channels
        send_urgent_notification(message)

# Register handler
notification_system.add_event_handler('large_deposit', custom_notification_handler)
```

### Error Handling and Recovery
```python
from exceptions import APIError, NetworkError
from api_client import APIClient, APIConfig
import time

def robust_api_call(url: str, max_retries: int = 3) -> Dict:
    config = APIConfig(max_retries=max_retries, timeout=30.0)

    with APIClient(url, config=config) as client:
        try:
            return client.get('balance')
        except NetworkError as e:
            logger.error(f"Network error: {e}")
            # Implement fallback logic
            return get_cached_balance()
        except APIError as e:
            logger.error(f"API error: {e}")
            if e.status_code == 429:
                # Rate limited - wait and retry
                time.sleep(60)
                return robust_api_call(url, max_retries - 1)
            raise
```

---

This API reference provides comprehensive documentation for developers working with the Balina2Droid system. For more specific implementation details, refer to the inline code documentation and test files.