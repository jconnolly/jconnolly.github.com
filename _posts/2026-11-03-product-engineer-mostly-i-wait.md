---
layout: post
title: "i'm a product engineer now. mostly i wait."
date: 2026-11-03 07:30:00 -0500
categories: [ai, engineering]
tags: [agents, claude-code, product-engineering, devx, formal-methods, inner-loop, outer-loop]
description: >
  Laurie Voss says we're all product engineers now. I pulled a few months of my own
  numbers to see what that actually looks like day to day. The code part is basically
  free. The waiting part is not, and the outer loop is where I spend my brain.
---

*Laurie Voss wrote [We are all Product Engineers now](https://seldo.com/posts/we-are-all-product-engineers-now/) in September and gave the talk version at AI Engineer in New York in October. I was in attendance, went up afterward to thank him for putting my daily reality on a stage. His read is that agents already ate the cost of writing code, review and ops are next, and the human job that's left is figuring out what to build and what "good" means. I agree with him. I also had a few months of my own delivery data sitting in a folder, so I went and looked at what it says.*

## tl;dr

I merged over 500 pull requests in about three months, roughly seven a day, with a median of **20 minutes** from first commit to merge. Code is cheap now. That part of Laurie's post is just true.

The time went somewhere else. Ticket to first commit, 80th percentile, was **15.5 days**. A PR that needed another human to review it waited **28 hours** at the median. Merged to accepted in QA ran up to **5.5 days**. None of that is typing.

The part of the job I actually spend my brain on is the outer loop: fix the bug, then make that whole class of bug impossible. That's where I think product engineering, DevX and (eventually) formal verification all end up being the same job.

## what I was doing

Lately I've been gluing two big systems together. I ran several Claude Code sessions in parallel on one repo, each in its own worktree, each cutting small slices. That's why the PR count is ridiculous. A PR stopped being a unit of work for me and turned into something closer to a save point.

I pulled the numbers because I wanted to get better at estimating, and estimating by PR count was obviously meaningless.

| | p50 | p80 | p90 |
|---|---|---|---|
| PR, first commit to merge | 20 min | 2.9 h | 15.7 h |
| ticket, first commit to last merge | 0.1 d | 2.1 d | 5.4 d |
| multi-PR ticket, first commit to last merge | 1.2 d | 6.9 d | |

Once I start on something, it lands. Usually same day.

## where the time actually went

| | p50 | p80 |
|---|---|---|
| ticket created to first commit | 0.3 d | 15.5 d |
| PR waiting on another person's review | 28 h | 132 h |
| last merge to accepted in QA | 0.7 d | 5.5 d |

The long tail before the first commit is almost never "I didn't get to it." It's "we hadn't agreed what this means," or "we were waiting on somebody else to confirm it." Review by agents takes seconds; review by people happens when people get to it, which is fine, it's just slow. And merged isn't done until somebody looks at it in a test environment and says yes.

The stuff that moved my dates was never in the editor. Mostly it was getting the person who can say yes into the room. A two-hour working session that settles six open questions beats two weeks of async questions every time. The rest was writing down what done looks like before anybody (or any clanker) writes code.

## inner loop, outer loop

People have started describing agent work in two loops, and I think it's the right frame for what a product engineer does now.

The **inner loop** is the tight one: write, run, test, fix. Philipp Schmid describes it as the agent [checking its own work inside a single task](https://www.philschmid.de/inner-loop-vs-outer-loop) before it answers you. Augment's guide goes further and argues agents now [run the whole pre-commit inner loop on their own](https://www.augmentcode.com/guides/inner-loop-vs-outer-loop-ai-agents), which pushes the human up a level, and makes review and CI the new bottleneck. That lines up with my 28-hour review number pretty exactly.

The **outer loop** is everything that learns across tasks. In Schmid's version it's memory, skills and rules files that stop the agent from repeating mistakes. In mine it's the same thing for the whole team.

Here's what that looks like day to day. A bug shows up. Zoom in: fix it. With agents that's often minutes. Then zoom out: why could that bug happen at all, and what would make it impossible next time? A real type instead of a string. A schema check at the boundary between two systems. A lint rule. A CI gate. A git hook that just refuses the commit. The fix for the one bug is cheap now. The fix for the whole family of bugs is where the leverage is, and that's EXACTLY the thing I end up doing all day.

I keep a plain-text pain ledger for this. Every time something bites me it gets a line: what happened, what I did about it, what the real fix would be. First time, a workaround is fine. Second time, the root cause gets fixed. Most of the lines turn out to be policy, not code. "Never deploy without the image tag pinned." "One owner per working tree." "Nothing goes to a person without a second read."

In a conversation at AI Engineer Europe, Tuomas Artman, Linear's CTO, made the case that agents can iterate and test their way to the effect you asked for, but [choosing the right effect is still a different skill](https://ai.engineer/talks/wjk0ulMAkbc-taste-craft-conversation-tuomas-artman-cto-linear). That's an outer-loop skill. So is knowing which invariant to write down.

## where formal verification comes in

If agents are going to write most of the code, and review already can't keep up (Laurie has numbers on this, most agent PRs get no recorded review at all), then the most valuable thing a human can write isn't the code. It's the invariant. The precise statement of what has to always be true.

"A record is never sent downstream before the thing it depends on exists." "A retry never creates a second copy." Those are both bugs I've fixed this year, more than once, before I wrote the rule down.

Once it's written in a form a machine can check, every agent-written change gets held to it for free. That can be a type, a property test, a model-checked state machine, or a TLA+ spec for how two systems hand work back and forth: trust, but verify. I'm early on the formal end of that and planning to go a lot further, because it's the most direct way I know to make "define good" concrete enough that an agent can't argue with it.

That's also the best definition of DevX I've got: a system where the wrong thing is hard to type.

## what I'd measure

Output per engineer is going to look incredible on every team for the next year or so. The numbers I wish I'd had on a dashboard from day one are the waits:

- question asked (or ticket created) to first commit
- ready for review to approved, people only
- merged to accepted
- hours in meetings per day, next to merged work per day
- and for the outer loop: how many times the same class of bug shows up twice

Thanks to Laurie for the post that got me to pull the numbers.

*Numbers are mine, rounded.*
