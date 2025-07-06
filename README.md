# synccast

**Real-time UI sync and messaging framework for Django — powered by MQTT.**

SyncCast enables your Django backend to publish scoped, channel-based real-time events over MQTT, supporting use cases like:

- 🗨️ Live chat
- 👤 Presence and typing indicators
- 🛎️ UI notifications
- 📊 Live dashboards

It is frontend-agnostic — your frontend simply subscribes to MQTT topics and reacts accordingly.

---

## Features

- 📡 Real-time event broadcasting over MQTT
- 🔐 Secure SDK interface with app credentials
- 🧱 Modular architecture (`core`, `api`, `exceptions`)
- 🎯 Compatible with any frontend
- 📦 Installable directly from GitHub

---

## Installation

Install directly from GitHub:

```bash
pip install git+https://github.com/smarakaranjan/syncast.git
