from abc import ABC, abstractmethod
import aiohttp
from ..models import BalanceResult

class BaseBalanceFetcher(ABC):
    """余额查询基类"""
    
    @abstractmethod
    def match(self, api_base: str) -> bool:
        """判断当前 Fetcher 是否支持该 api_base"""
        pass

    @abstractmethod
    async def fetch(self, session: aiohttp.ClientSession, api_key: str, api_base: str) -> BalanceResult:
        """执行查询"""
        pass