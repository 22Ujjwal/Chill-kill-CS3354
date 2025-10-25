#!/usr/bin/env python3
"""
Simple test server - just test Flask connectivity
"""
from flask import Flask, jsonify
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    logger.info("Starting simple test server...")
    port = int(os.getenv("PORT", 8000))
    logger.info(f"Listening on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
