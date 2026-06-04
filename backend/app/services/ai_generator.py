import json
import logging
from typing import Any, Dict

import httpx
from openai import OpenAI

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def _build_prompt(payload: Dict[str, Any]) -> str:
    return (
        "You are an expert marketing copywriter.\n"
        "Create engaging content for the given product and platform.\n"
        "Return ONLY valid JSON with the keys: caption, short_ad_text, hashtags, email_subject, cta.\n"
        "hashtags must be an array of strings.\n\n"
        f"Product name: {payload['product_name']}\n"
        f"Product description: {payload['product_description']}\n"
        f"Target audience: {payload['target_audience']}\n"
        f"Platform: {payload['platform_type']}\n"
    )


async def generate_marketing_copy(payload: Dict[str, Any]) -> Dict[str, Any]:
    prompt = _build_prompt(payload)

    if settings.ai_provider == "openai":
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured")
        client = OpenAI(api_key=settings.openai_api_key)
        completion = client.responses.create(
            model=settings.openai_model,
            input=prompt,
            text={
                "format": {
                    "type": "json_schema",
                    "name": "marketing_copy",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "caption": {"type": "string"},
                            "short_ad_text": {"type": "string"},
                            "hashtags": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                            "email_subject": {"type": "string"},
                            "cta": {"type": "string"},
                        },
                        "required": [
                            "caption",
                            "short_ad_text",
                            "hashtags",
                            "email_subject",
                            "cta",
                        ],
                        "additionalProperties": False,
                    },
                },
            },
        )
        text = completion.output_text
        logger.info("AI raw JSON response from OpenAI: %s", text)
        return json.loads(text)

    if settings.ai_provider == "gemini":
        if not settings.gemini_api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured")

        url = "https://generativelanguage.googleapis.com/v1beta/models/{}:generateContent".format(
            settings.gemini_model
        )
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                url,
                params={"key": settings.gemini_api_key},
                json={
                    "contents": [
                        {
                            "parts": [
                                {
                                    "text": (
                                        prompt
                                        + '\nReturn ONLY JSON like: {"caption": "...", '
                                        '"short_ad_text": "...", "hashtags": ["#a", "#b"], '
                                        '"email_subject": "...", "cta": "..."}.'
                                    )
                                }
                            ]
                        }
                    ]
                },
            )
        resp.raise_for_status()
        data = resp.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        logger.info("AI raw JSON response from Gemini: %s", text)
        return json.loads(text)

    raise RuntimeError("Unsupported AI provider configured")
