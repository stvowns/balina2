#!/usr/bin/env python3
"""
Data Processor - Handles data normalization and processing operations
"""

from typing import Dict, Any, Optional


class DataProcessor:
    """Handles data normalization and processing operations"""

    @staticmethod
    def safe_float(value, default=0.0) -> float:
        """Safely convert value to float (for dict fields that might be str/int/None)."""
        try:
            if value is None or value == "":
                return float(default)
            return float(value)
        except (TypeError, ValueError):
            return float(default)

    @staticmethod
    def normalize_margin_summary(margin_summary: Dict[str, Any]) -> Dict[str, float]:
        """Normalize numeric fields in marginSummary to floats to avoid type issues."""
        if not isinstance(margin_summary, dict):
            return {}

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
                normalized[key] = DataProcessor.safe_float(margin_summary.get(key), 0.0)

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

    @staticmethod
    def normalize_position_stats(stats: Dict[str, Any]) -> Dict[str, float]:
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

    @staticmethod
    def normalize_async_results(async_results: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize async wallet check results to ensure consistent data types"""
        if not isinstance(async_results, dict):
            return {}

        normalized = {}
        for wallet_id, wallet_results in async_results.items():
            if not isinstance(wallet_results, dict):
                print(f"⚠️ Warning: wallet_results is not a dict for {wallet_id}: {type(wallet_results)} - {wallet_results}")
                continue

            # Normalize numeric values
            normalized_wallet_results = {}
            for key, value in wallet_results.items():
                if key in ["old_balance", "new_balance", "balance_change"]:
                    normalized_wallet_results[key] = DataProcessor.safe_float(value, 0.0)
                elif key in ["balance_changed", "positions_changed", "success"]:
                    normalized_wallet_results[key] = bool(value)
                else:
                    normalized_wallet_results[key] = value

            normalized[wallet_id] = normalized_wallet_results

        return normalized

    @staticmethod
    def normalize_summary(summary: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize wallet summary data to ensure consistent types"""
        if not isinstance(summary, dict):
            return {}

        normalized = summary.copy()

        # Normalize eth_balance
        if "eth_balance" in normalized:
            normalized["eth_balance"] = DataProcessor.safe_float(normalized.get("eth_balance"), 0.0)

        # Normalize position_stats if present
        if "position_stats" in normalized:
            normalized["position_stats"] = DataProcessor.normalize_position_stats(normalized["position_stats"])

        # Normalize hyperliquid_positions marginSummary if present
        if "hyperliquid_positions" in normalized and isinstance(normalized["hyperliquid_positions"], dict):
            hl_positions = normalized["hyperliquid_positions"]
            if "marginSummary" in hl_positions:
                hl_positions["marginSummary"] = DataProcessor.normalize_margin_summary(hl_positions["marginSummary"])

        return normalized

    @staticmethod
    def process_wallet_results(wallet_results: Dict[str, Any]) -> Dict[str, Any]:
        """Process and validate wallet check results"""
        if not isinstance(wallet_results, dict):
            return {"error": "Invalid wallet results format", "success": False}

        processed = wallet_results.copy()

        # Ensure required fields exist
        if "wallet_id" not in processed:
            processed["wallet_id"] = "unknown"

        if "timestamp" not in processed:
            from datetime import datetime
            processed["timestamp"] = datetime.now().isoformat()

        # Normalize numeric fields
        numeric_fields = ["old_balance", "new_balance", "balance_change"]
        for field in numeric_fields:
            if field in processed:
                processed[field] = DataProcessor.safe_float(processed[field], 0.0)

        # Normalize boolean fields
        boolean_fields = ["balance_changed", "positions_changed", "success"]
        for field in boolean_fields:
            if field in processed:
                processed[field] = bool(processed[field])

        return processed