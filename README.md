# 🔥 RoastAPI — Roast as a Service

AI-powered roasts via REST API. Drop in a name, a job title, or a blob of code. Get back a surgical, category-specific roast powered by Claude Haiku.

**Live:** [roastapi.vercel.app](https://roastapi.vercel.app/web)

---

## Quick start

```bash
# Random roast
curl https://roastapi.vercel.app/api/roast

# Roast a developer at brutal level, Gordon Ramsay style
curl "https://roastapi.vercel.app/api/roast/developer?level=brutal&style=gordon_ramsay"

# Roast your code
curl -X POST https://roastapi.vercel.app/api/roast/code \
  -H "Content-Type: application/json" \
  -d '{"code": "for i in range(len(arr)):"}'
```

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/roast` | Random roast |
| `GET` | `/api/roast/{category}` | Roast by category |
| `POST` | `/api/roast/me` | Personalised roast |
| `POST` | `/api/roast/code` | Paste code, get roasted |
| `GET` | `/api/health` | Health check |

### Categories
`developer` `designer` `founder` `manager` `devops` `data_scientist`

### Query params (all endpoints)
| Param | Options | Default |
|-------|---------|---------|
| `level` | `mild` `medium` `savage` `brutal` | `savage` |
| `style` | `default` `gordon_ramsay` `shakespeare` `corporate` `senior_dev` | `default` |

### Response shape
```json
{
  "roast": "Your pull requests have cobwebs...",
  "damage_rating": 8.3,
  "level": "savage",
  "style": "gordon_ramsay",
  "category": "developer"
}
```

## Examples

### Python
```python
import requests

r = requests.get("https://roastapi.vercel.app/api/roast/founder",
                 params={"level": "brutal", "style": "corporate"})
print(r.json()["roast"])

# Personalised roast
r = requests.post("https://roastapi.vercel.app/api/roast/me",
                  json={"name": "Chad", "job": "10x Engineer", "bio": "I move fast and break things"})
print(r.json()["roast"])
```

### JavaScript
```js
// Roast a data scientist
const res = await fetch("https://roastapi.vercel.app/api/roast/data_scientist?level=savage");
const { roast, damage_rating } = await res.json();
console.log(`${roast} (${damage_rating}/10)`);

// Roast some code
const r = await fetch("https://roastapi.vercel.app/api/roast/code", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ code: "SELECT * FROM users" }),
});
console.log((await r.json()).roast);
```

### curl — code roast
```bash
curl -X POST https://roastapi.vercel.app/api/roast/code \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def get_user(id):\n    return eval(f\"users[{id}]\")"
  }'
```

---

## Run locally

```bash
git clone https://github.com/amaziahub/roastapi.git
cd roastapi
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env

python run.py
# API at http://localhost:8000
# Landing page at http://localhost:8000/web
# Docs at http://localhost:8000/api/docs
```

## Stack

- **[FastAPI](https://fastapi.tiangolo.com/)** — API framework
- **[Claude Haiku](https://anthropic.com)** — roast generation (~$0.0003/roast)
- **[Vercel](https://vercel.com)** — serverless hosting

## Pricing

| Tier | Price | Requests |
|------|-------|----------|
| Free | $0/mo | 100 req/month |
| Roaster | $9/mo | 10,000 req/month |
| Savage | $49/mo | 100,000 req/month |
