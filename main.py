from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.core.config.astrbot_config import AstrBotConfig
from .manager import BalanceManager

@register("balance_get", "SakuraChiyo0v0", "大模型余额查询。", "v0.1.0")
class MyPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config
        self.manager = BalanceManager()

    @filter.command("当前余额查询")
    async def balance(self, event: AstrMessageEvent):
        """查询当前大模型余额"""
        
        # 权限检查
        if self.config.get("admin_only", True):
            user_id = event.get_sender_id()
            admins = self.context.get_config().admins_id
            if user_id not in admins:
                yield event.plain_result("🚫 只有管理员可以使用此指令。")
                return

        # 1. 获取当前会话使用的 Provider
        try:
            provider = self.context.get_using_provider(umo=event.unified_msg_origin)
        except Exception as e:
            yield event.plain_result(f"获取当前模型配置失败: {e}")
            return

        # 2. 获取 Provider 的配置信息
        provider_config = provider.provider_config
        provider_id = provider_config.get("id", "unknown")
        provider_type = provider_config.get("type", "unknown")
        api_base = provider_config.get("api_base", "")
        api_key = ""

        # 尝试获取 API Key
        try:
            api_key = provider.get_current_key()
        except NotImplementedError:
            keys = provider_config.get("key", [])
            if keys:
                api_key = keys[0]

        if not api_key:
             yield event.plain_result("无法获取当前模型的 API Key。")
             return

        # 脱敏打印 API Key
        masked_key = api_key[:6] + "*" * max(0, len(api_key) - 9) + api_key[-3:] if len(api_key) > 9 else "****"
        logger.info(f"正在查询余额 - Provider ID: {provider_id}, Type: {provider_type}, Base: {api_base}, Key: {masked_key}")

        # 3. 使用 Manager 查询
        result = await self.manager.query(api_key, api_base)
        yield event.plain_result(result.to_string())