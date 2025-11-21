import os
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Pharma Corporate API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----- Models mirrored from schemas.py (simplified for responses) -----
class NewsItemModel(BaseModel):
    title: str
    summary: str
    url: Optional[str] = None
    date: str
    category: str

class PipelineItemModel(BaseModel):
    program_name: str
    therapeutic_area: str
    indication: Optional[str] = None
    phase: str
    description: Optional[str] = None
    clinical_data_url: Optional[str] = None

class ProductModel(BaseModel):
    name: str
    indication: str
    pi_url: str
    isi_url: str
    hcp_resources_url: Optional[str] = None

class JobModel(BaseModel):
    title: str
    location: str
    department: str
    apply_url: str
    description: Optional[str] = None

class FilingModel(BaseModel):
    form_type: str
    period: Optional[str] = None
    date: str
    url: Optional[str] = None

class ContactSubmissionModel(BaseModel):
    type: str  # medical | general | investor
    name: str
    email: str
    organization: Optional[str] = None
    message: Optional[str] = None


# Utilities to read from Mongo if available, otherwise provide safe demo data

def _db_available():
    try:
        from database import db
        return db is not None
    except Exception:
        return False


def _get_documents(collection: str):
    if _db_available():
        from database import get_documents
        try:
            return get_documents(collection)
        except Exception:
            return []
    return []


def _create_document(collection: str, data: dict):
    if _db_available():
        from database import create_document
        try:
            return create_document(collection, data)
        except Exception:
            return None
    return None


@app.get("/")
def root():
    return {"message": "Pharma Corporate API running"}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        from database import db
        if db is not None:
            response["database"] = "✅ Available"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
                response["connection_status"] = "Connected"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response


# -------------------- API Endpoints --------------------

@app.get("/api/news", response_model=List[NewsItemModel])
def get_news():
    docs = _get_documents("newsitem")
    if not docs:
        # Demo data
        docs = [
            {
                "title": "ApexBio Announces Positive Phase II Results for AB-101",
                "summary": "Primary endpoint met with strong safety profile.",
                "url": "#",
                "date": datetime.utcnow().strftime("%Y-%m-%d"),
                "category": "Press Release",
            },
            {
                "title": "Q2 Earnings Call Scheduled",
                "summary": "Join management for a review of financial and pipeline progress.",
                "url": "#",
                "date": datetime.utcnow().strftime("%Y-%m-%d"),
                "category": "Earnings",
            },
            {
                "title": "ApexBio to Present at Global Oncology Congress",
                "summary": "Four posters and one oral presentation accepted.",
                "url": "#",
                "date": datetime.utcnow().strftime("%Y-%m-%d"),
                "category": "News",
            },
        ]
    # Sort by date desc if field exists
    try:
        docs.sort(key=lambda d: d.get("date", ""), reverse=True)
    except Exception:
        pass
    return docs


@app.get("/api/pipeline", response_model=List[PipelineItemModel])
def get_pipeline():
    docs = _get_documents("pipelineitem")
    if not docs:
        docs = [
            {
                "program_name": "AB-101",
                "therapeutic_area": "Oncology",
                "indication": "Metastatic melanoma",
                "phase": "Phase II",
                "description": "Selective small molecule inhibitor targeting XYZ pathway.",
                "clinical_data_url": "#",
            },
            {
                "program_name": "AB-202",
                "therapeutic_area": "Cardiology",
                "indication": "Heart failure (HFrEF)",
                "phase": "Phase III",
                "description": "First-in-class biologic to improve myocardial efficiency.",
                "clinical_data_url": "#",
            },
            {
                "program_name": "AB-303",
                "therapeutic_area": "Immunology",
                "indication": "Atopic dermatitis",
                "phase": "Phase I",
                "description": "Topical JAK/SYK dual modulator.",
                "clinical_data_url": "#",
            },
            {
                "program_name": "AB-404",
                "therapeutic_area": "Neurology",
                "indication": "Alzheimer's disease",
                "phase": "Pre-Clinical",
                "description": "Gene therapy candidate in animal studies.",
                "clinical_data_url": "#",
            },
        ]
    return docs


@app.get("/api/products", response_model=List[ProductModel])
def get_products():
    docs = _get_documents("product")
    if not docs:
        docs = [
            {
                "name": "Virelexa",
                "indication": "For the treatment of chronic viral syndrome in adults",
                "pi_url": "https://example.com/pi/virelexa.pdf",
                "isi_url": "https://example.com/isi/virelexa",
                "hcp_resources_url": "#",
            },
            {
                "name": "Cardiavax",
                "indication": "Adjunct therapy to reduce risk of CV events",
                "pi_url": "https://example.com/pi/cardiavax.pdf",
                "isi_url": "https://example.com/isi/cardiavax",
                "hcp_resources_url": "#",
            },
        ]
    return docs


@app.get("/api/jobs", response_model=List[JobModel])
def get_jobs():
    docs = _get_documents("job")
    if not docs:
        docs = [
            {
                "title": "Senior Clinical Scientist",
                "location": "Boston, MA (Hybrid)",
                "department": "Clinical Development",
                "apply_url": "#",
                "description": "Lead protocol design and data interpretation across Ph II/III.",
            },
            {
                "title": "Research Associate, Biology",
                "location": "San Diego, CA (Onsite)",
                "department": "Research",
                "apply_url": "#",
                "description": "Bench biology, assay development, and cell culture.",
            },
        ]
    return docs


@app.get("/api/filings", response_model=List[FilingModel])
def get_filings():
    docs = _get_documents("filing")
    if not docs:
        docs = [
            {"form_type": "10-Q", "period": "Q2 2025", "date": "2025-08-07", "url": "#"},
            {"form_type": "8-K", "period": "—", "date": "2025-07-22", "url": "#"},
            {"form_type": "DEF 14A", "period": "2025 Proxy", "date": "2025-04-15", "url": "#"},
        ]
    return docs


@app.post("/api/contact")
def submit_contact(payload: ContactSubmissionModel):
    saved_id = _create_document("contactsubmission", payload.model_dump())
    return {"status": "ok", "id": saved_id}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
