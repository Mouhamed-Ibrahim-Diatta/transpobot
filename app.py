"""
TranspoBot — Backend FastAPI (Version Groq)
Projet GLSi L3 — ESP/UCAD
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
    "port":     int(os.getenv("DB_PORT", 3306)),
    "user":     os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "transpobot"),
}

LLM_API_KEY  = os.getenv("GROQ_API_KEY", "")
LLM_BASE_URL = "https://api.groq.com/openai/v1"
LLM_MODEL    = "llama3-8b-8192"

# ── Schéma DB ─────────────────────────────────────────────────
DB_SCHEMA = """
Tables MySQL disponibles :

vehicules(id, immatriculation, type[bus/minibus/taxi], capacite, statut[actif/maintenance/hors_service], kilometrage, date_acquisition)
chauffeurs(id, nom, prenom, telephone, numero_permis, categorie_permis, disponibilite, vehicule_id, date_embauche)
lignes(id, code, nom, origine, destination, distance_km, duree_minutes)
tarifs(id, ligne_id, type_client[normal/etudiant/senior], prix)
trajets(id, ligne_id, chauffeur_id, vehicule_id, date_heure_depart, date_heure_arrivee, statut[planifie/en_cours/termine/annule], nb_passagers, recette)
incidents(id, trajet_id, type[panne/accident/retard/autre], description, gravite[faible/moyen/grave], date_incident, resolu)
"""

SYSTEM_PROMPT = f"""Tu es TranspoBot, l'assistant intelligent de la compagnie de transport.
Tu aides les gestionnaires a interroger la base de donnees en langage naturel.

{DB_SCHEMA}

REGLES IMPORTANTES :
1. Genere UNIQUEMENT des requetes SELECT (pas de INSERT, UPDATE, DELETE, DROP).
2. Reponds TOUJOURS en JSON avec ce format :
   {{"sql": "SELECT ...", "explication": "Ce que fait la requete"}}
3. Si la question ne peut pas etre repondue avec SQL, reponds :
   {{"sql": null, "explication": "Explication de pourquoi"}}
4. Utilise des alias clairs dans les requetes.
5. Limite les resultats a 100 lignes maximum avec LIMIT.
"""

# ── Connexion MySQL ────────────────────────────────────────────
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

# ── Appel LLM Groq ────────────────────────────────────────────
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
                    {"role": "user",   "content": question},
                ],
                "temperature": 0,
            },
            timeout=60,
        )

        if response.status_code != 200:
            raise Exception(f"Erreur Groq {response.status_code}: {response.text}")

        content = response.json()["choices"][0]["message"]["content"]

        import json
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise Exception("Reponse LLM invalide")

# ── Routes API ─────────────────────────────────────────────────
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

@app.get("/api/stats")
def get_stats():
    stats = {}
    queries = {
        "total_trajets":     "SELECT COUNT(*) as n FROM trajets WHERE statut='termine'",
        "trajets_en_cours":  "SELECT COUNT(*) as n FROM trajets WHERE statut='en_cours'",
        "vehicules_actifs":  "SELECT COUNT(*) as n FROM vehicules WHERE statut='actif'",
        "incidents_ouverts": "SELECT COUNT(*) as n FROM incidents WHERE resolu=FALSE",
        "recette_totale":    "SELECT COALESCE(SUM(recette),0) as n FROM trajets WHERE statut='termine'",
    }
    for key, sql in queries.items():
        result = execute_query(sql)
        stats[key] = result[0]["n"] if result else 0
    return stats

@app.get("/api/vehicules")
def get_vehicules():
    return execute_query("SELECT * FROM vehicules ORDER BY immatriculation")

@app.get("/api/chauffeurs")
def get_chauffeurs():
    return execute_query("""
        SELECT c.*, v.immatriculation
        FROM chauffeurs c
        LEFT JOIN vehicules v ON c.vehicule_id = v.id
        ORDER BY c.nom
    """)

@app.get("/api/trajets/recent")
def get_trajets_recent():
    return execute_query("""
        SELECT t.*, l.nom as ligne, ch.nom as chauffeur_nom,
               v.immatriculation
        FROM trajets t
        JOIN lignes l ON t.ligne_id = l.id
        JOIN chauffeurs ch ON t.chauffeur_id = ch.id
        JOIN vehicules v ON t.vehicule_id = v.id
        ORDER BY t.date_heure_depart DESC
        LIMIT 20
    """)

@app.get("/health")
def health():
    return {"status": "ok", "app": "TranspoBot"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
