#!/usr/bin/env python3
"""
Test runner for crypto wallet tracker
"""

import unittest
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_all_tests():
    """Run all test suites"""
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern='test_*.py')

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return success status
    return result.wasSuccessful()

def run_multi_wallet_tests():
    """Run only multi-wallet related tests"""
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))

    # Load specific test modules
    suite = unittest.TestSuite()

    try:
        # Add multi-wallet tests
        suite.addTest(loader.loadTestsFromName('test_multi_wallet'))
        suite.addTest(loader.loadTestsFromName('test_config'))

        # Run tests
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)

        return result.wasSuccessful()
    except Exception as e:
        print(f"Error running multi-wallet tests: {e}")
        return False

if __name__ == '__main__':
    import sys

    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--multi":
        print("🧪 Running Multi-Wallet Tests")
        print("=" * 50)

        success = run_multi_wallet_tests()

        if success:
            print("\n✅ All multi-wallet tests passed!")
            sys.exit(0)
        else:
            print("\n❌ Some multi-wallet tests failed!")
            sys.exit(1)
    else:
        print("🧪 Running All Crypto Wallet Tracker Tests")
        print("=" * 50)

        success = run_all_tests()

        if success:
            print("\n✅ All tests passed!")
            sys.exit(0)
        else:
            print("\n❌ Some tests failed!")
            sys.exit(1)