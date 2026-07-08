"""
Innovation Blueprint Agent — Flask Backend
==========================================
IBM watsonx.ai + Granite/LLaMA models
"""

import os
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from agent_instructions import build_system_prompt

# ── Load environment variables ─────────────────────────────────────────────────
load_dotenv()

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# ── Flask App ─────────────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key-change-in-production")

# ── watsonx.ai Configuration ──────────────────────────────────────────────────
IBM_API_KEY        = os.getenv("IBM_API_KEY", "")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID", "")
WATSONX_URL        = os.getenv("WATSONX_URL", "https://eu-gb.ml.cloud.ibm.com")
WATSONX_MODEL_ID   = os.getenv("WATSONX_MODEL_ID", "meta-llama/llama-3-3-70b-instruct")

# ── Cached watsonx client ─────────────────────────────────────────────────────
_watsonx_client: ModelInference | None = None


def get_watsonx_model() -> ModelInference:
    global _watsonx_client
    if _watsonx_client is None:
        if not IBM_API_KEY or not WATSONX_PROJECT_ID:
            raise ValueError("IBM_API_KEY and WATSONX_PROJECT_ID must be set in your .env file.")
        credentials = Credentials(url=WATSONX_URL, api_key=IBM_API_KEY)
        _watsonx_client = ModelInference(
            model_id=WATSONX_MODEL_ID,
            credentials=credentials,
            project_id=WATSONX_PROJECT_ID,
            params={
                GenParams.MAX_NEW_TOKENS: 4096,
                GenParams.TEMPERATURE:    0.7,
                GenParams.TOP_P:          0.95,
                GenParams.TOP_K:          50,
                GenParams.REPETITION_PENALTY: 1.1,
            },
        )
        logger.info("watsonx.ai client initialized: %s", WATSONX_MODEL_ID)
    return _watsonx_client


def call_watsonx(user_message: str, mode: str = "chat") -> str:
    system_prompt = build_system_prompt(mode)
    full_prompt = f"{system_prompt}\n\n### User Input:\n{user_message}\n\n### Response:\n"
    model = get_watsonx_model()
    response = model.generate_text(prompt=full_prompt)
    return response.strip() if response else "No response generated."


# ── PAGE ROUTES ────────────────────────────────────────────────────────────────

@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/chat")
def chat():
    return render_template("chat.html")


@app.route("/validator")
def validator():
    return render_template("validator.html")


@app.route("/workflow")
def workflow():
    return render_template("workflow.html")


@app.route("/business-forge")
def business_forge():
    return render_template("business_forge.html")


@app.route("/pitch-builder")
def pitch_builder():
    return render_template("pitch_builder.html")


# ── API ENDPOINTS ─────────────────────────────────────────────────────────────

@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()
    if not user_message:
        return jsonify({"error": "Message cannot be empty."}), 400
    if len(user_message) > 4000:
        return jsonify({"error": "Message too long. Keep it under 4000 characters."}), 400
    try:
        reply = call_watsonx(user_message, mode="chat")
        return jsonify({"reply": reply, "timestamp": datetime.now().isoformat()})
    except ValueError as e:
        logger.error("Config error: %s", e)
        return jsonify({"error": f"Configuration error: {str(e)}"}), 500
    except Exception as e:
        logger.error("watsonx error (chat): %s", e)
        return jsonify({"error": "AI service temporarily unavailable. Please try again."}), 503


@app.route("/api/validate", methods=["POST"])
def api_validate():
    data = request.get_json(silent=True) or {}
    idea = (data.get("idea") or "").strip()
    if not idea:
        return jsonify({"error": "Idea description cannot be empty."}), 400
    try:
        reply = call_watsonx(idea, mode="validator")
        return jsonify({"result": reply, "timestamp": datetime.now().isoformat()})
    except Exception as e:
        logger.error("watsonx error (validator): %s", e)
        return jsonify({"error": "AI service temporarily unavailable. Please try again."}), 503


@app.route("/api/workflow", methods=["POST"])
def api_workflow():
    data = request.get_json(silent=True) or {}
    idea = (data.get("idea") or "").strip()
    if not idea:
        return jsonify({"error": "Process description cannot be empty."}), 400
    try:
        reply = call_watsonx(idea, mode="workflow")
        return jsonify({"result": reply, "timestamp": datetime.now().isoformat()})
    except Exception as e:
        logger.error("watsonx error (workflow): %s", e)
        return jsonify({"error": "AI service temporarily unavailable. Please try again."}), 503


@app.route("/api/business-forge", methods=["POST"])
def api_business_forge():
    data = request.get_json(silent=True) or {}
    idea = (data.get("idea") or "").strip()
    if not idea:
        return jsonify({"error": "Business idea cannot be empty."}), 400
    try:
        reply = call_watsonx(idea, mode="business_forge")
        return jsonify({"result": reply, "timestamp": datetime.now().isoformat()})
    except Exception as e:
        logger.error("watsonx error (business_forge): %s", e)
        return jsonify({"error": "AI service temporarily unavailable. Please try again."}), 503


@app.route("/api/pitch", methods=["POST"])
def api_pitch():
    data = request.get_json(silent=True) or {}
    idea = (data.get("idea") or "").strip()
    if not idea:
        return jsonify({"error": "Startup description cannot be empty."}), 400
    try:
        reply = call_watsonx(idea, mode="pitch")
        return jsonify({"result": reply, "timestamp": datetime.now().isoformat()})
    except Exception as e:
        logger.error("watsonx error (pitch): %s", e)
        return jsonify({"error": "AI service temporarily unavailable. Please try again."}), 503


@app.route("/api/health")
def health():
    return jsonify({
        "status":          "ok",
        "model":           WATSONX_MODEL_ID,
        "timestamp":       datetime.now().isoformat(),
        "api_key_set":     bool(IBM_API_KEY),
        "project_id_set":  bool(WATSONX_PROJECT_ID),
    })


# ── Error Handlers ─────────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error."}), 500


# ── Entry Point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    logger.info("Blueprint Agent starting on http://localhost:%d", port)
    app.run(host="0.0.0.0", port=port, debug=debug)
