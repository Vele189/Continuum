"""
PDF generation utility for invoices.

Uses WeasyPrint as primary method with ReportLab as fallback.
"""
import logging
from datetime import datetime
from decimal import Decimal
from typing import Optional
from io import BytesIO

from app.dbmodels import Invoice, Project, Client
from app.utils.file_upload import get_storage_backend

logger = logging.getLogger(__name__)

# Don't import at module level - use lazy imports
WEASYPRINT_AVAILABLE = None
REPORTLAB_AVAILABLE = None


def _check_weasyprint():
    """Check if WeasyPrint is available (lazy check)."""
    global WEASYPRINT_AVAILABLE  # pylint: disable=global-statement
    if WEASYPRINT_AVAILABLE is None:
        try:
            from weasyprint import HTML  # noqa: F401, C0415
            WEASYPRINT_AVAILABLE = True
        except (ImportError, OSError) as e:
            WEASYPRINT_AVAILABLE = False
            logger.warning("WeasyPrint not available: %s. Will use ReportLab fallback.", e)
    return WEASYPRINT_AVAILABLE


def _check_reportlab():
    """Check if ReportLab is available (lazy check)."""
    global REPORTLAB_AVAILABLE  # pylint: disable=global-statement
    if REPORTLAB_AVAILABLE is None:
        try:
            from reportlab.lib import colors  # noqa: F401, C0415
            REPORTLAB_AVAILABLE = True
        except ImportError as e:
            REPORTLAB_AVAILABLE = False
            logger.warning("ReportLab not available: %s", e)
    return REPORTLAB_AVAILABLE


def _format_currency(amount: Decimal) -> str:
    """Format decimal as currency string."""
    return f"${amount:,.2f}"


def _format_date(date: datetime) -> str:
    """Format datetime as readable date string."""
    return date.strftime("%B %d, %Y")


def _generate_html_invoice(
    invoice: Invoice, project: Project, client: Optional[Client] = None
) -> str:
    """Generate HTML template for invoice."""
    items_html = ""
    for item in invoice.items:
        user_name = item.user.display_name if item.user else "Unknown"
        task_info = f"<br><small>{item.task.title}</small>" if item.task and item.task.title else ""
        description = (item.description or 'No description').replace('\n', '<br>')
        items_html += f"""
        <tr>
            <td style="white-space: nowrap;">{_format_date(item.work_date)}</td>
            <td>{user_name}{task_info}</td>
            <td>{description}</td>
            <td style="text-align: right; white-space: nowrap;">{item.hours}</td>
            <td style="text-align: right; white-space: nowrap;">
                {_format_currency(item.hourly_rate)}
            </td>
            <td style="text-align: right; white-space: nowrap;">
                {_format_currency(item.line_total)}
            </td>
        </tr>
        """

    client_name = client.name if client else "N/A"
    client_email = client.email if client else "N/A"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                color: #333;
            }}
            .header {{
                margin-bottom: 30px;
            }}
            .invoice-title {{
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            .invoice-number {{
                font-size: 18px;
                color: #666;
            }}
            .info-section {{
                display: flex;
                justify-content: space-between;
                margin-bottom: 30px;
            }}
            .info-box {{
                width: 45%;
            }}
            .info-box h3 {{
                margin-top: 0;
                color: #555;
                border-bottom: 2px solid #333;
                padding-bottom: 5px;
            }}
            .info-box p {{
                margin: 5px 0;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 30px;
            }}
            th {{
                background-color: #333;
                color: white;
                padding: 12px 8px;
                text-align: left;
                font-size: 11px;
                white-space: nowrap;
            }}
            td {{
                padding: 10px 8px;
                border-bottom: 1px solid #ddd;
                font-size: 10px;
                vertical-align: top;
                word-wrap: break-word;
            }}
            td:nth-child(1) {{
                width: 12%;
            }}
            td:nth-child(2) {{
                width: 18%;
            }}
            td:nth-child(3) {{
                width: 30%;
                word-break: break-word;
            }}
            td:nth-child(4) {{
                width: 10%;
            }}
            td:nth-child(5) {{
                width: 15%;
            }}
            td:nth-child(6) {{
                width: 15%;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            .totals {{
                margin-left: auto;
                width: 300px;
            }}
            .totals table {{
                width: 100%;
            }}
            .totals td {{
                padding: 8px;
                border: none;
            }}
            .totals td:first-child {{
                text-align: right;
                font-weight: bold;
            }}
            .totals td:last-child {{
                text-align: right;
            }}
            .total-row {{
                font-size: 18px;
                font-weight: bold;
                border-top: 2px solid #333;
            }}
            .footer {{
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
                color: #666;
                font-size: 12px;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="invoice-title">INVOICE</div>
            <div class="invoice-number">Invoice #: {invoice.invoice_number}</div>
        </div>

        <div class="info-section">
            <div class="info-box">
                <h3>Bill To:</h3>
                <p><strong>{client_name}</strong></p>
                <p>{client_email}</p>
            </div>
            <div class="info-box">
                <h3>Project:</h3>
                <p><strong>{project.name}</strong></p>
                <p>
                    Billing Period: {_format_date(invoice.billing_period_start)} - 
                    {_format_date(invoice.billing_period_end)}
                </p>
                <p>Status: {invoice.status.value.upper()}</p>
            </div>
        </div>

        <table>
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Resource</th>
                    <th>Description</th>
                    <th style="text-align: right;">Hours</th>
                    <th style="text-align: right;">Rate</th>
                    <th style="text-align: right;">Amount</th>
                </tr>
            </thead>
            <tbody>
                {items_html}
            </tbody>
        </table>

        <div class="totals">
            <table>
                <tr>
                    <td>Subtotal:</td>
                    <td>{_format_currency(invoice.subtotal)}</td>
                </tr>
                <tr>
                    <td>Tax ({invoice.tax_rate * 100:.2f}%):</td>
                    <td>{_format_currency(invoice.tax_amount)}</td>
                </tr>
                <tr class="total-row">
                    <td>Total:</td>
                    <td>{_format_currency(invoice.total)}</td>
                </tr>
            </table>
        </div>

        <div class="footer">
            <p>Generated on {_format_date(invoice.created_at)}</p>
            <p>This is an automatically generated invoice from Continuum</p>
        </div>
    </body>
    </html>
    """
    return html


def _generate_pdf_weasyprint(
    invoice: Invoice, project: Project, client: Optional[Client] = None
) -> bytes:
    """Generate PDF using WeasyPrint."""
    from weasyprint import HTML
    html_content = _generate_html_invoice(invoice, project, client)
    pdf_bytes = HTML(string=html_content).write_pdf()
    return pdf_bytes


def _generate_pdf_reportlab(
    invoice: Invoice, project: Project, client: Optional[Client] = None
) -> bytes:
    """Generate PDF using ReportLab (fallback)."""
    # pylint: disable=import-outside-toplevel, too-many-locals
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#333333'),
        spaceAfter=30,
    )
    story.append(Paragraph("INVOICE", title_style))
    story.append(Paragraph(f"Invoice #: {invoice.invoice_number}", styles['Normal']))
    story.append(Spacer(1, 20))

    # Client and Project Info
    client_name = client.name if client else "N/A"
    client_email = client.email if client else "N/A"

    info_data = [
        ['Bill To:', 'Project:'],
        [client_name, project.name],
        [
            client_email,
            (
                f"Billing Period: {_format_date(invoice.billing_period_start)} - "
                f"{_format_date(invoice.billing_period_end)}"
            )
        ],
        ['', f"Status: {invoice.status.value.upper()}"]
    ]
    info_table = Table(info_data, colWidths=[3*inch, 3*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(info_table)
    story.append(Spacer(1, 20))

    # Items Table
    items_data = [['Date', 'Resource', 'Description', 'Hours', 'Rate', 'Amount']]
    for item in invoice.items:
        user_name = item.user.display_name if item.user else "Unknown"
        task_info = f"\n{item.task.title}" if item.task and item.task.title else ""

        # Use Paragraph for better text wrapping
        date_para = Paragraph(_format_date(item.work_date), styles['Normal'])
        resource_para = Paragraph(f"{user_name}{task_info}", styles['Normal'])
        desc_para = Paragraph(item.description or 'No description', styles['Normal'])
        hours_para = Paragraph(str(item.hours), styles['Normal'])
        rate_para = Paragraph(_format_currency(item.hourly_rate), styles['Normal'])
        amount_para = Paragraph(_format_currency(item.line_total), styles['Normal'])

        items_data.append([
            date_para,
            resource_para,
            desc_para,
            hours_para,
            rate_para,
            amount_para
        ])

    # Adjust column widths for better layout
    items_table = Table(
        items_data,
        colWidths=[0.9*inch, 1.4*inch, 2.2*inch, 0.6*inch, 0.9*inch, 1*inch]
    )
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (2, -1), 'LEFT'),
        ('ALIGN', (3, 0), (5, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
    ]))
    story.append(items_table)
    story.append(Spacer(1, 20))

    # Totals
    totals_data = [
        ['Subtotal:', _format_currency(invoice.subtotal)],
        [f'Tax ({invoice.tax_rate * 100:.2f}%):', _format_currency(invoice.tax_amount)],
        ['Total:', _format_currency(invoice.total)]
    ]
    totals_table = Table(totals_data, colWidths=[4*inch, 2*inch])
    totals_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('FONTSIZE', (0, 2), (-1, 2), 14),
        ('LINEABOVE', (0, 2), (-1, 2), 2, colors.black),
    ]))
    story.append(totals_table)

    # Footer
    story.append(Spacer(1, 30))
    story.append(
        Paragraph(
            f"Generated on {_format_date(invoice.created_at)}",
            styles['Normal']
        )
    )
    story.append(
        Paragraph(
            "This is an automatically generated invoice from Continuum",
            styles['Normal']
        )
    )

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def generate_invoice_pdf(
    invoice: Invoice,
    project: Project,
    client: Optional[Client] = None
) -> bytes:
    """
    Generate PDF invoice using WeasyPrint (primary) or ReportLab (fallback).

    Args:
        invoice: Invoice object with items loaded
        project: Project object
        client: Optional Client object

    Returns:
        PDF bytes

    Raises:
        RuntimeError if neither library is available
    """
    if _check_weasyprint():
        try:
            logger.info(
                "Generating PDF for invoice %s using WeasyPrint",
                invoice.invoice_number
            )
            return _generate_pdf_weasyprint(invoice, project, client)
        except Exception as e:
            logger.warning(
                "WeasyPrint PDF generation failed: %s, falling back to ReportLab",
                e
            )
            if _check_reportlab():
                return _generate_pdf_reportlab(invoice, project, client)
            raise RuntimeError(f"PDF generation failed: {e}") from e
    elif _check_reportlab():
        logger.info(
            "Generating PDF for invoice %s using ReportLab",
            invoice.invoice_number
        )
        return _generate_pdf_reportlab(invoice, project, client)
    else:
        raise RuntimeError(
            "Neither WeasyPrint nor ReportLab is available for PDF generation"
        )


def save_invoice_pdf(
    invoice: Invoice,
    project: Project,
    client: Optional[Client] = None
) -> str:
    """
    Generate and save invoice PDF to storage.

    Args:
        invoice: Invoice object with items loaded
        project: Project object
        client: Optional Client object

    Returns:
        Storage path of the saved PDF

    Raises:
        RuntimeError if PDF generation fails
    """
    # Generate PDF
    pdf_bytes = generate_invoice_pdf(invoice, project, client)

    # Create storage path: invoices/invoice_{invoice_id}/{invoice_number}.pdf
    file_path = f"invoices/invoice_{invoice.id}/{invoice.invoice_number}.pdf"

    # Save using storage backend
    storage = get_storage_backend()
    storage.save_file(pdf_bytes, file_path)

    logger.info("Saved invoice PDF to %s", file_path)
    return file_path
