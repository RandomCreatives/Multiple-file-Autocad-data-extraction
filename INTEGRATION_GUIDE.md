# AutoCAD Data Extraction Integration Guide

This guide explains how to integrate the newly implemented DXF extraction features into the **DigitalMehandis_V5.0** (EthioQS) project architecture.

## Overview
The integration allows users to upload AutoCAD DXF drawings to automatically extract block attributes, which can then be used to populate Bill of Quantities (BOQ) or Bar Bending Schedules (BBS).

## Components Added

### 1. Backend Service (`backend/app/services/dxf_service.py`)
- **Purpose**: Low-level parsing of DXF files.
- **Library**: Uses `ezdxf` to traverse the drawing's modelspace.
- **Logic**: Filters for `INSERT` entities (blocks) and maps their attribute tags to values.

### 2. API Endpoint (`backend/app/api/v1/endpoints/dxf.py`)
- **Purpose**: Provides a REST interface for the frontend.
- **Endpoint**: `POST /api/v1/dxf/extract`
- **Request**: `multipart/form-data` containing the DXF file.
- **Response**: A JSON object containing the filename, item count, and a list of extracted attribute dictionaries.

### 3. Frontend Component (`frontend/src/components/DXFUpload.tsx`)
- **Purpose**: User interface for file selection and data visualization.
- **Features**:
  - File validation (accepts only `.dxf`).
  - Loading states during processing.
  - Dynamic table generation based on extracted attribute tags.
  - Call-to-action for project quantity integration.

## Migration Steps for DigitalMehandis_V5.0

To fully integrate these files into the main project:

1.  **Dependency Alignment**:
    Ensure `ezdxf` and `pandas` are added to your `backend/requirements.txt`.

2.  **Route Registration**:
    In your main API router (likely `backend/app/api/v1/api.py`), include the new DXF router:
    ```python
    from app.api.v1.endpoints import dxf
    api_router.include_router(dxf.router, prefix="/dxf", tags=["dxf"])
    ```

3.  **UI Placement**:
    Import and use the `DXFUpload` component in the relevant project page (e.g., the Take-off or Drawings management section).
    ```tsx
    import DXFUpload from '@/components/DXFUpload';

    // Inside your page component
    <DXFUpload />
    ```

4.  **Quantity Mapping**:
    The "Add to Project Quantities" button in `DXFUpload.tsx` should be connected to your existing BOQ/BBS state management or API to save the extracted items into your database.
