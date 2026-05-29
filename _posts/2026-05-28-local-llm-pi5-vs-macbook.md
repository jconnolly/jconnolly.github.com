---
layout: post
title: "I spent a day trying to make a Pi 5 a local LLM appliance, then found a MacBook in a drawer"
date: 2026-05-28 12:00:00 -0400
categories: [ai, llm]
tags: [llm, ollama, qwen3, raspberry-pi, hailo, claude-code, local-ai, mcp, swe-bench]
image: /assets/img/og/local-llm-pi5-vs-macbook.png
description: >
  A real-time investigation log. Pi 5 16GB + Hailo-10H AI HAT+ vs.
  a 2023 MacBook Air M2 as Claude Code backends over the LAN.
  The MacBook wins by 5x on speed at a model twice as big, for $0.
  Notes on qwen3 vs qwen2.5-coder tool-use parsing, SD-card I/O stalls,
  NAND price spikes, and where the cloud frontier actually sits.
---

*I wanted a local LLM I could point Claude Code at over the LAN. The pitch on the Pi 5 16GB + AI HAT+ 2 (Hailo-10H NPU) was that quantized coding models would scream on a 40-TOPS NPU and sip 10 watts. I built three Pi-side stacks, hit four dead ends, and almost spent $200 on an SSD before the user said "there's a MacBook downstairs." The MacBook beat the Pi by 5x at a model twice as big, for $0.*

## tl;dr

If you have a spare Apple Silicon Mac on your LAN, **use it. Skip the Pi for LLM.** The Pi 5 is still a great Hailo / Whisper / vision experimentation box, just not an agent backend.

If the Pi 5 is all you have, **`qwen3:8b` on Ollama is the ceiling**: ~2 tokens/sec decode, painful but functional, an estimated 30-40% on SWE-bench Verified. **Drop to `qwen3:4b` if you'd rather wait less.**

If you have $1K to spend and want a one-box appliance, the Mac Mini M4 24GB BTO at $999 unlocks **Qwen3.6-27B at 77.2% SWE-bench Verified**, two points behind Claude Sonnet 4.6. Strix Halo Mini-ITX at $1499 unlocks Mistral Medium 3.5 (128B) at 77.6%.

Everything above 80% on the leaderboard (DeepSeek V4 Pro Max, GLM-5, Kimi K2.6, Opus 4.5+) needs $5K+ of hardware. Not a one-day build.

Repo with all of this, including benchmark runner and the launchd plists: [local-llm-pi5](https://github.com/jconnolly/local-llm-pi5).

## the goal

A LAN box Claude Code can talk to as its `ANTHROPIC_BASE_URL`. No data leaves the network, no per-token billing, always-on, can run while I sleep. The cloud Claude stays available for hard problems; the local LLM handles the routine. Memories and session transcripts live in `~/.claude/` on the laptop, the model is interchangeable.

## act 1 — the Pi 5 dream

Starting state:

- Raspberry Pi 5 16GB, Debian 13 trixie, kernel 6.12.75
- Raspberry Pi AI HAT+ 2 with the Hailo-10H NPU soldered on (40 TOPS, M.2 form factor)
- A spare 2023 MacBook Air M2 16GB sitting in a drawer that I did not know I had

The Hailo HAT was the headline. 40 TOPS, dedicated NPU, "compiled HEFs run quantized LLMs at native speed." This is what made me bite on the build in the first place.

## act 2 — Hailo-10H ambition

Spent fifteen minutes researching before installing anything. Three findings killed the plan:

**1. The largest LLM HEF for the Hailo-10H is 2B params.** The [Hailo Model Zoo GenAI v5.3.0 catalogue](https://github.com/hailo-ai/hailo_model_zoo_genai/blob/main/docs/MODELS.rst) ships exactly these:

| Model | Params | Quant | Ctx | Decode tok/s | Tool use |
|---|---|---|---|---|---|
| Llama3.2-1B-Instruct | 1B | A8W4 | 2048 | 9.89 | No |
| Qwen2.5-Coder-1.5B-Instruct | 1.5B | A8W4 | 2048 | 8.13 | No |
| **Qwen2-1.5B-Function-Calling-v1** | **1.5B** | **A8W4** | **2048** | **6.69** | **Yes** |
| Qwen3:1.7B | 1.7B | A8W4 | 2048 | 4.78 | No |
| Qwen2-VL-2B / Qwen3-VL-2B | 2B | A8W4 | 2048 | ~5-7 | No |

The *only* HEF with tool calling is a 1.5B fine-tune of Qwen2. Too small to drive an agent loop in any non-toy way.

**2. The Hailo runtime's context window caps at 2048 tokens.** Claude Code's own [official guidance](https://docs.anthropic.com/en/docs/claude-code/overview) recommends &ge;64k. The CC system prompt plus tool definitions plus a single small file read already overflows 2k. You cannot meaningfully use a Hailo HEF as a CC backend; you'd be re-prompting the model with a sliding 2k window and watching it forget context every other tool call.

**3. The `hailo-ollama` shim 500s on `tools` payloads.** Open [community thread from Feb 2026](https://community.hailo.ai/t/hailo-ollama-tools-support/18624) — the shim that bridges Hailo's runtime to Ollama's API throws `TreeToObjectMapper::mapString(): Node is NOT a STRING` whenever the request contains a `tools` field. A community fork patches it; it is not upstream and won't survive HailoRT 5.3 upgrades. So even the toy 1.5B function-calling model can't get its tool calls to a real Claude Code session without you maintaining a fork.

I installed the Hailo stack anyway — `hailo-h10-all` from the Pi extranet repo, plus the `hailo-apps` git tree. It works fine for vision and Whisper. It is just not an agent backend in May 2026.

**Lesson 1.** Don't pick the impressive hardware. Pick the matching software stack. The Hailo-10H is genuinely good at compiled HEF models — it's bad at agentic LLMs because the compiler, the runtime, and the bridging shim were not built for that workload.

## act 3 — Ollama on the Pi 5 CPU

Plan B. Ignore the HAT, run llama.cpp via Ollama on the Pi 5's Cortex-A76 quad-core. The Pi is memory-bandwidth-bound for inference, but it works.

### memory guardrails first

The Pi 5 has 16GB of RAM and a 2GB swap on the SD card. SD swap is roughly 10x slower than NVMe. If Ollama starts thrashing it, the Pi goes unresponsive worse than a Mac does — the kernel keeps answering ICMP (so your monitoring says "network is up") but every userspace service blocks indefinitely on disk.

systemd cgroup hard cap, so the kernel kills the model *before* swap thrash starts:

```ini
# /etc/systemd/system/ollama.service.d/override.conf
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
Environment="OLLAMA_MAX_LOADED_MODELS=1"
Environment="OLLAMA_NUM_PARALLEL=1"
Environment="OLLAMA_KEEP_ALIVE=5m"
Environment="OLLAMA_CONTEXT_LENGTH=8192"
MemoryHigh=11G
MemoryMax=12G
```

`MemoryMax=12G` is the load-bearing line. The model has plenty of room; the OS has plenty of room; nothing ever sees the SD card under load.

### model selection

I burned a few hours on this. The interesting failure mode is not "too slow" — it's "tool use silently broken in ways the model's own metadata won't tell you."

**Attempt 1: `qwen3-coder:7b`.** Does not exist on Ollama. Qwen3-Coder's smallest published variant is the 30B-A3B MoE, too big for a Pi 5 16GB. I'd hallucinated the model name from training-data overlap with Qwen3 and Qwen2.5-Coder. Always check `ollama list` for the actual registry.

**Attempt 2: `qwen2.5-coder:7b`.** Pulled, ran, decode 2.37 tok/s. Hit it with a `get_weather` tool call. Response:

```json
"content": [
  {"type": "text",
   "text": "{\"name\": \"get_weather\", \"arguments\": {\"city\": \"Paris\"}}"}
]
```

Tool use is broken. The model emits bare JSON instead of the `<tool_call>` XML wrapper its own template expects. Ollama's parser doesn't find the tag, dumps the raw output into a `text` block. Claude Code can't dispatch a tool call from a `text` block. The model's `tools` capability advertises "yes," its output disagrees.

**Attempt 3: `qwen3:4b`.** Pulled, ran, decode 4.05 tok/s. Same test:

```json
"content": [
  {"type": "thinking", "thinking": "I should call the weather tool..."},
  {"type": "tool_use", "id": "call_cdcrb8sm",
   "name": "get_weather", "input": {"city": "Paris"}}
],
"stop_reason": "tool_use"
```

Proper `tool_use` block. Proper `stop_reason`. Bonus `thinking` trace. Qwen3 was trained with native tool-call tokens; Ollama's parser recognizes them. The model emits exactly what its template promises.

**Attempt 4: `qwen3:8b`.** Pulled, ran, decode 1.92 tok/s warm. Tool use works. Realistic agent-loop math: 10 tool-calling steps × ~300 tokens per assistant message at 2 tok/s = roughly **25 minutes per loop**. Brutal for interactive use; OK for batch.

**Lesson 2.** A model's `tools` capability advertisement is a claim, not a contract. Test end-to-end with a real request. The lookup table that says "Qwen2.5-Coder supports tools" is technically true and operationally useless: the model produces output its own scaffolding can't parse. Qwen3 was trained for agentic loops; Qwen2.5-Coder was trained for code completion that *happens to mention* tools. They are not interchangeable.

### the I/O stall

Mid-investigation I tried to pull `qwen2.5-coder:3b` and `qwen3:8b` in parallel to save wall-time. Pi pinged. Every TCP service — SSH, Ollama, HTTP — went dead for five minutes. The kernel stayed alive; userspace blocked on disk.

Root cause: parallel 8 GB SD-card writes saturated the I/O queue. The SD card was the real reliability ceiling, not RAM, not CPU. Recovery required opening a terminal on the Pi's local GUI and `sudo systemctl restart ollama` once the queue drained.

**Lesson 3.** On an SD-card-rooted Pi 5, sustained parallel writes can lock all userspace services for minutes while the queue drains. ICMP keeps responding, so your monitor says "up." It is not up.

## act 4 — buying my way out (almost)

The obvious fix is "move root to NVMe over USB3." Looked at SSD prices. **NAND has spiked.** 1TB NVMe drives that were $50-70 in 2024 retail at $200+ in May 2026 — HBM and AI-accelerator demand crowding out consumer flash. Three-to-four-times normal.

The Pi 5's USB3 is gen1, 5 Gbps nominal, roughly 500 MB/s real. Any Gen3 NVMe (3000+ MB/s) saturates this. Paying for Gen4 or Gen5 specs gets you nothing.

Cheaper-with-same-bottleneck options:

- USB3 NVMe enclosure ($25) + 1TB NVMe ($200+) = $225+
- USB-SATA enclosure ($10) + Crucial MX500 1TB SATA ($70) = $80
- Crucial X9 Pro 1TB portable USB SSD = $80, no assembly

**Lesson 4.** Find the bottleneck first. Pi 5 USB3 caps at 500 MB/s. Any modern SSD is fine. Specifying past the bottleneck is just markup.

I was about to click buy on the X9 Pro when the user mentioned the MacBook.

## act 5 — SWE-bench reality check

Before pivoting, I wanted to be sure I knew what I was trading away. Pulled the live SWE-bench Verified leaderboard. Top of the chart, May 27 2026:

| Rank | Model | SWE-bench Verified | Open weights? |
|---|---|---|---|
| 1 | Claude Mythos Preview | 93.9% | closed |
| 2 | **Claude Opus 4.7 Adaptive** | **87.6%** | closed |
| 3 | GPT-5.3 Codex | 85.0% | closed |
| 4 | Claude Opus 4.5 | 80.9% | closed |
| 6 | **DeepSeek V4 Pro Max** | **80.6%** | **open** |
| 8 | **Kimi K2.6** | **80.2%** | **open** |
| 10 | Claude Sonnet 4.6 | 79.6% | closed |

The top three open models — DeepSeek V4 Pro Max (671B MoE), Kimi K2.6 (~1T MoE), GLM-5 (335B) — each need hundreds of gigs of RAM. Not a one-day appliance.

Filtered to "open + fits a $1K box":

| Model | SWE-bench Verified | Params | Q4 RAM |
|---|---|---|---|
| **Qwen3.6-27B** | **77.2%** | 27B dense | ~18 GB |
| Qwen3-Coder-30B-A3B (MoE) | 51.6% | 30B MoE | ~18 GB |
| Qwen3:14B (general) | ~45% est | 14B dense | ~9 GB |
| Qwen3:8B (general) | ~30-40% est | 8B dense | ~5 GB |

The local headline is **Qwen3.6-27B at 77.2%**, two points behind Claude Sonnet 4.6 (79.6%). Needs 24 GB unified RAM — Mac Mini M4 24GB BTO at $999.

Down at the 16GB tier, **`qwen3:14b` lands somewhere around 45%** estimated. That's a ~43-point drop versus Opus 4.7. Privacy and zero-quota are real; coding accuracy roughly halves.

## act 6 — "wait, I have a MacBook downstairs"

After six hours of Pi optimization and a near-miss SSD purchase: "Maral", a 2023 MacBook Air M2 15", 16 GB RAM, sitting in a drawer.

Found it via Bonjour. Apple devices advertise `_rfb._tcp` (Screen Sharing) as a strong macOS signal:

```bash
dns-sd -B _rfb._tcp local.
# → "Maral" instance
dns-sd -G v4 maral.local
# → 192.168.10.210
```

(Different subnet from my dev Mac. The Google Wifi mesh bridged mDNS across subnets transparently.)

Headless Ollama install on macOS without Homebrew, no `.pkg`, no UI. The binary lives inside the official `.app` bundle:

```bash
curl -L -o /tmp/Ollama-darwin.zip https://ollama.com/download/Ollama-darwin.zip
unzip /tmp/Ollama-darwin.zip -d /tmp/ollama-extract
cp /tmp/ollama-extract/Ollama.app/Contents/Resources/ollama ~/bin/ollama
chmod +x ~/bin/ollama
```

launchd user agent to keep `ollama serve` running, bound to the LAN:

```xml
<plist version="1.0"><dict>
  <key>Label</key><string>com.ollama.serve</string>
  <key>ProgramArguments</key>
  <array>
    <string>/Users/jconnolly/bin/ollama</string>
    <string>serve</string>
  </array>
  <key>EnvironmentVariables</key>
  <dict>
    <key>OLLAMA_HOST</key><string>0.0.0.0:11434</string>
    <key>OLLAMA_KEEP_ALIVE</key><string>10m</string>
    <key>OLLAMA_MAX_LOADED_MODELS</key><string>1</string>
  </dict>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
</dict></plist>
```

Plus `caffeinate -dimsu` as a second user agent to keep the Mac awake while the lid is open. Full lid-closed sleep still needs `sudo pmset -a disablesleep 1`.

Sanity check from my dev Mac:

```
$ curl -s http://192.168.10.210:11434/api/version
{"version":"0.24.0"}
```

## act 7 — the actual numbers

Benchmarks, May 27 2026:

| Device | Model | Tool use | Decode tok/s | Prefill tok/s | Est SWE-bench Verified |
|---|---|---|---|---|---|
| Pi 5 16GB CPU | qwen2.5-coder:3b | **broken** (bare JSON) | 5.89 | 10.25 | ~25% |
| Pi 5 16GB CPU | qwen2.5-coder:7b | **broken** (bare JSON) | 2.37 | 4.45 | ~30% |
| Pi 5 16GB CPU | qwen3:4b | works | 4.05 | 7.81 | ~25-30% |
| Pi 5 16GB CPU | qwen3:8b | works | **1.92** | 4.34 | ~30-40% |
| Pi 5 + Hailo-10H | Qwen2-1.5B-FC | broken shim | ~6.69 | n/a | ~10-15% |
| **MacBook Air M2 16GB** | **qwen3:14b** | **works** | **10.13** | **64.19** | **~40-50%** |
| Mac Mini M4 24GB ($999, hypothetical) | Qwen3.6-27B | works | ~20-25 | ~120 | **77.2%** |
| Claude Sonnet 4.6 (cloud) | n/a | works | ~100 streaming | n/a | 79.6% |
| Claude Opus 4.7 (cloud, 1M ctx) | n/a | works | ~50 streaming | n/a | **87.6%** |

The MacBook Air wins by **5.3x decode at a 2x bigger model** versus the Pi 5's `qwen3:8b` best. Prefill is ~15x faster, which matters more than decode for tool-use loops with long context.

Going local on existing hardware costs **roughly 42 percentage points of SWE-bench** versus Opus 4.7. Going local on $999 of new hardware (Mac Mini M4 + Qwen3.6-27B) costs roughly 10 points. Privacy and quota are real; coding accuracy roughly halves at the free tier, drops only ~10 points at the $999 tier.

## act 8 — wiring it without losing the cloud escape hatch

The local LLM is the *default*. Cloud Claude stays available for the hard problems. The constraint:

> "I want cloud Claude only if I specifically invoke it. I don't want it for 'complex task' — I want my Ollama to do memories and manage multiple sessions etc."

The reflex design — silent fallback when Maral is down — is wrong. "Maral momentarily unreachable" silently spends cloud quota. Intent should be explicit.

What shipped:

```sh
# ~/.zshrc
LOCAL_LLM_HOST="192.168.10.210:11434"
LOCAL_LLM_MODEL="qwen3:14b"
LOCAL_LLM_SMALL="qwen3:8b"

claude() {
  if [[ -n "$ANTHROPIC_FORCE_CLOUD" ]]; then
    env -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_API_KEY \
        -u ANTHROPIC_MODEL -u ANTHROPIC_SMALL_FAST_MODEL command claude "$@"
    return $?
  fi
  if ! curl -sf -m 1 "http://${LOCAL_LLM_HOST}/api/version" >/dev/null 2>&1; then
    echo "[claude] ERROR: Maral unreachable. Fix Maral, or use 'claude-cloud'." >&2
    return 1
  fi
  ANTHROPIC_BASE_URL="http://${LOCAL_LLM_HOST}" \
  ANTHROPIC_AUTH_TOKEN="ollama" \
  ANTHROPIC_API_KEY="" \
  ANTHROPIC_MODEL="${LOCAL_LLM_MODEL}" \
  ANTHROPIC_SMALL_FAST_MODEL="${LOCAL_LLM_SMALL}" \
    command claude "$@"
}
claude-cloud() { ANTHROPIC_FORCE_CLOUD=1 claude "$@"; }
```

`claude` is strict-local: Maral or error. `claude-cloud` is explicit cloud. No silent cloud spend.

The state that matters lives in `~/.claude/` on the laptop, not in the model:

| Directory | What | Survives backend switch? |
|---|---|---|
| `~/.claude/memory/` | Auto-memory + index | Yes |
| `~/.claude/projects/<hash>/messages/*.jsonl` | Per-project session transcripts | Yes |
| `~/.claude/.credentials.json` | OAuth tokens | Only used on the cloud path |
| `~/.claude/sessions/` | Active session state | Yes |
| `~/.claude/plugins/` | Installed plugins/skills | Yes |

Switching `claude` to Maral does not lose memories, transcripts, multi-project work, or skills. The model just answers the same conversation with worse reasoning. Auto-memory writes will be sloppier — that's a downstream cost worth accepting for the privacy and zero-quota win.

In-flight sessions hot-swap via `/exit` → `exec zsh` → `claude --resume`. The transcript replays into qwen3:14b's context; the session continues with the new backend's reasoning from that turn forward.

**Lesson 5.** Make cloud opt-in, not auto-fallback. Silent fallback hides intent and burns quota. An explicit `claude-cloud` command makes the choice visible every time.

**Lesson 6.** Backend env vars are launch-time, not runtime. The on-disk transcript is the actual state; the model is interchangeable.

## what the trip taught me

A few things I'd tell past-me at 9am:

1. **Don't pick the hardware first.** I bought the Hailo HAT because 40 TOPS sounded great. The constraint that mattered was 2k context and a broken Ollama shim — neither of which is in the marketing copy.
2. **Tool-use claims lie.** "Qwen2.5-Coder supports tools" is true in some narrow lookup-table sense and false for any Claude-Code-class agent. Always run the smoke test.
3. **Specify *to* the bottleneck, not past it.** Pi 5 USB3 caps at 500 MB/s. Don't buy Gen5 NVMe to feed a Gen1 host.
4. **The free hardware in your house probably beats the optimized hardware on your bench.** A 2023 MacBook Air M2 16GB is a better local LLM appliance than a Pi 5 + 40-TOPS NPU + $200 NVMe upgrade. Cost: $0.
5. **Explicit beats implicit when the implicit choice spends real money.** `claude-cloud` is one keystroke longer than auto-fallback. The keystroke is worth it.

The full notes, the launchd plists, the systemd guardrails, the benchmark runner, the tool-use smoke test, and the four-line zsh router all live in [local-llm-pi5](https://github.com/jconnolly/local-llm-pi5).

*Companion post on the Maral side-of-things is queued. Next up: a longer look at what `qwen3:14b` actually fails at in a Claude Code loop.*
