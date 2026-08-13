# 熊猫寨PopDEX <-> Lighter 价差套利工具

这是熊猫寨套利产品的一部分，整个产品由于涉及交易所数量较大，在技术细节与合作细节方面都需要时间处理。

最近Popdex热度不错，而且会在月底closed beta结束前再进行一次奖励，于是乎，我们推出了这款产品。

由于套利产品的特殊性，只有在PopDEX使用了[PANDA]邀请码的钱包可以成功使用此产品

有任何问题可以联系 https://t.me/Chosmos2025

为了使您在使用过程里顺利，希望您仔细阅读一下步骤！

## 1.服务器的购买

虽然为了满足不同客户的使用习惯，我们有Linux、MAC、windows的不同版本。

但依然希望您使用Linux运行脚本，这是因为个人设备存在网络与电源方面的不确定性，而云服务器会减少此方面的风险。

推荐在以下三个厂商购买云服务器：
1. vultr 【新人可领取100美金，但需要一个月内消耗掉，需要信用卡类似撸AWS】https://www.vultr.com/?ref=9915549-9J
2. 阿里云 https://www.aliyun.com/minisite/goods?userCode=bwzu4y9m
3. 腾讯云 https://curl.qcloud.com/eOn6o376

推荐服务器配置2C2G以上
推荐服务器地区：日本东京[关于服务器地区，详见 Lighter和PopDEX关于IP地区的规定]https://github.com/lihanyu81/PopDEX---Lighter-Arbitrage-Tool-From-PandaZhai/blob/main/Lighter%E5%92%8CPopDEX%E5%85%B3%E4%BA%8EIP%E5%9C%B0%E5%8C%BA%E7%9A%84%E8%A7%84%E5%AE%9A.md#lighter-%E5%92%8C-popdex-%E7%A6%81%E6%AD%A2%E5%9B%BD%E5%AE%B6%E5%8F%8A%E5%9C%B0%E5%8C%BA%E5%AF%B9%E7%85%A7%E8%A1%A8

## 2.部署脚本

### 2.1 Linux系统

#### 2.1.1 在VPS厂商的界面打开8000端口
此处以腾讯云为例（其他厂商操作类似）：
首先，

#### 2.1.2 导入工具进服务器
输入命令: git clone https://github.com/lihanyu81/PopDEX---Lighter-Arbitrage-Tool-From-PandaZhai

### 2.2 Windows系统

等待补充

### 2.3 Mac系统

等待补充

## 3.部署脚本

在命令行输入：

## 4. macOS Apple Silicon 封包下载

当前版本为 `v0.1.0`，适用于 Apple Silicon（arm64）和 macOS 15.5 或更高版本。Windows、Linux 以及 Intel Mac 不能使用此封包。

由于 GitHub 单次上传限制和网络稳定性，封包存放在 [`downloads/v0.1.0`](downloads/v0.1.0) 中并拆成连续分卷。使用以下命令下载仓库并自动合并：

```bash
git clone https://github.com/lihanyu81/PopDEX---Lighter-Arbitrage-Tool-From-PandaZhai.git
cd PopDEX---Lighter-Arbitrage-Tool-From-PandaZhai/downloads/v0.1.0

cat panda-arb-0.1.0-macos-arm64.tar.gz.part-* > panda-arb-0.1.0-macos-arm64.tar.gz
shasum -a 256 -c panda-arb-0.1.0-macos-arm64.tar.gz.sha256
tar -xzf panda-arb-0.1.0-macos-arm64.tar.gz
cd panda-arb-0.1.0-macos-arm64
```

校验结果必须显示：

```text
panda-arb-0.1.0-macos-arm64.tar.gz: OK
```

首次运行：

```bash
./panda-arb config init
./panda-arb wallet create
./panda-arb config check
./panda-arb serve
```

发布包已经包含 Python 运行时和依赖，不需要安装 Python 或执行 `pip install`。封包中不包含 Python 源码、`.env`、`.env.example`、Agent 私钥或运行数据库；`config init` 和 `wallet create` 会在每位用户自己的系统配置目录中生成对应文件。

macOS 封包目前尚未进行 Apple Developer 签名和公证。请务必先完成 SHA-256 校验，并仅在确认仓库来源可信后运行。
