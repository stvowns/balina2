"""
Position formatting utilities for consistent position display formatting
"""

from typing import Dict, Optional, Tuple
from constants import (
    POSITION_STATUS_EMOJIS, POSITION_SIDE_EMOJIS,
    PNL_EMOJIS, HIGHLIGHT_EMOJI, PERCENTAGE_MULTIPLIER
)


class PositionFormatter:
    """Handles position formatting operations with consistent logic"""

    @staticmethod
    def determine_position_emoji_and_status(pnl: float, size: float) -> Tuple[str, str]:
        """Determine position emoji and status based on PnL and side"""
        # Ensure pnl is numeric for comparison
        try:
            pnl_float = float(pnl) if pnl is not None else 0.0
        except (ValueError, TypeError):
            pnl_float = 0.0

        # Ensure size is numeric for comparison
        try:
            size_float = float(size) if size is not None else 0.0
        except (ValueError, TypeError):
            size_float = 0.0

        if pnl_float > 0:
            status = PNL_EMOJIS['profit']
        elif pnl_float < 0:
            status = PNL_EMOJIS['loss']
        else:
            status = PNL_EMOJIS['neutral']

        side_emoji = POSITION_SIDE_EMOJIS['long'] if size_float > 0 else POSITION_SIDE_EMOJIS['short']

        return side_emoji, status

    @staticmethod
    def calculate_position_metrics(position: Dict) -> Dict:
        """Calculate and format all position metrics"""
        size = float(position.get("szi") or 0)
        entry_price = float(position.get("entryPx") or 0)
        position_value = float(position.get("positionValue") or 0)
        pnl = float(position.get("unrealizedPnl") or 0)
        leverage = position.get("leverage", {}).get("value", 0)
        liquidation_price = float(position.get("liquidationPx") or 0)
        margin_used = float(position.get("marginUsed") or 0)

        # Calculate additional metrics
        side = "LONG" if size > 0 else "SHORT"
        size_abs = abs(size)
        current_price = abs(position_value / size) if size != 0 else 0
        roe = float(position.get("returnOnEquity") or 0) * PERCENTAGE_MULTIPLIER

        return {
            'side': side,
            'size_abs': size_abs,
            'entry_price': entry_price,
            'position_value': position_value,
            'pnl': pnl,
            'leverage': leverage,
            'liquidation_price': liquidation_price,
            'margin_used': margin_used,
            'current_price': current_price,
            'roe': roe
        }

    @staticmethod
    def format_funding_info(position: Dict) -> str:
        """Format funding information with emoji"""
        from constants import FUNDING_EMOJI

        funding = position.get("cumFunding", {})
        funding_since_open = float(funding.get("sinceOpen") or 0)
        funding_change = float(funding.get("sinceChange") or 0)

        return f"     {FUNDING_EMOJI} Funding: ${funding_since_open:+,.2f} (${funding_change:+,.2f} recent)\n\n"

    @staticmethod
    def format_position_summary(position: Dict, changed_coin: Optional[str] = None,
                              include_details: bool = True) -> str:
        """Format a single position summary with all details"""
        coin = position.get("coin", "Unknown")
        metrics = PositionFormatter.calculate_position_metrics(position)

        if metrics['size_abs'] == 0:
            return ""  # Skip closed positions

        # Determine emoji and status - ensure safe numeric comparison
        szi_value = position.get("szi", 0)
        try:
            szi_float = float(szi_value) if szi_value is not None else 0.0
        except (ValueError, TypeError):
            szi_float = 0.0

        side_emoji, status = PositionFormatter.determine_position_emoji_and_status(
            metrics['pnl'], metrics['size_abs'] if szi_float > 0 else -metrics['size_abs']
        )

        # Check if this is the changed position
        is_changed_position = (coin == changed_coin)
        highlight_marker = HIGHLIGHT_EMOJI if is_changed_position else "  "

        # Build position summary
        summary = f"{highlight_marker} {side_emoji} {coin} {metrics['side']}: {metrics['size_abs']:,.2f} @ ${metrics['entry_price']:,.2f} | {status}\n"

        if include_details:
            summary += f"    PnL: ${metrics['pnl']:,.2f} | Leverage: {metrics['leverage']}x\n"
            summary += f"    Position Value: ${metrics['position_value']:,.2f}\n"
            summary += f"    Liq Price: ${metrics['liquidation_price']:,.2f} | Margin Used: ${metrics['margin_used']:,.2f}\n\n"

        return summary

    @staticmethod
    def format_position_detailed(position: Dict, changed_coin: Optional[str] = None) -> str:
        """Format position with full details for summary views"""
        coin = position.get("coin", "Unknown")
        metrics = PositionFormatter.calculate_position_metrics(position)

        if metrics['size_abs'] == 0:
            return ""  # Skip closed positions

        # Check if this is the changed position
        is_changed_position = (coin == changed_coin)
        highlight_marker = HIGHLIGHT_EMOJI if is_changed_position else "  "

        # Determine emoji and status - ensure safe numeric comparison
        szi_value = position.get("szi", 0)
        try:
            szi_float = float(szi_value) if szi_value is not None else 0.0
        except (ValueError, TypeError):
            szi_float = 0.0

        side_emoji, status = PositionFormatter.determine_position_emoji_and_status(
            metrics['pnl'], metrics['size_abs'] if szi_float > 0 else -metrics['size_abs']
        )

        # Build detailed position summary
        summary = f"{highlight_marker} {side_emoji} {coin} {metrics['side']}: {metrics['size_abs']:,.2f} @ ${metrics['entry_price']:,.2f} | {status}\n"
        summary += f"     Current: ${metrics['current_price']:,.2f} | PnL: ${metrics['pnl']:,.2f} ({metrics['roe']:+.2f}%)\n"
        summary += f"     Value: ${metrics['position_value']:,.2f} | Lev: {metrics['leverage']}x | ROE: {metrics['roe']:+.1f}%\n"
        summary += f"     Liq Price: ${metrics['liquidation_price']:,.2f} | Margin: ${metrics['margin_used']:,.2f}\n"
        summary += PositionFormatter.format_funding_info(position)

        return summary

    @staticmethod
    def extract_positions_list(positions_data: Dict) -> list:
        """Extract and filter active positions from positions data"""
        asset_positions = positions_data.get("assetPositions", [])

        positions = []
        for pos_data in asset_positions:
            if "position" in pos_data and pos_data["position"]:
                position = pos_data["position"]
                size = float(position.get("szi") or 0)
                if size != 0:  # Only include active positions
                    positions.append(position)

        return positions