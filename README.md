# AstrBot Plugin Balance Get

<div align="center">

# 💰 大模型余额查询插件

一个用于 AstrBot 的插件，支持查询当前使用的 LLM 服务商的账户余额。

</div>

## ✨ 功能特性

- **自动识别**：自动检测当前会话正在使用的 LLM Provider，无需手动指定。
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
💰 DeepSeek 余额查询
━━━━━━━━━━━━━━
💵 币种: CNY
📈 总额: 10.00
📉 剩余: 8.56
```

```
用户: /所有余额查询
Bot:
💰 **所有模型余额汇总**
━━━━━━━━━━━━━━
🟢 **deepseek** (DeepSeek): 10.00 CNY
🟢 **kimi** (Moonshot(Kimi)): 50.00 CNY
--------------
⚪ **gpt-4** (OpenAI): 🚫 暂不支持
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
