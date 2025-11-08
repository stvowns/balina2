#!/usr/bin/env python3
"""
Async Performance Test Script
Tests the performance improvement of async vs sync wallet checking
"""

import time
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def load_config():
    """Load configuration for testing"""
    from config import load_secure_config
    return load_secure_config()

def test_sync_performance(config):
    """Test synchronous wallet checking performance"""
    print("🔄 Testing Synchronous Performance...")
    print("=" * 60)

    from multi_wallet_tracker import MultiWalletTracker

    # Create sync tracker
    sync_tracker = MultiWalletTracker(config, use_async=False)

    if not sync_tracker.trackers:
        print("❌ No wallets configured for testing")
        return None

    start_time = time.time()

    try:
        # Run sync checks
        results = sync_tracker.check_all_wallets()

        end_time = time.time()
        duration = end_time - start_time

        # Count results
        total_wallets = len(sync_tracker.trackers)
        total_changes = sum(len(changes) for changes in results.values())

        print(f"✅ Sync Performance Results:")
        print(f"   Wallets checked: {total_wallets}")
        print(f"   Changes found: {total_changes}")
        print(f"   Duration: {duration:.2f} seconds")
        print(f"   Average per wallet: {duration/total_wallets:.2f} seconds")

        return {
            "mode": "sync",
            "duration": duration,
            "wallets": total_wallets,
            "changes": total_changes,
            "avg_per_wallet": duration/total_wallets
        }

    except Exception as e:
        print(f"❌ Sync test failed: {e}")
        return None

def test_async_performance(config):
    """Test asynchronous wallet checking performance"""
    print("\n🚀 Testing Asynchronous Performance...")
    print("=" * 60)

    from multi_wallet_tracker import MultiWalletTracker

    # Create async tracker
    async_tracker = MultiWalletTracker(config, use_async=True)

    if not async_tracker.trackers:
        print("❌ No wallets configured for testing")
        return None

    start_time = time.time()

    try:
        # Run async checks
        results = async_tracker.check_all_wallets()

        end_time = time.time()
        duration = end_time - start_time

        # Count results
        total_wallets = len(async_tracker.trackers)
        total_changes = sum(len(changes) for changes in results.values())

        print(f"✅ Async Performance Results:")
        print(f"   Wallets checked: {total_wallets}")
        print(f"   Changes found: {total_changes}")
        print(f"   Duration: {duration:.2f} seconds")
        print(f"   Average per wallet: {duration/total_wallets:.2f} seconds")

        return {
            "mode": "async",
            "duration": duration,
            "wallets": total_wallets,
            "changes": total_changes,
            "avg_per_wallet": duration/total_wallets
        }

    except Exception as e:
        print(f"❌ Async test failed: {e}")
        return None

async def test_pure_async_performance(config):
    """Test pure async wallet checking performance (direct async calls)"""
    print("\n⚡ Testing Pure Asynchronous Performance...")
    print("=" * 60)

    from async_wallet_tracker import AsyncMultiWalletTracker

    # Create pure async tracker
    async_tracker = AsyncMultiWalletTracker(config)

    if not async_tracker.trackers:
        print("❌ No wallets configured for testing")
        return None

    start_time = time.time()

    try:
        # Run pure async checks
        results = await async_tracker.check_all_wallets_async()

        end_time = time.time()
        duration = end_time - start_time

        # Count results
        total_wallets = len(async_tracker.trackers)
        total_changes = sum(len(changes) for changes in results.values())

        print(f"✅ Pure Async Performance Results:")
        print(f"   Wallets checked: {total_wallets}")
        print(f"   Changes found: {total_changes}")
        print(f"   Duration: {duration:.2f} seconds")
        print(f"   Average per wallet: {duration/total_wallets:.2f} seconds")

        return {
            "mode": "pure_async",
            "duration": duration,
            "wallets": total_wallets,
            "changes": total_changes,
            "avg_per_wallet": duration/total_wallets
        }

    except Exception as e:
        print(f"❌ Pure async test failed: {e}")
        return None

def compare_results(sync_result, async_result, pure_async_result):
    """Compare performance results"""
    print("\n📊 Performance Comparison")
    print("=" * 60)

    if not sync_result or not async_result:
        print("❌ Cannot compare - one or more tests failed")
        return

    print(f"Sync duration: {sync_result['duration']:.2f}s")
    print(f"Async duration: {async_result['duration']:.2f}s")

    if pure_async_result:
        print(f"Pure Async duration: {pure_async_result['duration']:.2f}s")

    # Calculate improvements
    sync_improvement = ((sync_result['duration'] - async_result['duration']) / sync_result['duration']) * 100

    print(f"\n🚀 Hybrid Async Improvement:")
    print(f"   Time saved: {sync_result['duration'] - async_result['duration']:.2f}s")
    print(f"   Performance gain: {sync_improvement:.1f}%")
    print(f"   Speed factor: {sync_result['duration'] / async_result['duration']:.2f}x faster")

    if pure_async_result:
        pure_async_improvement = ((sync_result['duration'] - pure_async_result['duration']) / sync_result['duration']) * 100
        print(f"\n⚡ Pure Async Improvement:")
        print(f"   Time saved: {sync_result['duration'] - pure_async_result['duration']:.2f}s")
        print(f"   Performance gain: {pure_async_improvement:.1f}%")
        print(f"   Speed factor: {sync_result['duration'] / pure_async_result['duration']:.2f}x faster")

async def main():
    """Main test function"""
    print("🔬 Async Performance Test Suite")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    try:
        # Load configuration
        config = load_config()

        # Check if wallets are configured
        wallets = config.get("wallets", {})
        if not wallets:
            print("❌ No wallets found in configuration!")
            print("Please set up WALLETS_JSON or WALLET_* environment variables")
            return

        enabled_wallets = {k: v for k, v in wallets.items() if v.get("enabled", True)}
        print(f"📱 Found {len(enabled_wallets)} enabled wallets for testing")

        # Run tests
        sync_result = test_sync_performance(config)
        async_result = test_async_performance(config)

        # Run pure async test
        pure_async_result = None
        try:
            pure_async_result = await test_pure_async_performance(config)
        except Exception as e:
            print(f"⚠️  Pure async test skipped: {e}")

        # Compare results
        compare_results(sync_result, async_result, pure_async_result)

        # Summary
        print("\n🎯 Test Summary")
        print("=" * 60)

        if sync_result and async_result:
            print("✅ All tests completed successfully!")
            print(f"📈 Performance improvement achieved")
        else:
            print("❌ Some tests failed")

    except Exception as e:
        print(f"❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Starting async performance tests...")
    asyncio.run(main())