from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.dxf_service import DXFService
from typing import List, Dict, Any

router = APIRouter()

@router.post("/extract", response_model=Dict[str, Any])
async def extract_dxf_data(file: UploadFile = File(...)):
    """
    Endpoint to upload a DXF file and receive extracted block attributes.
    This data can be used to populate Bill of Quantities (BOQ) or Bar Bending Schedules (BBS).
    """
    if not file.filename.lower().endswith('.dxf'):
        raise HTTPException(status_code=400, detail="Only DXF files are supported.")

    try:
        content = await file.read()
        extracted_data = DXFService.extract_attributes(content)

        return {
            "filename": file.filename,
            "count": len(extracted_data),
            "items": extracted_data
        }

    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during processing: {str(e)}")
