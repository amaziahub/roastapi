import os
import random
from typing import Literal

from dotenv import load_dotenv

load_dotenv()

import anthropic
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
from pydantic import BaseModel

from .prompts import (
    CATEGORY_CONTEXT,
    build_code_roast_prompt,
    build_roast_prompt,
    build_system_prompt,
)

app = FastAPI(title="RoastAPI", version="1.0.0", docs_url="/api/docs", redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

Style = Literal["default", "gordon_ramsay", "shakespeare", "corporate", "senior_dev"]
Level = Literal["mild", "medium", "savage", "brutal"]
Category = Literal["developer", "designer", "founder", "manager", "devops", "data_scientist"]

CATEGORIES = list(CATEGORY_CONTEXT.keys())


def _get_client() -> anthropic.Anthropic:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY not configured")
    return anthropic.Anthropic(api_key=key)


def _call_claude(system: str, user: str) -> str:
    client = _get_client()
    try:
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=256,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
    except anthropic.AuthenticationError:
        raise HTTPException(status_code=500, detail="Invalid API key — check ANTHROPIC_API_KEY")
    except anthropic.BadRequestError as e:
        msg = e.body.get("error", {}).get("message", str(e)) if isinstance(e.body, dict) else str(e)
        raise HTTPException(status_code=502, detail=msg)
    except anthropic.APIError as e:
        raise HTTPException(status_code=502, detail=f"Anthropic API error: {e}")
    return message.content[0].text.strip()


def _damage_rating() -> float:
    return round(random.uniform(6.0, 9.9), 1)


def _roast_response(roast: str, level: str, style: str, category: str | None = None) -> dict:
    result = {
        "roast": roast,
        "damage_rating": _damage_rating(),
        "level": level,
        "style": style,
    }
    if category:
        result["category"] = category
    return result


@app.get("/web")
def landing():
    return FileResponse(Path(__file__).parent.parent / "web" / "index.html")


@app.get("/api/health")
def health():
    return {"status": "on fire 🔥"}


@app.get("/api/roast")
def roast_random(
    level: Level = Query(default="savage"),
    style: Style = Query(default="default"),
):
    system = build_system_prompt(style, level)
    prompt = build_roast_prompt(category=None, name=None, job=None, bio=None)
    roast = _call_claude(system, prompt)
    return _roast_response(roast, level, style)


@app.get("/api/roast/{category}")
def roast_by_category(
    category: Category,
    level: Level = Query(default="savage"),
    style: Style = Query(default="default"),
):
    system = build_system_prompt(style, level)
    prompt = build_roast_prompt(category=category, name=None, job=None, bio=None)
    roast = _call_claude(system, prompt)
    return _roast_response(roast, level, style, category)


class MeRequest(BaseModel):
    name: str | None = None
    job: str | None = None
    bio: str | None = None


@app.post("/api/roast/me")
def roast_me(
    body: MeRequest,
    level: Level = Query(default="savage"),
    style: Style = Query(default="default"),
):
    if not any([body.name, body.job, body.bio]):
        raise HTTPException(status_code=422, detail="Provide at least one of: name, job, bio")
    system = build_system_prompt(style, level)
    prompt = build_roast_prompt(category=None, name=body.name, job=body.job, bio=body.bio)
    roast = _call_claude(system, prompt)
    return _roast_response(roast, level, style)


class CodeRequest(BaseModel):
    code: str


@app.post("/api/roast/code")
def roast_code(
    body: CodeRequest,
    level: Level = Query(default="savage"),
    style: Style = Query(default="senior_dev"),
):
    if not body.code.strip():
        raise HTTPException(status_code=422, detail="code must not be empty")
    if len(body.code) > 8000:
        raise HTTPException(status_code=422, detail="code must be under 8000 characters")
    system = build_system_prompt(style, level)
    prompt = build_code_roast_prompt(body.code)
    roast = _call_claude(system, prompt)
    return _roast_response(roast, level, style, category="code")
