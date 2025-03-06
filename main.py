import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Configuración de CORS y entorno
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base de datos en memoria (diccionario)
facturas_db: Dict[str, dict] = {}

class Factura(BaseModel):
    cliente: str
    monto: float
    descripcion: str

class Pago(BaseModel):
    metodo_pago: str

@app.post("/factura/crear")
def crear_factura(factura: Factura):
    factura_id = str(uuid4())
    facturas_db[factura_id] = {**factura.dict(), "estado": "pendiente"}
    return {"id": factura_id, "mensaje": "Factura creada"}

@app.get("/factura/{factura_id}")
def obtener_factura(factura_id: str):
    if factura_id not in facturas_db:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return facturas_db[factura_id]

@app.post("/pago/realizar/{factura_id}")
def realizar_pago(factura_id: str, pago: Pago):
    if factura_id not in facturas_db:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    
    facturas_db[factura_id]["estado"] = "pagada"
    facturas_db[factura_id]["metodo_pago"] = pago.metodo_pago
    return {"mensaje": f"Pago realizado correctamente para la factura {factura_id}"}
