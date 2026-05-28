---
layout: post
title: "a linear.app clone as substrate for an MCP demo"
date: 2026-05-28 10:00:00 -0400
categories: [ai, mcp]
tags: [mcp, llm, claude, demo, linear, react, typescript, postgres]
description: >
  Why I rebuilt a Linear-style issue tracker from scratch in React +
  TypeScript + Express + Postgres before writing a single MCP server.
  Demoware needs a real domain underneath it, or the protocol talk
  collapses into a CRUD talk.
---

*Draft. Companion repo: [demo-mcp-dev-summit-linear](https://github.com/jconnolly/demo-mcp-dev-summit-linear).*

## what this is

A full-stack Linear.app clone &mdash; React + TypeScript + Express + Postgres, containerized with Docker Compose &mdash; built as the substrate for an MCP demo at the 2026 MCP Dev Summit.

## why bother with the substrate

Most MCP demos I've seen fall into one of two failure modes:

1. The MCP server wraps a toy in-memory list, the LLM "creates an issue", and nobody learns anything about real MCP tradeoffs (auth, resource exposure, prompt templates, capability boundaries).
2. The MCP server wraps a real third-party SaaS, the demo gets blocked on a credential the audience doesn't have, and the talk turns into a screenshot tour.

A real but local domain &mdash; issues, teams, cycles, projects, comments &mdash; gives you the same shape Linear has without the auth/credential drag, and lets the talk stay on what MCP actually adds.

## what the post will eventually cover

- The schema and why I matched Linear's vocabulary rather than inventing my own.
- Which MCP capabilities map cleanly onto an issue tracker (tools, resources, prompts) and which don't.
- The auth boundary &mdash; how the MCP server proves it's allowed to mutate which tenant's data.
- Where the LLM is actually useful inside the loop vs. where it's a worse UX than the existing keyboard shortcuts.

*&mdash; more soon.*
