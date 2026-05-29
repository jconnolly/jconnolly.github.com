---
layout: post
title: "shipping an internal MCP server: what dsg-tools is, what hurt"
date: 2026-05-30 09:00:00 -0400
categories: [ai, mcp]
tags: [mcp, claude-code, dsg-tools, jira, bitbucket, aws, internal-tools, agentic, auth]
image: /assets/img/og/dsg-tools-mcp.png
description: >
  dsg-tools is a Claude Code plugin + CLI my team uses every day to
  drive Jira, Bitbucket, and AWS. Nine skills, one CLI dispatcher,
  Keychain auth, audit log, scoped tokens. What shipped, what
  surprised me, what an MCP-style internal harness actually has
  to get right before it stops feeling like a toy.
---

*A real post-mortem on an internal agentic harness. Not "MCP for thought leaders" — what the actual auth boundary, audit log, and skill-vs-CLI design looked like when I had to make it survive nine engineers using it as a daily driver.*

## tl;dr

* TODO

## what dsg-tools actually does

Nine skills, one `dsg` CLI, distributed as a private Claude Code plugin. Each skill wraps one or more `dsg <group> <cmd>` invocations:

| Skill | What |
|---|---|
| `dsg-jira` | comment, transition |
| `dsg-bitbucket` | PRs, pipeline logs, deployment-env vars |
| `dsg-me` | morning stand-up (Jira + PRs + Slack) |
| `dsg-slack-send` | post one Slack message |
| `dsg-slack-agent` | auto-reply Bolt agent (experimental) |
| `dsg-aws-cost-report` | Cost Explorer by Project tag |
| `dsg-aws-cost-watch` | week-over-week spike detection |
| `dsg-aws-webhook-tunnel` | ephemeral EC2 + Caddy public-URL tunnel |
| `dsg-auth-rotate-atlassian-token` | rotate `~/.jira-credentials` |

* TODO: dek on the surface — colleagues install with `/plugin marketplace add … && /plugin install dsg-tools@dsg-tools`, then talk to it in plain English.

## the one-thing-per-tool rule

* TODO: design principle — each tool has a single entry point, takes args / env (no hidden state), prints to stdout for piping. Why this matters when an LLM is driving.

## the auth boundary

Atlassian "API tokens with scopes" are single-product: one token holds Jira scopes OR Bitbucket scopes, not both. `dsg auth set-atlassian` mints both and writes them to the platform secret store:

* macOS → Keychain (services `dsg-jira-token`, `dsg-bb-token`)
* Linux → `pass(1)`
* fallback → legacy plaintext `~/.jira-credentials`

Resolution precedence: env var → Keychain → pass(1) → plaintext.

* TODO: walk the COMPLIANCE_TODO §3 story — why we moved off plaintext, what the "scrub plaintext token lines after Keychain write" step actually does, and what the harness deny-list (`Read(~/.jira-credentials)`, `~/.dsg-tools.env`, `~/.aws/*`) buys you.

## the audit log

Every `dsg <group> <cmd>` invocation appends one line to `~/.dsg-tools.log`:

```
2026-05-28T14:33:10Z  pid=12345  user=jconnolly  cmd="dsg jira mine"
```

Token shapes (`xoxp-`, `xoxb-`, `atatt_`, `github_pat_`, `AKIA*`, etc.) are scrubbed before write. Rotates at 10 MiB, keeps 5 generations. Disable with `DSG_LOG_DISABLE=1`.

* TODO: why the audit log was load-bearing for the AI tool-use policy and what we learned about scrubbing patterns the first time we caught a near-leak.

## what was painful

### MCP wasn't the right primitive at first

* TODO: the early version was a "real" MCP server with stdio transport per skill. Worked in Claude Code Desktop, painful in CC CLI. Switched to a plugin-shipped `dsg` CLI + Claude Code skills — same UX for the user, much simpler infra.

### scope creep on the agent side

* TODO: the temptation to add a skill for everything someone asks about. Eventually you have a `dsg slack agent` that nobody understands. The rule we settled on: experimental skills live in `slack_agent/` and ship marked experimental.

### the Jira ADF thing

* TODO: Markdown does not render in this Atlassian instance. Comments must be ADF JSON. `dsg jira comment ISSUE --adf body.json` was forced on us. Story about catching the first month of comments that looked weird because somebody pasted markdown.

### the `dsg me` problem

* TODO: morning stand-up view — Jira tickets + PRs + Slack mentions in one CLI. People stopped checking Slack in the morning entirely. Good or bad?

## what I'd do differently

* TODO: top three. One is "ship the audit log on day one, not month three." Others to be filled in.

## what's next

* TODO: forward-looking, light. AWS cost tooling is moving toward dashboards; the Slack agent is getting smarter about voice-matching; Jira automation is getting close to a real bot.

---

*dsg-tools is internal — the source isn't public, but the design choices in this post are general. If your team is building an internal MCP / Claude Code harness, the [dsg-tools README](https://bitbucket.org/datasociety/dsg-tools) is what we hand new hires on day one.*
