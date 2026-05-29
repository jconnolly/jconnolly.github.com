---
layout: post
title: "what qwen3:14b actually gets wrong in a Claude Code loop"
date: 2026-05-29 09:00:00 -0400
categories: [ai, llm]
tags: [llm, qwen3, ollama, claude-code, local-ai, mcp, agentic, swe-bench, sqlite-vec]
image: /assets/img/og/maral-companion.png
description: >
  Companion to the Pi5 piece. Maral runs qwen3:14b at 10 tok/s and
  ~45% SWE-bench Verified. That's a -43 point gap vs Opus 4.7. This
  is what the gap actually looks like inside a Claude Code agent
  loop: tool-call misfires, RAG sidecar sync, the failure shapes I
  saw across two days of real work.
---

*Companion to [the Pi 5 vs MacBook piece]({% post_url 2026-05-28-local-llm-pi5-vs-macbook %}). That post made the case that a spare M2 Air beats a Pi 5 + Hailo for local LLM at home. This one is about what you actually trade away when you make qwen3:14b your daily driver.*

## tl;dr

* TODO

## the headline gap

Opus 4.7 sits at 87.6% on SWE-bench Verified. qwen3:14b Q4 on Maral lands around 45% estimated. **-43 points.** A long conversation about exactly what that gap looks like.

* TODO: framing for the rest of the post — quality drop vs operational cost vs privacy/latency wins

## where qwen3:14b actually wedges

### tool-call misfires

* TODO: 1-2 concrete examples from session log where the local model emitted a wrong tool name, or dispatched a tool with malformed args. Show the JSON.

### planning loops

* TODO: cases where the model re-reads the same file three times because it forgot it already read it. The Pi5 piece talked about Claude Code memory; here is what happens when the model writing those memories is the small one.

### thinking-trace tax

* TODO: qwen3's `thinking` block helps reasoning but adds tokens. At 10 tok/s that's real wall-clock cost on every turn. Numbers.

## the sqlite-vec hiccup (RAG sidecar)

I run `maral-rag` (a small MCP server on Maral) so today's local sessions can pull from yesterday's cloud thinking. Two bugs hit:

**1.** macOS bundles a Python built without `--enable-loadable-sqlite-extensions`. `sqlite-vec` needs that flag. Symptom:

```
AttributeError: 'sqlite3.Connection' object has no attribute 'enable_load_extension'
```

Fix: `uv python install 3.12` to get a python-build-standalone with extensions enabled.

**2.** `sqlite-vec`'s knn syntax requires `AND k = ?` *inside the WHERE clause*, not `LIMIT N` after `ORDER BY`. Wrong:

```sql
WHERE embedding MATCH ? ORDER BY distance LIMIT ?
```

Right:

```sql
WHERE embedding MATCH ? AND k = ? ORDER BY distance
```

One-line fix once you read the right error message.

## the boring step that breaks everything

Backend switching isn't really about the model. It's about the machine that knows your config, history, and skills.

* TODO: explain `~/.claude/` state, why path rewriting (`/Users/john.connolly` → `/Users/jconnolly`) matters when you migrate sessions, what stays portable, what doesn't.

## when I reach for `claude-cloud`

* TODO: rules of thumb that landed for me after a week. Things qwen3:14b handles fine (reading code, summarizing, simple refactors, shell help, sed/awk). Things it does not (multi-file edits in unfamiliar codebases, design reviews, anything where being wrong is expensive).

## what I'd build next on the local side

* TODO: ideas for the Maral sidecar — better memory writes, eval harness, model-mix routing per task class. Forward-looking, light.

---

*Code, configs, and the systemd/launchd files referenced in this post live in [local-llm-pi5](https://github.com/jconnolly/local-llm-pi5).*
