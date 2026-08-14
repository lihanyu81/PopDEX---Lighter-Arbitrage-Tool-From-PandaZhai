# MIT License; see OPEN_SOURCE_LICENSE.md at the product root.
from __future__ import annotations

import argparse
import os
import sys
from getpass import getpass
from pathlib import Path

import httpx


from panda_agent_wallet.paths import default_agent_env


POPDEX_MAINNET_RPC = "https://api.popdex.xyz/api/v1/web3/rpc"
POPDEX_MAINNET_CHAIN_ID = 2184
POPDEX_TIME_URL = "https://api.popdex.xyz/api/v1/public/time"
ACCOUNT_CONTRACT = "0x0000000000000000000000000000000000001008"

ACCOUNT_ABI = [
    {
        "type": "function",
        "name": "approveAgent",
        "stateMutability": "nonpayable",
        "inputs": [
            {"name": "agent", "type": "address"},
            {"name": "delegator", "type": "address"},
            {"name": "name", "type": "bytes32"},
            {"name": "expiresAt", "type": "uint64"},
            {"name": "initialNonce", "type": "uint64"},
            {"name": "isGlobal", "type": "bool"},
        ],
        "outputs": [],
    },
    {
        "type": "function",
        "name": "getAgentInfo",
        "stateMutability": "view",
        "inputs": [{"name": "agent", "type": "address"}],
        "outputs": [
            {"name": "exists", "type": "bool"},
            {"name": "expiresAt", "type": "uint64"},
            {"name": "isExpired", "type": "bool"},
            {"name": "delegator", "type": "address"},
            {"name": "name", "type": "bytes32"},
            {"name": "isGlobal", "type": "bool"},
            {"name": "agentType", "type": "uint8"},
            {"name": "scope", "type": "uint8"},
            {"name": "allowedRecipients", "type": "address[]"},
        ],
    },
]


def tty_input(prompt: str) -> str:
    """Read an interactive answer when the program itself came from a heredoc/pipe."""
    if os.name == "nt" or sys.stdin.isatty():
        return input(prompt).strip()
    print(prompt, end="", flush=True)
    with open("/dev/tty", "r", encoding="utf-8") as tty:
        return tty.readline().strip()


def read_agent_address(path: Path) -> str:
    if not path.exists():
        raise ValueError(f"找不到 Agent 配置：{path}")
    for line in path.read_text(encoding="utf-8").splitlines():
        key, separator, value = line.partition("=")
        if separator and key.strip() == "POPDEX_AGENT_ADDRESS" and value.strip():
            return value.strip()
    raise ValueError(f"{path} 中没有 POPDEX_AGENT_ADDRESS")


def encode_agent_name(name: str) -> bytes:
    value = name.encode("utf-8")
    if not value or len(value) > 32:
        raise ValueError("Agent 名称的 UTF-8 长度必须为 1 到 32 字节")
    return value.ljust(32, b"\0")


def fetch_popdex_time_ms() -> int:
    response = httpx.get(POPDEX_TIME_URL, timeout=15)
    response.raise_for_status()
    return int(response.json()["data"]["systemTs"])


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="用 POPDEX 主账户授权本地 Agent 钱包（默认仅预演）"
    )
    parser.add_argument(
        "--agent-env",
        type=Path,
        default=default_agent_env(),
        help="包含 POPDEX_AGENT_ADDRESS 的文件",
    )
    parser.add_argument(
        "--delegator",
        help="委托账户地址；省略时使用签署主账户本身",
    )
    parser.add_argument("--name", help="唯一 Agent 名称；省略时根据地址生成")
    parser.add_argument("--days", type=int, default=30, help="授权有效天数，默认 30")
    parser.add_argument("--rpc-url", default=POPDEX_MAINNET_RPC)
    parser.add_argument(
        "--send",
        action="store_true",
        help="模拟成功后允许确认并广播；不提供时绝不会广播",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    if args.days <= 0:
        raise SystemExit("--days 必须大于 0")

    try:
        from eth_account import Account
        from web3 import Web3
    except ImportError as exc:
        raise SystemExit("缺少实盘依赖，请运行：pip install -e '.[live]'") from exc

    try:
        agent = Web3.to_checksum_address(read_agent_address(args.agent_env))
    except (ValueError, TypeError) as exc:
        raise SystemExit(str(exc)) from exc

    private_key = getpass("请输入 POPDEX 主账户私钥（输入不会显示）：").strip()
    try:
        signer = Account.from_key(private_key)
    except Exception as exc:
        raise SystemExit("主账户私钥格式无效") from exc
    finally:
        private_key = ""

    try:
        delegator = Web3.to_checksum_address(args.delegator or signer.address)
    except (ValueError, TypeError) as exc:
        raise SystemExit("delegator 地址格式无效") from exc

    agent_name = args.name or f"arb-{agent[-8:].lower()}"
    try:
        name_bytes32 = encode_agent_name(agent_name)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    try:
        initial_nonce = fetch_popdex_time_ms()
    except Exception as exc:
        raise SystemExit(f"无法获取 POPDEX 官方时间：{exc}") from exc
    expires_at = initial_nonce + args.days * 24 * 60 * 60 * 1000

    web3 = Web3(Web3.HTTPProvider(args.rpc_url, request_kwargs={"timeout": 15}))
    if not web3.is_connected():
        raise SystemExit("无法连接 POPDEX RPC")
    if web3.eth.chain_id != POPDEX_MAINNET_CHAIN_ID:
        raise SystemExit(
            f"链 ID 错误：期望 {POPDEX_MAINNET_CHAIN_ID}，实际 {web3.eth.chain_id}"
        )

    contract = web3.eth.contract(
        address=Web3.to_checksum_address(ACCOUNT_CONTRACT), abi=ACCOUNT_ABI
    )
    approval = contract.functions.approveAgent(
        agent, delegator, name_bytes32, expires_at, initial_nonce, False
    )

    print("\n授权预览")
    print("  Chain ID   :", POPDEX_MAINNET_CHAIN_ID)
    print("  签署主账户 :", signer.address)
    print("  Agent      :", agent)
    print("  delegator  :", delegator)
    print("  名称       :", agent_name)
    print("  有效天数   :", args.days)
    print("  isGlobal   : False")
    print("  合约       :", ACCOUNT_CONTRACT)

    try:
        estimated_gas = approval.estimate_gas({"from": signer.address})
    except Exception as exc:
        raise SystemExit(f"\n授权模拟失败，交易未发送：\n{exc}") from exc
    print("  Gas 估算   :", estimated_gas)

    if not args.send:
        print("\n预演成功，未发送交易。确认地址后运行：panda-arb wallet authorize --send")
        return

    confirmation = tty_input("\n输入大写 AUTHORIZE 才会发送交易：")
    if confirmation != "AUTHORIZE":
        print("已取消，未发送任何交易")
        return

    latest_block = web3.eth.get_block("latest")
    base_fee = latest_block.get("baseFeePerGas") or Web3.to_wei(1, "gwei")
    transaction = approval.build_transaction(
        {
            "from": signer.address,
            "chainId": POPDEX_MAINNET_CHAIN_ID,
            "nonce": web3.eth.get_transaction_count(signer.address, "pending"),
            "gas": int(estimated_gas * 1.2),
            "type": 2,
            "maxFeePerGas": int(base_fee * 2),
            "maxPriorityFeePerGas": 0,
            "value": 0,
        }
    )
    signed = signer.sign_transaction(transaction)
    tx_hash = web3.eth.send_raw_transaction(signed.raw_transaction)
    print("\n交易已发送：", tx_hash.hex())
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=180)
    if receipt.status != 1:
        raise SystemExit(f"授权交易执行失败：{tx_hash.hex()}")
    print("授权交易成功，区块：", receipt.blockNumber)

    try:
        info = contract.functions.getAgentInfo(agent).call()
    except Exception as exc:
        print("交易成功，但读取 Agent 信息失败：", exc)
        return
    print("\n授权验证")
    print("  exists    :", info[0])
    print("  expiresAt :", info[1])
    print("  isExpired :", info[2])
    print("  delegator :", info[3])
    print("  isGlobal  :", info[5])


if __name__ == "__main__":
    main()
