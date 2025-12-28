import json
import re
from chat.llm import ask_llm


def _clean_json(text: str) -> str:
    text = text.strip()
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)
    return text.strip()


def _extract_entity(text: str) -> str:
    text = text.lower()
    text = re.sub(r"(goes down|fails|is down|breaks)", "", text)
    return text.strip()


def parse_intent(question: str) -> dict:
    q = question.lower().strip().replace("?", "")

    # ---------- OWNER ----------
    if q.startswith("who owns"):
        entity = _extract_entity(q.replace("who owns", ""))
        return {"intent": "owner", "entity": entity}

    # ---------- BLAST RADIUS ----------
    if "what breaks if" in q:
        entity = _extract_entity(q.split("what breaks if")[-1])
        return {"intent": "blast_radius", "entity": entity}

    # ---------- PATH ----------
    if q.startswith("how does") and "connect" in q:
        match = re.findall(r"how does (.*?) connect .*? (.*)", q)
        if match:
            src, tgt = match[0]
            return {"intent": "path", "entity": [src.strip(), tgt.strip()]}

    # ---------- LLM FALLBACK ----------
    prompt = f"""
Return ONLY valid JSON. No explanation.

Schema:
{{
  "intent": "owner | blast_radius | path",
  "entity": string | [string, string]
}}

Question: "{question}"
"""

    response = ask_llm(prompt)
    cleaned = _clean_json(response)

    try:
        return json.loads(cleaned)
    except Exception:
        return {"intent": "unknown"}
