---
layout: page
title: resume
permalink: /resume/
---

[Download PDF](/assets/files/john-connolly-resume.pdf) &middot; [LinkedIn](https://www.linkedin.com/in/jeconnol) &middot; [GitHub](https://github.com/jconnolly)

**Principal Engineer** &middot; LLM platforms & distributed systems &middot; Long Island, NY

## experience

### [Data Society Group](https://datasociety.com) &middot; Lead Product Engineer
*Principal-level IC, tech lead for AI / platform &middot; Jan 2025 &ndash; Present*

- Built an **LLM teaching assistant** on AWS Bedrock + Claude (Lambda, RDS, Next.js / React 19); answers grounded in course content via Bedrock Knowledge Bases.
- Stood up the **Post-Course Reporting** app (Next.js App Router, Tailwind 4, Prisma, ECS Fargate behind ALB OIDC + Google Workspace SSO), fed by a Glue/Python job mirroring a partner's Redshift `bi` schema into RDS Postgres.
- Wrote **dsg-tools**, an internal MCP server + Claude-skill suite the engineering team uses daily to drive Jira, Bitbucket, and AWS Cost Explorer.
- Shipped the **AI Course Recommender** (Bedrock + vector search via pgvector / OpenSearch k-NN, Cognito + Google IdP, ECS + ALB) that picks curricula from learner embeddings.
- Own the Terraform setup (ECS Fargate module, Route 53, ECR, RDS, cross-account IAM) and Bitbucket Pipelines (build &rarr; ECR &rarr; `terraform apply` &rarr; ECS/Lambda) for the AI/platform side.

### Independent Engineering Consultant
*Feb 2024 &ndash; Jan 2025*

### [Flow Commerce](https://www.flow.io/) &middot; Principal Software Engineer
*Acquired by Global-E (NASDAQ: GLBE) Dec 2021 &middot; Jul 2021 &ndash; Feb 2024*

- Tech lead for 3&ndash;5 engineers building the international checkout, payments, tax, and fulfillment engine behind **Shopify Managed Markets** (originally Markets Pro). Scala, Akka, Play, AWS, Kubernetes, Postgres.
- Took it from POC to **$50M+ GMV** across **3,500+ merchants** and **136 international markets**; hit GA on Shopify Plus by Feb 2024.
- After Global-E acquired the company, merged Flow's stack into the joint Managed Markets product: catalog, currency, tax, order routing.
- Tuned the engine for Shopify Plus BFCM traffic: multi-currency pricing, multi-region inventory, merchant-of-record tax.

### [Netsmart](https://www.ntst.com/) &middot; Team Lead & Senior Architect
*Behavioral-health EHR &middot; Feb 2020 &ndash; Jul 2021*

- Led 3&ndash;5 engineers migrating a legacy MUMPS/Java clinical stack to Angular, Spring Boot, Postgres, and Kubernetes.

### Perfumania Holdings &middot; Senior Applications Engineer
*Jan 2018 &ndash; Feb 2020*

- Migrated the legacy eCommerce stack to Shopify (dotcom and Amazon Marketplace).

### Earlier

Senior Software Engineer, OpenXchange (2016&ndash;2018) &middot; Senior Software Engineer, CooCoo (2015&ndash;2016) &middot; Software Engineer, TheLadders (2012&ndash;2015) &middot; Lead Software Engineer (team of 7&ndash;9), BugLabs (2008&ndash;2012).

## selected projects

**Virtual Teaching Assistant** &middot; *Data Society, 2025.* Bedrock + Claude teaching assistant for cohort-based courses. Retrieval against course materials via Knowledge Bases; tool-use for code lookups. Lambda + RDS, Next.js frontend.

**dsg-tools** &middot; *Data Society, 2025.* Internal MCP server + Claude-skill suite for Jira (transitions, comments, ADF), Bitbucket (PRs, pipeline logs, deployment vars), and AWS (Cost Explorer, SSM, ephemeral webhook tunnels).

See [/projects/](/projects/) for the rest, including recent AI/LLM hardware experiments.

## education

**Stony Brook University** &middot; B.S. Computer Science. Worked on game-theoretic research with Dr. Patrick Grim; co-authored papers in MIT's *Artificial Life* and *Public Affairs Quarterly* &mdash; see [/about/](/about/#writing).

**[Hacker School](https://www.recurse.com)** (now the [Recurse Center](https://www.recurse.com/about)) &middot; batch [2], winter 2012.

## skills

**AI / LLM:** AWS Bedrock, Anthropic Claude API, Bedrock Knowledge Bases, vector search (pgvector, OpenSearch k-NN), embeddings, MCP, tool-use / agentic workflows.

**Backend & infra:** AWS (ECS Fargate, Lambda, Glue, RDS Postgres, ALB, Cognito), Next.js / React, Akka, Play, Spring Boot, Prisma, Kubernetes, Docker, Terraform.

**Languages & tools:** Scala, Java, Python, TypeScript / JavaScript, bash; Terraform, Bitbucket Pipelines, Git.
