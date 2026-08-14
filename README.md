# 熊猫寨PopDEX <-> Lighter 价差套利工具

这是熊猫寨套利产品的一部分，整个产品由于涉及交易所数量较大，在技术细节与合作细节方面都需要时间处理。

最近Popdex热度不错，而且会在月底closed beta结束前再进行一次奖励，于是乎，我们推出了这款产品。

由于套利产品的特殊性，只有在PopDEX使用了[PANDA]邀请码的钱包可以成功使用此产品

有任何问题可以联系 https://t.me/Chosmos2025

为了使您在使用过程里顺利，希望您仔细阅读一下步骤！

## 1.服务器的购买

希望您使用Linux运行脚本，这是因为个人设备存在网络与电源方面的不确定性，而云服务器会减少此方面的风险。

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
输入命令

```bash
git clone https://github.com/lihanyu81/PopDEX---Lighter-Arbitrage-Tool-From-PandaZhai.git
cd PopDEX---Lighter-Arbitrage-Tool-From-PandaZhai

sha256sum -c panda-arb-0.1.0-linux-x64-onefile.sha256
chmod +x panda-arb-0.1.0-linux-x64-onefile
```

校验结果必须显示：

```text
panda-arb-0.1.0-linux-x64-onefile: OK
```
#### 2.1.3 授权PopDEX Agent钱包并补充.env

请阅读 https://github.com/lihanyu81/PopDEX---Lighter-Arbitrage-Tool-From-PandaZhai/tree/main/agent-wallet-source

#### 2.1.4 首次运行
检查配置
```bash
./panda-arb-0.1.0-linux-x64-onefile config init
./panda-arb-0.1.0-linux-x64-onefile wallet create
./panda-arb-0.1.0-linux-x64-onefile config check
```

运行
```bash
./panda-arb-0.1.0-linux-x64-onefile serve --host 0.0.0.0 --port 8000 --no-browser
```

查询8000端口占用
```bash
sudo lsof -i :8000
```

释放端口
```bash
kill -9 [PID]
```
单文件已经包含 Python 运行时、依赖、前端静态资源和 Lighter Linux signer。封包中不包含 `.env`、Agent 私钥或运行数据库；`config init` 和 `wallet create` 会在每位用户自己的系统配置目录中生成对应文件。请务必先完成 SHA-256 校验，并仅在确认仓库来源可信后运行。

