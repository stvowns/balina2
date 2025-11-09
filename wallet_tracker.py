import json
from datetime import datetime
import time
from typing import Dict, List, Optional, Tuple

# Import centralized constants
from constants import (
    # Business rules
    SIGNIFICANT_BALANCE_CHANGE,
    POSITION_CHANGE_PERCENTAGE,
    DEFAULT_CHECK_INTERVAL
)

# Import API service for external calls
from api_service import APIService, APIError

class WalletTrackerError(Exception):
    """Wallet tracker related errors"""
    pass

class APIError(WalletTrackerError):
    """API related errors"""
    pass

class WalletTracker:
    def __init__(self, wallet_address: str, etherscan_api_key: str):
        self.wallet_address = wallet_address
        self.etherscan_api_key = etherscan_api_key
        self.last_known_balance = None
        self.last_known_positions = None
        # Initialize API service
        self.api_service = APIService(etherscan_api_key)
        
    def get_eth_balance(self) -> Optional[float]:
        """Get current ETH balance using API service"""
        return self.api_service.get_eth_balance(self.wallet_address)
    
    def get_token_transfers(self, limit: int = 100) -> List[Dict]:
        """Get recent token transfers using API service"""
        return self.api_service.get_token_transfers(self.wallet_address, limit)
    
    def get_normal_transactions(self, limit: int = 100) -> List[Dict]:
        """Get recent normal transactions using API service"""
        return self.api_service.get_normal_transactions(self.wallet_address, limit)
    
    def check_deposit_withdrawal(self) -> Tuple[bool, List[Dict]]:
        """Check for new deposit or withdrawal transactions (ETH and tokens)"""
        try:
            # Get recent transactions and token transfers
            recent_eth_txs = self.get_normal_transactions(5)
            recent_token_txs = self.get_token_transfers(10)

            all_transfers = []
            current_time = int(time.time())

            # Check ETH transfers
            for tx in recent_eth_txs:
                # Check if it's a simple ETH transfer (not contract interaction)
                if (tx.get("to") == self.wallet_address.lower() or
                    tx.get("from") == self.wallet_address.lower()) and \
                   tx.get("isError", "0") == "0" and \
                   float(tx.get("value", 0)) > 0:  # Has ETH value

                    tx_time = int(tx.get("timeStamp", 0))

                    # Check if transaction is within last check interval
                    if current_time - tx_time <= DEFAULT_CHECK_INTERVAL:
                        tx["asset"] = "ETH"
                        all_transfers.append(tx)

            # Check token transfers (including BTC and other ERC-20 tokens)
            for tx in recent_token_txs:
                tx_time = int(tx.get("timeStamp", 0))

                # Check if transaction is within last check interval
                if current_time - tx_time <= DEFAULT_CHECK_INTERVAL:
                    tx["asset"] = tx.get("tokenSymbol", "Unknown")
                    all_transfers.append(tx)

            if all_transfers:
                return True, all_transfers
            return False, []

        except (ValueError, TypeError, KeyError) as e:
            print(f"Error checking deposits/withdrawals: {e}")
            return False, []
    
    def get_hyperliquid_positions(self) -> Optional[Dict]:
        """Get Hyperliquid perpetual positions using API service"""
        return self.api_service.get_hyperliquid_positions(self.wallet_address)
    
    def check_balance_change(self) -> Tuple[bool, float, float]:
        """Check if balance has changed significantly"""
        current_balance = self.get_eth_balance()
        if current_balance is None:
            return False, 0, 0

        if self.last_known_balance is None:
            self.last_known_balance = current_balance
            return False, current_balance, 0

        change = abs(current_balance - self.last_known_balance)
        if change > SIGNIFICANT_BALANCE_CHANGE:  # Significant change threshold
            significant_change = True
        else:
            significant_change = False

        self.last_known_balance = current_balance
        return significant_change, current_balance, change
    
    def check_position_changes(self) -> Tuple[bool, Dict, str]:
        """Check if positions have opened, closed, or significantly changed"""
        current_positions = self.get_hyperliquid_positions()
        if current_positions is None:
            return False, {}, "position_data_unavailable"

        if self.last_known_positions is None:
            self.last_known_positions = current_positions
            # Check if there are any active positions on first run
            asset_positions = current_positions.get("assetPositions", [])
            has_active_positions = any(
                pos.get("position", {}).get("szi", 0) != 0
                for pos in asset_positions
            )
            return has_active_positions, current_positions, "position_summary"

        # Extract current and previous positions
        current_asset_positions = current_positions.get("assetPositions", [])
        previous_asset_positions = self.last_known_positions.get("assetPositions", [])

        # Create dictionaries of positions by coin for easier comparison
        current_pos_dict = {}
        previous_pos_dict = {}

        for pos in current_asset_positions:
            if "position" in pos and pos["position"]:
                coin = pos["position"].get("coin", "")
                size = float(pos["position"].get("szi", 0))
                current_pos_dict[coin] = size

        for pos in previous_asset_positions:
            if "position" in pos and pos["position"]:
                coin = pos["position"].get("coin", "")
                size = float(pos["position"].get("szi", 0))
                previous_pos_dict[coin] = size

        # Check for position changes
        changes_detected = False
        change_type = "none"
        changed_coin = None

        # Check for new positions opened
        for coin, size in current_pos_dict.items():
            if size != 0:
                if coin not in previous_pos_dict or previous_pos_dict[coin] == 0:
                    changes_detected = True
                    change_type = "position_opened"
                    changed_coin = coin
                    break
                # Check for significant size change (more than 5% change)
                elif abs(size - previous_pos_dict[coin]) / abs(previous_pos_dict[coin]) > POSITION_CHANGE_PERCENTAGE:
                    changes_detected = True
                    change_type = "position_changed"
                    changed_coin = coin
                    break

        # Check for positions closed
        if not changes_detected:
            for coin, size in previous_pos_dict.items():
                if size != 0 and (coin not in current_pos_dict or current_pos_dict[coin] == 0):
                    changes_detected = True
                    change_type = "position_closed"
                    changed_coin = coin
                    break

        self.last_known_positions = current_positions

        # Add changed coin to positions data for notification formatting
        if changes_detected and changed_coin:
            current_positions["_changed_coin"] = changed_coin

        return changes_detected, current_positions, change_type
    
    def get_summary(self) -> Dict:
        """Get comprehensive wallet summary"""
        balance = self.get_eth_balance()
        positions = self.get_hyperliquid_positions()
        recent_txs = self.get_normal_transactions(5)
        token_txs = self.get_token_transfers(5)

        # Calculate additional statistics
        stats = self.calculate_position_stats(positions) if positions else {}

        return {
            "wallet_address": self.wallet_address,
            "eth_balance": balance if balance is not None else 0.0,
            "hyperliquid_positions": positions,
            "position_stats": stats,
            "recent_transactions": recent_txs,
            "token_transfers": token_txs,
            "timestamp": datetime.now().isoformat()
        }
    
    def calculate_position_stats(self, positions: Dict) -> Dict:
        """Calculate detailed position statistics"""
        try:
            margin_summary = positions.get("marginSummary", {})
            asset_positions = positions.get("assetPositions", [])

            account_value = float(margin_summary.get("accountValue") or 0)
            total_ntl_pos = float(margin_summary.get("totalNtlPos") or 0)
            margin_used = float(margin_summary.get("totalMarginUsed") or 0)

            # Calculate PnL
            total_unrealized_pnl = 0
            long_value = 0
            short_value = 0
            position_count = 0
            winning_positions = 0

            for pos_data in asset_positions:
                if "position" in pos_data and pos_data["position"]:
                    position = pos_data["position"]
                    pnl = float(position.get("unrealizedPnl") or 0)
                    position_value = float(position.get("positionValue") or 0)
                    size = float(position.get("szi") or 0)

                    if size != 0:  # Active position
                        position_count += 1
                        total_unrealized_pnl += pnl

                        if size > 0:  # Long position
                            long_value += position_value
                        else:  # Short position
                            short_value += abs(position_value)

                        if pnl > 0:
                            winning_positions += 1

            # Calculate win rate
            win_rate = (winning_positions / position_count * 100) if position_count > 0 else 0

            # Calculate ROE (Return on Equity)
            roe = (total_unrealized_pnl / account_value * 100) if account_value > 0 else 0

            return {
                "account_value": account_value,
                "total_position_value": total_ntl_pos,
                "long_value": long_value,
                "short_value": short_value,
                "total_unrealized_pnl": total_unrealized_pnl,
                "position_count": position_count,
                "winning_positions": winning_positions,
                "win_rate": win_rate,
                "roe_percentage": roe,
                "leverage": total_ntl_pos / account_value if account_value > 0 else 0,
                "long_percentage": (long_value / total_ntl_pos * 100) if total_ntl_pos > 0 else 0,
                "short_percentage": (short_value / total_ntl_pos * 100) if total_ntl_pos > 0 else 0
            }
        except (ValueError, TypeError, KeyError, ZeroDivisionError) as e:
            print(f"Error calculating position stats: {e}")
            return {}
