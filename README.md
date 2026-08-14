# 熊猫寨 PopDEX ↔ Lighter 价差套利工具

[![Version](https://img.shields.io/badge/version-0.1.0-blue)](#)
[![Platform](https://img.shields.io/badge/platform-Linux%20x86__64-orange)](#)
[![GitHub Stars](https://img.shields.io/github/stars/lihanyu81/PopDEX---Lighter-Arbitrage-Tool-From-PandaZhai?style=social)](https://github.com/lihanyu81/PopDEX---Lighter-Arbitrage-Tool-From-PandaZhai/stargazers)

本工具用于监控 PopDEX 与 Lighter 之间的价格差异，并按照用户配置执行价差交易，是熊猫寨套利产品的一部分。

由于完整产品需要适配多个交易平台，相关技术细节、交易风控和合作方案仍在持续完善中。本仓库目前提供 PopDEX ↔ Lighter 版本。

> [!IMPORTANT]
> 由于产品授权机制限制，只有在 PopDEX 使用邀请码 `PANDA` 的钱包才能正常使用本工具。

如有使用问题，请通过 Telegram 联系：

- https://t.me/Chosmos2025
- 视频配置教程 https://youtu.be/kfeVYszfr20?si=c2rnAwP4RAQBEJSW

## 使用前须知

本工具涉及数字资产交易。价差的出现不代表一定能够获得利润，实际结果可能受到以下因素影响：

- 交易手续费和资金费率
- 网络延迟和行情变化
- 滑点、深度不足与部分成交
- API、RPC、交易所或签名服务异常
- 账户权限、保证金和清算风险
- PopDEX、Lighter 规则或接口发生变化
- 所在国家或地区的法律及平台访问限制

请先使用小额资金测试，确认配置、授权、下单方向和风控参数均符合预期后，再决定是否扩大使用规模。

本工具不构成投资建议，也不承诺任何收益。用户应自行承担交易、账户和资金风险。

---

## 1. 运行环境

### 1.1 为什么推荐使用云服务器

建议在 Linux 云服务器上运行本工具。

个人电脑可能受到断网、休眠、断电和系统更新等因素影响；云服务器通常能够提供相对稳定的网络和持续运行环境，但仍不能保证服务绝对不中断。

### 1.2 推荐配置

| 项目 | 建议配置 |
|---|---|
| 操作系统 | Ubuntu 22.04/24.04 或其他主流 Linux |
| CPU | 2 核及以上 |
| 内存 | 2 GB 及以上 |
| 架构 | x86_64 |
| 磁盘 | 20 GB 及以上 |
| 网络 | 稳定、低延迟 |

当前仓库中的 Linux 单文件版本仅适用于 `x86_64`。登录服务器后，可运行以下命令检查架构：

```bash
uname -m
```

正确结果应为：

```text
x86_64
```

如果显示 `aarch64` 或 `arm64`，说明服务器采用 ARM 架构，无法直接运行当前的 Linux x64 文件。

### 1.3 云服务器厂商

可根据所在地区、支付方式和网络质量选择云服务器：

1. [Vultr](https://www.vultr.com/?ref=9915549-9J)
2. [阿里云](https://www.aliyun.com/minisite/goods?userCode=bwzu4y9m)
3. [腾讯云](https://curl.qcloud.com/eOn6o376)

优惠活动、赠金条件和有效期可能随时变化，请以厂商官方页面显示的信息为准。

### 1.4 服务器地区

服务器地区必须同时符合：

- 用户所在地的法律和监管要求
- PopDEX 的服务条款和地区限制
- Lighter 的服务条款和地区限制
- 云服务器厂商的使用政策

可参考：

- [Lighter 和 PopDEX 关于 IP 地区的规定](./Lighter和PopDEX关于IP地区的规定.md)

该文档仅用于辅助查询，平台的官方条款和最新公告具有更高优先级。请勿使用云服务器规避平台限制。

---

## 2. Linux 部署

### 2.1 登录服务器

使用 SSH 登录服务器：

```bash
ssh 用户名@服务器IP
```

不同厂商的默认用户名可能不同，例如：

```text
root
ubuntu
debian
```

建议优先使用 SSH 密钥登录，并关闭不必要的公网端口。

### 2.2 下载工具

```bash
git clone https://github.com/lihanyu81/PopDEX---Lighter-Arbitrage-Tool-From-PandaZhai.git
cd PopDEX---Lighter-Arbitrage-Tool-From-PandaZhai
```

### 2.3 校验文件完整性

运行：

```bash
sha256sum -c panda-arb-0.1.0-linux-x64-onefile.sha256
```

校验结果必须显示：

```text
panda-arb-0.1.0-linux-x64-onefile: OK
```

如果出现 `FAILED`、找不到文件或哈希值不一致，请不要继续运行。应重新下载文件，并确认仓库地址正确。

校验通过后添加执行权限：

```bash
chmod +x panda-arb-0.1.0-linux-x64-onefile
```

可以先查看命令帮助：

```bash
./panda-arb-0.1.0-linux-x64-onefile --help
```

---

## 3. 初始化配置与 Agent 钱包

### 3.1 初始化配置

```bash
./panda-arb-0.1.0-linux-x64-onefile config init
```

请根据提示完成配置。不要把 `.env`、API Key、私钥或其他凭据发送给任何人，也不要提交到 GitHub。

### 3.2 创建 Agent 钱包

```bash
./panda-arb-0.1.0-linux-x64-onefile wallet create
```

检查生成的 Agent 信息：

```bash
./panda-arb-0.1.0-linux-x64-onefile wallet inspect
```

Linux 默认将 Agent 文件保存在：

```text
~/.config/panda-arb/agent.env
```

该文件包含 Agent 地址和私钥，必须严格保密。

建议检查文件权限：

```bash
ls -l ~/.config/panda-arb/agent.env
```

不要执行以下操作：

- 不要将 Agent 文件提交到 Git
- 不要截图或复制私钥到聊天软件
- 不要通过 Telegram、邮件或工单发送私钥
- 不要在共享服务器上使用生产私钥
- 不要让不受信任的人员获得服务器登录权限

### 3.3 授权 PopDEX Agent

请完整阅读：

- [POPDEX Agent 钱包开源模块与授权说明](./agent-wallet-source/README.md)

授权工具默认只进行预演和 Gas 估算，不会直接广播交易。请仔细核对：

- 签署账户
- Agent 地址
- Delegator
- 网络与合约地址
- 授权期限
- Gas 估算

确认所有信息无误后，再按照文档显式执行授权。

### 3.4 检查配置

完成配置和 Agent 授权后运行：

```bash
./panda-arb-0.1.0-linux-x64-onefile config check
```

如果检查未通过，请先根据错误提示修正配置，不要直接启动交易服务。

---

## 4. 启动服务

### 4.1 推荐方式：仅监听本机地址

在服务器中启动：

```bash
./panda-arb-0.1.0-linux-x64-onefile serve \
  --host 127.0.0.1 \
  --port 8000 \
  --no-browser
```

这种方式不会直接把管理页面暴露到公网。

然后在自己的电脑上建立 SSH 隧道：

```bash
ssh -L 8000:127.0.0.1:8000 用户名@服务器IP
```

保持该终端窗口开启，在本地浏览器访问：

```text
http://127.0.0.1:8000
```

使用 SSH 隧道时，通常不需要在云服务器安全组中开放公网 8000 端口。

### 4.2 公网访问方式

只有在明确了解风险的情况下，才使用：

```bash
./panda-arb-0.1.0-linux-x64-onefile serve \
  --host 0.0.0.0 \
  --port 8000 \
  --no-browser
```

如果需要公网访问，请在云服务器安全组中：

1. 添加 TCP 8000 入站规则。
2. 来源地址设置为你自己当前的公网 IP，例如 `1.2.3.4/32`。
3. 不要将来源设置为 `0.0.0.0/0`。
4. 使用结束后及时关闭该规则。

然后访问：

```text
http://服务器IP:8000
```

> [!WARNING]
> 如果服务本身没有登录认证或 HTTPS，不应直接暴露在公网。推荐始终使用 SSH 隧道。

---

## 5. 后台运行

直接运行程序时，关闭 SSH 窗口可能导致程序退出。临时后台运行可以使用：

```bash
nohup ./panda-arb-0.1.0-linux-x64-onefile serve \
  --host 127.0.0.1 \
  --port 8000 \
  --no-browser \
  > panda-arb.log 2>&1 &

echo $! > panda-arb.pid
```

查看日志：

```bash
tail -f panda-arb.log
```

退出日志查看：

```text
Ctrl+C
```

停止后台程序：

```bash
kill "$(cat panda-arb.pid)"
```

如果程序未能正常退出，确认 PID 无误后再使用强制结束：

```bash
kill -9 "$(cat panda-arb.pid)"
```

长期运行建议配置 `systemd` 服务，以便在程序异常退出或服务器重启后自动恢复。

---

## 6. 端口检查与故障排查

检查 8000 端口是否正在监听：

```bash
sudo ss -ltnp | grep ':8000'
```

如果系统安装了 `lsof`，也可以运行：

```bash
sudo lsof -i :8000
```

常见问题：

### `Permission denied`

重新添加执行权限：

```bash
chmod +x panda-arb-0.1.0-linux-x64-onefile
```

### `Exec format error`

通常表示服务器架构不兼容。运行：

```bash
uname -m
```

当前版本要求结果为：

```text
x86_64
```

### 8000 端口被占用

查找占用端口的进程：

```bash
sudo lsof -i :8000
```

先尝试正常结束：

```bash
kill PID
```

仅在进程无法正常退出时使用：

```bash
kill -9 PID
```

也可以更换端口：

```bash
./panda-arb-0.1.0-linux-x64-onefile serve \
  --host 127.0.0.1 \
  --port 8001 \
  --no-browser
```

建立 SSH 隧道时同步修改端口：

```bash
ssh -L 8001:127.0.0.1:8001 用户名@服务器IP
```

然后访问：

```text
http://127.0.0.1:8001
```

---

## 7. 封包与数据说明

Linux 单文件版本已经包含：

- Python 运行时
- 程序依赖
- 前端静态资源
- Lighter Linux signer

封包中不包含：

- 用户 `.env`
- PopDEX Agent 私钥
- 用户 API Key
- 运行数据库
- 用户交易数据

`config init` 和 `wallet create` 会在每位用户自己的系统配置目录中生成对应文件。

运行前请务必：

1. 确认仓库地址正确。
2. 完成 SHA-256 校验。
3. 阅读 Agent 授权源码和说明。
4. 检查配置与钱包地址。
5. 使用小额资金完成测试。
6. 确认服务器地区符合平台规定。
7. 妥善保管所有私钥和凭据。

---

## 8. 支持与反馈

如遇到问题，请联系：

- Telegram：https://t.me/Chosmos2025

反馈问题时可以提供：

- 操作系统版本
- CPU 架构
- 工具版本
- 执行的命令
- 已脱敏的错误信息

请勿提供：

- 私钥或助记词
- `.env` 完整内容
- API Secret
- Agent 私钥
- 身份验证 Token
- 其他能够控制账户或资金的凭据
