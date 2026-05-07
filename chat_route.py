from flask import Blueprint, request, jsonify
from gemini_service import chat

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/chat", methods=["POST"])
def chat_endpoint():
    data = request.get_json(silent=True)

    if not data or not isinstance(data.get("message"), str) or not data["message"].strip():
        return jsonify({
            "error":   "Bad Request",
            "message": "Body must contain a non-empty 'message' string.",
        }), 400

    try:
        result = chat(data["message"].strip())
        return jsonify({
            "response": result["content"],
            "tokens": {
                "prompt":     result["tokens"]["prompt"],
                "completion": result["tokens"]["completion"],
                "total":      result["tokens"]["total"],
            }
        }), 200

    except Exception as exc:
        print(f"[ERROR] {exc}")
        msg = str(exc).lower()
        if "api_key" in msg or "invalid" in msg or "api key" in msg:
            return jsonify({"error": "Unauthorized", "message": "Invalid Gemini API key."}), 401
        if "quota" in msg or "limit" in msg or "429" in msg:
            return jsonify({"error": "Rate Limited", "message": "Gemini quota exceeded."}), 429
        return jsonify({"error": "Internal Server Error", "message": str(exc)}), 500