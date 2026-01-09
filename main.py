from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.core.config.astrbot_config import AstrBotConfig
from .manager import BalanceManager
import asyncio

@register("balance_get", "SakuraChiyo0v0", "大模型余额查询。", "v0.3.0")
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

        # 1. 分组去重：(api_base, api_key) -> provider
        # 只要 Base 和 Key 相同，就视为同一个钱包
        unique_credentials = {}

        for p in providers:
            cfg = p.provider_config
            api_base = cfg.get("api_base", "")
            try:
                api_key = p.get_current_key()
            except:
                keys = cfg.get("key", [])
                api_key = keys[0] if keys else ""

            if not api_key:
                continue

            # 使用 (api_base, api_key) 作为唯一标识
            # 这里的 api_key 不脱敏，用于实际查询，但在内存中处理
            unique_credentials[(api_base, api_key)] = p

        if not unique_credentials:
            yield event.plain_result("⚠️ 未找到有效的 API Key 配置。")
            return

        yield event.plain_result(f"🔄 正在查询 {len(unique_credentials)} 个平台的余额，请稍候...")

        # 2. 并发查询
        tasks = []
        providers_list = [] # 用于记录对应的 Provider，以便获取 ID
        for (base, key), p in unique_credentials.items():
            tasks.append(self.manager.query(key, base))
            providers_list.append(p)

        results = await asyncio.gather(*tasks)

        # 3. 拼接结果
        msg = "💰 **全平台余额汇总**\n"
        msg += "━━━━━━━━━━━━━━\n"

        success_msgs = []
        error_msgs = []
        unsupported_ids = []

        for i, res in enumerate(results):
            if res.error:
                if "暂不支持" in res.error:
                    # 获取 Provider ID
                    p_id = providers_list[i].provider_config.get("id", "Unknown")
                    # 简化 ID：如果包含 /，只保留前半部分（平台名）
                    if "/" in p_id:
                        p_id = p_id.split("/")[0]
                    unsupported_ids.append(p_id)
                else:
                    error_msgs.append(f"🔴 **{res.source_name}**\n   ❌ {res.error}")
            else:
                # 成功
                success_msgs.append(f"🟢 **{res.source_name}**\n   💵 {res.total_balance} {res.currency}")

        if success_msgs:
            msg += "\n━━━━━━━━━━━━━━\n".join(success_msgs) + "\n"

        if error_msgs:
            if success_msgs:
                msg += "━━━━━━━━━━━━━━\n"
            msg += "\n━━━━━━━━━━━━━━\n".join(error_msgs) + "\n"

        if unsupported_ids and self.config.get("show_unsupported", True):
            # 去重并排序
            unsupported_ids = sorted(list(set(unsupported_ids)))
            if success_msgs or error_msgs:
                msg += "━━━━━━━━━━━━━━\n"
            msg += "⚪ **未适配平台**:\n   " + ", ".join(unsupported_ids) + "\n"

        # 如果没有成功也没有错误也没有不支持（理论上不可能），提示一下
        if not success_msgs and not error_msgs and not unsupported_ids:
            msg += "⚠️ 未检测到有效的平台配置。"

        yield event.plain_result(msg)