#!/usr/bin/env python3
"""
Async Wallet Tracker - High-performance concurrent wallet monitoring
"""

import asyncio
import aiohttp
import json
import time
import math
import random
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

# Import centralized constants
from common.constants import (
    # Ethereum constants
    WEI_TO_ETH_DIVISOR,

    # API URLs
    ETHERSCAN_API_URL,
    ETHERSCAN_API_URL_V1,
    ETHERSCAN_CHAIN_ID,
    HYPERLIQUID_API_URL,

    # Default values
    DEFAULT_LIMIT,
    DEFAULT_BALANCE_CHANGE_THRESHOLD,
    DEFAULT_POSITION_CHANGE_THRESHOLD,
    DEFAULT_CHECK_INTERVAL,
    DEFAULT_TIMEOUT_SECONDS,
    DEFAULT_RATE_LIMIT_ETHERSCAN,
    DEFAULT_RATE_LIMIT_HYPERLIQUID,
    MAX_CONCURRENT_REQUESTS,

    # Business rules
    SIGNIFICANT_BALANCE_CHANGE,
    POSITION_CHANGE_PERCENTAGE,

    # HTTP status codes
    HTTP_SUCCESS_CODE
)

# Custom exception hierarchy
class AsyncWalletTrackerError(Exception):
    """Base exception for async wallet tracker"""
    pass

class AsyncAPIError(AsyncWalletTrackerError):
    """API-related errors in async operations"""
    pass

class CircuitBreakerError(AsyncWalletTrackerError):
    """Circuit breaker specific errors"""
    pass

class SimpleThrottler:
    """Simple rate limiter for API calls"""

    def __init__(self, calls_per_second: int):
        self.calls_per_second = calls_per_second
        self.min_interval = 1.0 / calls_per_second
        self.last_call = 0.0

    async def __aenter__(self):
        """Context manager entry - throttle the call"""
        elapsed = time.time() - self.last_call
        if elapsed < self.min_interval:
            await asyncio.sleep(self.min_interval - elapsed)
        self.last_call = time.time()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        pass

class CircuitBreaker:
    """Circuit Breaker Pattern implementation for API resilience"""

    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60, expected_exception: type = Exception):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    async def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        if self.state == "OPEN":
            if self._should_attempt_reset():
                self.state = "HALF_OPEN"
            else:
                raise CircuitBreakerError(f"Circuit breaker is OPEN. Last failure: {self._get_time_since_last_failure():.2f}s ago")

        try:
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)

            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise e

    def _should_attempt_reset(self) -> bool:
        """Check if circuit breaker should attempt reset"""
        return time.time() - self.last_failure_time >= self.recovery_timeout

    def _get_time_since_last_failure(self) -> float:
        """Get time elapsed since last failure"""
        return time.time() - (self.last_failure_time or 0)

    def _on_success(self):
        """Handle successful function call"""
        self.failure_count = 0
        self.state = "CLOSED"

    def _on_failure(self):
        """Handle failed function call"""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"

    def get_state(self) -> str:
        """Get current circuit breaker state"""
        return self.state

class RetryWithExponentialBackoff:
    """Retry mechanism with exponential backoff and jitter"""

    def __init__(self,
                 max_retries: int = 3,
                 base_delay: float = 1.0,
                 max_delay: float = 60.0,
                 exponential_base: float = 2.0,
                 jitter: bool = True):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter

    async def execute(self, func, *args, **kwargs):
        """Execute function with retry logic"""
        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                if attempt > 0:
                    delay = self._calculate_delay(attempt)
                    print(f"🔄 Retry attempt {attempt}/{self.max_retries} after {delay:.2f}s delay...")
                    await asyncio.sleep(delay)

                if asyncio.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)

                if attempt > 0:
                    print(f"✅ Retry successful on attempt {attempt}")
                return result

            except Exception as e:
                last_exception = e
                if attempt < self.max_retries:
                    print(f"⚠️ Attempt {attempt + 1} failed: {type(e).__name__}: {str(e)}")
                else:
                    print(f"❌ All {self.max_retries + 1} attempts failed. Last error: {type(e).__name__}: {str(e)}")

        raise last_exception

    def _calculate_delay(self, attempt: int) -> float:
        """Calculate delay with exponential backoff and optional jitter"""
        delay = min(self.base_delay * (self.exponential_base ** (attempt - 1)), self.max_delay)

        if self.jitter:
            # Add jitter to prevent thundering herd
            jitter_amount = delay * 0.1
            delay += random.uniform(-jitter_amount, jitter_amount)

        return max(0, delay)  # Ensure non-negative

class AsyncWalletTracker:
    """High-performance async wallet tracker with concurrent processing"""

    def __init__(self, wallet_address: str, etherscan_api_key: str):
        self.wallet_address = wallet_address
        self.etherscan_api_key = etherscan_api_key
        self.base_url = ETHERSCAN_API_URL
        self.hyperliquid_url = HYPERLIQUID_API_URL
        self.last_known_balance = None
        self.last_known_positions = None

        # Initialize rate limiters
        self.etherscan_throttler = SimpleThrottler(DEFAULT_RATE_LIMIT_ETHERSCAN)
        self.hyperliquid_throttler = SimpleThrottler(DEFAULT_RATE_LIMIT_HYPERLIQUID)

        # Initialize circuit breakers and retry mechanisms
        self.etherscan_circuit_breaker = CircuitBreaker(
            failure_threshold=3,
            recovery_timeout=60,
            expected_exception=(aiohttp.ClientError, asyncio.TimeoutError)
        )

        self.hyperliquid_circuit_breaker = CircuitBreaker(
            failure_threshold=3,
            recovery_timeout=60,
            expected_exception=(aiohttp.ClientError, asyncio.TimeoutError)
        )

        self.etherscan_retry = RetryWithExponentialBackoff(
            max_retries=3,
            base_delay=1.0,
            max_delay=30.0
        )

        self.hyperliquid_retry = RetryWithExponentialBackoff(
            max_retries=2,
            base_delay=1.0,
            max_delay=20.0
        )

        self.session = None

    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=DEFAULT_TIMEOUT_SECONDS),
            connector=aiohttp.TCPConnector(limit=MAX_CONCURRENT_REQUESTS)
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()

    async def close(self):
        """Close the session"""
        if self.session:
            await self.session.close()
            self.session = None

    async def check_balance_change(self) -> Tuple[bool, float, float]:
        """Check if balance has changed significantly"""
        current_balance = await self.get_eth_balance_async()
        if current_balance is None:
            return False, 0, 0

        if self.last_known_balance is None:
            self.last_known_balance = current_balance
            return False, current_balance, 0

        change = abs(current_balance - self.last_known_balance)
        if change > SIGNIFICANT_BALANCE_CHANGE:  # Significant change threshold
            significant_change = True
        else:
            significant_change = False

        self.last_known_balance = current_balance
        return significant_change, current_balance, change

    async def check_position_changes(self) -> Tuple[bool, Dict, str]:
        """Check if positions have opened, closed, or significantly changed"""
        current_positions = await self.get_hyperliquid_positions_async()
        if current_positions is None:
            return False, {}, "position_data_unavailable"

        if self.last_known_positions is None:
            self.last_known_positions = current_positions
            # Check if there are any active positions on first run
            asset_positions = current_positions.get("assetPositions", [])
            has_active_positions = any(
                pos.get("position", {}).get("szi", 0) != 0
                for pos in asset_positions
            )
            return has_active_positions, current_positions, "position_summary"

        # For simplicity, just check if positions data has changed
        # In production, you'd want more sophisticated comparison logic
        positions_changed = current_positions != self.last_known_positions
        self.last_known_positions = current_positions

        if positions_changed:
            return True, current_positions, "position_changed"
        else:
            return False, current_positions, "no_change"

    async def check_deposit_withdrawal(self):
        """Placeholder for deposit/withdrawal checking"""
        # This would be implemented similar to the sync version
        return False, []

    async def get_eth_balance_async(self) -> Optional[float]:
        """Get current ETH balance with enhanced error handling"""
        async with self.etherscan_throttler:
            return await self._get_eth_balance_with_protection()

    async def _get_eth_balance_with_protection(self) -> Optional[float]:
        """Internal method with circuit breaker and retry protection"""
        async def fetch_balance():
            params = {
                "chainid": ETHERSCAN_CHAIN_ID,
                "module": "account",
                "action": "balance",
                "address": self.wallet_address,
                "tag": "latest",
                "apikey": self.etherscan_api_key
            }

            async with self.session.get(self.base_url, params=params) as response:
                response.raise_for_status()
                data = await response.json()

                if data["status"] == "1":
                    return float(data["result"]) / WEI_TO_ETH_DIVISOR
                else:
                    error_msg = data.get('message', 'Unknown error')
                    if "deprecated" in error_msg.lower():
                        print("⚠️ Etherscan API deprecated, attempting fallback...")
                        return await self._get_eth_balance_v1_fallback()
                    else:
                        raise AsyncAPIError(f"Etherscan API error: {error_msg}")

        # Apply retry and circuit breaker protection
        return await self.etherscan_circuit_breaker.call(
            self.etherscan_retry.execute,
            fetch_balance
        )

    async def _get_eth_balance_v1_fallback(self) -> Optional[float]:
        """Fallback to V1 API when V2 fails"""
        try:
            params = {
                "module": "account",
                "action": "balance",
                "address": self.wallet_address,
                "tag": "latest",
                "apikey": self.etherscan_api_key
            }

            async with self.session.get(ETHERSCAN_API_URL_V1, params=params) as response:
                response.raise_for_status()
                data = await response.json()

                if data["status"] == "1":
                    return float(data["result"]) / WEI_TO_ETH_DIVISOR
                else:
                    print(f"⚠️ V1 fallback also failed: {data.get('message', 'Unknown error')}")
                    return None
        except Exception as e:
            print(f"⚠️ V1 fallback error: {e}")
            return None

    async def get_hyperliquid_positions_async(self) -> Optional[Dict]:
        """Get Hyperliquid perpetual positions with enhanced error handling"""
        async with self.hyperliquid_throttler:
            return await self._get_hyperliquid_positions_with_protection()

    async def _get_hyperliquid_positions_with_protection(self) -> Optional[Dict]:
        """Internal method with circuit breaker and retry protection"""
        async def fetch_positions():
            payload = {
                "type": "clearinghouseState",
                "user": self.wallet_address
            }

            async with self.session.post(self.hyperliquid_url, json=payload) as response:
                response.raise_for_status()
                data = await response.json()

                if data and "marginSummary" in data:
                    return data
                else:
                    raise AsyncAPIError("Invalid response format from Hyperliquid API")

        # Apply retry and circuit breaker protection
        return await self.hyperliquid_circuit_breaker.call(
            self.hyperliquid_retry.execute,
            fetch_positions
        )

    async def get_summary(self) -> Dict:
        """Get comprehensive wallet summary"""
        balance = await self.get_eth_balance_async()
        positions = await self.get_hyperliquid_positions_async()

        return {
            "wallet_address": self.wallet_address,
            "eth_balance": balance if balance is not None else 0.0,
            "hyperliquid_positions": positions,
            "timestamp": datetime.now().isoformat()
        }

# Multi-wallet async tracker for concurrent processing
class AsyncMultiWalletTracker:
    """Multi-wallet tracker with concurrent processing capabilities"""

    def __init__(self, config: Dict):
        self.config = config
        self.wallet_configs = config.get("wallets", {})
        self.trackers = {}
        self.notification_systems = {}

        # Initialize async trackers for each wallet
        for wallet_id, wallet_config in self.wallet_configs.items():
            if wallet_config.get("enabled", True):
                self.trackers[wallet_id] = AsyncWalletTracker(
                    wallet_config["address"],
                    config.get("etherscan_api_key", "")
                )

    async def check_all_wallets_async(self) -> Dict[str, Dict]:
        """Check all wallets concurrently"""
        tasks = []
        wallet_ids = []

        # Create tasks for all enabled wallets
        for wallet_id, tracker in self.trackers.items():
            tasks.append(self._check_single_wallet_async(wallet_id, tracker))
            wallet_ids.append(wallet_id)

        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        wallet_results = {}
        for i, result in enumerate(results):
            wallet_id = wallet_ids[i]
            if isinstance(result, Exception):
                print(f"❌ Error checking wallet {wallet_id}: {result}")
                wallet_results[wallet_id] = {"error": str(result), "success": False}
            else:
                wallet_results[wallet_id] = {**result, "success": True}

        return wallet_results

    async def _check_single_wallet_async(self, wallet_id: str, tracker: AsyncWalletTracker) -> Dict:
        """Check a single wallet asynchronously"""
        async with tracker:
            balance_changed, new_balance, balance_change = await tracker.check_balance_change()
            positions_changed, new_positions, change_type = await tracker.check_position_changes()

            return {
                "wallet_id": wallet_id,
                "balance_changed": balance_changed,
                "new_balance": new_balance,
                "balance_change": balance_change,
                "positions_changed": positions_changed,
                "new_positions": new_positions,
                "position_change_type": change_type,
                "timestamp": datetime.now().isoformat()
            }

    async def get_all_summaries_async(self) -> Dict[str, Dict]:
        """Get summaries for all wallets concurrently"""
        tasks = []
        wallet_ids = []

        for wallet_id, tracker in self.trackers.items():
            tasks.append(self._get_wallet_summary_async(wallet_id, tracker))
            wallet_ids.append(wallet_id)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        wallet_summaries = {}
        for i, result in enumerate(results):
            wallet_id = wallet_ids[i]
            if isinstance(result, Exception):
                wallet_summaries[wallet_id] = {"error": str(result)}
            else:
                wallet_summaries[wallet_id] = result

        return wallet_summaries

    async def get_all_wallets_summary_async(self) -> Dict[str, Dict]:
        """Get summaries for all wallets concurrently - alias for get_all_summaries_async"""
        return await self.get_all_summaries_async()

    async def _get_wallet_summary_async(self, wallet_id: str, tracker: AsyncWalletTracker) -> Dict:
        """Get summary for a single wallet asynchronously"""
        async with tracker:
            summary = await tracker.get_summary()
            return {"wallet_id": wallet_id, **summary}

    async def close_all(self):
        """Close all tracker sessions"""
        for tracker in self.trackers.values():
            await tracker.close()

# Utility functions for standalone usage
async def run_wallet_checks(config: Dict) -> Dict[str, Dict]:
    """Run checks for all configured wallets"""
    tracker = AsyncMultiWalletTracker(config)
    try:
        return await tracker.check_all_wallets_async()
    finally:
        await tracker.close_all()

async def run_wallet_summary(config: Dict) -> Dict[str, Dict]:
    """Get summary for all configured wallets"""
    tracker = AsyncMultiWalletTracker(config)
    try:
        return await tracker.get_all_summaries_async()
    finally:
        await tracker.close_all()