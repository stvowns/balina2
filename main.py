#!/usr/bin/env python3
"""
Crypto Wallet Tracker
Monitors multiple Ethereum wallets and Hyperliquid positions for changes
"""

import time
from datetime import datetime
import schedule
from multi_wallet_tracker import MultiWalletTracker
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
        self.config = load_config()
        self.multi_tracker = MultiWalletTracker(self.config)
        self.check_interval = self.config["check_interval"]

        wallet_count = len(self.multi_tracker.trackers)
        print(f"🚀 Starting multi-wallet tracker for {wallet_count} wallet(s)")
        print(f"⏰ Check interval: {self.check_interval} seconds")
        print(f"📧 Email notifications: {'Enabled' if self.config['notification_settings']['email']['enabled'] else 'Disabled'}")
        print(f"📱 Telegram notifications: {'Enabled' if self.config['notification_settings']['telegram']['enabled'] else 'Disabled'}")

        # List configured wallets
        for wallet_id, wallet_config in self.multi_tracker.wallets.items():
            if wallet_config.get("enabled", True):
                from utils import format_address
                status = "✅ Active" if wallet_id in self.multi_tracker.trackers else "❌ Error"
                print(f"  {status} {wallet_config['name']} ({format_address(wallet_config['address'])})")
        
    def check_wallet_changes(self):
        """Main check function for wallet changes"""
        try:
            print(f"\n🔍 Checking all wallets at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            # Check all wallets
            results = self.multi_tracker.check_all_wallets()

            # Count total changes
            total_changes = sum(len(changes) for changes in results.values())

            # Only print completion message if there were no important changes
            if total_changes == 0:
                print("✅ No important changes detected across all wallets")
            else:
                print(f"✅ Check completed - {total_changes} notifications sent")

        except Exception as e:
            print(f"❌ Error during wallet check: {e}")
    
    def send_initial_summary(self):
        """Send initial wallet summary on startup"""
        try:
            self.multi_tracker.send_initial_summary()
            print("✅ Initial summaries sent")
        except Exception as e:
            print(f"❌ Error sending initial summary: {e}")
    
    def run_manual_check(self):
        """Run a one-time check and display full summary"""
        print("🔍 Running manual multi-wallet check...")
        summaries = self.multi_tracker.get_all_wallets_summary()

        print(f"\n{'='*80}")
        print(f"📊 MULTI-WALLET SUMMARY - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")

        total_eth_balance = 0

        for wallet_id, summary in summaries.items():
            wallet_config = self.multi_tracker.get_wallet_config(wallet_id)
            print(f"\n📱 Wallet: {wallet_config['name']}")
            print(f"   Address: {summary['wallet_address']}")
            print(f"   Status: {'✅ Active' if summary.get('enabled', True) else '❌ Disabled'}")

            if 'error' in summary:
                print(f"   Error: {summary['error']}")
                continue

            eth_balance = summary.get('eth_balance', 0)
            if eth_balance:
                print(f"   ETH Balance: {eth_balance:.4f} ETH")
                total_eth_balance += eth_balance
            else:
                print(f"   ETH Balance: N/A")

            # Hyperliquid positions summary
            if summary.get('hyperliquid_positions'):
                positions = summary['hyperliquid_positions']
                if 'marginSummary' in positions:
                    margin = positions['marginSummary']
                    print(f"   Account Value: ${float(margin.get('accountValue', 0)):,.2f}")
                    print(f"   Position Value: ${float(margin.get('totalNotion', 0)):,.2f}")
                    print(f"   Margin Usage: {float(margin.get('marginUsage', 0))*100:.2f}%")

            # Recent transactions
            if summary.get('recent_transactions'):
                print(f"   Recent Transactions: {len(summary['recent_transactions'])}")

        # Overall summary
        print(f"\n{'='*80}")
        print(f"💰 TOTAL ETH BALANCE: {total_eth_balance:.4f} ETH")
        print(f"📱 ACTIVE WALLETS: {len([s for s in summaries.values() if s.get('enabled', True) and 'error' not in s])}")
        print(f"{'='*80}")
    
    def start_monitoring(self):
        """Start continuous monitoring"""
        self.send_initial_summary()

        # Schedule regular checks
        schedule.every(self.check_interval).seconds.do(self.check_wallet_changes)

        print(f"🔄 Multi-wallet monitoring started. Checking every {self.check_interval} seconds.")
        print("Press Ctrl+C to stop")

        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Multi-wallet monitoring stopped by user")

def main():
    monitor = CryptoWalletMonitor()

    # Check command line arguments
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        monitor.run_manual_check()
    elif len(sys.argv) > 1 and sys.argv[1] == "--list":
        # List configured wallets
        print("\n📱 Configured Wallets:")
        print(f"{'='*60}")
        for wallet_id, wallet_config in monitor.multi_tracker.wallets.items():
            status = "✅ Active" if monitor.multi_tracker.is_wallet_enabled(wallet_id) else "❌ Disabled"
            from utils import format_address
            print(f"  {status} {wallet_config['name']}")
            print(f"      Address: {format_address(wallet_config['address'])}")
            print(f"      ID: {wallet_id}")
            if wallet_config.get("telegram_chat_id"):
                print(f"      Telegram Chat: {wallet_config['telegram_chat_id']}")
            if wallet_config.get("email_recipient"):
                print(f"      Email: {wallet_config['email_recipient']}")
            print()
    else:
        monitor.start_monitoring()

if __name__ == "__main__":
    main()
