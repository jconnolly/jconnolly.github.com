---
layout: page
title: uses
permalink: /uses/
image: /assets/img/og/uses.png
description: >
  Hardware, dotfiles, and the LLM stack I actually run day to day.
  In the spirit of uses.tech — what's on the machine when I'm working.
---

What's on the machine when I'm working, May 2026. Updated occasionally; if anything below looks stale, it probably is.

## hardware

- **dev**: M-series Mac with Cursor as the day-job editor, VS Code and Sublime kept warm for the things they're each best at, iTerm2 with MesloLGS Nerd Font as the terminal.
- **maral**: a spare 2023 MacBook Air M2 16GB on the LAN running a local LLM stack — Ollama serving `qwen3:14b` to Claude Code over `ANTHROPIC_BASE_URL`. [Full story](/2026/05/28/local-llm-pi5-vs-macbook/).
- **pi 5**: a Raspberry Pi 5 16GB with a Hailo-10H AI HAT+ 2. Was meant to be the LLM appliance; turned out to be a great vision / Whisper / experimentation box and a slow agent backend.
- **router**: a Google WiFi mesh of six AC-1304 pucks running OpenWRT, [unbricked the hard way](/2026/05/27/unbricking-six-google-wifi-pucks/).

## shell + system

- **zsh + oh-my-zsh**, with bounded marker blocks in `~/.zshrc` for project-specific functions so they don't bleed into each other.
- **macOS 26.3**.
- **Porkbun** for DNS (this domain). **ProtonMail** for inbox.

## ai / llm

- **Claude Code** is the primary work driver, used both directly and through a [router](/2026/05/28/local-llm-pi5-vs-macbook/#act-8--wiring-it-without-losing-the-cloud-escape-hatch) that defaults to the local Maral and requires explicit `claude-cloud` to spend cloud quota.
- **MCP** for tool plumbing — at work, an internal MCP server + Claude-skill suite drives Jira, Bitbucket, and AWS Cost Explorer.
- **AWS Bedrock + Anthropic API** day-job stack: Knowledge Bases for RAG, Lambda for orchestration, `pgvector` and OpenSearch k-NN for vector search.
- **qwen3 family** for the local side. qwen3:14b on Maral, qwen3:8b as the small-fast fallback.

## languages + frameworks (at work)

- **TypeScript** + **React 19** + **Next.js App Router** + **Tailwind 4** on the frontend.
- **Node 20+** or **Python 3.12** on the backend, depending on the service.
- **Scala / Akka / Play** if you go far enough back — that was the Flow Commerce era. Not the daily driver anymore.
- **Prisma** as the ORM when there's a DB.
- **Postgres** for OLTP, **RDS** with a Glue/Python mirror of partner Redshift `bi` schemas for analytics.

## infra

- **AWS ECS Fargate** + **ALB** + **ECR** for long-running services.
- **AWS Lambda (container image)** + **EventBridge Scheduler** for headless jobs.
- **AWS Glue (Python)** for batch / pipeline work.
- **Terraform** for all of the above, S3 + DynamoDB backend.
- **Bitbucket Pipelines** for CI/CD.
- **Secrets Manager** for secrets, **SSM Parameter Store** for non-secret config.

## the blog itself

- **Jekyll**, github-pages gem, kramdown + rouge for syntax highlighting.
- **jekyll-seo-tag** for OG / meta. Per-post 1200x630 cards rendered by a small Playwright script in `_scripts/og.py`.
- Hosted on GitHub Pages with a Let's Encrypt cert for `ollyconn.com`, fronted by Porkbun DNS.

