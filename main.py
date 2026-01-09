from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.core.config.astrbot_config import AstrBotConfig
from .manager import BalanceManager
import asyncio

@register("balance_get", "SakuraChiyo0v0", "大模型余额查询。", "v0.1.2")
class MyPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config
        self.manager = BalanceManager()

    @filter.command("当前余额查询")
    async def balance(self, event: AstrMessageEvent):
        """查询当前大模型余额"""
        # ... (保持原有逻辑不变) ...
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

    @filter.command("所有余额查询")
    async def query_all_balances(self, event: AstrMessageEvent):
        """查询所有已配置模型的余额"""

        # 权限检查
        if self.config.get("admin_only", True):
            user_id = event.get_sender_id()
            admins = self.context.get_config().admins_id
            if user_id not in admins:
                yield event.plain_result("🚫 只有管理员可以使用此指令。")
                return

        providers = self.context.get_all_providers()
        if not providers:
            yield event.plain_result("⚠️ 当前未配置任何模型提供商。")
            return

        yield event.plain_result(f"🔄 正在并发查询 {len(providers)} 个模型的余额，请稍候...")

        # 并发查询所有 Provider
        tasks = [self._query_single_provider(p) for p in providers]
        results = await asyncio.gather(*tasks)

        # 拼接结果
        msg = "💰 **所有模型余额汇总**\n"
        msg += "━━━━━━━━━━━━━━\n"

        # 分类展示，成功的排前面
        success_msgs = []
        error_msgs = []
        unsupported_msgs = []

        for res in results:
            if res['status'] == 'success':
                success_msgs.append(res['msg'])
            elif res['status'] == 'unsupported':
                unsupported_msgs.append(res['msg'])
            else:
                error_msgs.append(res['msg'])

        if success_msgs:
            msg += "\n".join(success_msgs) + "\n"

        if error_msgs:
            msg += "--------------\n" + "\n".join(error_msgs) + "\n"

        if unsupported_msgs:
            msg += "--------------\n" + "\n".join(unsupported_msgs)

        yield event.plain_result(msg)

    async def _query_single_provider(self, provider) -> dict:
        """辅助方法：查询单个 Provider"""
        cfg = provider.provider_config
        p_id = cfg.get("id", "unknown")
        api_base = cfg.get("api_base", "")

        try:
            api_key = provider.get_current_key()
        except:
            keys = cfg.get("key", [])
            api_key = keys[0] if keys else ""

        if not api_key:
            return {"status": "error", "msg": f"⚪ **{p_id}**: ❌ 未配置 API Key"}

        result = await self.manager.query(api_key, api_base)

        if result.error:
            if "暂不支持" in result.error:
                return {"status": "unsupported", "msg": f"⚪ **{p_id}**: 🚫 暂不支持"}
            return {"status": "error", "msg": f"🔴 **{p_id}**: ❌ {result.error}"}

        return {"status": "success", "msg": f"🟢 **{p_id}** ({result.source_name}): {result.total_balance} {result.currency}"}