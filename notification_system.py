import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, Optional, List
from utils import format_address
from constants import (
    # Formatting constants
    ADDRESS_TRUNCATE_LENGTH,
    TRANSACTION_HASH_TRUNCATE_LENGTH,
    DEFAULT_TOKEN_DECIMALS,
    DEFAULT_NUMERIC_VALUE,
    DEFAULT_STRING_VALUE,
    PERCENTAGE_MULTIPLIER,

    # Position status mappings
    POSITION_STATUS_EMOJIS,
    POSITION_SIDE_EMOJIS,
    PNL_EMOJIS,
    DIRECTION_EMOJIS,
    FUNDING_EMOJI,
    HIGHLIGHT_EMOJI,

    # Display formatting
    CONSOLE_LINE_LENGTH,
    COLOR_CODES,

    # HTTP status codes
    HTTP_SUCCESS_CODE,

    # Ethereum constants
    WEI_TO_ETH_DIVISOR,

    # Timeouts and limits
    TELEGRAM_MESSAGE_MAX_LENGTH,
    DEFAULT_TIMEOUT_SECONDS
)
from position_formatter import PositionFormatter

class NotificationError(Exception):
    """Notification system related errors"""
    pass

class NotificationSystem:
    def __init__(self, config: Dict):
        self.email_config = config.get("email", {})
        self.telegram_config = config.get("telegram", {})
        self.console_enabled = config.get("console", {}).get("enabled", True)
        self.wallet_address = config.get("wallet_address", "")
        self.wallet_name = config.get("wallet_name", "Unknown Wallet")

        # Emoji configuration for Telegram compatibility
        self.emoji_style = config.get("emoji_style", "modern")  # "modern" or "classic"

    def get_pnl_emoji(self, pnl: float) -> str:
        """Get PnL emoji based on configured style"""
        if pnl > 0:
            return PNL_EMOJIS['profit']
        elif pnl < 0:
            return PNL_EMOJIS['loss']
        else:
            return PNL_EMOJIS['neutral']
    
    def send_notification(self, message: str, title: str = "Wallet Update") -> bool:
        """Send notification through all enabled channels"""
        success = True
        
        # Send to console
        if self.console_enabled:
            self._send_to_console(message, title)
        
        # Send email
        if self.email_config.get("enabled", False):
            email_success = self._send_email(message, title)
            success = success and email_success
        
        # Send Telegram
        if self.telegram_config.get("enabled", False):
            telegram_success = self._send_telegram(message)
            success = success and telegram_success
        
        return success
    
    def _send_to_console(self, message: str, title: str):
        """Print notification to console with enhanced formatting"""
        # Use centralized color codes
        colors = COLOR_CODES
        
        print(f"\n{colors['cyan']}{'='*CONSOLE_LINE_LENGTH}{colors['end']}")
        print(f"{colors['bold']}{colors['yellow']}🔔 {title} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{colors['end']}")
        print(f"{colors['cyan']}{'='*CONSOLE_LINE_LENGTH}{colors['end']}")
        
        # Format message with colors for better readability
        formatted_lines = []
        for line in message.split('\n'):
            if line.strip():
                # Color coding based on content
                if '📊' in line or 'POSITION SUMMARY' in line:
                    formatted_lines.append(f"{colors['bold']}{colors['blue']}{line}{colors['end']}")
                elif '📈' in line or 'POSITION BREAKDOWN' in line:
                    formatted_lines.append(f"{colors['bold']}{colors['cyan']}{line}{colors['end']}")
                elif '🔍' in line or 'ACTIVE POSITIONS' in line:
                    formatted_lines.append(f"{colors['bold']}{colors['magenta']}{line}{colors['end']}")
                elif '✅' in line:
                    formatted_lines.append(f"{colors['green']}{line}{colors['end']}")
                elif '❌' in line:
                    formatted_lines.append(f"{colors['red']}{line}{colors['end']}")
                elif '💰' in line or 'DEPOSIT' in line or 'WITHDRAWAL' in line:
                    formatted_lines.append(f"{colors['bold']}{colors['yellow']}{line}{colors['end']}")
                elif '🚀' in line or 'POSITION OPENED' in line:
                    formatted_lines.append(f"{colors['bold']}{colors['green']}{line}{colors['end']}")
                elif '✅' in line or 'POSITION CLOSED' in line:
                    formatted_lines.append(f"{colors['bold']}{colors['blue']}{line}{colors['end']}")
                elif '🔄' in line or 'POSITION CHANGED' in line:
                    formatted_lines.append(f"{colors['bold']}{colors['yellow']}{line}{colors['end']}")
                elif '🔥' in line:  # Highlighted changed position
                    formatted_lines.append(f"{colors['bold']}{colors['red']}{line}{colors['end']}")
                elif '$' in line and ('PnL:' in line or 'Value:' in line):
                    # Highlight monetary values
                    formatted_lines.append(f"{colors['green']}{line}{colors['end']}")
                elif line.startswith('•'):
                    formatted_lines.append(f"  {colors['white']}{line}{colors['end']}")
                elif line.startswith('   '):
                    formatted_lines.append(f"    {colors['cyan']}{line}{colors['end']}")
                else:
                    formatted_lines.append(line)
            else:
                formatted_lines.append(line)
        
        print('\n'.join(formatted_lines))
        print(f"{colors['cyan']}{'='*CONSOLE_LINE_LENGTH}{colors['end']}\n")
    
    def _send_email(self, message: str, title: str) -> bool:
        """Send email notification"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_config["sender_email"]
            msg['To'] = self.email_config["recipient_email"]
            msg['Subject'] = title

            msg.attach(MIMEText(message, 'plain'))

            server = smtplib.SMTP(self.email_config["smtp_server"], self.email_config["smtp_port"])
            server.starttls()
            server.login(self.email_config["sender_email"], self.email_config["sender_password"])
            text = msg.as_string()
            server.sendmail(self.email_config["sender_email"], self.email_config["recipient_email"], text)
            server.quit()

            print("Email notification sent successfully")
            return True
        except smtplib.SMTPAuthenticationError as e:
            print(f"Email authentication failed: {e}")
            return False
        except smtplib.SMTPConnectError as e:
            print(f"Email server connection failed: {e}")
            return False
        except smtplib.SMTPException as e:
            print(f"Email sending failed: {e}")
            return False
        except KeyError as e:
            print(f"Email configuration missing: {e}")
            return False
    
    def _send_telegram(self, message: str) -> bool:
        """Send Telegram notification"""
        try:
            url = f"https://api.telegram.org/bot{self.telegram_config['bot_token']}/sendMessage"
            payload = {
                "chat_id": self.telegram_config["chat_id"],
                "text": message,
                "parse_mode": "HTML"
            }
            response = requests.post(url, json=payload, timeout=DEFAULT_TIMEOUT_SECONDS)
            if response.status_code == HTTP_SUCCESS_CODE:
                print("Telegram notification sent successfully")
                return True
            else:
                print(f"Telegram API error: {response.text}")
                return False
        except requests.RequestException as e:
            print(f"Failed to send Telegram notification: {e}")
            return False
        except KeyError as e:
            print(f"Telegram configuration missing: {e}")
            return False
    
    def format_balance_change(self, old_balance: float, new_balance: float, change: float) -> str:
        """Format balance change notification"""
        direction = DIRECTION_EMOJIS['up'] if change > 0 else DIRECTION_EMOJIS['down']
        return f"""
{direction} BALANCE CHANGE DETECTED
Wallet: {self.wallet_name} ({format_address(self.wallet_address)})
Previous Balance: {old_balance:.4f} ETH
New Balance: {new_balance:.4f} ETH
Change: {change:+.4f} ETH ({(change/float(old_balance or 1)*100):+.2f}%)
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
    
    def format_position_change(self, positions: Dict, change_type: str = "change") -> str:
        """
        Hyperliquid pozisyon değişimi bildirimini formatlar.

        Güvenli tip dönüşümleri:
        - marginSummary içindeki tüm sayısal alanlar _safe_float ile normalize edilir.
        - _changed_coin vurgusu korunur (alev/emoji desteği PositionFormatter içinde).
        """
        if not positions or "marginSummary" not in positions:
            return "Position data unavailable"

        # marginSummary güvenli normalize
        margin_summary = positions.get("marginSummary", {}) or {}
        normalized_margin = {
            "accountValue": self._safe_float(margin_summary.get("accountValue", 0)),
            "totalNotion": self._safe_float(
                margin_summary.get("totalNtlPos", margin_summary.get("totalNotion", 0))
            ),
            "unrealizedPnl": self._safe_float(margin_summary.get("unrealizedPnl", 0)),
            "marginUsage": self._safe_float(margin_summary.get("marginUsage", 0)),
        }

        # Eski anahtarları koru ki başka yerler kırılmasın
        margin_summary.update(normalized_margin)

        # Özet başlık (POSITION SUMMARY / OPENED / CLOSED / CHANGED)
        summary_info = self._format_margin_summary(margin_summary, change_type, positions)

        # Değişen coin
        changed_coin = positions.get("_changed_coin", None)

        # Pozisyon detayları (alev/vurgu mantığı PositionFormatter'da)
        positions_section = self._format_positions_section(positions, changed_coin, detailed=False)

        return summary_info + positions_section

    def _format_margin_summary(self, margin_summary: Dict, change_type: str, positions: Dict = None) -> str:
        """Format the margin summary section"""
        account_value = self._safe_float(margin_summary.get("accountValue", 0))
        total_notion = self._safe_float(margin_summary.get("totalNotion", 0))
        unrealized_pnl = self._safe_float(margin_summary.get("unrealizedPnl", 0))
        margin_usage = self._safe_float(margin_summary.get("marginUsage", 0))

        # Choose appropriate emoji and title based on change type
        emoji, title = self._get_change_type_info(change_type)

        # Get changed coin if available
        changed_coin = positions.get("_changed_coin", None)
        if changed_coin:
            title += f" - {changed_coin}"

        # Global başlangıç / özet bildirimleri için okunaklı KAR / ZARAR etiketi:
        if unrealized_pnl > 0:
            global_pnl_tag = " ⬆️ KAR ⬆️"
        elif unrealized_pnl < 0:
            global_pnl_tag = " ⬇️ ZARAR ⬇️"
        else:
            global_pnl_tag = " ➡️ NÖTR"

        return f"""
{emoji} {title}
Wallet: {self.wallet_name} ({format_address(self.wallet_address)})
Account Value: ${account_value:,.2f}
Total Position Value: ${total_notion:,.2f}
Unrealized PnL: ${unrealized_pnl:,.2f}{global_pnl_tag}
Margin Usage: {margin_usage*100:.2f}%
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """

    def _get_change_type_info(self, change_type: str) -> tuple:
        """Get emoji and title based on change type"""
        if change_type == "position_opened":
            return "🚀", "POSITION OPENED"
        elif change_type == "position_closed":
            return "✅", "POSITION CLOSED"
        elif change_type == "position_summary":
            return "📊", "POSITION SUMMARY"
        else:
            return "🔄", "POSITION CHANGED"

    def _format_positions_section(self, positions: Dict, changed_coin: str = None, detailed: bool = True) -> str:
        """
        Pozisyon listesini formatlar.

        İyileştirmeler:
        - changed_coin için ekstra vurgu:
          • Satır başında özel emoji.
          • Pozisyon satır sonuna "CHANGED" etiketi.
        - Her pozisyonda unrealized PnL'e göre durum etiketi:
          • Kâr: "⬆️ KAR ⬆️"
          • Zarar: "⬇️ ZARAR ⬇️"
          • Nötr: "➡️ NÖTR"
        """
        asset_positions = positions.get("assetPositions", [])
        if not asset_positions:
            return ""

        summary = "\n📈 POSITIONS:\n"
        for pos_data in asset_positions:
            if "position" not in pos_data or not pos_data["position"]:
                continue

            position = pos_data["position"]
            coin = position.get("coin", "")
            pnl = self._safe_float(position.get("unrealizedPnl", 0))

            # PnL etiketi
            if pnl > 0:
                pnl_tag = " ⬆️ KAR ⬆️"
            elif pnl < 0:
                pnl_tag = " ⬇️ ZARAR ⬇️"
            else:
                pnl_tag = " ➡️ NÖTR"

            # PositionFormatter'dan temel format
            base_text = PositionFormatter.format_position_detailed(position, changed_coin)

            # Eğer formatlama boş dönerse atla
            if not base_text:
                continue

            # Değişen coin için ekstra vurgu
            if changed_coin and coin == changed_coin:
                # Başına belirgin emoji ekle, sonuna CHANGED etiketi koy
                highlighted = f"🔥 {base_text.strip()} 🔥 [CHANGED]{pnl_tag}\n"
                summary += highlighted
            else:
                summary += f"{base_text.strip()}{pnl_tag}\n"

        return summary
    
    def format_transaction_alert(self, tx: Dict) -> str:
        """Format transaction notification"""
        value_eth = float(tx.get("value", 0)) / WEI_TO_ETH_DIVISOR
        direction = "OUT" if tx["from"].lower() == self.wallet_address.lower() else "IN"

        return f"""
💰 NEW TRANSACTION DETECTED
Direction: {direction}
Value: {value_eth:.4f} ETH
To: {format_address(tx.get('to', 'N/A'))}
Hash: {tx.get('hash', 'N/A')}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
    
    def format_deposit_withdrawal(self, transactions: List[Dict]) -> str:
        """Format deposit/withdrawal notifications"""
        if not transactions:
            return "No transactions to display"
        
        summary = "💰 DEPOSIT/WITHDRAWAL DETECTED\n"
        summary += f"Wallet: {self.wallet_name} ({format_address(self.wallet_address)})\n"
        summary += f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        for tx in transactions:
            asset = tx.get("asset", "Unknown")
            wallet_address = self.wallet_address.lower()
            
            # Calculate value based on asset type
            if asset == "ETH":
                value = float(tx.get("value", 0)) / WEI_TO_ETH_DIVISOR
                value_str = f"{value:.4f} {asset}"
            else:
                # For tokens (like BTC), the value is already in the correct decimal format
                value = float(tx.get("value", 0)) / (10 ** int(tx.get("tokenDecimal", DEFAULT_TOKEN_DECIMALS)))
                value_str = f"{value:.6f} {asset}"
            
            # Determine if it's a deposit or withdrawal
            if tx.get("from", "").lower() == wallet_address:
                tx_type = "WITHDRAWAL"
                emoji = "📤"
                recipient = tx.get("to", "Unknown")[:ADDRESS_TRUNCATE_LENGTH] + "..." if tx.get("to") else DEFAULT_STRING_VALUE
                summary += f"{emoji} {tx_type}: {value_str}\n"
                summary += f"   To: {recipient}\n"
            elif tx.get("to", "").lower() == wallet_address:
                tx_type = "DEPOSIT"
                emoji = "📥"
                sender = tx.get("from", "Unknown")[:ADDRESS_TRUNCATE_LENGTH] + "..." if tx.get("from") else DEFAULT_STRING_VALUE
                summary += f"{emoji} {tx_type}: {value_str}\n"
                summary += f"   From: {sender}\n"
            
            summary += f"   Hash: {tx.get('hash', DEFAULT_STRING_VALUE)[:TRANSACTION_HASH_TRUNCATE_LENGTH]}...\n\n"
        
        return summary
    
    def format_hyperliquid_summary(self, positions: Dict, stats: Dict = None) -> str:
        """
        Hyperliquid pozisyon özetini güvenli şekilde formatlar.
        - Tüm numeric alanlar _safe_float ile normalize edilir.
        - Böylece '>' not supported between instances of 'str' and 'int' hatası engellenir.
        - Özet + ACTIVE POSITIONS içinde hem global hem coin bazlı KAR/ZARAR görünür.
        """
        if not positions or "marginSummary" not in positions:
            return "Position data unavailable"

        margin_summary = positions.get("marginSummary", {}) or {}
        asset_positions = positions.get("assetPositions", []) or []

        # marginSummary normalize (hem eski hem yeni anahtar isimleri)
        normalized_margin = {
            "accountValue": self._safe_float(margin_summary.get("accountValue", 0)),
            "totalNtlPos": self._safe_float(
                margin_summary.get("totalNtlPos", margin_summary.get("totalNotion", 0))
            ),
            "unrealizedPnl": self._safe_float(margin_summary.get("unrealizedPnl", 0)),
            "totalMarginUsed": self._safe_float(margin_summary.get("totalMarginUsed", 0)),
            "marginUsage": self._safe_float(margin_summary.get("marginUsage", 0)),
        }
        margin_summary.update(normalized_margin)

        # İstatistikler normalize
        normalized_stats = {}
        if isinstance(stats, dict):
            for k, v in stats.items():
                if k == "position_count":
                    try:
                        normalized_stats[k] = int(float(v)) if v not in (None, "") else 0
                    except (TypeError, ValueError):
                        normalized_stats[k] = 0
                else:
                    normalized_stats[k] = self._safe_float(v, 0.0)

        # Build summary header (global KAR/ZARAR etiketi _format_margin_summary içinde)
        header = self._format_summary_header(margin_summary, normalized_stats or None, asset_positions)

        # Add position breakdown if stats available
        breakdown = self._format_position_breakdown(normalized_stats) if normalized_stats else ""

        # Add individual positions:
        # - Position change bildirimi için changed_coin vurgusu zaten _format_positions_section içinde.
        # - Global özet için burada da aynı fonksiyonu kullanırsak, ACTIVE POSITIONS içinde 🔥 + KAR/ZARAR olur.
        changed_coin = positions.get("_changed_coin")
        positions_section = self._format_positions_section(positions, changed_coin, detailed=True)

        return header + breakdown + positions_section

    def _format_summary_header(self, margin_summary: Dict, stats: Dict, asset_positions: list) -> str:
        """
        Hyperliquid özet başlığı.

        Hedef:
        - Hiç açık pozisyon yoksa kullanıcıya anlamsız 0 değerleri yığmak yerine sade mesaj göster.
        - Açık pozisyon varsa detaylı metrikleri göster.
        - Tüm sayısal alanları _safe_float ile normalize ederek tip hatalarını engelle.
        """
        account_value = self._safe_float(margin_summary.get("accountValue", 0))

        # totalNtlPos / totalNotion öncelikli
        base_total = self._safe_float(
            margin_summary.get("totalNtlPos", margin_summary.get("totalNotion", 0))
        )

        # Aktif pozisyonlar
        asset_positions = asset_positions or []
        active_positions = [
            pos for pos in asset_positions
            if self._safe_float(pos.get("position", {}).get("szi", 0)) != 0
        ]
        active_count = len(active_positions)

        # Eğer API 0 döndürmüş ama aktif pozisyon varsa, total position value'yu pozisyonlardan hesapla
        total_pos_value = base_total
        if total_pos_value == 0 and active_positions:
            total_pos_value = sum(
                self._safe_float(pos.get("position", {}).get("positionValue", 0))
                for pos in active_positions
            )

        # Unrealized PnL:
        unrealized_pnl = self._safe_float(margin_summary.get("unrealizedPnl", 0))
        if unrealized_pnl == 0 and active_positions:
            unrealized_pnl = sum(
                self._safe_float(pos.get("position", {}).get("unrealizedPnl", 0))
                for pos in active_positions
            )

        # Margin Usage:
        total_margin_used = self._safe_float(margin_summary.get("totalMarginUsed", 0))
        margin_usage = total_margin_used / account_value if account_value > 0 else 0

        # Hiç aktif pozisyon yoksa basit ve temiz çıktı
        if active_count == 0:
            return f"""
📊 HYPERLIQUID POSITION SUMMARY
Wallet: {self.wallet_name} ({format_address(self.wallet_address)})
Account Value: ${account_value:,.2f}
No open perpetual positions.
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """

        # Aktif pozisyon varsa stats (varsa) üzerinden detayları güvenli şekilde kullan
        win_rate = 0.0
        leverage = 0.0
        position_count = active_count

        if isinstance(stats, dict):
            total_pos_value = self._safe_float(
                stats.get("total_position_value", total_pos_value)
            )
            win_rate = self._safe_float(stats.get("win_rate", 0.0))
            leverage = self._safe_float(stats.get("leverage", 0.0))

            raw_pc = stats.get("position_count", position_count)
            try:
                if raw_pc not in (None, ""):
                    position_count = int(float(raw_pc))
            except (TypeError, ValueError):
                position_count = position_count

        return f"""
📊 HYPERLIQUID POSITION SUMMARY
Wallet: {self.wallet_name} ({format_address(self.wallet_address)})
Account Value: ${account_value:,.2f}
Total Position Value: ${total_pos_value:,.2f}
Unrealized PnL: ${unrealized_pnl:,.2f}
Margin Usage: {margin_usage*100:.2f}%
Open Positions: {position_count}
Win Rate: {win_rate:.1f}%
Leverage: {leverage:.2f}x
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """

    def _format_position_breakdown(self, stats: Dict) -> str:
        """Format the position breakdown section"""
        long_value = self._safe_float(stats.get("long_value", 0))
        short_value = self._safe_float(stats.get("short_value", 0))
        long_pct = self._safe_float(stats.get("long_percentage", 0))
        short_pct = self._safe_float(stats.get("short_percentage", 0))

        # Additional validation to ensure we have meaningful data
        if long_value == 0 and short_value == 0:
            return ""

        return f"""
📈 POSITION BREAKDOWN:
• Long: ${long_value:,.2f} ({long_pct:.1f}%)
• Short: ${short_value:,.2f} ({short_pct:.1f}%)
        """
    
    def _safe_float(self, value, default=0.0) -> float:
        """Safely convert value to float to avoid type errors."""
        try:
            if value is None or value == "":
                return float(default)
            return float(value)
        except (TypeError, ValueError):
            return float(default)

    def _format_active_positions(self, positions: Dict) -> str:
        """
        Aktif pozisyonlar bölümünü formatlar.

        Global geliştirme:
        - Her pozisyon için unrealized PnL'e göre KAR/ZARAR etiketi eklenir:
          • PnL > 0  -> " ⬆️ KAR ⬆️"
          • PnL < 0  -> " ⬇️ ZARAR ⬇️"
          • PnL = 0  -> " ➡️ NÖTR"
        - Böylece başlangıç bildirimleri ve tüm ACTIVE POSITIONS bloklarında,
          her pozisyon satırında net kar/zarar bilgisi görünür.
        """
        asset_positions = positions.get("assetPositions", [])
        if not asset_positions:
            return ""

        summary = "\n🔍 ACTIVE POSITIONS:\n"
        for pos_data in asset_positions:
            if "position" not in pos_data or not pos_data["position"]:
                continue

            position = pos_data["position"]
            pnl = self._safe_float(position.get("unrealizedPnl", 0))

            # Var olan detay formatı kullan
            base = PositionFormatter.format_position_detailed(position)
            if not base:
                continue
            base = base.rstrip("\n")

            # Global PnL etiketi
            if pnl > 0:
                pnl_tag = " ⬆️ KAR ⬆️"
            elif pnl < 0:
                pnl_tag = " ⬇️ ZARAR ⬇️"
            else:
                pnl_tag = " ➡️ NÖTR"

            # Son satıra PnL tag ekle
            lines = base.split("\n")
            if lines:
                lines[-1] = f"{lines[-1]}{pnl_tag}"
            formatted_with_tag = "\n".join(lines)

            summary += formatted_with_tag + "\n"

        return summary
