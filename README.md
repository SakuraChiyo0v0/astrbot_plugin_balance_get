# AstrBot Plugin Balance Get

<div align="center">

# 💰 大模型余额查询插件

一个用于 AstrBot 的插件，支持查询当前使用的 LLM 服务商的账户余额。

</div>

## ✨ 功能特性

- **自动识别**：自动检测当前会话正在使用的 LLM Provider，无需手动指定。
- **智能去重**：在查询所有余额时，自动根据 API Key 和 Base URL 去重，避免重复显示。
- **多厂商支持**：目前已适配以下服务商：
  - 🦈 **DeepSeek (深度求索)**
  - 🌙 **Moonshot AI (Kimi)**
  - ☁️ **SiliconCloud (硅基流动)**
- **权限控制**：支持配置仅管理员可用，保护账户隐私。
- **安全日志**：日志中自动脱敏 API Key，防止泄露。

## 🚀 使用方法

### 指令

| 指令 | 描述 | 权限 |
| :--- | :--- | :--- |
| `/当前余额查询` | 查询当前 LLM 模型的账户余额 | 默认仅管理员 |
| `/所有余额查询` | 查询所有已配置模型的账户余额 | 默认仅管理员 |

### 示例

```
用户: /当前余额查询
Bot:
💰 **当前余额查询**
━━━━━━━━━━━━━━
🟢 **DeepSeek**
   💵 10.00 CNY
```

```
用户: /所有余额查询
Bot:
💰 **全平台余额汇总**
━━━━━━━━━━━━━━
🟢 **DeepSeek**
   💵 10.00 CNY
━━━━━━━━━━━━━━
🟢 **Moonshot(Kimi)**
   💵 50.00 CNY
━━━━━━━━━━━━━━
⚪ **未适配平台**:
   openai, claude
```

## 💿 安装

### 方法一：通过 AstrBot 管理面板（推荐）

1. 打开 AstrBot 管理面板。
2. 进入“插件”页面。
3. 点击“安装插件”，输入本插件的 GitHub 仓库地址：`https://github.com/SakuraChiyo0v0/astrbot_plugin_balance_get`。
4. 安装完成后重启 AstrBot。

### 方法二：手动安装

1. 将本仓库克隆或下载到 AstrBot 的 `data/plugins/` 目录下：
   ```bash
   cd data/plugins
   git clone https://github.com/SakuraChiyo0v0/astrbot_plugin_balance_get
   ```
2. 重启 AstrBot。

## ⚙️ 配置说明

插件支持以下配置项（可在 AstrBot 管理面板中修改）：

| 配置项 | 类型 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| `admin_only` | bool | `true` | 是否仅允许管理员使用 `/balance` 指令。建议开启以防止群友随意查询。 |
| `show_unsupported` | bool | `true` | 在 `/所有余额查询` 中，是否显示未适配的平台列表。 |
| `output_template` | string | `🟢 **{{source_name}}**\n   💵 {{balance}} {{currency}}` | 自定义余额显示模板。支持变量见下表。 |
| `header_template` | string | `💰 **{{title}}**` | 消息头部的格式。支持变量：`{{title}}`。标题下方会自动添加分隔符。 |
| `separator_template` | string | `\n━━━━━━━━━━━━━━\n` | 标题与内容、以及多项结果之间的分隔符。 |

### 模板变量说明

| 变量名 | 说明 |
| :--- | :--- |
| `{{source_name}}` | 平台名称 (如 DeepSeek) |
| `{{currency}}` | 币种 (如 CNY) |
| `{{balance}}` | 智能余额（如果剩余=总额，显示总额；否则显示剩余） |
| `{{total_balance}}` | 总额 |
| `{{remaining_balance}}` | 剩余余额 |
| `{{used_balance}}` | 已用额度 |
| `{{raw_info}}` | 备注信息 |

## 📅 未来计划

- [ ] **文转图支持**：支持将查询结果生成为图片发送，更加美观。
- [ ] **更多平台**：在现有 DeepSeek、Kimi、SiliconCloud 的基础上，接入更多国内外大模型服务商。

## 🛠️ 开发与扩展

本插件采用策略模式设计，易于扩展新的厂商支持。

如果你想添加新的厂商支持：
1. 在 `fetchers/` 目录下创建一个新的 `.py` 文件。
2. 继承 `BaseBalanceFetcher` 类并实现 `match` 和 `fetch` 方法。
3. 在 `fetchers/__init__.py` 中导出你的类。
4. 在 `manager.py` 的 `BalanceManager` 中注册你的 Fetcher。

## ⚠️ 注意事项

- 插件通过 AstrBot 核心获取当前 Provider 的 API Key 进行查询，请确保你的 AstrBot 配置中 API Key 是正确的。
- 对于中转站（OneAPI/NewAPI），目前暂未提供通用支持（因为接口标准不一），建议使用官方直连配置。

## 📄 License

MIT
