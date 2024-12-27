from django.shortcuts import render
from django.views.generic import ListView
from app.models import Order
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime

#   Report Lab module
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import inch

# Create your views here.

class OrderListView(ListView):
    model = Order
    template_name = 'reports/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-created_at')

def OderBill(request,*args, **kwargs):
    pk = kwargs.get('pk')
    order = get_object_or_404(Order,pk = pk)
    # Fetch all OrderItems associated with this order
    order_items = order.orderitem_set.all()  # Default reverse relationship
    current_datetime = datetime.now()  # Get current date and time

    template_path = 'reports/order_bill.html'
    context = {'order': order,
        'order_items': order_items,
        'current_datetime': current_datetime,}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #Download
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    #Show
    response['Content-Disposition'] = 'filename="bill.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response,)
    # if error then show some funny view
    if pisa_status.err:
       pass
    #    return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def reportlabview(request ,*args, **kwargs):
    pk = kwargs.get('pk')
    order = get_object_or_404(Order,pk = pk)
    # Fetch all OrderItems associated with this order
    order_items = order.orderitem_set.all()  # Default reverse relationship
    current_datetime = datetime.now()  # Get current date and time
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=letter)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # Set initial positions for text
    x_start = 50  # Horizontal margin
    y_start = 750  # Vertical starting position (from top of the page)
    line_height = 20  # Space between lines

    # Add header
    p.setFont("Helvetica-Bold", 14)
    p.drawString(x_start, y_start, "Order Details")
    y_start -= line_height

    # Add order information
    p.setFont("Helvetica", 12)
    p.drawString(x_start, y_start, f"Customer Name: {order.customer_name}")
    y_start -= line_height
    p.drawString(x_start, y_start, f"Total Order Price: {order.total_order_price}")
    y_start -= line_height
    p.drawString(x_start, y_start, f"Date: {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
    y_start -= (line_height * 2)  # Add extra space before item list

    # Add column headers for order items
    p.setFont("Helvetica-Bold", 12)
    p.drawString(x_start, y_start, "Product Name")
    p.drawString(x_start + 200, y_start, "Price")
    p.drawString(x_start + 300, y_start, "Quantity")
    p.drawString(x_start + 400, y_start, "Total")
    y_start -= line_height

    # Add order items
    p.setFont("Helvetica", 12)
    for item in order_items:
        if y_start < 50:  # Check if we're running out of space on the page
            p.showPage()  # Start a new page
            y_start = 750  # Reset y position for the new page

        p.drawString(x_start, y_start, item.product.name)
        p.drawString(x_start + 200, y_start, f"{item.product.price:.2f}")
        p.drawString(x_start + 300, y_start, f"{item.quantity}")
        p.drawString(x_start + 400, y_start, f"{item.total_product_price:.2f}")
        y_start -= line_height

    

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="hello.pdf")

def reportlabtableview(request, *args, **kwargs):
    pk = kwargs.get('pk')
    order = get_object_or_404(Order, pk=pk)
    order_items = order.orderitem_set.all()
    current_datetime = datetime.now()

    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object using SimpleDocTemplate
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Title and Order Info
    elements.append(Table(
        [[f"Order Details for {order.customer_name}"]],
        colWidths=[450],
        style=[
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 14),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ],
    ))
    elements.append(Table(
        [[
            f"Date: {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total Order Price: {order.total_order_price:.2f}"
        ]],
        colWidths=[225, 225],
        style=[
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ],
    ))

    # Header Row for Table
    data = [["Product Name", "Price", "Quantity", "Total"]]

    # Add Order Items to Table
    for item in order_items:
        data.append([
            item.product.name,
            f"{item.product.price:.2f}",
            f"{item.quantity}",
            f"{item.total_product_price:.2f}",
        ])

    # Add Total Row
    data.append(["", "", "Total Order Price:", f"{order.total_order_price:.2f}"])

    # Create the Table
    table = Table(data, colWidths=[200, 80, 80, 100])

    # Add Styling to Table
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
    ]))

    # Add Table to Elements
    elements.append(table)

    # Build PDF
    doc.build(elements)

    # Return the PDF Response
    buffer.seek(0)
    # return FileResponse(buffer, as_attachment=True, filename="order_details.pdf")
    response = HttpResponse(buffer, content_type="application/pdf")
    response['Content-Disposition'] = 'inline; filename="order_details.pdf"'
    return response