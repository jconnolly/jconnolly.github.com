---
layout: page
title: projects
permalink: /projects/
---

Selected recent work. Full list at [github.com/jconnolly](https://github.com/jconnolly).

## AI / LLM

**[local-llm-pi5](https://github.com/jconnolly/local-llm-pi5)** &middot; SOTA local LLM at home, two-track investigation: Raspberry Pi 5 16GB + Hailo-10H AI HAT+ 2 vs. a spare M2 MacBook Air. Verdict, with measured numbers: if you have spare Apple Silicon on the LAN, use it. qwen3:14b at ~10 tok/s on Maral beats qwen3:8b at ~2 tok/s on the Pi, for $0. Hailo-10H is good at compiled HEFs (vision, Whisper) but not at agentic LLMs &mdash; 2B param ceiling, 2k context, broken `tools` payload in `hailo-ollama`. Notes on tool-use parsing (qwen2.5-coder emits bare JSON, qwen3 emits proper `tool_calls`), memory guardrails so Ollama can't thrash SD-card swap, and the Claude Code wiring.

**[demo-mcp-dev-summit-linear](https://github.com/jconnolly/demo-mcp-dev-summit-linear)** &middot; Full-stack Linear.app clone &mdash; React + TypeScript + Express + Postgres, Docker Compose &mdash; built as the substrate for an MCP demo at the 2026 MCP Dev Summit.

**[spotify-cagebreak](https://github.com/jconnolly/spotify-cagebreak)** &middot; Weekly "algorithm cage-break" music discovery. Dumps your Spotify taste profile, asks a local Ollama model for opinionated picks adjacent to your taste but not in your library and not recommended before, then builds a dated playlist and a markdown digest. No recommender-algorithm feedback loop &mdash; you get LLM taste, not Spotify's.

## Hardware / OpenWRT

**[google-wifi-suzyq-console-macos](https://github.com/jconnolly/google-wifi-suzyq-console-macos)** &middot; Serial console + OpenWRT flashing for Google WiFi (Gale, AC-1304) from a Mac via a $7 SuzyQ/SuzyQable USB-C debug adapter. No Chromebook, no Linux laptop, no kext. Companion to the [unbricking-six-google-wifi-pucks]({% post_url 2026-05-27-unbricking-six-google-wifi-pucks %}) post.

## Other recent

**[constradoak-vacation-hunter](https://github.com/jconnolly/constradoak-vacation-hunter)** &middot; 2027 Presidents Day family vacation hunter &mdash; destination research, airfare playbook, automated fare-watch monitoring notes.
