#!/usr/bin/env python3
"""
Test configuration for crypto wallet tracker
"""

import os
import unittest
from unittest.mock import patch
from config import validate_ethereum_address, ConfigurationError, load_secure_config

class TestConfig(unittest.TestCase):
    """Test configuration validation"""

    def setUp(self):
        """Set up test environment"""
        self.test_address = "0x742d35Cc6634C0532925a3b8D4C9db96C4b4Db45"

    def test_validate_ethereum_address_valid(self):
        """Test valid Ethereum address validation"""
        self.assertTrue(validate_ethereum_address(self.test_address))

    def test_validate_ethereum_address_invalid_length(self):
        """Test invalid Ethereum address - wrong length"""
        invalid_address = "0x742d35Cc6634C0532925a3b8D4C9db96C4b4Db4"
        self.assertFalse(validate_ethereum_address(invalid_address))

    def test_validate_ethereum_address_invalid_prefix(self):
        """Test invalid Ethereum address - wrong prefix"""
        invalid_address = "1x742d35Cc6634C0532925a3b8D4C9db96C4b4Db45"
        self.assertFalse(validate_ethereum_address(invalid_address))

    def test_validate_ethereum_address_invalid_chars(self):
        """Test invalid Ethereum address - invalid characters"""
        invalid_address = "0x742d35Cc6634C0532925a3b8D4C9db96C4b4DbG5"
        self.assertFalse(validate_ethereum_address(invalid_address))

    def test_validate_ethereum_address_empty(self):
        """Test empty address"""
        self.assertFalse(validate_ethereum_address(""))
        self.assertFalse(validate_ethereum_address(None))

    @patch.dict(os.environ, {
        'WALLET_ADDRESS': '0x742d35Cc6634C0532925a3b8D4C9db96C4b4Db45',
        'ETHERSCAN_API_KEY': 'test_api_key',
        'TELEGRAM_BOT_TOKEN': 'test_bot_token',
        'TELEGRAM_CHAT_ID': '123456789'
    })
    def test_load_secure_config_success(self):
        """Test successful configuration loading"""
        config = load_secure_config()
        self.assertIn('wallets', config)
        self.assertIn('default', config['wallets'])
        self.assertEqual(config['wallets']['default']['address'], '0x742d35Cc6634C0532925a3b8D4C9db96C4b4Db45')
        self.assertEqual(config['wallets']['default']['name'], 'Default Wallet')
        self.assertTrue(config['wallets']['default']['enabled'])
        self.assertTrue(config['telegram']['enabled'])

    @patch.dict(os.environ, {}, clear=True)
    def test_load_secure_config_missing_wallet(self):
        """Test configuration loading with missing wallet address"""
        with self.assertRaises(ConfigurationError):
            load_secure_config()

    @patch.dict(os.environ, {
        'WALLET_ADDRESS': 'invalid_address',
        'ETHERSCAN_API_KEY': 'test_api_key'
    })
    def test_load_secure_config_invalid_address(self):
        """Test configuration loading with invalid address"""
        with self.assertRaises(ConfigurationError):
            load_secure_config()

if __name__ == '__main__':
    unittest.main()