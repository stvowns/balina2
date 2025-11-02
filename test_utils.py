#!/usr/bin/env python3
"""
Test utilities for crypto wallet tracker
"""

import unittest
from datetime import datetime
from utils import format_wei_to_ether, format_address, format_timestamp, calculate_price_change

class TestUtils(unittest.TestCase):
    """Test utility functions"""

    def test_format_wei_to_ether(self):
        """Test Wei to Ether conversion"""
        self.assertEqual(format_wei_to_ether(1000000000000000000), 1.0)
        self.assertEqual(format_wei_to_ether(500000000000000000), 0.5)
        self.assertEqual(format_wei_to_ether(0), 0.0)

    def test_format_address_valid(self):
        """Test address formatting"""
        address = "0x742d35Cc6634C0532925a3b8D4C9db96C4b4Db45"
        result = format_address(address)
        # Check that it starts with first 6 chars and ends with last 4 chars
        self.assertTrue(result.startswith("0x742d"))
        self.assertTrue(result.endswith("b45"))
        self.assertTrue("..." in result)
        # Check that total length is much shorter than original
        self.assertLess(len(result), len(address))

    def test_format_address_short(self):
        """Test short address formatting"""
        short_address = "0x123"
        self.assertEqual(format_address(short_address), short_address)

    def test_format_timestamp_valid(self):
        """Test timestamp formatting"""
        timestamp = "2024-01-01T12:00:00Z"
        result = format_timestamp(timestamp)
        self.assertIn("2024-01-01", result)
        self.assertIn("12:00:00", result)

    def test_format_timestamp_invalid(self):
        """Test invalid timestamp formatting"""
        invalid_timestamp = "invalid_timestamp"
        self.assertEqual(format_timestamp(invalid_timestamp), invalid_timestamp)

    def test_calculate_price_change_normal(self):
        """Test normal price change calculation"""
        result = calculate_price_change(100, 150)
        self.assertEqual(result, 50.0)

    def test_calculate_price_change_decrease(self):
        """Test price decrease calculation"""
        result = calculate_price_change(200, 150)
        self.assertEqual(result, -25.0)

    def test_calculate_price_change_zero_old_price(self):
        """Test calculation with zero old price"""
        result = calculate_price_change(0, 100)
        self.assertEqual(result, 0)

if __name__ == '__main__':
    unittest.main()