from typing import List, Optional
import aiohttp
from .models import BalanceResult
from .fetchers import BaseBalanceFetcher, DeepSeekFetcher, MoonshotFetcher, SiliconCloudFetcher, ChatAnywhereFetcher

class BalanceManager:
    def __init__(self):
        self.fetchers: List[BaseBalanceFetcher] = [
            DeepSeekFetcher(),
            MoonshotFetcher(),
            SiliconCloudFetcher(),
            ChatAnywhereFetcher(),
        ]
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    async def query(self, api_key: str, api_base: str) -> BalanceResult:
        session = await self._get_session()
        for fetcher in self.fetchers:
            if fetcher.match(api_base):
                try:
                    return await fetcher.fetch(session, api_key, api_base)
                except aiohttp.ClientError as e:
                    return BalanceResult("Unknown", "Unknown", "0", error=f"Network Error: {str(e)}")
                except Exception as e:
                    return BalanceResult("Unknown", "Unknown", "0", error=f"Internal Error: {str(e)}")

        return BalanceResult("System", "Unknown", "0", error=f"暂不支持该 API Base: {api_base}")