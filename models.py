from dataclasses import dataclass

@dataclass
class BalanceResult:
    """统一的余额返回结果"""
    source_name: str
    currency: str
    total_balance: str
    used_balance: str = "0"
    remaining_balance: str = "0"
    is_available: bool = True
    raw_info: str = ""
    error: str = None

    def to_string(self) -> str:
        if self.error:
            return f"❌ {self.source_name} 查询失败: {self.error}"
        
        msg = f"💰 {self.source_name} 余额查询\n"
        msg += f"━━━━━━━━━━━━━━\n"
        msg += f"💵 币种: {self.currency}\n"
        msg += f"📈 总额: {self.total_balance}\n"
        if self.remaining_balance != "0":
            msg += f"📉 剩余: {self.remaining_balance}\n"
        if self.used_balance != "0":
            msg += f"📊 已用: {self.used_balance}\n"
        
        if self.raw_info:
            msg += f"📝 备注: {self.raw_info}\n"
        return msg