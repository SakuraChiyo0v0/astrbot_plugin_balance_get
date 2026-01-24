import aiohttp
from datetime import datetime, timedelta
from ..models import BalanceResult
from .base import BaseBalanceFetcher

class ChatAnywhereFetcher(BaseBalanceFetcher):
    def match(self, api_base: str) -> bool:
        return "chatanywhere" in api_base

    async def fetch(self, session: aiohttp.ClientSession, api_key: str, api_base: str) -> BalanceResult:
        # 处理 api_base，确保指向根域名
        # 例如 https://api.chatanywhere.tech/v1 -> https://api.chatanywhere.tech
        base_url = api_base
        if "/v1" in base_url:
            base_url = base_url.split("/v1")[0]
        
        # 1. 获取订阅信息 (总额度)
        sub_url = f"{base_url}/v1/dashboard/billing/subscription"
        headers = {
            'Authorization': f'Bearer {api_key}'
        }
        
        total_balance = 0.0
        currency = "USD"
        
        try:
            async with session.get(sub_url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    # ChatAnywhere 通常返回 hard_limit_usd
                    total_balance = data.get("hard_limit_usd", 0.0)
                else:
                    # 如果获取订阅失败，可能是不支持该接口，尝试继续
                    pass
        except Exception as e:
            pass

        # 2. 获取使用量 (已用额度)
        # 通常需要查询当月的使用量，或者从很久以前到现在
        usage_url = f"{base_url}/v1/dashboard/billing/usage"
        
        # 查询最近 100 天的使用量 (覆盖足够长的时间)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=99)
        
        params = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }
        
        used_balance = 0.0
        
        try:
            async with session.get(usage_url, headers=headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    # total_usage 是美分，需要除以 100
                    total_usage_cents = data.get("total_usage", 0)
                    used_balance = total_usage_cents / 100
                else:
                    # 如果获取使用量失败
                    pass
        except Exception as e:
            pass

        # 计算剩余额度
        remaining = total_balance - used_balance
        
        # 如果获取到的都是 0，且没有报错，可能是不支持
        if total_balance == 0 and used_balance == 0:
             return BalanceResult("ChatAnywhere", "Unknown", "0", error="无法获取余额信息 (API不支持或返回为空)")

        return BalanceResult(
            source_name="ChatAnywhere",
            currency=currency,
            total_balance=f"{total_balance:.2f}",
            remaining_balance=f"{remaining:.2f}",
            used_balance=f"{used_balance:.2f}",
            raw_info=""
        )
