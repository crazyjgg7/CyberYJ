#!/usr/bin/env python3
"""
Run HTTP API adapter for Wechat mini-program.
"""

import uvicorn

from cyberYJ.api.http_app import create_app


if __name__ == "__main__":
    uvicorn.run(create_app(), host="0.0.0.0", port=8080)

