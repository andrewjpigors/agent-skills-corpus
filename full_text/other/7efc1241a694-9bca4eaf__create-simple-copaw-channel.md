---
name: "create-simple-copaw-channel"
description: "Creates a simple Copaw channel with WebSocket support. Invoke when user wants to create a new Copaw channel, add external client communication, or improve message display."
---

# Create Simple Copaw Channel

This skill helps you create a simple Copaw custom channel that communicates with external clients via WebSocket, with proper thinking/tool message handling for natural web display.

## Overview

A Copaw channel is a communication bridge that allows agents to interact with external systems. This skill creates a channel that:
- Listens for incoming messages via WebSocket
- Forwards messages to the Copaw agent
- Sends agent responses back to external clients
- Properly distinguishes thinking, tool, and message types for display

## Channel Structure

```
<channel_name>/
├── __init__.py           # Package initialization
├── channel.py            # Main channel implementation
├── test_ws_server.py     # Standalone test server
└── config.json           # Configuration template

install.bat               # Windows batch script
install.ps1               # Windows PowerShell script
install.sh                # Unix/Linux shell script
```

> **IMPORTANT**: All install scripts (`.bat`, `.ps1`, `.sh`) MUST use **English only**. Do NOT use Chinese characters or non-ASCII text in these scripts to avoid encoding issues on different systems.

## Required Files

### 1. channel.py

```python
# -*- coding: utf-8 -*-
"""<Channel Name>.

A custom channel that communicates with external clients via WebSocket.
"""
from __future__ import annotations

import asyncio
import json
import logging
import uuid
from typing import Any, Dict, Optional

import websockets

from agentscope_runtime.engine.schemas.agent_schemas import (
    ContentType,
    MessageType,
    TextContent,
)

from copaw.app.channels.base import BaseChannel
from copaw.app.channels.schema import ChannelType

logger = logging.getLogger(__name__)

TOOL_MESSAGE_TYPES = {
    MessageType.FUNCTION_CALL,
    MessageType.FUNCTION_CALL_OUTPUT,
    MessageType.PLUGIN_CALL,
    MessageType.PLUGIN_CALL_OUTPUT,
    MessageType.MCP_TOOL_CALL,
    MessageType.MCP_TOOL_CALL_OUTPUT,
}


class <ChannelName>Channel(BaseChannel):
    """Custom channel that communicates with external clients via WebSocket."""

    channel: ChannelType = "<channel_name>"

    def __init__(
        self,
        process: Any,
        enabled: bool = True,
        bot_prefix: str = "",
        ws_port: int = 7887,
        show_tool_details: bool = True,
        filter_tool_messages: bool = False,
        filter_thinking: bool = False,
        dm_policy: str = "open",
        group_policy: str = "open",
        allow_from: Optional[list] = None,
        deny_message: str = "",
        require_mention: bool = False,
        on_reply_sent: Optional[Any] = None,
    ):
        super().__init__(
            process,
            on_reply_sent=on_reply_sent,
            show_tool_details=show_tool_details,
            filter_tool_messages=filter_tool_messages,
            filter_thinking=filter_thinking,
            dm_policy=dm_policy,
            group_policy=group_policy,
            allow_from=allow_from,
            deny_message=deny_message,
            require_mention=require_mention,
        )
        self.enabled = enabled
        self.bot_prefix = bot_prefix
        self.ws_port = ws_port
        self._server_task: Optional[asyncio.Task] = None
        self._server: Any = None
        self._clients: Dict[str, Any] = {}
        self._server_running = False

    @classmethod
    def from_config(
        cls,
        process: Any,
        config: Any,
        on_reply_sent: Optional[Any] = None,
        show_tool_details: bool = True,
        filter_tool_messages: bool = False,
        filter_thinking: bool = False,
        **kwargs: Any,
    ) -> "<ChannelName>Channel":
        return cls(
            process=process,
            enabled=getattr(config, "enabled", True),
            bot_prefix=getattr(config, "bot_prefix", ""),
            ws_port=getattr(config, "ws_port", 7887),
            show_tool_details=show_tool_details,
            filter_tool_messages=filter_tool_messages,
            filter_thinking=filter_thinking,
            dm_policy=getattr(config, "dm_policy", "open"),
            group_policy=getattr(config, "group_policy", "open"),
            allow_from=getattr(config, "allow_from", []),
            deny_message=getattr(config, "deny_message", ""),
            require_mention=getattr(config, "require_mention", False),
            on_reply_sent=on_reply_sent,
        )

    def build_agent_request_from_native(self, native_payload: Any) -> Any:
        payload = native_payload if isinstance(native_payload, dict) else {}
        channel_id = payload.get("channel_id") or self.channel
        sender_id = payload.get("sender_id") or ""
        meta = payload.get("meta") or {}
        session_id = self.resolve_session_id(sender_id, meta)
        text = payload.get("text", "")
        content_parts = [TextContent(type=ContentType.TEXT, text=text)]
        request = self.build_agent_request_from_user_content(
            channel_id=channel_id,
            sender_id=sender_id,
            session_id=session_id,
            content_parts=content_parts,
            channel_meta=meta,
        )
        request.channel_meta = meta
        return request

    async def start(self) -> None:
        if not self.enabled:
            logger.info("<ChannelName>Channel is disabled")
            return

        logger.info(f"Starting <ChannelName>Channel WebSocket server on port {self.ws_port}")
        self._server_running = True
        self._server = websockets.serve(
            self._handle_client,
            "0.0.0.0",
            self.ws_port,
            ping_interval=30,
            ping_timeout=10,
        )
        self._server_task = asyncio.create_task(self._run_server())

    async def stop(self) -> None:
        logger.info("Stopping <ChannelName>Channel WebSocket server")
        self._server_running = False

        for client_id, websocket in list(self._clients.items()):
            try:
                await websocket.close(1001, "Server shutting down")
            except Exception as e:
                logger.debug(f"Error closing client {client_id}: {e}")

        self._clients.clear()

        if hasattr(self, '_server') and self._server:
            self._server.close()
            try:
                await asyncio.wait_for(self._server.wait_closed(), timeout=5)
            except asyncio.TimeoutError:
                logger.warning("Server close timed out")
            except Exception as e:
                logger.debug(f"Server close error: {e}")

        if self._server_task:
            self._server_task.cancel()
            try:
                await self._server_task
            except asyncio.CancelledError:
                pass
            self._server_task = None

    async def _run_server(self) -> None:
        try:
            async with self._server:
                logger.info(f"<ChannelName>Channel WebSocket server running on ws://0.0.0.0:{self.ws_port}")
                while self._server_running:
                    await asyncio.sleep(1)
        except asyncio.CancelledError:
            logger.info("Server task cancelled")
            raise
        except Exception as e:
            logger.error(f"Server error: {e}")

    async def _handle_client(
        self,
        websocket: Any,
    ) -> None:
        client_id = str(uuid.uuid4())[:8]
        self._clients[client_id] = websocket
        logger.info(f"Client {client_id} connected")

        try:
            async for raw_message in websocket:
                try:
                    message = json.loads(raw_message)
                    msg_type = message.get("type", "")

                    if msg_type == "chat":
                        sender_id = message.get("sender_id", client_id)
                        text = message.get("text", "")
                        request_id = message.get("request_id") or str(uuid.uuid4())
                        meta = dict(message.get("meta", {}))

                        meta["client_id"] = client_id
                        meta["bot_prefix"] = self.bot_prefix
                        meta["request_id"] = request_id

                        payload = {
                            "channel_id": self.channel,
                            "sender_id": sender_id,
                            "text": text,
                            "meta": meta,
                        }

                        request = self.build_agent_request_from_native(payload)
                        self._enqueue(request)

                    elif msg_type == "ping":
                        await websocket.send(json.dumps({
                            "type": "pong",
                            "timestamp": message.get("timestamp"),
                        }))

                    elif msg_type == "close":
                        break

                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON from client {client_id}")
                    await websocket.send(json.dumps({
                        "type": "error",
                        "error": "Invalid JSON format",
                    }))

        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Client {client_id} disconnected")
        except Exception as e:
            logger.error(f"Error handling client {client_id}: {e}")
        finally:
            self._clients.pop(client_id, None)
            logger.info(f"Client {client_id} cleanup complete")

    async def _send_ws_payload(
        self,
        client_id: str,
        payload: Dict[str, Any],
    ) -> None:
        websocket = self._clients.get(client_id)
        if not websocket:
            logger.debug("No active websocket for client_id=%s", client_id)
            return
        await websocket.send(json.dumps(payload, ensure_ascii=False))

    async def _send_text_message(
        self,
        text: str,
        meta: Optional[Dict[str, Any]] = None,
        ws_type: str = "message",
    ) -> None:
        meta = meta or {}
        client_id = meta.get("client_id")
        if not client_id:
            logger.debug("Missing client_id for ws_type=%s", ws_type)
            return

        payload = {
            "type": ws_type,
            "text": text,
            "bot_prefix": meta.get("bot_prefix", self.bot_prefix),
            "request_id": meta.get("request_id"),
            "session_id": meta.get("session_id"),
            "message_type": meta.get("message_type")
            or (
                "reasoning"
                if ws_type == "thinking"
                else MessageType.MESSAGE
            ),
        }
        try:
            await self._send_ws_payload(client_id, payload)
        except Exception as e:
            logger.error(
                "Failed to send %s message to client %s: %s",
                ws_type,
                client_id,
                e,
            )

    async def send(
        self,
        to_handle: str,
        text: str,
        meta: Optional[Dict[str, Any]] = None,
    ) -> None:
        del to_handle
        if not text.strip():
            return
        await self._send_text_message(text.strip(), meta, ws_type="message")

    async def on_event_message_completed(
        self,
        request: Any,
        to_handle: str,
        event: Any,
        send_meta: Dict[str, Any],
    ) -> None:
        session_id = getattr(request, "session_id", None)
        parts = self._message_to_content_parts(event)
        if not parts:
            return
        msg_type = getattr(event, "type", None)
        if msg_type == MessageType.REASONING:
            ws_type = "thinking"
        elif msg_type in TOOL_MESSAGE_TYPES:
            ws_type = "tool"
        else:
            ws_type = "message"
        await self.send_content_parts(
            to_handle,
            parts,
            {
                **send_meta,
                "ws_type": ws_type,
                "message_type": msg_type,
                "session_id": session_id,
            },
        )

    async def _on_consume_error(
        self,
        request: Any,
        to_handle: str,
        err_text: str,
    ) -> None:
        del to_handle
        meta = getattr(request, "channel_meta", None) or {}
        client_id = meta.get("client_id")
        if not client_id:
            return
        try:
            await self._send_ws_payload(
                client_id,
                {
                    "type": "error",
                    "error": err_text,
                    "request_id": meta.get("request_id"),
                    "session_id": getattr(request, "session_id", None),
                },
            )
        except Exception as e:
            logger.error("Failed to send error to client %s: %s", client_id, e)

    async def send_content_parts(
        self,
        to_handle: str,
        parts: list,
        meta: Optional[Dict[str, Any]] = None,
    ) -> None:
        del to_handle
        meta = meta or {}
        body = self._renderer.parts_to_text(
            parts,
            prefix=meta.get("bot_prefix", self.bot_prefix) or "",
        )
        if not body:
            return
        await self._send_text_message(
            body,
            meta,
            ws_type=meta.get("ws_type", "message"),
        )
```

### 2. __init__.py

```python
# -*- coding: utf-8 -*-
"""<Channel Name> Channel package."""

from .channel import <ChannelName>Channel

__all__ = ["<ChannelName>Channel"]
```

### 3. config.json

```json
{
  "<channel_name>": {
    "enabled": true,
    "bot_prefix": "",
    "ws_port": 7887,
    "show_tool_details": true,
    "filter_tool_messages": false,
    "filter_thinking": false
  }
}
```

### 4. test_ws_server.py (Standalone Test Server)

```python
# -*- coding: utf-8 -*-
"""Standalone WebSocket server for testing the client.

Run this to test the client without needing the full Copaw setup.
"""
from __future__ import annotations

import asyncio
import json
import logging
import uuid
from typing import Any
import websockets

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def handle_client(websocket: Any) -> None:
    client_id = str(uuid.uuid4())[:8]
    logger.info(f"Client {client_id} connected")

    try:
        async for raw_message in websocket:
            try:
                message = json.loads(raw_message)
                msg_type = message.get("type", "")

                if msg_type == "chat":
                    sender_id = message.get("sender_id", client_id)
                    text = message.get("text", "")

                    await websocket.send(json.dumps({
                        "type": "response",
                        "request_id": str(uuid.uuid4()),
                        "session_id": f"test:{sender_id}",
                        "text": f"Echo: {text}",
                        "sender_id": sender_id,
                    }))

                elif msg_type == "ping":
                    await websocket.send(json.dumps({
                        "type": "pong",
                        "timestamp": message.get("timestamp"),
                    }))

                elif msg_type == "close":
                    break

            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON from client {client_id}")
                await websocket.send(json.dumps({
                    "type": "error",
                    "error": "Invalid JSON format",
                }))

    except websockets.exceptions.ConnectionClosed:
        logger.info(f"Client {client_id} disconnected")
    except Exception as e:
        logger.error(f"Error handling client {client_id}: {e}")

    logger.info(f"Client {client_id} cleanup complete")


async def main():
    port = 7887
    logger.info(f"Starting test WebSocket server on port {port}")

    async with websockets.serve(
        handle_client,
        "0.0.0.0",
        port,
        ping_interval=30,
        ping_timeout=10,
    ):
        logger.info(f"Test server running on ws://0.0.0.0:{port}")
        logger.info("Open client/index.html in browser to test")
        await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped")
```

### 5. install.bat (Windows Batch Script)

```batch
@echo off
setlocal

set "CHANNEL_NAME=<channel_name>"
set "SCRIPT_DIR=%~dp0"
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

set "SOURCE_DIR=%SCRIPT_DIR%\%CHANNEL_NAME%"
set "TARGET_ROOT=%USERPROFILE%\.copaw\custom_channels"
set "TARGET_DIR=%TARGET_ROOT%\%CHANNEL_NAME%"

echo ========================================
echo Install %CHANNEL_NAME%
echo ========================================
echo.

if not exist "%SOURCE_DIR%\" (
    echo ERROR: source directory not found: "%SOURCE_DIR%"
    echo Please keep install.bat beside the %CHANNEL_NAME% directory.
    exit /b 1
)

if not exist "%TARGET_ROOT%" (
    mkdir "%TARGET_ROOT%"
    if errorlevel 1 (
        echo ERROR: failed to create "%TARGET_ROOT%"
        exit /b 1
    )
)

if exist "%TARGET_DIR%\" (
    echo Remove old target: "%TARGET_DIR%"
    rmdir /s /q "%TARGET_DIR%"
)

echo Copy channel directory to:
echo   %TARGET_DIR%
robocopy "%SOURCE_DIR%" "%TARGET_DIR%" /E /NFL /NDL /NJH /NJS /NC /NS >nul

if errorlevel 8 (
    echo ERROR: robocopy failed with exit code %ERRORLEVEL%
    exit /b %ERRORLEVEL%
)

echo.
echo Done.
echo Installed to: %TARGET_DIR%
echo.
echo Next steps:
echo 1. Edit %%USERPROFILE%%\.copaw\config.json
echo    Add the %CHANNEL_NAME% channel config under channels.
echo 2. Edit your agent workspace agent.json
echo    Enable %CHANNEL_NAME% under channels.
echo 3. Restart Copaw after updating the configs.
exit /b 0
```

### 6. install.ps1 (Windows PowerShell Script)

```powershell
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$ChannelName = "<channel_name>"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SourceDir = Join-Path $ScriptDir $ChannelName
$TargetRoot = Join-Path $env:USERPROFILE ".copaw\custom_channels"
$TargetDir = Join-Path $TargetRoot $ChannelName

Write-Host "========================================"
Write-Host "Install $ChannelName"
Write-Host "========================================"
Write-Host ""

if (-not (Test-Path -LiteralPath $SourceDir -PathType Container)) {
    Write-Error "ERROR: source directory not found: $SourceDir"
}

if (-not (Test-Path -LiteralPath $TargetRoot -PathType Container)) {
    New-Item -ItemType Directory -Path $TargetRoot -Force | Out-Null
}

Write-Host "Copy channel directory to:"
Write-Host "  $TargetDir"

$null = New-Item -ItemType Directory -Path $TargetDir -Force
robocopy $SourceDir $TargetDir /MIR /NFL /NDL /NJH /NJS /NC /NS | Out-Null

if ($LASTEXITCODE -ge 8) {
    throw "robocopy failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "Done."
Write-Host "Installed to: $TargetDir"
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Edit $env:USERPROFILE\.copaw\config.json"
Write-Host "   Add the $ChannelName channel config under channels."
Write-Host "2. Edit your agent workspace agent.json"
Write-Host "   Enable $ChannelName under channels."
Write-Host "3. Restart Copaw after updating the configs."
```

### 7. install.sh (Unix/Linux Shell Script)

```bash
#!/usr/bin/env bash

set -e

CHANNEL_NAME="<channel_name>"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
SOURCE_DIR="$SCRIPT_DIR/$CHANNEL_NAME"

resolve_home_dir() {
    if [ -n "${USERPROFILE:-}" ]; then
        if command -v cygpath >/dev/null 2>&1; then
            cygpath -u "$USERPROFILE"
            return
        fi
        printf '%s\n' "$USERPROFILE" | sed 's#\\#/#g'
        return
    fi

    if command -v cmd.exe >/dev/null 2>&1; then
        win_profile="$(cmd.exe /c echo %USERPROFILE% 2>/dev/null | tr -d '\r')"
        if [ -n "$win_profile" ]; then
            if command -v cygpath >/dev/null 2>&1; then
                cygpath -u "$win_profile"
                return
            fi
            printf '%s\n' "$win_profile" | sed 's#\\#/#g'
            return
        fi
    fi

    if [ -n "${HOME:-}" ]; then
        printf '%s\n' "$HOME"
        return
    fi

    cd ~ && pwd
}

BASE_HOME="$(resolve_home_dir)"
TARGET_ROOT="$BASE_HOME/.copaw/custom_channels"
TARGET_DIR="$TARGET_ROOT/$CHANNEL_NAME"

echo "========================================"
echo "Install $CHANNEL_NAME"
echo "========================================"
echo ""

if [ ! -d "$SOURCE_DIR" ]; then
    echo "ERROR: source directory not found: $SOURCE_DIR"
    echo "Please keep install.sh beside the $CHANNEL_NAME directory."
    exit 1
fi

mkdir -p "$TARGET_ROOT"

if [ -d "$TARGET_DIR" ]; then
    echo "Remove old target: $TARGET_DIR"
    rm -rf "$TARGET_DIR"
fi

echo "Copy channel directory to:"
echo "  $TARGET_DIR"
cp -R "$SOURCE_DIR" "$TARGET_DIR"

echo ""
echo "Done."
echo "Installed to: $TARGET_DIR"
echo ""
echo "Next steps:"
echo "1. Edit ~/.copaw/config.json"
echo "   Add the $CHANNEL_NAME channel config under channels."
echo "2. Edit your agent workspace agent.json"
echo "   Enable $CHANNEL_NAME under channels."
echo "3. Restart Copaw after updating the configs."
```

## WebSocket Protocol

### Client to Server

**Send Chat Message:**
```json
{
  "type": "chat",
  "request_id": "req_1234567890",
  "sender_id": "user123",
  "text": "Hello",
  "meta": {}
}
```

**Ping (Heartbeat):**
```json
{
  "type": "ping",
  "timestamp": 1234567890
}
```

### Server to Client

**Message Response:**
```json
{
  "type": "message",
  "text": "Hello! How can I help you?",
  "bot_prefix": "",
  "request_id": "req_1234567890",
  "session_id": "session_xxx",
  "message_type": "message"
}
```

**Thinking (Agent reasoning process):**
```json
{
  "type": "thinking",
  "text": "The user is asking about...",
  "bot_prefix": "",
  "request_id": "req_1234567890",
  "session_id": "session_xxx",
  "message_type": "reasoning"
}
```

**Tool (Tool execution details):**
```json
{
  "type": "tool",
  "text": "🔧 **search**: Searching for...",
  "bot_prefix": "",
  "request_id": "req_1234567890",
  "session_id": "session_xxx",
  "message_type": "function_call"
}
```

**Error Response:**
```json
{
  "type": "error",
  "error": "Error message",
  "request_id": "req_xxx",
  "session_id": "session_xxx"
}
```

**Pong (Heartbeat Response):**
```json
{
  "type": "pong",
  "timestamp": 1234567890
}
```

## Installation

### Option 1: Using Installation Scripts (Recommended)

Place all three install scripts in the project root directory (same level as `<channel_name>/` folder):

| Platform | Script | Command |
|----------|--------|---------|
| Windows (CMD) | `install.bat` | Double-click or run `install.bat` |
| Windows (PowerShell) | `install.ps1` | Run `.\install.ps1` |
| Linux/Mac | `install.sh` | Run `chmod +x install.sh && ./install.sh` |

The script will copy the entire `<channel_name>/` folder to `~/.copaw/custom_channels/`

### Option 2: Manual Installation

1. Create the channel directory in Copaw's custom channels folder:
   ```
   ~/.copaw/custom_channels/<channel_name>/
   ```

2. Copy your channel files there:
   - `channel.py`
   - `__init__.py`
   - `config.json`

3. **Manually configure channels** (see Configuration section below)

4. Restart Copaw

## Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| enabled | true | Whether the channel is enabled |
| ws_port | 7887 | WebSocket server port |
| bot_prefix | "" | Prefix for bot messages |
| show_tool_details | true | Show tool execution details |
| filter_tool_messages | false | Filter out tool messages |
| filter_thinking | false | Filter out thinking messages |

## Configuration (Required After Installation)

After running the install script or copying files, you MUST configure the channel in **TWO** places:

### 1. Configure in `~/.copaw/config.json`

Open `~/.copaw/config.json` and add the channel configuration to the `channels` section:

```json
{
  "channels": {
    "<channel_name>": {
      "enabled": true,
      "bot_prefix": "",
      "ws_port": 7887,
      "show_tool_details": true,
      "filter_tool_messages": false,
      "filter_thinking": false
    }
  }
}
```

**Example with existing channels:**
```json
{
  "channels": {
    "myowncopawchannel1": {
      "enabled": true,
      "ws_port": 7887
    },
    "<channel_name>": {
      "enabled": true,
      "ws_port": 7888
    }
  }
}
```

### 2. Configure in Your Agent's `agent.json`

Open your agent's `agent.json` (in the agent's workspace folder) and add the channel to the `channels` section:

```json
{
  "channels": {
    "<channel_name>": {
      "enabled": true,
      "ws_port": 7887
    }
  }
}
```

### ⚠️ Important Reminders

- **Both configurations are required!** Without them, the channel won't work.
- If `config.json` has syntax errors, Copaw may fail to start.
- After making changes, **restart Copaw** to apply the configuration.
- The `ws_port` must be unique across all channels.

## Critical Patterns (Avoid Common Mistakes)

### 1. Do NOT Detect Thinking by Text Prefix

**WRONG** - Unreliable text matching:
```python
async def send(self, to_handle: str, text: str, meta: Optional[Dict[str, Any]] = None) -> None:
    is_thinking = text.strip().startswith("Thinking")
    await self._send_text_message(text, meta, ws_type="thinking" if is_thinking else "message")
```

**CORRECT** - Use `MessageType.REASONING` from event type:
```python
async def on_event_message_completed(
    self,
    request: Any,
    to_handle: str,
    event: Any,
    send_meta: Dict[str, Any],
) -> None:
    msg_type = getattr(event, "type", None)
    if msg_type == MessageType.REASONING:
        ws_type = "thinking"
    elif msg_type in TOOL_MESSAGE_TYPES:
        ws_type = "tool"
    else:
        ws_type = "message"
    # ... send with proper ws_type
```

### 2. Always Include request_id in Messages

**WRONG** - Missing request tracking causes UI sync issues:
```python
payload = {
    "type": ws_type,
    "text": text,
}
```

**CORRECT** - Include request_id for tracking:
```python
payload = {
    "type": ws_type,
    "text": text,
    "request_id": meta.get("request_id"),
    "session_id": meta.get("session_id"),
    "message_type": meta.get("message_type"),
}
```

### 3. Define TOOL_MESSAGE_TYPES Constant

```python
TOOL_MESSAGE_TYPES = {
    MessageType.FUNCTION_CALL,
    MessageType.FUNCTION_CALL_OUTPUT,
    MessageType.PLUGIN_CALL,
    MessageType.PLUGIN_CALL_OUTPUT,
    MessageType.MCP_TOOL_CALL,
    MessageType.MCP_TOOL_CALL_OUTPUT,
}
```

### 4. Override build_agent_request_from_native

```python
def build_agent_request_from_native(self, native_payload: Any) -> Any:
    payload = native_payload if isinstance(native_payload, dict) else {}
    channel_id = payload.get("channel_id") or self.channel
    sender_id = payload.get("sender_id") or ""
    meta = payload.get("meta") or {}
    session_id = self.resolve_session_id(sender_id, meta)
    text = payload.get("text", "")
    content_parts = [TextContent(type=ContentType.TEXT, text=text)]
    request = self.build_agent_request_from_user_content(
        channel_id=channel_id,
        sender_id=sender_id,
        session_id=session_id,
        content_parts=content_parts,
        channel_meta=meta,
    )
    request.channel_meta = meta
    return request
```

## Example Client (Modern UI)

A modern web client with proper thinking/tool message display:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><Channel Name> Client</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            width: 100%;
            max-width: 600px;
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px 30px;
            text-align: center;
        }
        .status {
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 14px;
            background: rgba(255, 255, 255, 0.2);
        }
        .status.connected { background: rgba(76, 175, 80, 0.9); }
        .status.disconnected { background: rgba(244, 67, 54, 0.9); }
        .chat-area {
            height: 400px;
            overflow-y: auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .message { margin-bottom: 15px; animation: fadeIn 0.3s ease; }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .message.user { text-align: right; }
        .message.bot { text-align: left; }
        .message .bubble {
            display: inline-block;
            padding: 12px 18px;
            border-radius: 18px;
            max-width: 80%;
            word-wrap: break-word;
            line-height: 1.5;
        }
        .message.user .bubble {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-bottom-right-radius: 4px;
        }
        .message.bot .bubble {
            background: white;
            color: #333;
            border: 1px solid #e0e0e0;
            border-bottom-left-radius: 4px;
        }
        .message .sender { font-size: 12px; color: #999; margin-bottom: 4px; }
        .input-area {
            padding: 20px;
            background: white;
            border-top: 1px solid #e0e0e0;
        }
        .input-wrapper { display: flex; gap: 10px; }
        .input-wrapper input {
            flex: 1;
            padding: 15px 20px;
            border: 2px solid #e0e0e0;
            border-radius: 30px;
            font-size: 16px;
            outline: none;
        }
        .input-wrapper button {
            padding: 15px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 30px;
            font-size: 16px;
            cursor: pointer;
        }
        .typing {
            text-align: center;
            padding: 10px;
            color: #999;
            font-size: 14px;
        }
        .message.thinking .bubble {
            background: linear-gradient(135deg, #fff9e6 0%, #fff3cd 100%);
            color: #856404;
            font-style: italic;
            border: 2px solid #ffc107;
        }
        .message.thinking .sender { color: #856404; font-weight: 600; }
        .message.tool .bubble {
            background: linear-gradient(135deg, #eef6ff 0%, #dbeafe 100%);
            color: #1e3a8a;
            border: 2px solid #60a5fa;
        }
        .message.tool .sender { color: #1d4ed8; font-weight: 600; }
        .thinking-content, .tool-content {
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid rgba(0,0,0,0.1);
            white-space: pre-wrap;
            font-size: 13px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 <Channel Name></h1>
            <span id="status" class="status disconnected">🔴 未连接</span>
        </div>
        <div id="chatArea" class="chat-area"></div>
        <div id="typingIndicator" class="typing" style="display: none;">正在输入...</div>
        <div class="input-area">
            <div class="input-wrapper">
                <input type="text" id="messageInput" placeholder="输入消息..." disabled>
                <button id="sendBtn" disabled>发送</button>
            </div>
        </div>
    </div>

    <script>
        const chatArea = document.getElementById('chatArea');
        const messageInput = document.getElementById('messageInput');
        const sendBtn = document.getElementById('sendBtn');
        const statusEl = document.getElementById('status');
        const typingIndicator = document.getElementById('typingIndicator');

        let ws = null;
        let senderId = 'user_' + Math.random().toString(36).substring(2, 8);
        let pendingRequests = new Map();

        function updateStatus(connected) {
            statusEl.textContent = connected ? '🟢 已连接' : '🔴 未连接';
            statusEl.className = 'status ' + (connected ? 'connected' : 'disconnected');
            messageInput.disabled = !connected;
            sendBtn.disabled = !connected;
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        function addMessage(text, sender, isUser = false, messageKind = 'normal') {
            const msgDiv = document.createElement('div');
            msgDiv.className = `message ${isUser ? 'user' : 'bot'} ${messageKind !== 'normal' ? messageKind : ''}`;

            let senderLabel, icon;
            if (messageKind === 'thinking') {
                senderLabel = 'Thinking';
                icon = '💭';
            } else if (messageKind === 'tool') {
                senderLabel = 'Tool';
                icon = '🛠️';
            } else {
                senderLabel = sender === 'user' ? '你' : 'Bot';
                icon = sender === 'user' ? '👤' : '🤖';
            }

            const content = messageKind !== 'normal'
                ? `<details style="margin-top:8px"><summary style="cursor:pointer">查看详情</summary><div class="${messageKind}-content">${escapeHtml(text)}</div></details>`
                : escapeHtml(text);

            msgDiv.innerHTML = `
                <div class="sender">${icon} ${senderLabel}</div>
                <div class="bubble">${content}</div>
            `;
            chatArea.appendChild(msgDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }

        function showTyping(show) {
            typingIndicator.style.display = show ? 'block' : 'none';
        }

        function trackPendingRequest(requestId) {
            const timeoutId = setTimeout(() => {
                pendingRequests.delete(requestId);
                if (pendingRequests.size === 0) showTyping(false);
                addMessage('请求超时', 'system');
            }, 120000);
            pendingRequests.set(requestId, timeoutId);
            showTyping(true);
        }

        function clearPendingRequest(requestId) {
            if (requestId) {
                const timeoutId = pendingRequests.get(requestId);
                if (timeoutId) {
                    clearTimeout(timeoutId);
                    pendingRequests.delete(requestId);
                }
            }
            if (pendingRequests.size === 0) showTyping(false);
        }

        function connect() {
            try {
                ws = new WebSocket('ws://localhost:7887');
            } catch (e) {
                updateStatus(false);
                return;
            }

            ws.onopen = () => {
                updateStatus(true);
                addMessage('已连接', 'system');
            };

            ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    handleMessage(data);
                } catch (e) {}
            };

            ws.onclose = () => {
                updateStatus(false);
                setTimeout(connect, 3000);
            };
        }

        function handleMessage(data) {
            if (data.type === 'pong') return;

            if (data.type === 'response' || data.type === 'message') {
                clearPendingRequest(data.request_id);
                if (data.text) addMessage(data.text, 'bot');
            }

            if (data.type === 'thinking') {
                clearPendingRequest(data.request_id);
                addMessage(data.text, 'bot', false, 'thinking');
            }

            if (data.type === 'tool') {
                clearPendingRequest(data.request_id);
                addMessage(data.text, 'bot', false, 'tool');
            }

            if (data.type === 'error') {
                clearPendingRequest(data.request_id);
                addMessage('错误: ' + data.error, 'system');
            }
        }

        function sendMessage() {
            const text = messageInput.value.trim();
            if (!text || !ws || ws.readyState !== WebSocket.OPEN) return;

            const requestId = 'req_' + Date.now();
            const message = {
                type: 'chat',
                request_id: requestId,
                sender_id: senderId,
                text: text,
                meta: {}
            };

            addMessage(text, 'user', true);
            messageInput.value = '';
            trackPendingRequest(requestId);
            ws.send(JSON.stringify(message));
        }

        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
        sendBtn.addEventListener('click', sendMessage);
        connect();
    </script>
</body>
</html>
```

## Notes

- The channel class name MUST end with `Channel` (e.g., `MyChannelChannel`)
- The `channel` attribute MUST match the config key (e.g., `"my_channel"`)
- WebSocket port must be unique across all channels
- Use `MessageType.REASONING` for thinking detection, NOT text prefix
- Always include `request_id` in messages for proper UI tracking
- Tool messages are grouped and displayed with collapsible details
