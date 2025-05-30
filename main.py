from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
from docxtpl import DocxTemplate
import uuid

app = FastAPI()

class Contacto(BaseModel):
    contact_name: str
    contact_email: str
    contact_phone: str

class Highlight(BaseModel):
    client_name: str
    summary: str
    matter_value: str
    other_info: str

class Payload(BaseModel):
    firm_name: str
    practice_area: str
    location: str
    contactos: List[Contacto]
    highlights: List[Highlight]  # <- ahora es una lista

@app.post("/generar-docx")
def generar_docx(data: Payload):
    doc = DocxTemplate("plantilla.docx")
    doc.render(data.model_dump())
    filename = f"/tmp/{uuid.uuid4()}.docx"
    doc.save(filename)
    return FileResponse(
        path=filename,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename="salida.docx"
    )
