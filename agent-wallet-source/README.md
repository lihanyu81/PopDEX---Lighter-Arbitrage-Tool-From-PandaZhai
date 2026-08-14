# POPDEX Agent 钱包开源模块

本目录包含 PandaArb 成品中用于本机生成、检查和授权 POPDEX Agent 钱包的可审计源码，采用 MIT 许可证。套利策略、执行、风控及行情处理代码不在本目录中。

## 安装

需要 Python 3.12 或更高版本：

```bash
cd agent-wallet-source
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

## Agent 文件

成品程序可用以下命令在本机生成独立 Agent：

```bash
../panda-arb-0.1.0-linux-x64-onefile wallet create
../panda-arb-0.1.0-linux-x64-onefile wallet inspect
```

Linux 默认保存到 `~/.config/panda-arb/agent.env`，文件包含 Agent 地址和私钥，必须保持私密，绝不能提交到 Git。

## 授权

默认命令只做预演和 Gas 估算，不会发送交易：

```bash
popdex-agent-authorize
```

核对签署账户、Agent、delegator、网络、合约和 Gas 估算后，显式允许广播：

```bash
popdex-agent-authorize --send
```

程序还会要求再次输入大写 `AUTHORIZE`。POPDEX 主账户私钥通过终端隐藏输入临时读取，不会写入 Agent 文件、日志或数据库。

可选参数：

```text
--agent-env PATH   指定 Agent 文件
--delegator 0x...  指定委托账户
--name NAME        指定不超过 32 字节的 Agent 名称
--days N           授权有效天数，默认 30
--rpc-url URL      指定 POPDEX RPC
--send             允许确认后广播授权交易
```

## 安全边界

- `wallet.py` 负责本机随机生成 Agent、原子写入私钥文件并限制文件权限。
- `authorize.py` 负责构造 `approveAgent`、模拟、签名和可选广播。
- `paths.py` 负责 Windows、macOS 和 Linux 用户配置路径。
- 源码不包含任何生产私钥、API Key 或 Telegram Token。
