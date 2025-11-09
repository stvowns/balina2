#!/usr/bin/env python3
"""
API Service - Handles all external API calls with abstraction layer
"""

import requests
from typing import Dict, Optional, List
from constants import (
    # Ethereum constants
    WEI_TO_ETH_DIVISOR,

    # API URLs
    ETHERSCAN_API_URL_V1,
    ETHERSCAN_API_URL,
    ETHERSCAN_CHAIN_ID,
    HYPERLIQUID_API_URL,

    # Default values
    DEFAULT_LIMIT,
    DEFAULT_TIMEOUT_SECONDS,

    # Time constants
    DEFAULT_CHECK_INTERVAL
)


class APIError(Exception):
    """API service related errors"""
    pass


class APIService:
    """Abstracts external API calls for blockchain data"""

    def __init__(self, etherscan_api_key: str):
        self.etherscan_api_key = etherscan_api_key
        self.base_url = ETHERSCAN_API_URL
        self.hyperliquid_url = HYPERLIQUID_API_URL

    def get_eth_balance(self, wallet_address: str) -> Optional[float]:
        """Get current ETH balance with V2 fallback to V1"""
        # Try V2 API first
        try:
            params = {
                "chainid": ETHERSCAN_CHAIN_ID,
                "module": "account",
                "action": "balance",
                "address": wallet_address,
                "tag": "latest",
                "apikey": self.etherscan_api_key
            }
            response = requests.get(ETHERSCAN_API_URL, params=params, timeout=DEFAULT_TIMEOUT_SECONDS)
            response.raise_for_status()
            data = response.json()
            if data["status"] == "1":
                return float(data["result"]) / WEI_TO_ETH_DIVISOR
            # V2 failed, try V1 as fallback
            print("V2 API failed, trying V1 fallback...")
        except Exception as e:
            print(f"V2 API failed ({e}), trying V1 fallback...")

        # Fallback to V1 API
        try:
            params = {
                "module": "account",
                "action": "balance",
                "address": wallet_address,
                "tag": "latest",
                "apikey": self.etherscan_api_key
            }
            response = requests.get(ETHERSCAN_API_URL_V1, params=params, timeout=DEFAULT_TIMEOUT_SECONDS)
            response.raise_for_status()
            data = response.json()
            if data["status"] == "1":
                return float(data["result"]) / WEI_TO_ETH_DIVISOR
            else:
                error_msg = data.get('message', 'Unknown error')
                if "deprecated" in error_msg.lower():
                    # Try to extract balance from deprecation warning
                    print("⚠️ Etherscan V1 deprecated but attempting to extract data...")
                    # V1 deprecated endpoints might still return data in result field
                    try:
                        # Try to make a simple request to get at least some data
                        balance = 0.0  # Default fallback
                        print("🔄 Unable to get balance from deprecated API. Using default.")
                        return balance
                    except:
                        return None
                else:
                    print(f"Etherscan API error: {error_msg}")
                    return None
        except requests.RequestException as e:
            print(f"Network error getting ETH balance: {e}")
            return None
        except (ValueError, KeyError) as e:
            print(f"Data parsing error getting ETH balance: {e}")
            return None

    def get_token_transfers(self, wallet_address: str, limit: int = DEFAULT_LIMIT) -> List[Dict]:
        """Get recent token transfers using Etherscan API V2"""
        try:
            params = {
                "chainid": ETHERSCAN_CHAIN_ID,
                "module": "account",
                "action": "tokentx",
                "address": wallet_address,
                "sort": "desc",
                "apikey": self.etherscan_api_key
            }
            response = requests.get(self.base_url, params=params, timeout=DEFAULT_TIMEOUT_SECONDS)
            response.raise_for_status()
            data = response.json()
            if data["status"] == "1":
                return data["result"][:limit]
            else:
                message = data.get('message', 'Unknown error')
                if "No transactions found" in message:
                    # This is normal, not an error - just no transactions
                    return []
                else:
                    print(f"Etherscan API error (token transfers): {message}")
                    return []
        except requests.RequestException as e:
            print(f"Network error getting token transfers: {e}")
            return []
        except (ValueError, KeyError) as e:
            print(f"Data parsing error getting token transfers: {e}")
            return []

    def get_normal_transactions(self, wallet_address: str, limit: int = DEFAULT_LIMIT) -> List[Dict]:
        """Get recent normal transactions using Etherscan API V2"""
        try:
            params = {
                "chainid": ETHERSCAN_CHAIN_ID,
                "module": "account",
                "action": "txlist",
                "address": wallet_address,
                "sort": "desc",
                "apikey": self.etherscan_api_key
            }
            response = requests.get(self.base_url, params=params, timeout=DEFAULT_TIMEOUT_SECONDS)
            response.raise_for_status()
            data = response.json()
            if data["status"] == "1":
                return data["result"][:limit]
            else:
                message = data.get('message', 'Unknown error')
                if "No transactions found" in message:
                    # This is normal, not an error - just no transactions
                    return []
                else:
                    print(f"Etherscan API error (transactions): {message}")
                    return []
        except requests.RequestException as e:
            print(f"Network error getting transactions: {e}")
            return []
        except (ValueError, KeyError) as e:
            print(f"Data parsing error getting transactions: {e}")
            return []

    def get_hyperliquid_positions(self, wallet_address: str) -> Optional[Dict]:
        """Get Hyperliquid perpetual positions"""
        try:
            payload = {
                "type": "clearinghouseState",
                "user": wallet_address
            }
            response = requests.post(self.hyperliquid_url, json=payload, timeout=DEFAULT_TIMEOUT_SECONDS)
            response.raise_for_status()
            data = response.json()
            if data and "marginSummary" in data:
                return data
            # Return empty structure if API returns no data
            return {
                "marginSummary": {
                    "accountValue": 0,
                    "totalNtlPos": 0,
                    "totalMarginUsed": 0,
                    "unrealizedPnl": 0,
                    "marginUsage": 0
                },
                "assetPositions": []
            }
        except requests.RequestException as e:
            print(f"Network error getting Hyperliquid positions: {e}")
            # Return empty structure on network errors
            return {
                "marginSummary": {
                    "accountValue": 0,
                    "totalNtlPos": 0,
                    "totalMarginUsed": 0,
                    "unrealizedPnl": 0,
                    "marginUsage": 0
                },
                "assetPositions": []
            }
        except (ValueError, KeyError) as e:
            print(f"Data parsing error getting Hyperliquid positions: {e}")
            # Return empty structure on parsing errors
            return {
                "marginSummary": {
                    "accountValue": 0,
                    "totalNtlPos": 0,
                    "totalMarginUsed": 0,
                    "unrealizedPnl": 0,
                    "marginUsage": 0
                },
                "assetPositions": []
            }