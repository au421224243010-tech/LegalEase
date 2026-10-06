from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from io import BytesIO
from dotenv import load_dotenv
from ai_core.gemini_generator import GeminiDocumentGenerator
from utils.document_formatter import format_docx, format_pdf, sanitize_text

load_dotenv()
app = FastAPI(title="LegalEase", version="1.0.0")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
generator = GeminiDocumentGenerator()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

@app.get("/health")
async def health():
    return {"app": "LegalEase", "status": "ok"}

@app.post("/generate")
async def generate_document(
    document_type: str = Form(...), parties: str = Form(...), terms: str = Form(...),
    effective_date: str = Form(...), company_name: str = Form("")
):
    if not parties.strip() or not terms.strip():
        raise HTTPException(status_code=400, detail="Parties and terms are required.")
    try:
        text = await generator.generate_document(document_type, parties, terms, effective_date, company_name)
        return {"document": sanitize_text(text), "document_type": document_type}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))

@app.post("/export/docx")
async def export_docx(document: str = Form(...), document_type: str = Form("Legal Document"),
                      company_name: str = Form("LegalEase"), logo: UploadFile | None = File(None)):
    logo_bytes = await logo.read() if logo and logo.filename else None
    data = format_docx(document, document_type, company_name, logo_bytes)
    return StreamingResponse(BytesIO(data), media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                             headers={"Content-Disposition": 'attachment; filename="legalease_document.docx"'})

@app.post("/export/pdf")
async def export_pdf(document: str = Form(...), document_type: str = Form("Legal Document"),
                     company_name: str = Form("LegalEase"), logo: UploadFile | None = File(None)):
    logo_bytes = await logo.read() if logo and logo.filename else None
    data = format_pdf(document, document_type, company_name, logo_bytes)
    return StreamingResponse(BytesIO(data), media_type="application/pdf",
                             headers={"Content-Disposition": 'attachment; filename="legalease_document.pdf"'})

@app.post("/export/txt")
async def export_txt(document: str = Form(...)):
    return StreamingResponse(BytesIO(document.encode("utf-8")), media_type="text/plain; charset=utf-8",
                             headers={"Content-Disposition": 'attachment; filename="legalease_document.txt"'})
