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

    def to_string(self, template: str = "") -> str:
        if self.error:
            return f"🔴 **{self.source_name}**\n   ❌ {self.error}"

        # 智能余额：如果剩余=总额，则 balance 代表总额；否则代表剩余
        smart_balance = self.remaining_balance

        # 如果没有提供模板，使用默认逻辑（为了兼容旧代码调用，虽然现在都会传模板）
        if not template:
            # 默认逻辑
            if self.remaining_balance == self.total_balance:
                msg = f"🟢 **{self.source_name}**\n"
                msg += f"   💵 {self.total_balance} {self.currency}"
            else:
                msg = f"🟢 **{self.source_name}**\n"
                msg += f"   💵 余额: {self.remaining_balance} {self.currency}\n"
                msg += f"   📈 总额: {self.total_balance} {self.currency}"
                if self.used_balance != "0":
                    msg += f"\n   📊 已用: {self.used_balance} {self.currency}"
            if self.raw_info:
                msg += f"\n   📝 {self.raw_info}"
            return msg

        # 使用模板渲染
        # 简单的字符串替换
        result = template
        result = result.replace("{{source_name}}", self.source_name)
        result = result.replace("{{currency}}", self.currency)
        result = result.replace("{{balance}}", smart_balance)
        result = result.replace("{{total_balance}}", self.total_balance)
        result = result.replace("{{remaining_balance}}", self.remaining_balance)
        result = result.replace("{{used_balance}}", self.used_balance)
        result = result.replace("{{raw_info}}", self.raw_info)

        # 处理换行符
        result = result.replace("\\n", "\n")

        return result