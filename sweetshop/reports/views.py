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
from reportlab.lib.pagesizes import letter, A4

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

    # Add a total line
    if y_start < 50:  # Check if we need a new page for the total
        p.showPage()
        y_start = 750

    p.setFont("Helvetica-Bold", 12)
    y_start -= line_height
    p.drawString(x_start, y_start, "Total Order Price:")
    p.drawString(x_start + 400, y_start, f"{order.total_order_price:.2f}")

    

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="hello.pdf")