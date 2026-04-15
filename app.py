"""
TranspoBot — Backend FastAPI (Version Groq OK)
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector
import os
import re
import httpx
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="TranspoBot API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Configuration ──────────────────────────────────────────────
DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "user":     os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "transpobot"),
}

# 🔥 IMPORTANT : utiliser GROQ_API_KEY
LLM_API_KEY  = os.getenv("GROQ_API_KEY")

# 🔥 Base URL Groq obligatoire
LLM_BASE_URL = "https://api.groq.com/openai/v1"

# 🔥 Modèle compatible Groq
LLM_MODEL = "llama3-8b-8192"


# ── Schéma DB ─────────────────────────────────────────────────
DB_SCHEMA = """
Tables MySQL disponibles :

vehicules(id, immatriculation, type, capacite, statut, kilometrage, date_acquisition)
chauffeurs(id, nom, prenom, telephone, numero_permis, categorie_permis, disponibilite, vehicule_id, date_embauche)
lignes(id, code, nom, origine, destination, distance_km, duree_minutes)
tarifs(id, ligne_id, type_client, prix)
trajets(id, ligne_id, chauffeur_id, vehicule_id, date_heure_depart, date_heure_arrivee, statut, nb_passagers, recette)
incidents(id, trajet_id, type, description, gravite, date_incident, resolu)
"""

SYSTEM_PROMPT = f"""
Tu es TranspoBot.

{DB_SCHEMA}

RÈGLES :
- uniquement SELECT
- réponse JSON : {{"sql": "...", "explication": "..."}}
- LIMIT 100 max
"""

# ── DB ────────────────────────────────────────────────────────
def get_db():
    return mysql.connector.connect(**DB_CONFIG)

def execute_query(sql: str):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


# ── LLM (Groq) ────────────────────────────────────────────────
async def ask_llm(question: str) -> dict:

    if not LLM_API_KEY:
        raise Exception("GROQ_API_KEY manquante")

    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{LLM_BASE_URL}/chat/completions",
            headers=headers,
            json={
                "model": LLM_MODEL,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": question},
                ],
                "temperature": 0,
            },
            timeout=60,
        )

        # 🔥 debug utile
        if response.status_code != 200:
            raise Exception(f"Erreur Groq: {response.text}")

        content = response.json()["choices"][0]["message"]["content"]

        import json
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            return json.loads(match.group())

        raise Exception("Réponse LLM invalide")


# ── API ───────────────────────────────────────────────────────
class ChatMessage(BaseModel):
    question: str

@app.post("/api/chat")
async def chat(msg: ChatMessage):
    try:
        llm_response = await ask_llm(msg.question)

        sql = llm_response.get("sql")
        explication = llm_response.get("explication", "")

        if not sql:
            return {"answer": explication, "data": [], "sql": None}

        data = execute_query(sql)

        return {
            "answer": explication,
            "data": data,
            "sql": sql,
            "count": len(data),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health():
    return {"status": "ok"}
