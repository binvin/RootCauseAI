<<<<<<< HEAD
# RootCause AI — Evidence-first incident investigation agent

Streamlit prototype for investigating uploaded technical logs using bounded read-only tools. Supports deterministic offline baseline and optional NVIDIA Nemotron agent via Nebius Token Factory.

## Run locally (Windows PowerShell)

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -q
python -m streamlit run app.py
```

Try `samples/tls_failure.log` or `samples/python_dependency.log` in **Offline baseline**. This mode is deterministic and **is not an LLM agent**.

## Enable Nebius inference

1. Obtain Nebius Token Factory access and confirm a Nemotron model is available.
2. In PowerShell set `$env:NEBIUS_API_KEY = '...'` locally. Never share or commit the key. Or copy `.env.example` to `.env` and use `python-dotenv` explicitly; this prototype reads OS environment variables directly.
3. Optionally set `NEBIUS_MODEL` to the exact model ID from the Nebius catalog and `NEBIUS_BASE_URL` if your account's API documentation specifies a different endpoint.
4. Restart Streamlit, select **Nebius Nemotron agent**, and upload sample logs.
5. Check that the investigation trace shows **model-selected tool calls**, not only offline baseline tool invocations.

> An API integration is implemented but has **not** been tested against your private Nebius account. Model availability, JSON tool-call compatibility and response formats must be verified live. Mock mode alone is not a qualifying Nebius hackathon submission.

## Architecture

```
Streamlit → selected mode
             ├─ Offline deterministic baseline → read-only log tools → report
             └─ Nebius/NVIDIA Nemotron → model tool selection → local read-only tools
                                           ↖ tool results / loop ↙ → report + trace
```

Tools: `search_logs`, `detect_patterns`, `extract_timeline`, `validate_evidence`. No shell or external target execution. Maximum five model/tool cycles; final model summary follows if budget is exhausted.

## Safety and privacy

Logs are untrusted input. Never upload production logs containing secrets, personal or confidential information. The prototype performs best-effort redaction of simple secrets but cannot guarantee sanitization. In Nebius mode, selected log content is transmitted to an external model service. Conclusions are hypotheses, not verified fixes, and must be reviewed by a human.

## Hackathon status

The Nebius x NVIDIA hackathon requires a working application making real Nebius Token Factory inference calls or deployed on Nebius AI Cloud, using an NVIDIA open-source model, plus a public demo and public open-source repo. This starter is **not submission-ready** until live Nemotron agent behavior and hosting are demonstrated.
=======
# RootCauseAI
Evidence-driven AI agent for technical incident investigation
>>>>>>> a1b880545e1ae60698e53458753cae4433e651e1
