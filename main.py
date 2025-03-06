from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from uuid import uuid4

app = FastAPI()

# Base de datos en memoria (diccionario)
facturas_db: Dict[str, dict] = {}

class Factura(BaseModel):
    cliente: str
    monto: float
    descripcion: str

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
