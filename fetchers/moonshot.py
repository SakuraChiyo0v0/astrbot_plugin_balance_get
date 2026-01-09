import aiohttp
from ..models import BalanceResult
from .base import BaseBalanceFetcher

class MoonshotFetcher(BaseBalanceFetcher):
    def match(self, api_base: str) -> bool:
        return "moonshot.cn" in api_base

    async def fetch(self, session: aiohttp.ClientSession, api_key: str, api_base: str) -> BalanceResult:
        url = "https://api.moonshot.cn/v1/users/me/balance"
        headers = {
            'Authorization': f'Bearer {api_key}'
        }
        
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                text = await response.text()
                return BalanceResult("Moonshot(Kimi)", "Unknown", "0", error=f"HTTP {response.status}: {text}")
            
            data = await response.json()
            # 检查业务状态码
            if data.get("code") != 0 or not data.get("status"):
                 return BalanceResult("Moonshot(Kimi)", "Unknown", "0", error=f"API Error: {data}")

            data_inner = data.get("data", {})
            # available_balance: 可用余额
            available = data_inner.get("available_balance", 0)
            
            return BalanceResult(
                source_name="Moonshot(Kimi)",
                currency="CNY",
                total_balance=str(available),
                remaining_balance=str(available),
                raw_info=""
            )