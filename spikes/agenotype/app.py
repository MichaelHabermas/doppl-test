"""Web entrypoint for the Fusion demo on Render."""

from __future__ import annotations

import html
import io
import os
from contextlib import redirect_stderr, redirect_stdout

from dotenv import load_dotenv
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse

from fusion_demo import DEFAULT_PROMPT, DEFAULT_ROUNDS, make_client, run_loop
from html_trace import render_trace_html

load_dotenv()

app = FastAPI(title="Doppl Fusion Demo")

LANDING_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Doppl Fusion Demo</title>
  <style>
    :root {
      --bg: #0c0f14;
      --surface: #141a22;
      --border: #2a3544;
      --text: #e8edf4;
      --muted: #8b9bb0;
      --accent: #c084fc;
      --panel: #3dd68c;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "SF Pro Text", "Segoe UI", system-ui, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.55;
      min-height: 100vh;
    }
    .wrap { max-width: 760px; margin: 0 auto; padding: 3rem 1.25rem 4rem; }
    header { text-align: center; margin-bottom: 2rem; }
    header h1 { font-size: 1.85rem; font-weight: 650; margin: 0 0 0.35rem; }
    header p { color: var(--muted); margin: 0; }
    .pipeline {
      display: flex; flex-wrap: wrap; justify-content: center; gap: 0.5rem;
      margin: 1.25rem 0 2rem; font-size: 0.8rem;
    }
    .pipeline span {
      padding: 0.3rem 0.65rem; border-radius: 999px;
      border: 1px solid var(--border); background: var(--surface);
    }
    .pipeline .arrow { border: none; background: none; color: var(--muted); padding: 0 0.1rem; }
    form {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 1.5rem;
    }
    label {
      display: block;
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--accent);
      margin-bottom: 0.5rem;
      font-weight: 600;
    }
    textarea {
      width: 100%;
      min-height: 160px;
      resize: vertical;
      border: 1px solid var(--border);
      border-radius: 10px;
      background: #0c0f14;
      color: var(--text);
      padding: 0.85rem 1rem;
      font: inherit;
      line-height: 1.5;
    }
    .row { display: flex; gap: 1rem; align-items: end; margin-top: 1rem; flex-wrap: wrap; }
    .field { flex: 1; min-width: 120px; }
    input[type="number"] {
      width: 100%;
      border: 1px solid var(--border);
      border-radius: 10px;
      background: #0c0f14;
      color: var(--text);
      padding: 0.65rem 0.85rem;
      font: inherit;
    }
    button {
      border: none;
      border-radius: 10px;
      background: linear-gradient(135deg, #a855f7, #6366f1);
      color: white;
      font: inherit;
      font-weight: 600;
      padding: 0.75rem 1.35rem;
      cursor: pointer;
    }
    button:disabled { opacity: 0.6; cursor: wait; }
    .hint { color: var(--muted); font-size: 0.85rem; margin-top: 1rem; }
    .loading { display: none; margin-top: 1.25rem; color: var(--panel); font-size: 0.9rem; }
    form.submitting .loading { display: block; }
    form.submitting button { opacity: 0.7; }
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <h1>Doppl Fusion Demo</h1>
      <p>Parent agenomes → judge → critic → breed child on blind spots. Vague prompts work best.</p>
      <div class="pipeline">
        <span>Parents</span><span class="arrow">→</span>
        <span>Judge</span><span class="arrow">→</span>
        <span>Critic</span><span class="arrow">→</span>
        <span>Breed</span><span class="arrow">→</span>
        <span>Offspring</span>
      </div>
    </header>
    <form id="run-form" method="post" action="/run">
      <label for="prompt">Prompt</label>
      <textarea id="prompt" name="prompt" required>__DEFAULT_PROMPT__</textarea>
      <div class="row">
        <div class="field">
          <label for="rounds">Max rounds</label>
          <input id="rounds" name="rounds" type="number" min="1" max="5" value="__DEFAULT_ROUNDS__" />
        </div>
        <button type="submit">Run fusion</button>
      </div>
      <p class="loading">Running panel + judge + critic… this usually takes 1–3 minutes.</p>
      <p class="hint">Default prompt is vague on purpose so Gen 1 usually fails and a bred offspring runs in Gen 2.</p>
    </form>
  </div>
  <script>
    document.getElementById("run-form").addEventListener("submit", function () {
      this.classList.add("submitting");
      this.querySelector("button").disabled = true;
    });
  </script>
</body>
</html>"""


def _landing_page() -> str:
    return (
        LANDING_HTML.replace("__DEFAULT_PROMPT__", html.escape(DEFAULT_PROMPT.strip()))
        .replace("__DEFAULT_ROUNDS__", str(DEFAULT_ROUNDS))
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    return HTMLResponse(_landing_page())


@app.post("/run", response_class=HTMLResponse)
def run_fusion(
    prompt: str = Form(default=DEFAULT_PROMPT),
    rounds: int = Form(default=DEFAULT_ROUNDS),
) -> HTMLResponse:
    if not os.environ.get("OPENROUTER_API_KEY", "").strip():
        raise HTTPException(
            status_code=503,
            detail="OPENROUTER_API_KEY is not configured on this server.",
        )

    max_rounds = max(1, min(rounds, 5))
    with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
        with make_client() as client:
            trace = run_loop(client, prompt.strip(), max_rounds)

    return HTMLResponse(render_trace_html(trace))
