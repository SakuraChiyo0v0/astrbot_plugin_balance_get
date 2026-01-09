# Changelog

All notable changes to this project will be documented in this file.

## [v0.1.1] - 2026-01-09

### 🐛 Fixes

- **Command Conflict**: Renamed command from `/balance` to `/当前余额查询` to avoid conflicts with other plugins.

## [v0.1.0] - 2026-01-09

### 🚀 Features

- **Initial Release**: First version of the balance query plugin.
- **Multi-Provider Support**:
  - DeepSeek (CNY)
  - Moonshot AI / Kimi (CNY)
  - SiliconCloud (USD)
- **Auto-Detection**: Automatically identifies the current LLM provider based on `api_base`.
- **Permission Control**: Added `admin_only` configuration (default: true).
- **Security**: API Keys are masked in logs.
