import os
import sys
from flask import Flask, request
from bot import application

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
async def handle_webhook():
    await application.initialize()
    await application.process_update(request.get_json(force=True))
    return "ok", 200
