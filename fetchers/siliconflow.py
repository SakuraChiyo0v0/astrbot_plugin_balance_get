import aiohttp
from ..models import BalanceResult
from .base import BaseBalanceFetcher

class SiliconCloudFetcher(BaseBalanceFetcher):
    def match(self, api_base: str) -> bool:
        return "siliconflow" in api_base

    async def fetch(self, session: aiohttp.ClientSession, api_key: str, api_base: str) -> BalanceResult:
        # 优先使用 .com，如果 api_base 里明确是 .cn 则用 .cn
        domain = "api.siliconflow.com"
        if "siliconflow.cn" in api_base:
            domain = "api.siliconflow.cn"
            
        url = f"https://{domain}/v1/user/info"
        headers = {
            'Authorization': f'Bearer {api_key}'
        }
        
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                text = await response.text()
                return BalanceResult("SiliconCloud", "Unknown", "0", error=f"HTTP {response.status}: {text}")
            
            data = await response.json()
            if data.get("code") != 20000:
                 return BalanceResult("SiliconCloud", "Unknown", "0", error=f"API Error: {data.get('message')}")

            data_inner = data.get("data", {})
            
            # 根据文档：
            # totalBalance: 总余额
            # balance: 可能是赠送余额
            # chargeBalance: 充值余额
            
            total = data_inner.get("totalBalance")
            if not total:
                # Fallback: 如果 totalBalance 为空，尝试用 balance
                total = data_inner.get("balance", "0")
            
            return BalanceResult(
                source_name="硅基流动(SiliconCloud)",
                currency="USD", # 修正为 USD
                total_balance=str(total),
                remaining_balance=str(total),
                raw_info=""
            )