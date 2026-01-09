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
            return f"🔴 **{self.source_name}**\n   ❌ {self.error}"

        # 如果剩余余额等于总余额，说明是纯余额型账户，只显示一行
        if self.remaining_balance == self.total_balance:
            msg = f"🟢 **{self.source_name}**\n"
            msg += f"   💵 {self.total_balance} {self.currency}"
        else:
            # 额度型账户，显示详情
            msg = f"🟢 **{self.source_name}**\n"
            msg += f"   💵 余额: {self.remaining_balance} {self.currency}\n"
            msg += f"   📈 总额: {self.total_balance} {self.currency}"
            if self.used_balance != "0":
                msg += f"\n   📊 已用: {self.used_balance} {self.currency}"

        if self.raw_info:
            msg += f"\n   📝 {self.raw_info}"

        return msg