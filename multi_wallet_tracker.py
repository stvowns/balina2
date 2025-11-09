#!/usr/bin/env python3
"""
Multi-Wallet Tracker - Orchestrates multiple wallet trackers with single responsibility
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any
from wallet_tracker import WalletTracker, WalletTrackerError
from async_wallet_tracker import AsyncMultiWalletTracker, AsyncWalletTrackerError
from notification_gateway import NotificationGateway
from data_processor import DataProcessor
from utils import format_address

class MultiWalletTracker:
    """Orchestrates multiple wallet trackers with clear separation of concerns"""

    def __init__(self, config: Dict[str, Any], use_async: bool = True):
        self.config = config
        self.wallets = config.get("wallets", {})
        self.etherscan_api_key = config.get("etherscan_api_key", "")
        self.check_interval = config.get("check_interval", 600)
        self.balance_threshold = config.get("balance_change_threshold", 0.1)

        # Choose between sync and async implementation
        self.use_async = use_async

        # Initialize components with single responsibilities
        self.trackers = {}
        self.async_tracker = None
        self.notification_gateway = NotificationGateway(config)
        self.data_processor = DataProcessor()

        if self.use_async:
            print("🚀 Using Async Multi-Wallet Tracker for improved performance")
        else:
            print("🔄 Using Sync Multi-Wallet Tracker")

        self._initialize_wallets()

    def _initialize_wallets(self):
        """Initialize wallet trackers and setup notification gateway"""
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

                print(f"✅ Initialized wallet: {wallet_config['name']} ({format_address(wallet_config['address'])})")

            except Exception as e:
                print(f"❌ Failed to initialize wallet {wallet_id}: {e}")

        # Initialize notification gateway after all wallets are set up
        self.notification_gateway.create_notification_systems()

    def check_all_wallets(self) -> Dict[str, List[Dict]]:
        """Check all enabled wallets for changes (sync or async based on configuration)"""
        if self.use_async:
            return self._check_all_wallets_async()
        else:
            return self._check_all_wallets_sync()

    def _check_all_wallets_sync(self) -> Dict[str, List[Dict]]:
        """Check all enabled wallets for changes (synchronous implementation)"""
        results = {}

        for wallet_id, tracker in self.trackers.items():
            wallet_config = self.wallets[wallet_id]

            wallet_results = []

            try:
                print(f"\n🔍 Checking wallet: {wallet_config['name']} ({format_address(wallet_config['address'])}) at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

                # Check balance changes
                balance_changed, current_balance, change = tracker.check_balance_change()
                if balance_changed:
                    old_balance = tracker.last_known_balance - change
                    success = self.notification_gateway.send_balance_change_notification(wallet_id, old_balance, current_balance, change)
                    if not success:
                        print(f"❌ Failed to send balance change notification for wallet {wallet_id}")

                    wallet_results.append({
                        "type": "balance_change",
                        "wallet_id": wallet_id,
                        "wallet_name": wallet_config["name"],
                        "old_balance": old_balance,
                        "new_balance": current_balance,
                        "change": change
                    })

                # Check position changes
                positions_changed, positions, change_type = tracker.check_position_changes()
                if positions_changed:
                    success = self.notification_gateway.send_position_change_notification(wallet_id, positions, change_type)
                    if not success:
                        print(f"❌ Failed to send position change notification for wallet {wallet_id}")

                    changed_coin = positions.get("_changed_coin", "Unknown")
                    wallet_results.append({
                        "type": "position_change",
                        "wallet_id": wallet_id,
                        "wallet_name": wallet_config["name"],
                        "change_type": change_type,
                        "positions": positions,
                        "changed_coin": changed_coin
                    })

                # Check for deposit/withdrawal transactions
                has_deposit_withdrawal, deposit_txs = tracker.check_deposit_withdrawal()
                if has_deposit_withdrawal:
                    success = self.notification_gateway.send_deposit_withdrawal_notification(wallet_id, deposit_txs)
                    if not success:
                        print(f"❌ Failed to send deposit/withdrawal notification for wallet {wallet_id}")

                    wallet_results.append({
                        "type": "deposit_withdrawal",
                        "wallet_id": wallet_id,
                        "wallet_name": wallet_config["name"],
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

  
    def send_initial_summary(self):
        """
        Send initial summary notifications for all wallets (sync or async based on configuration).
        """
        print("📊 Generating initial multi-wallet summary...")

        if self.use_async:
            try:
                # Use asyncio.run() which handles event loop creation properly
                asyncio.run(self._send_initial_summary_async())
            except Exception as e:
                print(f"❌ Error in async initial summary, falling back to sync: {e}")
                self._send_initial_summary_sync()
        else:
            self._send_initial_summary_sync()

    def _send_initial_summary_sync(self):
        """Send initial summary notifications (synchronous implementation)"""
        for wallet_id, tracker in self.trackers.items():
            if not self.is_wallet_enabled(wallet_id):
                continue

            wallet_config = self.wallets[wallet_id]

            try:
                summary = tracker.get_summary()
                # Normalize summary data
                normalized_summary = self.data_processor.normalize_summary(summary)

                # Send notification through gateway
                self.notification_gateway.send_initial_summary(wallet_id, normalized_summary, use_async=False)

            except Exception as e:
                # Log and continue with other wallets instead of aborting all
                print(f"❌ Error sending initial summary for wallet {wallet_id}: {e}")

    async def _send_initial_summary_async(self):
        """Send initial summary notifications (asynchronous implementation)"""
        if not self.async_tracker:
            self.async_tracker = AsyncMultiWalletTracker(self.config)

        try:
            # Get async summaries for all wallets
            summaries = await self.async_tracker.get_all_summaries_async()

            for wallet_id, summary in summaries.items():
                if not self.is_wallet_enabled(wallet_id) or "error" in summary:
                    continue

                try:
                    # Normalize summary data
                    normalized_summary = self.data_processor.normalize_summary(summary)

                    # Send notification through gateway
                    self.notification_gateway.send_initial_summary(wallet_id, normalized_summary, use_async=True)

                except Exception as e:
                    # Log and continue with other wallets instead of aborting all
                    print(f"❌ Error sending async initial summary for wallet {wallet_id}: {e}")

        except Exception as e:
            print(f"❌ Error in async initial summary: {e}")

    def __del__(self):
        """Cleanup when object is destroyed"""
        if self.async_tracker:
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # Schedule cleanup in the background
                    asyncio.create_task(self.async_tracker.close_all())
                else:
                    # Run cleanup immediately
                    loop.run_until_complete(self.async_tracker.close_all())
            except Exception:
                pass  # Ignore cleanup errors

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

    def _check_all_wallets_async(self) -> Dict[str, List[Dict]]:
        """Check all enabled wallets for changes (asynchronous implementation)"""
        try:
            # Use asyncio.run() which handles event loop creation properly
            return asyncio.run(self._run_async_checks())
        except Exception as e:
            print(f"❌ Error in async wallet checks: {e}")
            # Fallback to sync mode
            print("🔄 Falling back to synchronous mode")
            return self._check_all_wallets_sync()

    async def _run_async_checks(self) -> Dict[str, List[Dict]]:
        """Run async wallet checks and handle notifications"""
        if not self.async_tracker:
            self.async_tracker = AsyncMultiWalletTracker(self.config)

        try:
            # Get async results
            async_results = await self.async_tracker.check_all_wallets_async()

            # Normalize async results to ensure consistent data types
            normalized_results = self.data_processor.normalize_async_results(async_results)

            # Process notifications for each wallet through gateway
            for wallet_id, wallet_results in normalized_results.items():
                # Check for balance change
                if wallet_results.get("balance_changed", False):
                    success = self.notification_gateway.send_balance_change_notification(
                        wallet_id,
                        wallet_results.get("old_balance", 0),
                        wallet_results.get("new_balance", 0),
                        wallet_results.get("balance_change", 0)
                    )
                    if not success:
                        print(f"❌ Failed to send async balance change notification for wallet {wallet_id}")

                # Check for position change
                if wallet_results.get("positions_changed", False):
                    positions = wallet_results.get("new_positions", {})
                    change_type = wallet_results.get("position_change_type", "position_changed")

                    success = self.notification_gateway.send_position_change_notification(wallet_id, positions, change_type)
                    if not success:
                        print(f"❌ Failed to send async position change notification for wallet {wallet_id}")

            return async_results

        except AsyncWalletTrackerError as e:
            print(f"❌ Async wallet tracker error: {e}")
            # Fallback to sync mode
            return self._check_all_wallets_sync()
        except Exception as e:
            print(f"❌ Unexpected error in async checks: {e}")
            import traceback
            print(f"🔍 Full traceback: {traceback.format_exc()}")
            return {}

    async def get_all_wallets_summary_async(self) -> Dict[str, Dict]:
        """Get comprehensive summary of all wallets asynchronously"""
        if not self.async_tracker:
            self.async_tracker = AsyncMultiWalletTracker(self.config)

        try:
            return await self.async_tracker.get_all_summaries_async()
        except Exception as e:
            print(f"❌ Error getting async summary: {e}")
            # Fallback to sync mode
            return self.get_all_wallets_summary()

    def get_all_wallets_summary(self) -> Dict[str, Dict]:
        """Get comprehensive summary of all wallets (sync or async based on configuration)"""
        if self.use_async:
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # If already in async context, create new loop
                    import concurrent.futures
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(asyncio.run, self.get_all_wallets_summary_async())
                        return future.result()
                else:
                    return asyncio.run(self.get_all_wallets_summary_async())
            except Exception as e:
                print(f"❌ Error in async summary, falling back to sync: {e}")
                return self._get_all_wallets_summary_sync()
        else:
            return self._get_all_wallets_summary_sync()

    def _get_all_wallets_summary_sync(self) -> Dict[str, Dict]:
        """Get comprehensive summary of all wallets (synchronous implementation)"""
        summary = {}

        for wallet_id, tracker in self.trackers.items():
            wallet_config = self.wallets[wallet_id]

            try:
                wallet_summary = tracker.get_summary()
                # Normalize summary data through data processor
                normalized_summary = self.data_processor.normalize_summary(wallet_summary)
                normalized_summary["wallet_id"] = wallet_id
                normalized_summary["wallet_name"] = wallet_config["name"]
                normalized_summary["enabled"] = wallet_config.get("enabled", True)
                summary[wallet_id] = normalized_summary

            except Exception as e:
                summary[wallet_id] = {
                    "wallet_id": wallet_id,
                    "wallet_name": wallet_config["name"],
                    "enabled": wallet_config.get("enabled", True),
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }

        return summary