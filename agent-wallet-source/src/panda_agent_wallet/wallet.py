# MIT License; see OPEN_SOURCE_LICENSE.md at the product root.
from __future__ import annotations

import os
import stat
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

from panda_agent_wallet.paths import default_agent_env


@dataclass(frozen=True, slots=True)
class AgentInfo:
    address: str
    path: Path
    private_key_matches: bool
    permissions_private: bool


def _read_values(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        key, separator, value = raw.partition("=")
        if separator and key.strip() in {
            "POPDEX_AGENT_ADDRESS",
            "POPDEX_SIGNER_PRIVATE_KEY",
        }:
            values[key.strip()] = value.strip()
    return values


def _private_permissions(path: Path) -> bool:
    if os.name == "nt":
        # Windows ACLs do not map faithfully to POSIX mode bits. Creation uses
        # the current user's profile directory; installers should additionally
        # apply a user-only ACL.
        return True
    return stat.S_IMODE(path.stat().st_mode) & 0o077 == 0


def _harden_private_file(path: Path) -> None:
    if os.name != "nt":
        path.chmod(0o600)
        return
    # icacls accepts well-known SIDs independent of the Windows UI language.
    # Remove inherited entries and grant only the current owner and SYSTEM.
    username = os.environ.get("USERNAME")
    if not username:
        raise RuntimeError("无法确定当前 Windows 用户，Agent 文件权限未设置")
    completed = subprocess.run(
        [
            "icacls",
            str(path),
            "/inheritance:r",
            "/grant:r",
            f"{username}:(F)",
            "*S-1-5-18:(F)",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "无法将 Agent 文件限制为当前 Windows 用户："
            + (completed.stderr.strip() or completed.stdout.strip())
        )


def create_agent(path: Path | None = None, *, force: bool = False) -> AgentInfo:
    """Generate an Agent locally and atomically persist its env file."""
    try:
        from eth_account import Account
    except ImportError as exc:
        raise RuntimeError("缺少 eth-account；请使用完整发布包") from exc

    target = (path or default_agent_env()).expanduser().resolve()
    if target.exists() and not force:
        raise FileExistsError(f"Agent 配置已存在，拒绝覆盖：{target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    if os.name != "nt":
        target.parent.chmod(0o700)

    agent = Account.create()
    private_key = agent.key.hex()
    if not private_key.startswith("0x"):
        private_key = "0x" + private_key
    content = (
        f"POPDEX_AGENT_ADDRESS={agent.address}\n"
        f"POPDEX_SIGNER_PRIVATE_KEY={private_key}\n"
    )
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=".agent-", suffix=".tmp", dir=target.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        if os.name != "nt":
            temporary.chmod(0o600)
        temporary.replace(target)
        try:
            _harden_private_file(target)
        except Exception:
            target.unlink(missing_ok=True)
            raise
    finally:
        if temporary.exists():
            temporary.unlink()
        private_key = ""
        content = ""
    return AgentInfo(agent.address, target, True, _private_permissions(target))


def inspect_agent(path: Path | None = None) -> AgentInfo:
    """Validate address/key consistency without printing or returning the key."""
    try:
        from eth_account import Account
    except ImportError as exc:
        raise RuntimeError("缺少 eth-account；请使用完整发布包") from exc

    target = (path or default_agent_env()).expanduser().resolve()
    if not target.exists():
        raise FileNotFoundError(f"找不到 Agent 配置：{target}")
    values = _read_values(target)
    address = values.get("POPDEX_AGENT_ADDRESS")
    private_key = values.get("POPDEX_SIGNER_PRIVATE_KEY")
    if not address or not private_key:
        raise ValueError("Agent 配置缺少地址或私钥")
    try:
        derived = Account.from_key(private_key).address
    finally:
        private_key = ""
    return AgentInfo(
        address=address,
        path=target,
        private_key_matches=derived.lower() == address.lower(),
        permissions_private=_private_permissions(target),
    )
