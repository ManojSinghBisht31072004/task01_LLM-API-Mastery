# Day 1 – OpenAI API + Token Logging (Python)

A Python/Flask app that calls the OpenAI Chat Completions API and logs token usage on every request.

## Project Structure

```
day1-openai-python/
├── app.py              ← Entry point (loads .env, starts Flask)
├── openai_service.py   ← OpenAI call + token logging
├── chat_route.py       ← POST /chat route + error handling
├── requirements.txt    ← Dependencies
├── .env.example        ← Template for your .env (safe to commit)
└── .gitignore          ← Excludes .env and __pycache__
```

## Setup

```bash
# 1. Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create your .env file
cp .env.example .env
# Then edit .env and paste your real OpenAI API key

# 4. Start the server
python app.py
```

## Usage

### POST /chat
```bash
curl -X POST http://localhost:3000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the capital of France?"}'
```

**Response:**
```json
{
  "response": "The capital of France is Paris.",
  "tokens": {
    "prompt": 15,
    "completion": 9,
    "total": 24
  }
}
```

**Terminal log (every request):**
```
─────────────────────────────────────────────
[TOKEN LOG] 2024-06-01T10:23:45.123456+00:00
  Prompt tokens    : 15
  Completion tokens: 9
  Total tokens     : 24
─────────────────────────────────────────────
```

### GET /health
```bash
curl http://localhost:3000/health
# → {"status":"ok"}
```

## Error Responses

| Scenario             | Status | Message                                          |
|----------------------|--------|--------------------------------------------------|
| Missing/empty message | 400   | "Body must contain a non-empty 'message' string." |
| Invalid API key       | 401   | "Invalid or missing OpenAI API key."              |
| Rate limit exceeded   | 429   | "OpenAI rate limit exceeded."                     |
| Network failure       | 503   | "Could not reach the OpenAI API."                 |
| Other error           | 500   | "Something went wrong..."                         |

## Key Points
- **Never commit `.env`** — it's in `.gitignore`
- Token usage is logged to console on every request
- Server never crashes on API errors — all wrapped in try/except
