# RootCause AI – Agentic Log Investigation with Reachy Mini

**A conversational robotic assistant that investigates application failures using NVIDIA Nemotron 3 Super through Nebius Token Factory.**

RootCause AI brings agentic troubleshooting into the physical world. Instead of manually searching through application logs, users can simply ask Reachy Mini to investigate an incident and explain its findings.

The project also includes a Streamlit web application for interactive log analysis and detailed report inspection.

## Demo

**Demo video:** https://www.youtube.com/watch?v=FW8zpWtonnM

**Live Streamlit application:** https://rootcause-ai-demo.streamlit.app/

**Architecture:** 
<img width="1672" height="941" alt="arch" src="https://github.com/user-attachments/assets/edf7310b-ff4a-4a0f-a2f4-3e04c4619ec2" />


## Inspiration

Application troubleshooting often involves reviewing extensive error logs, identifying related failures, reconstructing timelines, and determining likely root causes.

I wanted to explore a different approach:

**What if an engineer could simply ask a robot to investigate an application failure?**

RootCause AI combines physical robotics, natural voice interaction, and autonomous investigation tools to create an interactive technical troubleshooting assistant.

## What It Does

Users can interact naturally with Reachy Mini.

**User:** "Reachy, investigate the error log."

Reachy invokes the RootCause AI backend, which uses NVIDIA Nemotron to investigate the configured log file.

The agent autonomously selects appropriate read-only tools, analyzes their results, and generates a structured investigation report.

**User:** "Why did the application return HTTP 500 errors?"

Reachy answers using the previous investigation context, without rerunning the complete investigation.

### Key Features

- Voice-triggered log investigations through Reachy Mini
- Autonomous, multi-step tool selection by NVIDIA Nemotron
- Error-pattern detection and incident timeline reconstruction
- Evidence-backed findings with log-line citations
- Explicit distinction between observations and hypotheses
- Suggested troubleshooting and preventive actions
- Conversational follow-up questions
- Markdown investigation reports and JSON execution traces
- Streamlit interface for web-based analysis

## Architecture

RootCause AI consists of four main components:

**1. Reachy Mini Conversation App**

A native Reachy Mini application provides voice interaction and invokes two custom tools:

- `investigate_log`: Starts a fresh investigation.
- `ask_about_report`: Answers questions about the most recent investigation.

**2. RootCause AI Backend**

A Python FastAPI service handles investigation requests, report generation, and follow-up questions.

The working robot demonstration uses an authenticated SSH tunnel to communicate with the backend running on a Windows machine.

**3. NVIDIA Nemotron through Nebius Token Factory**

The investigation agent uses:

- Model: `nvidia/nemotron-3-super-120b-a12b`
- Provider: Nebius Token Factory
- Interface: OpenAI-compatible API with tool calling

Nemotron determines which tools to execute, examines their results, and reasons about the incident.

**4. Read-only Investigation Tools**

The agent can invoke:

| Tool | Purpose |
|---|---|
| `search_logs` | Find relevant errors and events |
| `detect_patterns` | Identify recurring failures and patterns |
| `extract_timeline` | Reconstruct incident events |
| `validate_evidence` | Check referenced log evidence |

Tool execution takes place within a bounded investigation loop.

## How Nemotron Is Used

Nemotron is not used merely to summarize a predefined analysis.

The agent receives numbered, sanitized log entries along with definitions of its available tools. It chooses tool calls, examines structured results, and continues investigating until it generates a final report or reaches its tool-call budget.

Reports include supporting evidence, plausible root-cause hypotheses, uncertainties, and recommendations.

Nemotron also supports follow-up questions grounded in the saved investigation context.

Nebius Token Factory enables this workflow through hosted inference without requiring local GPU infrastructure.

## Running RootCause AI

### Prerequisites

- Python 3.11 or later
- Nebius Token Factory API key
- Dependencies listed in `requirements.txt`
- Reachy Mini hardware for the robotics integration

### Web Application

Clone the repository, install the dependencies, and configure:

```text
NEBIUS_API_KEY=<your-key>
NEBIUS_MODEL=nvidia/nemotron-3-super-120b-a12b
```

Then launch the Streamlit application using the entry point in the repository.

### Reachy Mini Integration

The Reachy Mini application uses the native Reachy Mini Conversation App framework.

The robot connects to a RootCause AI FastAPI backend using:

```text
ROOTCAUSE_BRIDGE_URL=<backend-url>
REACHY_BRIDGE_TOKEN=<authentication-token>
```

For the local demonstration, the backend runs on Windows and is accessed through an authenticated SSH reverse tunnel.

The native app includes the `investigate_log` and `ask_about_report` tools. A detailed installation and configuration guide is provided in the `reachy-mini/` folder.

**Security:** Never commit API keys, shared authentication tokens, sensitive production logs, or private investigation reports.

## Example Investigation

In a sample incident, application logs showed:

- Database connection refused
- Database retry attempts failed
- HTTP 500 errors on `/api/orders`
- Database connectivity restored
- Successful HTTP 200 responses afterward

RootCause AI reconstructed the sequence and identified the database connectivity failure as the immediate observed cause of the HTTP 500 errors.

It also documented that the underlying reason for the database connection refusal could not be conclusively determined from those logs alone.

This distinction between evidence and hypotheses is a central design principle.

## Challenges and Learnings

The main challenges included integrating Reachy Mini's realtime voice interface with a remote investigation agent, implementing reliable custom tool execution, and preserving evidence-grounded reasoning.

The project demonstrated that a physical robot can provide a practical conversational interface to specialized agentic workflows.

It also reinforced the importance of inspectable tool traces and explicit uncertainty in AI-assisted troubleshooting.

## Future Improvements

- Public cloud-hosted investigation API
- Reusable Reachy Mini installation package
- Dynamic voice-based log selection
- Multi-log and cross-service correlation
- Persistent investigation history
- Proactive incident detection
- Monitoring and incident-management integrations

## Built With

Python · NVIDIA Nemotron 3 Super · Nebius Token Factory · Reachy Mini · Reachy Mini SDK · Hugging Face Realtime Conversation Backend · FastAPI · Streamlit · REST APIs · WebSocket

## License

See the repository's `LICENSE` file. Third-party components retain their respective licenses.
