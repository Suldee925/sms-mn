# sms-mn

Production-ready Python library for sending SMS through the Unitel Premium Number API.

This package is designed so your backend only needs to provide:

- `to`
- `message`

Everything else is handled by the client.

## Features

- Simple `send(to, message)` API
- Sync and async clients
- Input validation
- Configurable timeout
- Retry support for transient failures
- Clean exception hierarchy
- `src/` layout for packaging
- Wheel/sdist ready

## Install

```bash
pip install sms-mn