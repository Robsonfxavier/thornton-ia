from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

class Pergunta(BaseModel):
    mensagem: str

def carregar_conhecimento():
    textos = []
    for arquivo in os.listdir("knowledge"):
        with open(f"knowledge/{arquivo}", "r", encoding="utf-8") as f:
            textos.append(f.read())
    return "\n".join(textos)

@app.post("/chat")
async def chat(pergunta: Pergunta):

    system_prompt = open("prompt/system.txt", encoding="utf-8").read()
    conhecimento = carregar_conhecimento()

    resposta = openai.ChatCompletion.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": conhecimento},
            {"role": "user", "content": pergunta.mensagem}
        ]
    )

    return {
        "resposta": resposta.choices[0].message.content
    }
