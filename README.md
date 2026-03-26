# Some Python Codes

A growing collection of small Python projects. This repository is published gradually,
with one project added per day by the automation scripts in this repo.

## Publishing Roadmap

| Order | Project | Folder | Main file | Status |
| --- | --- | --- | --- | --- |
| 1 | Caesar Encryption | `Cesar_encryption` | `Cesar_encryption/cesar.py` | Published |
| 2 | Random Word Game | `Random Word game` | `Random Word game/RandomWordGame.py` | Next in queue |
| 3 | Search Engine | `Search Engine` | `Search Engine/ExaEngine.py` | Queued |
| 4 | Discord Chatbot | `discord_chatbot` | `discord_chatbot/discord vhatbot.py` | Queued |
| 5 | YouTube Video Downloader | `youtube_video_downloader` | `youtube_video_downloader/YT.py` | Queued |

## Published Projects

### 1. Caesar Encryption

- Folder: `Cesar_encryption`
- Main file: `Cesar_encryption/cesar.py`
- Summary: A simple Caesar cipher example that shifts alphabetic text while keeping punctuation unchanged.
- Highlights:
  - Supports both uppercase and lowercase letters.
  - Uses modulo arithmetic to wrap around the alphabet cleanly.
  - Includes a small example that encrypts the word 'mohamed' with a shift of 3.
- Requirements:
  - Python 3

## Automation

- `daily_github_pusher.py` publishes the next unpublished project, regenerates this
  README, commits the changes, and pushes them to `origin/main`.
- `run_daily_publish.ps1` runs the publisher and stores a log file in
  `.publish_logs/`.
- `watch_daily_publish.ps1` is a lightweight watcher that can stay running in the
  background and trigger one publish attempt per day.

## Manual Commands

```powershell
python .\daily_github_pusher.py --dry-run
python .\daily_github_pusher.py --refresh-readme-only
.\run_daily_publish.ps1
.\watch_daily_publish.ps1
```

The publish step uses your local git credentials, so the repository must exist on
GitHub and your machine must already be able to push to `origin`.
