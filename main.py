#!/usr/bin/env python3
"""
Crypto Wallet Tracker
Monitors multiple Ethereum wallets and Hyperliquid positions for changes
"""

import time
from datetime import datetime
import schedule
from multi_wallet_tracker import MultiWalletTracker
from logger_config import (
    setup_logging, get_logger, log_startup, log_wallet_summary,
    log_wallet_action, log_error, log_notification
)
try:
    from config import load_config
    from utils import save_transaction_log
except ImportError:
    # Fallback if utils is not available
    from config import load_config
    def save_transaction_log(*args, **kwargs):
        pass

class CryptoWalletMonitor:
    def __init__(self):
        # Initialize logging
        setup_logging(level="INFO", log_file="wallet_tracker.log")
        self.logger = get_logger(__name__)

        self.config = load_config()
        self.multi_tracker = MultiWalletTracker(self.config)
        self.check_interval = self.config["check_interval"]

        wallet_count = len(self.multi_tracker.trackers)

        # Log startup information
        log_startup(wallet_count, self.check_interval)

        email_enabled = self.config['notification_settings']['email']['enabled']
        telegram_enabled = self.config['notification_settings']['telegram']['enabled']
        self.logger.info(f"📧 Email notifications: {'Enabled' if email_enabled else 'Disabled'}")
        self.logger.info(f"📱 Telegram notifications: {'Enabled' if telegram_enabled else 'Disabled'}")

        # List configured wallets
        for wallet_id, wallet_config in self.multi_tracker.wallets.items():
            if wallet_config.get("enabled", True):
                from utils import format_address
                formatted_address = format_address(wallet_config['address'])
                status = "active" if wallet_id in self.multi_tracker.trackers else "error"
                log_wallet_summary(wallet_config['name'], formatted_address, status)
        
    def check_wallet_changes(self):
        """Main check function for wallet changes"""
        try:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_wallet_action("Checking all wallets", f"at {current_time}")

            # Check all wallets
            results = self.multi_tracker.check_all_wallets()

            # Count total changes
            total_changes = sum(len(changes) for changes in results.values())

            # Only print completion message if there were no important changes
            if total_changes == 0:
                self.logger.info("✅ No important changes detected across all wallets")
            else:
                self.logger.info(f"✅ Check completed - {total_changes} notifications sent")

        except Exception as e:
            log_error("wallet check", e, "Multi-wallet tracker")
    
    def send_initial_summary(self):
        """Send initial wallet summary on startup"""
        try:
            self.multi_tracker.send_initial_summary()
            self.logger.info("✅ Initial summaries sent")
        except Exception as e:
            log_error("initial summary", e, "Multi-wallet tracker")
    
    def run_manual_check(self):
        """Run a one-time check and display full summary"""
        self.logger.info("🔍 Running manual multi-wallet check...")
        summaries = self.multi_tracker.get_all_wallets_summary()

        separator = "=" * 80
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.logger.info(f"\n{separator}")
        self.logger.info(f"📊 MULTI-WALLET SUMMARY - {current_time}")
        self.logger.info(f"{separator}")

        total_eth_balance = 0

        for wallet_id, summary in summaries.items():
            wallet_config = self.multi_tracker.get_wallet_config(wallet_id)
            self.logger.info(f"\n📱 Wallet: {wallet_config['name']}")
            self.logger.info(f"   Address: {summary['wallet_address']}")
            status = "✅ Active" if summary.get('enabled', True) else "❌ Disabled"
            self.logger.info(f"   Status: {status}")

            if 'error' in summary:
                self.logger.error(f"   Error: {summary['error']}")
                continue

            eth_balance = summary.get('eth_balance', 0)
            if eth_balance:
                self.logger.info(f"   ETH Balance: {eth_balance:.4f} ETH")
                total_eth_balance += eth_balance
            else:
                self.logger.info(f"   ETH Balance: N/A")

            # Hyperliquid positions summary
            if summary.get('hyperliquid_positions'):
                positions = summary['hyperliquid_positions']
                if 'marginSummary' in positions:
                    margin = positions['marginSummary']
                    account_value = float(margin.get('accountValue', 0))
                    position_value = float(margin.get('totalNotion', 0))
                    margin_usage = float(margin.get('marginUsage', 0)) * 100

                    self.logger.info(f"   Account Value: ${account_value:,.2f}")
                    self.logger.info(f"   Position Value: ${position_value:,.2f}")
                    self.logger.info(f"   Margin Usage: {margin_usage:.2f}%")

            # Recent transactions
            if summary.get('recent_transactions'):
                self.logger.info(f"   Recent Transactions: {len(summary['recent_transactions'])}")

        # Overall summary
        active_wallets = len([s for s in summaries.values() if s.get('enabled', True) and 'error' not in s])
        self.logger.info(f"\n{separator}")
        self.logger.info(f"💰 TOTAL ETH BALANCE: {total_eth_balance:.4f} ETH")
        self.logger.info(f"📱 ACTIVE WALLETS: {active_wallets}")
        self.logger.info(f"{separator}")
    
    def start_monitoring(self):
        """Start continuous monitoring"""
        self.send_initial_summary()

        # Schedule regular checks
        schedule.every(self.check_interval).seconds.do(self.check_wallet_changes)

        self.logger.info(f"🔄 Multi-wallet monitoring started. Checking every {self.check_interval} seconds.")
        self.logger.info("Press Ctrl+C to stop")

        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("\n👋 Multi-wallet monitoring stopped by user")

def main():
    monitor = CryptoWalletMonitor()

    # Check command line arguments
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        monitor.run_manual_check()
    elif len(sys.argv) > 1 and sys.argv[1] == "--list":
        # List configured wallets
        logger = get_logger(__name__)
        logger.info("\n📱 Configured Wallets:")
        logger.info(f"{'='*60}")

        # Display notification settings summary
        email_enabled = monitor.config['notification_settings']['email']['enabled']
        telegram_enabled = monitor.config['notification_settings']['telegram']['enabled']
        check_interval = monitor.config['check_interval']

        logger.info(f"📧 Email: {'✅ Enabled' if email_enabled else '❌ Disabled'}")
        logger.info(f"📱 Telegram: {'✅ Enabled' if telegram_enabled else '❌ Disabled'}")
        logger.info(f"⏰ Check Interval: {check_interval} seconds ({check_interval//60} minutes)")
        logger.info(f"{'='*60}")

        for wallet_id, wallet_config in monitor.multi_tracker.wallets.items():
            status = "✅ Active" if monitor.multi_tracker.is_wallet_enabled(wallet_id) else "❌ Disabled"
            from utils import format_address

            logger.info(f"  {status} {wallet_config['name']}")
            logger.info(f"      Address: {format_address(wallet_config['address'])}")
            logger.info(f"      System ID: {wallet_id} (internal identifier)")

            # Show custom notification settings
            custom_telegram = wallet_config.get("telegram_chat_id")
            custom_email = wallet_config.get("email_recipient")

            if custom_telegram or custom_email:
                logger.info(f"      📨 Custom Notifications:")
                if custom_telegram:
                    logger.info(f"        📱 Telegram Chat: {custom_telegram}")
                if custom_email:
                    logger.info(f"        📧 Email: {custom_email}")
            logger.info("")
    else:
        monitor.start_monitoring()

if __name__ == "__main__":
    main()
