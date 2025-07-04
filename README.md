
# PulseTrack_bot – The bridge between your people and actionable insights.
**Author:** Brian Mutuku  
**Role:** Bot Engineer / Integrations – PulseTrack Hackathon Project

---

## Overview

PulseTrack_bot is the conversational interface component of the PulseTrack solution. It enables employees to interact with the system via SMS or WhatsApp, powered by Twilio. The bot collects feedback, check-in responses, and other communications, then forwards and stores them for analysis by the backend AI/ML services (e.g., Django + NLP pipelines). This repository contains the code for deploying and running the bot, as well as guides for integrating it with the PulseTrack backend and dashboard.

---

## Architecture & Integration Points

```
User (SMS/WhatsApp) 
   │
   ▼
PulseTrack_bot (Twilio Webhook Endpoint)
   │
   ▼
Backend (Django REST API)
   │
   ▼
AI/ML Processing → Dashboard & Reports
```


---

## Features

- Automated check-in prompts to employees (customizable frequency/message)
- Receives and forwards replies via Twilio SMS/WhatsApp
- Anonymous or identified feedback modes
- Forwards messages with metadata to backend API
- Handles delivery receipts, errors, and fallback mechanisms
- Easily extensible for new communication channels

---

## Getting Started

### Prerequisites

- Python 3.8+
- Twilio Account (with WhatsApp/SMS enabled)
- Backend API URL (Django REST endpoint, provided by Backend Team)
- (Optional) Docker

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Bra-yo/PulseTrack_bot.git
   cd PulseTrack_bot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   Or, using Docker:
   ```bash
   docker build -t pulsetrack_bot .
   ```

3. **Configure environment:**
   - Copy `.env.example` to `.env`
   - Fill in:
     - `TWILIO_ACCOUNT_SID`
     - `TWILIO_AUTH_TOKEN`
     - `TWILIO_PHONE_NUMBER`
     - `BACKEND_API_URL` (provided by Django backend team)
     - Any other required keys

4. **Expose a webhook:**
   - Use [ngrok](https://ngrok.com/) for local development:
     ```bash
     ngrok http 5000
     ```
   - Set the webhook URL in your Twilio console to your server's `/webhook` endpoint.

### Running the Bot

- **Locally:**
  ```bash
  python main.py
  ```
- **With Docker:**
  ```bash
  docker run --env-file .env -p 5000:5000 pulsetrack_bot
  ```

---

## Connecting to the Backend (Django/ML Team)

- This bot expects a backend REST API endpoint to POST collected messages/feedback.
- The backend must implement an endpoint (e.g., `/api/feedback/`) that accepts JSON payloads like:
  ```json
  {
    "user_id": "optional-or-anonymous",
    "message": "Feeling overwhelmed tbh. Deadlines too close.",
    "timestamp": "2025-07-04T10:08:01Z",
    "channel": "whatsapp",
    "metadata": {
      "department": "Engineering"
    }
  }
  ```
- Configure the `BACKEND_API_URL` in your `.env` to point to this API.
- The bot will handle retries and error-logging if the backend is temporarily unavailable.

---

## Customizing Prompts & Frequency

- Prompts can be edited in the bot settings or the code (e.g., `config.py` or similar).
- Scheduling can be handled via a cron/scheduler, or delegated to the backend for batch sends.

---

## Extending / Integrating with Other Components

- To add new channels (e.g., Telegram), create a new handler module and register it in the main app.
- For additional metadata (e.g., team, location), extend the payload sent to the backend.
- The bot can be triggered by the backend via REST API (for campaign/batch pushes).

---

## Troubleshooting

- **Webhook not receiving messages?**
  - Ensure Twilio webhook URL is correct and publicly accessible (use ngrok or deploy to a public server).
- **Messages not forwarded to backend?**
  - Check `BACKEND_API_URL` and backend service status.
  - Review logs for error details.

---

## Contribution

- Fork the repo and submit PRs for improvements or bugfixes.
- See [CONTRIBUTING.md](CONTRIBUTING.md) if available.

---

## License

MIT License – see [LICENSE](LICENSE) for details.

---

## Contact

For integration help, backend API details, or other queries, contact Brian Mutuku (repo owner) or open an issue.

---

**PulseTrack_bot – The bridge between your people and actionable insights.**
