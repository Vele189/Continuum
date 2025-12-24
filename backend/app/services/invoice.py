from typing import List, Optional
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException, status

from app.dbmodels import (
    Invoice,
    InvoiceItem,
    InvoiceStatus,
    LoggedHour,
    Project,
    ProjectMember,
    User,
    UserRole
)
from app.schemas.invoice import InvoiceGenerate, InvoiceUpdate


def _is_admin(user: User) -> bool:
    """Check if user has admin privileges."""
    return user.role in {UserRole.ADMIN, UserRole.PROJECTMANAGER}


def _check_project_access(
    db: Session,
    project_id: int,
    user: User
) -> Project:
    """Check if user has access to project (member or admin)."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    is_admin = _is_admin(user)
    if is_admin:
        return project

    # Check if user is a project member
    member = db.query(ProjectMember).filter(
        and_(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == user.id
        )
    ).first()

    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be a project member or admin to generate invoices"
        )

    return project


def _generate_invoice_number(db: Session, year: int) -> str:
    """
    Generate sequential invoice number in format INV-YYYY-XXX.

    Returns the next invoice number for the given year.
    """
    # Find the highest invoice number for this year
    year_prefix = f"INV-{year}-"

    # Query for invoices with this year prefix, ordered by invoice number
    # We need to extract the numeric part and sort properly
    last_invoice = db.query(Invoice).filter(
        Invoice.invoice_number.like(f"{year_prefix}%")
    ).order_by(Invoice.invoice_number.desc()).first()

    if last_invoice:
        # Extract the number part (last 3 digits after the last dash)
        try:
            parts = last_invoice.invoice_number.split("-")
            if len(parts) == 3:
                last_number = int(parts[-1])
                next_number = last_number + 1
            else:
                # Fallback if format is unexpected
                next_number = 1
        except (ValueError, IndexError):
            # Fallback if format is unexpected
            next_number = 1
    else:
        next_number = 1

    # Format as XXX (3 digits, zero-padded)
    return f"{year_prefix}{next_number:03d}"


def generate_invoice(  # pylint: disable=too-many-locals
    db: Session,
    invoice_in: InvoiceGenerate,
    current_user: User
) -> Invoice:
    """
    Generate an invoice from logged hours for a project.

    Business Rules:
    - User must be project member or admin
    - Billing period must have logged hours
    - Invoice items snapshot hours + rates at generation time
    - Totals are calculated and stored immutably
    """
    # Validate date range
    if invoice_in.billing_period_start >= invoice_in.billing_period_end:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Billing period start must be before end"
        )

    # Check project access (validates project exists and user has access)
    _check_project_access(db, invoice_in.project_id, current_user)

    # Fetch logged hours within billing period
    logged_hours = db.query(LoggedHour).filter(
        and_(
            LoggedHour.project_id == invoice_in.project_id,
            LoggedHour.logged_at >= invoice_in.billing_period_start,
            LoggedHour.logged_at <= invoice_in.billing_period_end
        )
    ).all()

    if not logged_hours:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No logged hours found for the specified billing period"
        )

    # Get all users involved to fetch their hourly rates
    user_ids = {lh.user_id for lh in logged_hours}
    users = {u.id: u for u in db.query(User).filter(User.id.in_(user_ids)).all()}

    # Validate all users have hourly rates
    users_without_rates = [
        uid for uid in user_ids
        if not users[uid].hourly_rate or users[uid].hourly_rate == 0
    ]
    if users_without_rates:
        user_names = [
            users[uid].display_name or users[uid].email
            for uid in users_without_rates
        ]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Users without hourly rates: {', '.join(user_names)}"
        )

    # Generate invoice number
    year = invoice_in.billing_period_start.year
    invoice_number = _generate_invoice_number(db, year)

    # Create invoice items from logged hours
    invoice_items = []
    subtotal = Decimal("0.0")

    for lh in logged_hours:
        user = users[lh.user_id]
        hourly_rate = Decimal(str(user.hourly_rate))
        hours = Decimal(str(lh.hours))
        line_total = hours * hourly_rate

        invoice_item = InvoiceItem(
            user_id=lh.user_id,
            task_id=lh.task_id,
            logged_hour_id=lh.id,
            description=lh.note or f"Work on {lh.logged_at.strftime('%Y-%m-%d') if lh.logged_at else 'date unknown'}",
            hours=hours,
            hourly_rate=hourly_rate,
            line_total=line_total,
            work_date=lh.logged_at
        )
        invoice_items.append(invoice_item)
        subtotal += line_total

    # Calculate tax and total
    tax_rate = invoice_in.tax_rate or Decimal("0.0")
    tax_amount = subtotal * tax_rate
    total = subtotal + tax_amount

    # Create invoice
    invoice = Invoice(
        project_id=invoice_in.project_id,
        invoice_number=invoice_number,
        status=InvoiceStatus.DRAFT,
        billing_period_start=invoice_in.billing_period_start,
        billing_period_end=invoice_in.billing_period_end,
        subtotal=subtotal,
        tax_rate=tax_rate,
        tax_amount=tax_amount,
        total=total,
        created_by=current_user.id
    )

    db.add(invoice)
    db.flush()  # Get invoice ID

    # Set invoice_id for all items
    for item in invoice_items:
        item.invoice_id = invoice.id
        db.add(item)

    db.commit()
    db.refresh(invoice)

    # Load items relationship
    db.refresh(invoice)

    return invoice


def get_invoice(
    db: Session,
    invoice_id: int,
    current_user: User
) -> Invoice:
    """Get an invoice by ID with access control."""
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()

    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )

    # Check access: must be project member or admin
    _check_project_access(db, invoice.project_id, current_user)

    return invoice


def list_invoices(
    db: Session,
    current_user: User,
    project_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Invoice]:
    """List invoices with access control."""
    is_admin = _is_admin(current_user)

    query = db.query(Invoice)

    # Non-admins can only see invoices for projects they're members of
    if not is_admin:
        # Get project IDs user is a member of
        member_projects = db.query(ProjectMember.project_id).filter(
            ProjectMember.user_id == current_user.id
        ).subquery()
        query = query.filter(Invoice.project_id.in_(db.query(member_projects.c.project_id)))

    if project_id is not None:
        # Verify access to this project
        _check_project_access(db, project_id, current_user)
        query = query.filter(Invoice.project_id == project_id)

    return query.order_by(Invoice.created_at.desc()).offset(skip).limit(limit).all()


def update_invoice_status(
    db: Session,
    invoice_id: int,
    invoice_update: InvoiceUpdate,
    current_user: User
) -> Invoice:
    """Update invoice status (admin only)."""
    invoice = get_invoice(db, invoice_id, current_user)

    # Only admins can update status
    if not _is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update invoice status"
        )

    # Map enum string to InvoiceStatus enum
    status_map = {
        "draft": InvoiceStatus.DRAFT,
        "sent": InvoiceStatus.SENT,
        "paid": InvoiceStatus.PAID,
        "overdue": InvoiceStatus.OVERDUE,
        "cancelled": InvoiceStatus.CANCELLED
    }

    new_status = status_map.get(invoice_update.status.value)
    if not new_status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status: {invoice_update.status}"
        )

    invoice.status = new_status
    db.commit()
    db.refresh(invoice)

    return invoice
