#!/usr/bin/env python3
"""
Notification Gateway - Handles notification sending and formatting coordination
"""

from typing import Dict, List, Any
from notification_system import NotificationSystem
from utils import save_transaction_log, format_address
from datetime import datetime


class NotificationGateway:
    """Manages notification sending and formatting coordination"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.notification_systems = {}
        self.notification_settings = config.get("notification_settings", {})
        self.wallets = config.get("wallets", {})

    def create_notification_systems(self):
        """Create notification systems for all enabled wallets"""
        for wallet_id, wallet_config in self.wallets.items():
            if not wallet_config.get("enabled", True):
                continue

            try:
                # Create notification configuration for this wallet
                notification_config = self._create_notification_config(wallet_config)

                # Create notification system
                notification_system = NotificationSystem(notification_config)
                self.notification_systems[wallet_id] = notification_system

                print(f"✅ Initialized notifications for: {wallet_config['name']} ({format_address(wallet_config['address'])})")

            except Exception as e:
                print(f"❌ Failed to initialize notifications for wallet {wallet_id}: {e}")

    def _create_notification_config(self, wallet_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create notification configuration for a specific wallet"""
        notification_config = self.notification_settings.copy()
        notification_config["wallet_address"] = wallet_config["address"]
        notification_config["wallet_name"] = wallet_config["name"]

        # Override Telegram chat ID if specified for this wallet
        if wallet_config.get("telegram_chat_id"):
            if "telegram" in notification_config:
                notification_config["telegram"]["chat_id"] = wallet_config["telegram_chat_id"]
                notification_config["telegram"]["enabled"] = True

        # Override email recipient if specified for this wallet
        if wallet_config.get("email_recipient"):
            if "email" in notification_config:
                notification_config["email"]["recipient_email"] = wallet_config["email_recipient"]
                notification_config["email"]["enabled"] = True

        return notification_config

    def send_balance_change_notification(self, wallet_id: str, old_balance: float, new_balance: float, change: float) -> bool:
        """Send balance change notification"""
        if wallet_id not in self.notification_systems:
            return False

        notification_system = self.notification_systems[wallet_id]

        try:
            message = notification_system.format_balance_change(old_balance, new_balance, change)
            success = notification_system.send_notification(message, "BALANCE CHANGE")

            if success:
                save_transaction_log({
                    "wallet_id": wallet_id,
                    "type": "balance_change",
                    "old_balance": old_balance,
                    "new_balance": new_balance,
                    "change": change
                })

            return success
        except Exception as e:
            print(f"❌ Failed to send balance change notification for wallet {wallet_id}: {e}")
            return False

    def send_position_change_notification(self, wallet_id: str, positions: Dict, change_type: str) -> bool:
        """Send position change notification"""
        if wallet_id not in self.notification_systems:
            return False

        notification_system = self.notification_systems[wallet_id]

        try:
            changed_coin = positions.get("_changed_coin", "Unknown")
            print(f"\n🔥 POSITION DETECTED: {change_type.upper()} - {changed_coin}")
            print(f"💰 Wallet: {self.wallets[wallet_id]['name']} ({wallet_id})")
            print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            message = notification_system.format_position_change(positions, change_type)
            success = notification_system.send_notification(message, f"POSITION {change_type.upper()}")

            if success:
                save_transaction_log({
                    "wallet_id": wallet_id,
                    "type": "position_change",
                    "change_type": change_type,
                    "positions": positions
                })

            return success
        except Exception as e:
            print(f"❌ Failed to send position change notification for wallet {wallet_id}: {e}")
            return False

    def send_deposit_withdrawal_notification(self, wallet_id: str, transactions: List[Dict]) -> bool:
        """Send deposit/withdrawal notification"""
        if wallet_id not in self.notification_systems:
            return False

        notification_system = self.notification_systems[wallet_id]

        try:
            message = notification_system.format_deposit_withdrawal(transactions)
            success = notification_system.send_notification(message, "DEPOSIT/WITHDRAWAL")

            if success:
                save_transaction_log({
                    "wallet_id": wallet_id,
                    "type": "deposit_withdrawal",
                    "transactions": transactions
                })

            return success
        except Exception as e:
            print(f"❌ Failed to send deposit/withdrawal notification for wallet {wallet_id}: {e}")
            return False

    def send_initial_summary(self, wallet_id: str, summary: Dict, use_async: bool = False):
        """Send initial summary notification for a wallet"""
        if wallet_id not in self.notification_systems:
            return

        notification_system = self.notification_systems[wallet_id]
        wallet_config = self.wallets[wallet_id]

        try:
            # Build message
            wallet_name = wallet_config.get("name", f"Wallet {wallet_id}")
            wallet_addr = summary.get("wallet_address") or wallet_config.get("address", "")
            eth_balance_val = self._safe_float(summary.get("eth_balance"), 0.0)
            eth_balance_str = f"{eth_balance_val:.4f} ETH" if eth_balance_val > 0 else "N/A"

            message_lines = [
                "🚀 WALLET TRACKER STARTED",
                f"Wallet: {wallet_name} ({format_address(wallet_addr)})",
                f"ETH Balance: {eth_balance_str}",
                f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "",
                "🚀 Async monitoring active..." if use_async else "Monitoring active..."
            ]

            # Add Hyperliquid summary if available
            hl_positions = summary.get("hyperliquid_positions") or {}
            hl_stats = summary.get("position_stats") or {}

            if isinstance(hl_positions, dict) and hl_positions.get("marginSummary"):
                hl_summary = notification_system.format_hyperliquid_summary(
                    hl_positions,
                    hl_stats if hl_stats else None,
                )
                if hl_summary:
                    message_lines.append("")
                    message_lines.append(hl_summary)

            # Add recent transactions count
            recent_txs = summary.get("recent_transactions")
            if isinstance(recent_txs, list) and recent_txs:
                message_lines.append(f"Recent Transactions: {len(recent_txs)}")

            # Send message
            message = "\n".join(
                str(line)
                for line in message_lines
                if line is not None and str(line).strip() != ""
            )

            success = notification_system.send_notification(message, "TRACKER STARTED")
            if not success:
                print(f"❌ Failed to send tracker started notification for wallet {wallet_id}")

        except Exception as e:
            print(f"❌ Error sending initial summary for wallet {wallet_id}: {e}")

    def _safe_float(self, value, default=0.0) -> float:
        """Safely convert value to float"""
        try:
            if value is None or value == "":
                return float(default)
            return float(value)
        except (TypeError, ValueError):
            return float(default)

    def get_notification_system(self, wallet_id: str):
        """Get notification system for a specific wallet"""
        return self.notification_systems.get(wallet_id)