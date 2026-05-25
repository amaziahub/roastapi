# RoastAPI — Project Context

## What this is
Roast as a Service — a REST API that generates AI-powered roasts via HTTP.
Decisions and context from the design phase are captured here.

## Key decisions made
- **Stack**: Python 3.12 + FastAPI on Vercel serverless functions
- **Model**: Claude Haiku (`claude-haiku-4-5-20251001`) — fast + cheap (~$0.0003/roast)
- **Hosting**: Vercel — handles both the API (`/api/*`) and landing page (`/web`)
- **No auth on free tier** — 100 req/month enforced later via Stripe + API keys

## Business model (for context)
- Free: 100 req/month, no key
- Roaster: $9/mo, 10k req
- Savage: $49/mo, 100k req
- Target: $5k MRR via dev tools, Slack bots, B2B events

## Monetisation — not built yet, coming next
- Stripe billing
- API key generation + rate limiting
- Usage dashboard

## Roast engine design
- Styles: default, gordon_ramsay, shakespeare, corporate, senior_dev
- Levels: mild, medium, savage, brutal
- `/roast/code` is the killer feature — defaults to senior_dev + savage
- damage_rating is random float 6.0–9.9 (purely for fun)

## Client ecosystem — decided, in progress
Target users are developers who live in the terminal, CI/CD, and Slack.
Building clients to meet them there, each in its own repo:

| Repo | Status |
|------|--------|
| `amaziahub/roastapi` | Live — the API |
| `amaziahub/roastapi-python` | In progress — Python SDK + CLI |
| `amaziahub/roastapi-node` | Planned — Node/TypeScript SDK |
| `amaziahub/roastapi-action` | Planned — GitHub Action |

**Python SDK + CLI** ships together in one repo (CLI is a thin wrapper on the SDK).
**Node SDK** and **GitHub Action** are separate repos with separate versioning.
Slack/Teams bots come after the SDKs are published.

## Repos
- API: github.com/amaziahub/roastapi
- Python SDK + CLI: github.com/amaziahub/roastapi-python (in progress)
- Node SDK: github.com/amaziahub/roastapi-node (planned)
- GitHub Action: github.com/amaziahub/roastapi-action (planned)
