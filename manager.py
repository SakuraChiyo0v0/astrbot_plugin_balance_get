from typing import List
import aiohttp
from .models import BalanceResult
from .fetchers import BaseBalanceFetcher, DeepSeekFetcher, MoonshotFetcher, SiliconCloudFetcher

class BalanceManager:
    def __init__(self):
        self.fetchers: List[BaseBalanceFetcher] = [
            DeepSeekFetcher(),
            MoonshotFetcher(),
            SiliconCloudFetcher(),
        ]

    async def query(self, api_key: str, api_base: str) -> BalanceResult:
        async with aiohttp.ClientSession() as session:
            for fetcher in self.fetchers:
                if fetcher.match(api_base):
                    try:
                        return await fetcher.fetch(session, api_key, api_base)
                    except Exception as e:
                        return BalanceResult("Unknown", "Unknown", "0", error=f"Internal Error: {str(e)}")
            
            return BalanceResult("System", "Unknown", "0", error=f"暂不支持该 API Base: {api_base}")