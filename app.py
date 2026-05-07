import os
import sys
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY", "")
if not api_key or api_key == "your-gemini-api-key-here":
    print("❌  GEMINI_API_KEY is missing or not set in .env – exiting.")
    sys.exit(1)

from flask import Flask, jsonify
from chat_route import chat_bp

app = Flask(__name__)
app.register_blueprint(chat_bp)


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.errorhandler(404)
def not_found(_):
    return jsonify({"error": "Not Found"}), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    print(f"✅  Server running on http://localhost:{port}")
    print(f"    POST http://localhost:{port}/chat")
    print(f"    GET  http://localhost:{port}/health")
    app.run(host="0.0.0.0", port=port, debug=False)