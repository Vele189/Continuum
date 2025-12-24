from typing import List, Optional
import logging
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session, joinedload

from app.api import deps
from app.dbmodels import User, Invoice, InvoiceItem, Project, InvoiceStatus
from app.schemas.invoice import (
    InvoiceGenerate,
    InvoiceUpdate,
    Invoice as InvoiceSchema,
    InvoiceWithItems
)
from app.services import invoice as invoice_service
from app.utils.pdf_generator import save_invoice_pdf
from app.utils.file_upload import get_storage_backend

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/generate", response_model=InvoiceSchema, status_code=status.HTTP_201_CREATED)
def generate_invoice(
    invoice_in: InvoiceGenerate,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    """
    Generate an invoice from logged hours for a project.

    - **Authentication required**
    - User must be a project member or admin
    - Billing period must contain logged hours
    - Invoice items snapshot hours and rates at generation time
    - PDF is generated and stored automatically
    """
    # Generate invoice
    invoice = invoice_service.generate_invoice(db, invoice_in, current_user)

    # Load relationships for PDF generation
    invoice = db.query(Invoice).options(
        joinedload(Invoice.items).joinedload(InvoiceItem.user),
        joinedload(Invoice.items).joinedload(InvoiceItem.task),
        joinedload(Invoice.project).joinedload(Project.client)
    ).filter(Invoice.id == invoice.id).first()

    # Generate and save PDF
    try:
        pdf_path = save_invoice_pdf(invoice, invoice.project, invoice.project.client)
        invoice.pdf_path = pdf_path
        db.commit()
        db.refresh(invoice)
    except Exception as e:
        # Log error but don't fail invoice creation
        logger.error("Failed to generate PDF for invoice %s: %s", invoice.id, e)
        # Invoice is still created, PDF can be regenerated later

    return invoice


@router.get("/", response_model=List[InvoiceSchema])
def list_invoices(
    project_id: Optional[int] = Query(None, description="Filter by project ID"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    """
    List invoices.

    - **Authentication required**
    - Users can only see invoices for projects they're members of
    - Admins can see all invoices
    - Can filter by project_id
    """
    return invoice_service.list_invoices(
        db=db,
        current_user=current_user,
        project_id=project_id,
        skip=skip,
        limit=limit
    )


@router.get("/{invoice_id}", response_model=InvoiceWithItems)
def get_invoice(
    invoice_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    """
    Get invoice details with items.

    - **Authentication required**
    - User must be a project member or admin
    - Returns full invoice with all line items
    """
    invoice = invoice_service.get_invoice(db, invoice_id, current_user)

    # Load items with relationships
    invoice = db.query(Invoice).options(
        joinedload(Invoice.items).joinedload(InvoiceItem.user),
        joinedload(Invoice.items).joinedload(InvoiceItem.task),
        joinedload(Invoice.project).joinedload(Project.client)
    ).filter(Invoice.id == invoice_id).first()

    return invoice


@router.put("/{invoice_id}", response_model=InvoiceSchema)
def update_invoice(
    invoice_id: int,
    invoice_update: InvoiceUpdate,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    """
    Update invoice status.

    - **Authentication required**
    - **Admin only**
    - Only status can be updated (totals are immutable)
    - Valid statuses: draft, sent, paid, overdue, cancelled
    """
    return invoice_service.update_invoice_status(
        db=db,
        invoice_id=invoice_id,
        invoice_update=invoice_update,
        current_user=current_user
    )


@router.get("/{invoice_id}/pdf")
def download_invoice_pdf(
    invoice_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    """
    Download invoice PDF.

    - **Authentication required**
    - User must be a project member or admin
    - Generates PDF if it doesn't exist
    - Returns PDF file for download
    """
    # Get invoice with access check
    invoice = invoice_service.get_invoice(db, invoice_id, current_user)

    # Load relationships for PDF generation
    invoice = db.query(Invoice).options(
        joinedload(Invoice.items).joinedload(InvoiceItem.user),
        joinedload(Invoice.items).joinedload(InvoiceItem.task),
        joinedload(Invoice.project).joinedload(Project.client)
    ).filter(Invoice.id == invoice_id).first()

    # Check if PDF exists, generate if not
    if not invoice.pdf_path:
        try:
            pdf_path = save_invoice_pdf(invoice, invoice.project, invoice.project.client)
            invoice.pdf_path = pdf_path
            db.commit()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate PDF: {str(e)}"
            ) from e

    # Verify PDF file exists
    storage = get_storage_backend()
    if not storage.file_exists(invoice.pdf_path):
        # Regenerate if file is missing
        try:
            pdf_path = save_invoice_pdf(invoice, invoice.project, invoice.project.client)
            invoice.pdf_path = pdf_path
            db.commit()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to regenerate PDF: {str(e)}"
            ) from e

    # Return PDF file
    try:
        pdf_bytes = storage.get_file(invoice.pdf_path)
        return StreamingResponse(
            iter([pdf_bytes]),
            media_type="application/pdf",
            headers={
                "Content-Disposition": (
                    f'attachment; filename="invoice_{invoice.invoice_number}.pdf"'
                )
            }
        )
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PDF file not found"
        ) from exc
