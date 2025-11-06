#!/usr/bin/env python3
"""
Simple CLI client for the Nintendo RAG Chatbot backend.

Usage:
  python cli_chat.py                  # interactive mode
  python cli_chat.py --once "Your question here"   # one-shot question

Environment variables:
  CHATBOT_BASE_URL   Base URL for the backend (default: http://127.0.0.1:5002)
"""

import os
import sys
import json
import argparse
from typing import Optional

import requests


def get_base_url() -> str:
    return os.environ.get("CHATBOT_BASE_URL", "http://127.0.0.1:5002")


def health(base_url: str) -> dict:
    try:
        r = requests.get(f"{base_url}/api/health", timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}


def initialize(base_url: str, rebuild: bool = False) -> dict:
    try:
        payload = {"rebuild": bool(rebuild)}
        r = requests.post(f"{base_url}/api/initialize", json=payload, timeout=300)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}


def query(base_url: str, text: str) -> dict:
    try:
        payload = {"query": text}
        r = requests.post(f"{base_url}/api/query", json=payload, timeout=60)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}


def reset(base_url: str) -> dict:
    try:
        r = requests.post(f"{base_url}/api/reset", timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}


def ensure_initialized(base_url: str, auto_init: bool = True) -> None:
    h = health(base_url)
    ready = bool(h.get("chatbot_ready")) if isinstance(h, dict) else False
    if ready:
        return
    if not auto_init:
        print("Backend not initialized. Run POST /api/initialize first.")
        sys.exit(1)
    print("Initializing backend (this may take a minute)...")
    res = initialize(base_url, rebuild=False)
    if res.get("status") != "initialized":
        print("Initialization did not complete successfully:", res)
        # Don't exit; query endpoint will still report clear error.


def interactive_loop(base_url: str) -> int:
    print("\nNintendo RAG Chatbot CLI")
    print("Type your question and press Enter")
    print("Commands: /reset to clear conversation, /exit to quit\n")

    ensure_initialized(base_url, auto_init=True)

    while True:
        try:
            text = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            return 0

        if not text:
            continue
        if text.lower() in {"/exit", ":q", "quit"}:
            print("Bye!")
            return 0
        if text.lower() == "/reset":
            res = reset(base_url)
            print("Bot:", res.get("message", res))
            continue

        res = query(base_url, text)
        if res.get("status") == "success":
            print("Bot:", res.get("response", ""))
        else:
            print("Bot:", res.get("message", res))

    return 0


def one_shot(base_url: str, question: str) -> int:
    ensure_initialized(base_url, auto_init=True)
    res = query(base_url, question)
    if res.get("status") == "success":
        print(res.get("response", ""))
        return 0
    print(json.dumps(res, indent=2))
    return 1


def main(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(description="Nintendo RAG Chatbot CLI")
    parser.add_argument("--once", metavar="QUESTION", help="Ask a single question and exit")
    args = parser.parse_args(argv)

    base_url = get_base_url()

    if args.once:
        return one_shot(base_url, args.once)
    return interactive_loop(base_url)


if __name__ == "__main__":
    raise SystemExit(main())
