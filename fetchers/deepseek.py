import aiohttp
from ..models import BalanceResult
from .base import BaseBalanceFetcher

class DeepSeekFetcher(BaseBalanceFetcher):
    def match(self, api_base: str) -> bool:
        return "deepseek" in api_base

    async def fetch(self, session: aiohttp.ClientSession, api_key: str, api_base: str) -> BalanceResult:
        url = "https://api.deepseek.com/user/balance"
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                text = await response.text()
                return BalanceResult("DeepSeek", "Unknown", "0", error=f"HTTP {response.status}: {text}")
            
            data = await response.json()
            if not data.get("is_available"):
                return BalanceResult("DeepSeek", "Unknown", "0", error="账户状态不可用")

            infos = data.get("balance_infos", [])
            if not infos:
                return BalanceResult("DeepSeek", "Unknown", "0", error="未找到余额信息")

            # 取第一个主要的余额信息
            info = infos[0]
            currency = info.get("currency", "CNY")
            total = info.get("total_balance", "0")

            return BalanceResult(
                source_name="DeepSeek",
                currency=currency,
                total_balance=total,
                remaining_balance=total, # DeepSeek 返回的是当前可用余额
                raw_info="" # 不再显示赠送和充值详情
            )