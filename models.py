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

    def _get_default_string(self) -> str:
        """生成默认格式的字符串"""
        msg = f"🟢 **{self.source_name}**\n"
        if self.remaining_balance == self.total_balance:
            msg += f"   💵 {self.total_balance} {self.currency}"
        else:
            msg += f"   💵 余额: {self.remaining_balance} {self.currency}\n"
            msg += f"   📈 总额: {self.total_balance} {self.currency}"
            if self.used_balance != "0":
                msg += f"\n   📊 已用: {self.used_balance} {self.currency}"
        if self.raw_info:
            msg += f"\n   📝 {self.raw_info}"
        return msg

    def to_string(self, template: str = "") -> str:
        if self.error:
            return f"🔴 **{self.source_name}**\n   ❌ {self.error}"

        if not template:
            return self._get_default_string()

        # 智能余额：如果剩余=总额，则 balance 代表总额；否则代表剩余
        smart_balance = self.remaining_balance

        # 使用模板渲染
        replacements = {
            "{{source_name}}": self.source_name,
            "{{currency}}": self.currency,
            "{{balance}}": smart_balance,
            "{{total_balance}}": self.total_balance,
            "{{remaining_balance}}": self.remaining_balance,
            "{{used_balance}}": self.used_balance,
            "{{raw_info}}": self.raw_info,
        }

        result = template
        for key, value in replacements.items():
            result = result.replace(key, str(value))

        # 处理换行符
        return result.replace("\\n", "\n")