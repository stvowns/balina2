#!/usr/bin/env python3
"""
Test multi-wallet tracker functionality
"""

import unittest
from unittest.mock import patch, MagicMock
import os
from multi_wallet_tracker import MultiWalletTracker
from config import load_wallets_config, ConfigurationError

class TestMultiWalletConfig(unittest.TestCase):
    """Test multi-wallet configuration loading"""

    def test_load_wallets_from_json(self):
        """Test loading wallets from JSON configuration"""
        wallets_json = '''{
            "trading": {
                "address": "0x742d35Cc6634C0532925a3b8D4C9db96C4b4Db45",
                "name": "Trading Wallet",
                "enabled": true,
                "telegram_chat_id": "123456789"
            },
            "savings": {
                "address": "0x1234567890123456789012345678901234567890",
                "name": "Savings Wallet",
                "enabled": false
            }
        }'''

        with patch.dict(os.environ, {'WALLETS_JSON': wallets_json}):
            wallets = load_wallets_config()

            self.assertEqual(len(wallets), 2)
            self.assertEqual(wallets["trading"]["address"], "0x742d35Cc6634C0532925a3b8D4C9db96C4b4Db45")
            self.assertEqual(wallets["trading"]["name"], "Trading Wallet")
            self.assertTrue(wallets["trading"]["enabled"])
            self.assertEqual(wallets["trading"]["telegram_chat_id"], "123456789")

            self.assertEqual(wallets["savings"]["address"], "0x1234567890123456789012345678901234567890")
            self.assertEqual(wallets["savings"]["name"], "Savings Wallet")
            self.assertFalse(wallets["savings"]["enabled"])

    def test_load_wallets_from_env_vars(self):
        """Test loading wallets from individual environment variables"""
        with patch.dict(os.environ, {
            'WALLET_1_ADDRESS': '0x742d35Cc6634C0532925a3b8D4C9db96C4b4Db45',
            'WALLET_1_NAME': 'First Wallet',
            'WALLET_1_ENABLED': 'true',
            'WALLET_2_ADDRESS': '0x1234567890123456789012345678901234567890',
            'WALLET_2_NAME': 'Second Wallet',
            'WALLET_2_ENABLED': 'false'
        }):
            wallets = load_wallets_config()

            self.assertEqual(len(wallets), 2)
            self.assertEqual(wallets["wallet_1"]["address"], "0x742d35Cc6634C0532925a3b8D4C9db96C4b4Db45")
            self.assertEqual(wallets["wallet_1"]["name"], "First Wallet")
            self.assertTrue(wallets["wallet_1"]["enabled"])

            self.assertEqual(wallets["wallet_2"]["address"], "0x1234567890123456789012345678901234567890")
            self.assertEqual(wallets["wallet_2"]["name"], "Second Wallet")
            self.assertFalse(wallets["wallet_2"]["enabled"])

    def test_invalid_wallet_address_in_json(self):
        """Test validation of invalid wallet addresses in JSON"""
        wallets_json = '''{
            "invalid": {
                "address": "invalid_address",
                "name": "Invalid Wallet",
                "enabled": true
            }
        }'''

        with patch.dict(os.environ, {'WALLETS_JSON': wallets_json}):
            with self.assertRaises(ConfigurationError):
                load_wallets_config()

    def test_invalid_json_format(self):
        """Test handling of invalid JSON format"""
        with patch.dict(os.environ, {'WALLETS_JSON': 'invalid_json'}):
            with self.assertRaises(ConfigurationError):
                load_wallets_config()

class TestMultiWalletTracker(unittest.TestCase):
    """Test multi-wallet tracker functionality"""

    def setUp(self):
        """Set up test configuration"""
        self.test_config = {
            "wallets": {
                "wallet_1": {
                    "address": "0x742d35Cc6634C0532925a3b8D4C9db96C4b4Db45",
                    "name": "Test Wallet 1",
                    "enabled": True,
                    "telegram_chat_id": "123456789"
                },
                "wallet_2": {
                    "address": "0x1234567890123456789012345678901234567890",
                    "name": "Test Wallet 2",
                    "enabled": False
                }
            },
            "etherscan_api_key": "test_api_key",
            "notification_settings": {
                "console": {"enabled": True},
                "telegram": {"enabled": True, "bot_token": "test_token"},
                "email": {"enabled": False}
            },
            "check_interval": 600,
            "balance_change_threshold": 0.1
        }

    @patch('multi_wallet_tracker.WalletTracker')
    @patch('multi_wallet_tracker.NotificationSystem')
    def test_initialization(self, mock_notification, mock_tracker):
        """Test multi-wallet tracker initialization"""
        mock_tracker.return_value = MagicMock()
        mock_notification.return_value = MagicMock()

        tracker = MultiWalletTracker(self.test_config)

        # Should only initialize enabled wallets
        self.assertEqual(len(tracker.trackers), 1)
        self.assertEqual(len(tracker.notification_systems), 1)

        # Should create tracker for wallet_1 (enabled)
        mock_tracker.assert_called_once_with(
            "0x742d35Cc6634C0532925a3b8D4C9db96C4b4Db45",
            "test_api_key"
        )

        # Should not create tracker for wallet_2 (disabled)
        self.assertNotIn("wallet_2", tracker.trackers)

    def test_get_wallet_ids(self):
        """Test getting wallet IDs"""
        with patch('multi_wallet_tracker.WalletTracker'), \
             patch('multi_wallet_tracker.NotificationSystem'):
            tracker = MultiWalletTracker(self.test_config)
            wallet_ids = tracker.get_wallet_ids()

            self.assertEqual(len(wallet_ids), 1)
            self.assertEqual(wallet_ids[0], "wallet_1")

    def test_is_wallet_enabled(self):
        """Test checking if wallet is enabled"""
        with patch('multi_wallet_tracker.WalletTracker'), \
             patch('multi_wallet_tracker.NotificationSystem'):
            tracker = MultiWalletTracker(self.test_config)

            self.assertTrue(tracker.is_wallet_enabled("wallet_1"))
            self.assertFalse(tracker.is_wallet_enabled("wallet_2"))
            self.assertFalse(tracker.is_wallet_enabled("nonexistent"))

    def test_get_wallet_config(self):
        """Test getting wallet configuration"""
        with patch('multi_wallet_tracker.WalletTracker'), \
             patch('multi_wallet_tracker.NotificationSystem'):
            tracker = MultiWalletTracker(self.test_config)

            config = tracker.get_wallet_config("wallet_1")
            self.assertEqual(config["name"], "Test Wallet 1")
            self.assertEqual(config["address"], "0x742d35Cc6634C0532925a3b8D4C9db96C4b4Db45")

            config = tracker.get_wallet_config("nonexistent")
            self.assertIsNone(config)

if __name__ == '__main__':
    unittest.main()