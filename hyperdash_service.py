#!/usr/bin/env python3
"""
HyperDash Service - Fetch trading statistics from HyperLiquid dashboard
"""

import asyncio
from typing import Dict, Optional
from playwright.async_api import async_playwright
from constants import DEFAULT_TIMEOUT_SECONDS


class HyperDashService:
    """Service for fetching trading statistics from HyperLiquid dashboard"""

    def __init__(self):
        self.timeout = DEFAULT_TIMEOUT_SECONDS

    async def get_trader_stats_async(self, wallet_address: str) -> Optional[Dict]:
        """
        Fetch trading statistics from HyperLiquid dashboard for given wallet address

        Returns:
            Dict with win_rate, total_positions, winning_positions, leverage, account_value
        """
        try:
            async with async_playwright() as p:
                # Launch browser
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()

                # Navigate to trader page
                url = f"https://hyperdash.info/trader/{wallet_address}"
                await page.goto(url, timeout=self.timeout * 1000)

                # Wait for content to load
                await page.wait_for_timeout(3000)  # 3 seconds

                # Extract data using JavaScript
                data = await page.evaluate("""
                    () => {
                        const result = {};

                        // Win Rate ve Position Count
                        const positionsElements = Array.from(document.querySelectorAll('*')).filter(el =>
                            el.textContent.includes(' win') && el.textContent.includes('Positions')
                        );
                        if (positionsElements.length > 0) {
                            const positionsText = positionsElements[0].textContent;
                            const positionsMatch = positionsText.match(/(\\d+)\\s*\\((\\d+) win\\)/);
                            if (positionsMatch) {
                                result.total_positions = parseInt(positionsMatch[1]);
                                result.winning_positions = parseInt(positionsMatch[2]);
                                result.win_rate = (result.winning_positions / result.total_positions * 100).toFixed(1);
                            }
                        }

                        // Leverage - Tüm 2.x, 3x, 5x, 15x değerlerini ara
                        const leverageElements = Array.from(document.querySelectorAll('*')).filter(el => {
                            const text = el.textContent;
                            return /\\d+\\.?\\d*x/.test(text) &&
                                   el.textContent.includes('x') &&
                                   (el.parentElement?.textContent.includes('Leverage') ||
                                    el.closest('td')?.textContent.includes('x'));
                        });

                        if (leverageElements.length > 0) {
                            // Ortalama leverage hesapla
                            const leverageValues = [];
                            leverageElements.forEach(el => {
                                const leverageMatch = el.textContent.match(/(\\d+\\.?\\d*)x/);
                                if (leverageMatch) {
                                    leverageValues.push(parseFloat(leverageMatch[1]));
                                }
                            });

                            if (leverageValues.length > 0) {
                                // En yüksek leverage'i kullan (ana pozisyon için)
                                result.leverage = Math.max(...leverageValues);
                            }
                        }

                        // Account Value
                        const totalValueElements = Array.from(document.querySelectorAll('h3')).filter(el =>
                            el.textContent.includes('Total Value')
                        );
                        if (totalValueElements.length > 0) {
                            const valueContainer = totalValueElements[0].parentElement;
                            const valueText = valueContainer.textContent;
                            const valueMatch = valueText.match(/Total Value[\\s\\S]*?\\$([\\d,]+(?:\\.\\d+)?)/);
                            result.account_value = valueMatch ? valueMatch[1] : null;
                        }

                        return result;
                    }
                """)

                await browser.close()
                return data if data.get('total_positions') else None

        except Exception as e:
            print(f"Error fetching HyperLiquid dashboard data: {e}")
            return None

    def get_trader_stats(self, wallet_address: str) -> Optional[Dict]:
        """Synchronous wrapper for async dashboard fetching"""
        try:
            return asyncio.run(self.get_trader_stats_async(wallet_address))
        except Exception as e:
            print(f"Error in HyperLiquid dashboard service: {e}")
            return None


# Test function
if __name__ == "__main__":
    service = HyperDashService()
    test_wallet = "0x9eec98d048d06d9cd75318fffa3f3960e081daab"
    stats = service.get_trader_stats(test_wallet)
    print("Dashboard stats:", stats)