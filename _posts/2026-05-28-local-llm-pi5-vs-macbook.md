---
layout: post
title: "running a SOTA local LLM at home: pi 5 vs. a spare macbook"
date: 2026-05-28 09:00:00 -0400
categories: [ai, llm]
tags: [llm, ollama, qwen3, raspberry-pi, hailo, claude-code, local-ai, mcp]
description: >
  Two-track investigation into running a usable local LLM as a Claude Code
  backend over LAN. Pi 5 16GB + Hailo-10H AI HAT+ 2 vs. a spare M2 MacBook
  Air. With measured tok/s, the verdict is unambiguous, and not the one I
  expected when I bought the Hailo.
---

*Draft. The detail lives in the [local-llm-pi5](https://github.com/jconnolly/local-llm-pi5) repo for now &mdash; this post will catch up.*

## the setup

I wanted a SOTA-ish local LLM on my LAN that Claude Code could talk to as its `ANTHROPIC_BASE_URL`. The Pi 5 16GB + Hailo-10H AI HAT+ 2 was the original target &mdash; small, quiet, dedicated NPU for offload.

Halfway in I pivoted to a spare 2023 MacBook Air M2 16GB sitting in a drawer.

## the verdict

If you have a spare Apple Silicon Mac on your LAN, use that. Skip the Pi for LLM.

| Track | Model ceiling | Decode tok/s |
|---|---|---|
| Pi 5 16GB CPU | qwen3:8b Q4_K_M | ~1.9 |
| Pi 5 + Hailo-10H | (unusable for CC) | &mdash; |
| M2 MBA 16GB | qwen3:14b | ~10 |

The MBA wins by 5x on speed, runs a bigger model, and cost nothing because it was already in the house.

## why hailo didn't pan out for claude code

Three dealbreakers, all of them structural rather than tuning:

1. Largest Hailo-Executable-Format LLM ceiling is ~2B params.
2. Hailo context window caps at 2048 tokens. Claude Code's official guidance is &ge;64k.
3. `hailo-ollama` 500s when you POST a `tools` payload. Open upstream bug.

The Hailo is still good at the workloads it was designed for &mdash; compiled vision graphs, Whisper STT &mdash; just not at agentic LLM serving.

## why qwen3 and not qwen2.5-coder

I started with qwen2.5-coder:7b on the assumption that "coder" beats "general" for a Claude Code backend. It doesn't, because of a tool-use parser mismatch:

- qwen2.5-coder emits bare JSON for tool calls.
- Ollama's chat template for qwen2.5-coder expects `<tool_call>...</tool_call>` XML wrappers.
- The parser fails, the tool call comes back in a `text` block instead of a `tool_use` block, and Claude Code can't dispatch it.

qwen3 was trained with native tool-use tokens, emits the right structured `tool_calls`, and Ollama's `/v1/messages` shim translates those correctly to Anthropic `tool_use` blocks. Bonus: it includes a `thinking` reasoning trace.

## memory guardrails so ollama can't brick the pi

Pi 5 has 16GB RAM and a 2GB swap on the SD card. SD swap is ~10x slower than NVMe &mdash; if Ollama starts thrashing it, the Pi goes unresponsive worse than a Mac would. The systemd drop-in I'm running:

```ini
# /etc/systemd/system/ollama.service.d/override.conf
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
Environment="OLLAMA_MAX_LOADED_MODELS=1"
Environment="OLLAMA_NUM_PARALLEL=1"
Environment="OLLAMA_KEEP_ALIVE=5m"
```

Full writeup with stack diagrams, model benchmarks, and the agent-loop math (10-step turn at 2 tok/s ≈ 25 min, which is brutal) is in the [repo README](https://github.com/jconnolly/local-llm-pi5).

*&mdash; more soon.*
