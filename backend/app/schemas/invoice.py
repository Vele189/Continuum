from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class InvoiceStatusEnum(str, Enum):
    """Invoice status enum for API"""

    DRAFT = "draft"
    SENT = "sent"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class InvoiceItemBase(BaseModel):
    """Base schema for invoice items"""

    description: Optional[str] = None
    hours: Decimal
    hourly_rate: Decimal
    line_total: Decimal
    work_date: datetime


class InvoiceItemCreate(InvoiceItemBase):
    """Schema for creating invoice items (internal use)"""

    user_id: int
    task_id: Optional[int] = None
    logged_hour_id: Optional[int] = None


class InvoiceItem(InvoiceItemBase):
    """Schema for invoice item response"""

    id: int
    invoice_id: int
    user_id: int
    task_id: Optional[int] = None
    logged_hour_id: Optional[int] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class InvoiceBase(BaseModel):
    """Base schema for invoices"""

    project_id: int
    billing_period_start: datetime
    billing_period_end: datetime
    status: InvoiceStatusEnum = InvoiceStatusEnum.DRAFT
    tax_rate: Decimal = Decimal("0.0")


class InvoiceGenerate(InvoiceBase):
    """Schema for invoice generation request"""


class InvoiceUpdate(BaseModel):
    """Schema for updating invoice (status only)"""

    status: InvoiceStatusEnum


class Invoice(InvoiceBase):
    """Schema for invoice response"""

    id: int
    invoice_number: str
    subtotal: Decimal
    tax_amount: Decimal
    total: Decimal
    pdf_path: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    items: List[InvoiceItem] = []

    model_config = ConfigDict(from_attributes=True)


class InvoiceWithItems(Invoice):
    """Invoice with full item details"""

    items: List[InvoiceItem] = []
