#!/usr/bin/env python3
"""
Multi-Wallet Tracker - Manages multiple wallet trackers
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from wallet_tracker import WalletTracker, WalletTrackerError
from notification_system import NotificationSystem, NotificationError
from utils import save_transaction_log, format_address

class MultiWalletTracker:
    """Manages multiple wallet trackers and their notifications"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.wallets = config.get("wallets", {})
        self.etherscan_api_key = config.get("etherscan_api_key", "")
        self.notification_settings = config.get("notification_settings", {})
        self.check_interval = config.get("check_interval", 600)
        self.balance_threshold = config.get("balance_change_threshold", 0.1)

        # Initialize trackers and notification systems for each wallet
        self.trackers = {}
        self.notification_systems = {}

        self._initialize_wallets()

    def _initialize_wallets(self):
        """Initialize wallet trackers and notification systems"""
        for wallet_id, wallet_config in self.wallets.items():
            if not wallet_config.get("enabled", True):
                continue

            try:
                # Create tracker for this wallet
                tracker = WalletTracker(
                    wallet_config["address"],
                    self.etherscan_api_key
                )
                self.trackers[wallet_id] = tracker

                # Create notification system for this wallet
                notification_config = self._create_notification_config(wallet_config)
                notification_system = NotificationSystem(notification_config)
                self.notification_systems[wallet_id] = notification_system

                print(f"✅ Initialized wallet: {wallet_config['name']} ({format_address(wallet_config['address'])})")

            except Exception as e:
                print(f"❌ Failed to initialize wallet {wallet_id}: {e}")

    def _create_notification_config(self, wallet_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create notification configuration for a specific wallet"""
        notification_config = self.notification_settings.copy()
        notification_config["wallet_address"] = wallet_config["address"]
        notification_config["wallet_name"] = wallet_config["name"]  # Add wallet name

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

    def check_all_wallets(self) -> Dict[str, List[Dict]]:
        """Check all enabled wallets for changes"""
        results = {}

        for wallet_id, tracker in self.trackers.items():
            wallet_config = self.wallets[wallet_id]
            notification_system = self.notification_systems[wallet_id]

            wallet_results = []

            try:
                print(f"\n🔍 Checking wallet: {wallet_config['name']} ({format_address(wallet_config['address'])}) at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

                # Check balance changes
                balance_changed, current_balance, change = tracker.check_balance_change()
                if balance_changed:
                    message = notification_system.format_balance_change(
                        tracker.last_known_balance - change,
                        current_balance,
                        change
                    )
                    success = notification_system.send_notification(message, "BALANCE CHANGE")
                    if not success:
                        print(f"❌ Failed to send balance change notification for wallet {wallet_id}")

                    wallet_results.append({
                        "type": "balance_change",
                        "wallet_id": wallet_id,
                        "wallet_name": wallet_config["name"],
                        "old_balance": tracker.last_known_balance - change,
                        "new_balance": current_balance,
                        "change": change
                    })

                    save_transaction_log({
                        "wallet_id": wallet_id,
                        "type": "balance_change",
                        "old_balance": tracker.last_known_balance - change,
                        "new_balance": current_balance,
                        "change": change
                    })

                # Check position changes
                positions_changed, positions, change_type = tracker.check_position_changes()
                if positions_changed:
                    changed_coin = positions.get("_changed_coin", "Unknown")
                    print(f"\n🔥 POSITION DETECTED: {change_type.upper()} - {changed_coin}")
                    print(f"💰 Wallet: {wallet_config['name']} ({wallet_id})")
                    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

                    message = notification_system.format_position_change(positions, change_type)
                    success = notification_system.send_notification(message, f"POSITION {change_type.upper()}")
                    if not success:
                        print(f"❌ Failed to send position change notification for wallet {wallet_id}")

                    wallet_results.append({
                        "type": "position_change",
                        "wallet_id": wallet_id,
                        "wallet_name": wallet_config["name"],
                        "change_type": change_type,
                        "positions": positions,
                        "changed_coin": changed_coin
                    })

                    save_transaction_log({
                        "wallet_id": wallet_id,
                        "type": "position_change",
                        "change_type": change_type,
                        "positions": positions
                    })

                # Check for deposit/withdrawal transactions
                has_deposit_withdrawal, deposit_txs = tracker.check_deposit_withdrawal()
                if has_deposit_withdrawal:
                    message = notification_system.format_deposit_withdrawal(deposit_txs)
                    success = notification_system.send_notification(message, "DEPOSIT/WITHDRAWAL")
                    if not success:
                        print(f"❌ Failed to send deposit/withdrawal notification for wallet {wallet_id}")

                    wallet_results.append({
                        "type": "deposit_withdrawal",
                        "wallet_id": wallet_id,
                        "wallet_name": wallet_config["name"],
                        "transactions": deposit_txs
                    })

                    save_transaction_log({
                        "wallet_id": wallet_id,
                        "type": "deposit_withdrawal",
                        "transactions": deposit_txs
                    })

                # Only print completion message if there were no important changes
                if not wallet_results:
                    print("✅ No important changes detected")
                else:
                    print(f"✅ Found {len(wallet_results)} changes")

                results[wallet_id] = wallet_results

            except Exception as e:
                print(f"❌ Error checking wallet {wallet_id}: {e}")
                wallet_results.append({
                    "type": "error",
                    "wallet_id": wallet_id,
                    "wallet_name": wallet_config["name"],
                    "error": str(e)
                })
                results[wallet_id] = wallet_results

        return results

    def get_all_wallets_summary(self) -> Dict[str, Dict]:
        """Get comprehensive summary of all wallets"""
        summary = {}

        for wallet_id, tracker in self.trackers.items():
            wallet_config = self.wallets[wallet_id]

            try:
                wallet_summary = tracker.get_summary()
                wallet_summary["wallet_id"] = wallet_id
                wallet_summary["wallet_name"] = wallet_config["name"]
                wallet_summary["enabled"] = wallet_config.get("enabled", True)
                summary[wallet_id] = wallet_summary

            except Exception as e:
                summary[wallet_id] = {
                    "wallet_id": wallet_id,
                    "wallet_name": wallet_config["name"],
                    "enabled": wallet_config.get("enabled", True),
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }

        return summary

    def _safe_float(self, value, default=0.0) -> float:
        """Safely convert value to float (for dict fields that might be str/int/None)."""
        try:
            if value is None or value == "":
                return float(default)
            return float(value)
        except (TypeError, ValueError):
            return float(default)

    def _normalize_margin_summary(self, margin_summary: Dict[str, Any]) -> Dict[str, float]:
        """Normalize numeric fields in marginSummary to floats to avoid type issues."""
        normalized = {}
        # Common keys returned by Hyperliquid
        keys = [
            "accountValue",
            "totalNtlPos",
            "totalNotional",
            "totalMarginUsed",
            "unrealizedPnl",
            "marginUsage",
        ]
        for key in keys:
            if key in margin_summary:
                normalized[key] = self._safe_float(margin_summary.get(key), 0.0)
        # Keep other fields as-is
        for key, val in margin_summary.items():
            if key not in normalized:
                # If looks numeric, normalize as well; otherwise keep raw
                if isinstance(val, (int, float)):
                    normalized[key] = float(val)
                else:
                    try:
                        normalized[key] = float(val)
                    except (TypeError, ValueError):
                        normalized[key] = val
        return normalized

    def _normalize_position_stats(self, stats: Dict[str, Any]) -> Dict[str, float]:
        """Normalize numeric fields in stats to floats to avoid '>' between str and int."""
        if not isinstance(stats, dict):
            return {}
        normalized = {}
        for k, v in stats.items():
            if isinstance(v, (int, float)):
                normalized[k] = float(v)
            else:
                try:
                    normalized[k] = float(v)
                except (TypeError, ValueError):
                    # Non-numeric values become 0.0 for safe comparisons
                    normalized[k] = 0.0
        return normalized

    def send_initial_summary(self):
        """
        Send initial summary notifications for all wallets.

        Fixes:
        - Avoid '>' not supported between instances of 'str' and 'int' by normalizing numeric fields.
        - Guard against missing/partial Hyperliquid data.
        - Ensure one walletın hatası tüm süreci bozmasın.
        """
        print("📊 Generating initial multi-wallet summary...")

        for wallet_id, tracker in self.trackers.items():
            if not self.is_wallet_enabled(wallet_id):
                continue

            notification_system = self.notification_systems[wallet_id]
            wallet_config = self.wallets[wallet_id]

            try:
                summary = tracker.get_summary()

                # Basic safe fields
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
                    "Monitoring active..."
                ]

                # Hyperliquid positions (defensive numeric normalization)
                hl_positions = summary.get("hyperliquid_positions") or {}
                hl_stats_raw = summary.get("position_stats") or {}

                if isinstance(hl_positions, dict) and hl_positions.get("marginSummary"):
                    margin_summary = hl_positions.get("marginSummary") or {}
                    hl_positions["marginSummary"] = self._normalize_margin_summary(margin_summary)
                    hl_stats = self._normalize_position_stats(hl_stats_raw)

                    # Build formatted HL summary
                    hl_summary = notification_system.format_hyperliquid_summary(
                        hl_positions,
                        hl_stats if hl_stats else None,
                    )
                    if hl_summary:
                        message_lines.append("")
                        message_lines.append(hl_summary)

                # Add recent tx count (optional, safe)
                recent_txs = summary.get("recent_transactions")
                if isinstance(recent_txs, list) and recent_txs:
                    message_lines.append(f"Recent Transactions: {len(recent_txs)}")

                # Final message (ensure all lines are strings)
                message = "\n".join(
                    str(line)
                    for line in message_lines
                    if line is not None and str(line).strip() != ""
                )

                success = notification_system.send_notification(message, "TRACKER STARTED")
                if not success:
                    print(f"❌ Failed to send tracker started notification for wallet {wallet_id}")

            except Exception as e:
                # Log and continue with other wallets instead of aborting all
                print(f"❌ Error sending initial summary for wallet {wallet_id}: {e}")

    def get_wallet_ids(self) -> List[str]:
        """Get list of all wallet IDs"""
        return list(self.trackers.keys())

    def get_wallet_config(self, wallet_id: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific wallet"""
        return self.wallets.get(wallet_id)

    def is_wallet_enabled(self, wallet_id: str) -> bool:
        """Check if a wallet is enabled"""
        wallet_config = self.wallets.get(wallet_id)
        return wallet_config.get("enabled", True) if wallet_config else False