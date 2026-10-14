---
layout: page
title: resume
permalink: /resume/
image: /assets/img/og/resume.png
---

[Download PDF](/assets/files/john-connolly-resume.pdf) &middot; [LinkedIn](https://www.linkedin.com/in/jeconnol) &middot; [GitHub](https://github.com/jconnolly) &middot; [john@connol.ly](mailto:john@connol.ly)

**Principal Engineer** &middot; AI Engineer: LLM apps, RAG, evals, agents, MCP &middot; Product & Forward-Deployed Engineering &middot; Python, TypeScript, Azure, AWS, Terraform

## experience

### [Data Society Group](https://datasociety.com) &middot; Lead Product Engineer
*Principal-level IC &middot; Remote &middot; Jan 2025 &ndash; Present*

Ran engineering, delivery and product for a construction client's program while building the backend and running the infrastructure myself.

**Project intake and financial operations platform** (bid to accounting and operations, ERP integration)

- Reviewed the proposal and estimate early; shaped the schedule, roles and split of work across onshore, offshore and partner developers.
- Solutions architecture: Figma designs to data model and OpenAPI spec. Designed and built the integration with the client's ERP: contract and project creation, approval callbacks, outbox dispatch, reconciliation.
- Led delivery to go-live with the client and integration partner: Jira program, sprint planning, stakeholder reporting.
- Playwright end-to-end tests confirming records landed in the ERP.
- AI-assisted development: parallel Claude Code agents in isolated devcontainers and git worktrees, adversarial PR review, verify-before-merge CI gates. Documented it for the team.

**Generative AI document Q&A pilot on Azure** (Jun 2026 &ndash; present)

- Ingestion: Azure AI Document Intelligence and native Office extractors produce validated JSON, chunked and embedded into pgvector. Hybrid retrieval with version-aware answers.
- Golden-question eval harness with a recorded baseline, turn logging and a conversation audit trail. An end-to-end pipeline integration test caught a real cross-PR bug.
- Azure infra in Terraform: Container Apps and Jobs, GitHub OIDC deploys, Entra ID JWT auth. The agent UI runs as a Module Federation remote inside the client's app.

**Internal / platform**

- Stood up the Post-Course Reporting app (Next.js App Router, Tailwind 4, Prisma, ECS Fargate behind ALB OIDC + Google Workspace SSO), fed by a Glue/Python job mirroring a partner's Redshift schema into RDS Postgres.
- Owned Terraform (ECS Fargate module, Route 53, ECR, RDS, cross-account IAM) and Bitbucket Pipelines (build &rarr; ECR &rarr; `terraform apply` &rarr; ECS/Lambda) for the AI/platform side.
- LLM teaching assistant (Amazon Bedrock + Claude, RAG over course content) and AI course recommender (embeddings + vector search) on AWS ECS/Lambda.
- **dsg-tools**: an MCP server and Claude skills the engineering team uses daily for Jira, Bitbucket and AWS.

### Career break
*Feb 2024 &ndash; Dec 2024*

Planned break for family time and hands-on work. Restoring a 13' Boston Whaler (stripped to bare fiberglass; sanding, fairing, gelcoat; mahogany trim to come). Worked on a 1993 Volvo to learn car mechanics from the ground up.

### [Flow Commerce](https://www.flow.io/) &middot; Principal Software Engineer
*Acquired by Global-e (NASDAQ: GLBE) &middot; Jul 2021 &ndash; Feb 2024*

- Tech lead for 3&ndash;5 engineers on the checkout, payments, tax and fulfillment engine behind **Shopify Markets Pro** (now Shopify Managed Markets). Scala, Akka, Play, PostgreSQL, AWS, Kubernetes.
- Took it from proof of concept to **$50M+ GMV** across **3,500+ merchants** and **136 international markets**.
- After the Global-e acquisition, merged Flow's stack into the joint product: catalog, currency, tax, order routing.
- Tuned for Shopify Plus Black Friday / Cyber Monday traffic.

### [Netsmart](https://www.ntst.com/) &middot; Software Architect Team Lead
*Software Architect Team Lead, Nov 2020 &ndash; Jul 2021 &middot; Lead Software Architect, Jun 2020 &ndash; Nov 2020*

- Led the team modernizing the flagship Avatar platform (a 40-year-old application) onto Java 11, Spring Boot and Angular.
- Mixed persistence across PostgreSQL and InterSystems Caché/MUMPS, with language translation tooling to move legacy code.
- CI/CD and containers: Docker, Kubernetes/OpenShift, Jenkins, JMeter.

### Perfumania &middot; Senior Applications Engineer
*Jan 2018 &ndash; Feb 2020*

- Owned perfumania.com end to end, from content publishing to order fulfillment.
- Migrated the legacy IBM WebSphere Commerce stack to Shopify (dotcom and Amazon Marketplace).
- Linux, Apache, deployments; integrations in Java, Mule, SQL Server and DB2.

### Bug Labs &middot; Lead Software Engineer
*Feb 2008 &ndash; Apr 2012*

Grew from QA to development lead of a 7&ndash;9 person team.

- SDK and rootfs for the BUG modular embedded Linux platform: OMAP kernels, Linaro/OpenEmbedded upstream work, drivers.
- Java/JNI/C APIs for hardware modules; XMPP and chunked-HTTP cloud messaging.
- DARPA street-level capture pilot (OpenCV, Python); Processing color-tracking demo at MoMA's *Talk to Me* (2011); IoT data service backend (now dweet.io).

### Earlier

Senior Software Engineer, Open-Xchange (2016&ndash;2017) &middot; Senior Software Engineer, CooCoo (2015&ndash;2016; backend and middleware: Java 8, Apache Camel, AWS SQS/CloudWatch, MySQL, WildFly) &middot; Software Engineer, Platform & API Services, TheLadders (2012&ndash;2015; Storm, RabbitMQ, Scala, Java, Clojure, Couchbase, Elasticsearch; metrics infra, CI, email migration ETL, data access for data science).

## projects

**local-llm-pi5** &middot; *2026.* Raspberry Pi 5 + Hailo-10H vs. Apple Silicon with measured tok/s. Hailo wins on compiled vision/Whisper models, not agentic LLMs (2B ceiling, 2k context).

## publications

- Grim, Selinger, Braynen, Rosenberger, Au, Louie, Connolly. "Reducing Prejudice: A Spatialized Game-Theoretic Model for the Contact Hypothesis." *Artificial Life IX*, MIT Press, 2004, pp. 244&ndash;250.
- Grim, Selinger, Braynen, Rosenberger, Au, Louie, Connolly. "Modeling Prejudice Reduction: Spatialized Game Theory and the Contact Hypothesis." *Public Affairs Quarterly* 19(2), 2005, pp. 95&ndash;125.

## education

**Stony Brook University** &middot; B.S. Computer Science.

## skills

**Leadership & architecture:** Technical Leadership, Solutions Architecture, API Design, Data Modeling, Stakeholder Management, Program Management.

**AI / LLM:** Generative AI, Retrieval-Augmented Generation (RAG), LLM Evaluation, AI Agents, Model Context Protocol (MCP), Claude API, Azure OpenAI, Azure AI Document Intelligence, Amazon Bedrock, pgvector.

**Engineering:** Python, TypeScript, Scala, Terraform, Kubernetes, PostgreSQL, Playwright, CI/CD, Embedded Linux, OpenCV.
