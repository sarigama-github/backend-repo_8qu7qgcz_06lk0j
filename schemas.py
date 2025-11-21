"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal

# ------------------ Core Corporate Site Schemas ------------------

class NewsItem(BaseModel):
    title: str = Field(..., description="Headline for press release or news item")
    summary: str = Field(..., description="Short summary copy")
    url: Optional[str] = Field(None, description="Link to full release or article")
    date: str = Field(..., description="ISO date string, e.g., 2025-01-31")
    category: Literal["Press Release", "News", "Earnings", "Filing"] = "Press Release"

class PipelineItem(BaseModel):
    program_name: str = Field(..., description="Program or asset name")
    therapeutic_area: str = Field(..., description="E.g., Oncology, Cardiology")
    indication: Optional[str] = Field(None, description="Primary indication")
    phase: Literal["Pre-Clinical", "Phase I", "Phase II", "Phase III"]
    description: Optional[str] = None
    clinical_data_url: Optional[str] = None

class Product(BaseModel):
    name: str
    indication: str
    pi_url: str = Field(..., description="Full Prescribing Information URL")
    isi_url: str = Field(..., description="Important Safety Information URL")
    hcp_resources_url: Optional[str] = None

class Job(BaseModel):
    title: str
    location: str
    department: str
    apply_url: str
    description: Optional[str] = None

class ContactSubmission(BaseModel):
    type: Literal["medical", "general", "investor"]
    name: str
    email: EmailStr
    organization: Optional[str] = None
    message: Optional[str] = None

class Filing(BaseModel):
    form_type: Literal["10-K", "10-Q", "8-K", "S-1", "DEF 14A"]
    period: Optional[str] = None
    date: str
    url: Optional[str] = None

# Example legacy schemas retained for reference
class User(BaseModel):
    name: str
    email: str
    address: str
    age: Optional[int] = None
    is_active: bool = True

# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
