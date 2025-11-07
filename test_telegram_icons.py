#!/usr/bin/env python3
"""
Test script for updated Telegram notification icons
"""

from notification_system import NotificationSystem

def test_icon_changes():
    # Create test notification system
    config = {
        "wallet_name": "Test Wallet",
        "wallet_address": "0x1234567890abcdef1234567890abcdef12345678",
        "telegram": {"enabled": False},
        "email": {"enabled": False},
        "console": {"enabled": True}
    }

    notifier = NotificationSystem(config)

    # Create mock position data with different scenarios
    mock_positions = {
        "marginSummary": {
            "accountValue": 50000,
            "totalNotion": 30000,
            "unrealizedPnl": 1500,
            "marginUsage": 0.25
        },
        "assetPositions": [
            {
                "position": {
                    "coin": "INJ",
                    "szi": 10.5,  # LONG position
                    "entryPx": 13.06,
                    "positionValue": 14000,
                    "unrealizedPnl": 250,
                    "leverage": {"value": 3.5},
                    "liquidationPx": 8.5,
                    "marginUsed": 4000,
                    "returnOnEquity": 0.0625,
                    "cumFunding": {"sinceOpen": 15.2, "sinceChange": 2.1}
                }
            },
            {
                "position": {
                    "coin": "BTC",
                    "szi": -0.5,  # SHORT position
                    "entryPx": 65000,
                    "positionValue": -16000,
                    "unrealizedPnl": -500,  # Zararda
                    "leverage": {"value": 2.0},
                    "liquidationPx": 75000,
                    "marginUsed": 8000,
                    "returnOnEquity": -0.0625,
                    "cumFunding": {"sinceOpen": -10.5, "sinceChange": -1.2}
                }
            },
            {
                "position": {
                    "coin": "ETH",
                    "szi": 15.0,  # LONG position
                    "entryPx": 3200,
                    "positionValue": 4800,
                    "unrealizedPnl": 0,  # Nötr
                    "leverage": {"value": 4.0},
                    "liquidationPx": 2400,
                    "marginUsed": 1200,
                    "returnOnEquity": 0.0,
                    "cumFunding": {"sinceOpen": 0, "sinceChange": 0}
                }
            }
        ]
    }

    print("🧪 Testing Telegram notification icon changes...\n")
    print("="*60)

    # Test format_hyperliquid_summary
    print("📊 Testing HYPERLIQUID POSITION SUMMARY:")
    print("-"*40)
    summary = notifier.format_hyperliquid_summary(mock_positions)
    print(summary)

    print("\n" + "="*60)
    print("🔄 Testing POSITION CHANGE notification:")
    print("-"*40)

    # Test with specific changed coin
    mock_positions_with_change = mock_positions.copy()
    mock_positions_with_change["_changed_coin"] = "INJ"  # Sadece INJ pozisyonu değişti

    change_notification = notifier.format_position_change(mock_positions_with_change, "position_changed")
    print(change_notification)

    print("\n" + "="*60)
    print("✅ Icon changes test completed!")
    print("\nÖrnek çıktıdaki değişiklikler:")
    print("- 🟢 INJ LONG pozisyonu (yeşil yuvarlak)")
    print("- 🔴 BTC SHORT pozisyonu (kırmızı yuvarlak)")
    print("- 🟢 ETH LONG pozisyonu (yeşil yuvarlak)")
    print("- KARda ifadesi ⬆️KARDA⬆️, ZARARDA ifadesi ⬇️ZARARDA⬇️ şeklinde")
    print("- Position Changed bildiriminde sadece INJ'de 🔥 işareti var")

if __name__ == "__main__":
    test_icon_changes()