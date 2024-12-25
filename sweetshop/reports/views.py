from django.shortcuts import render
from django.views.generic import ListView
from app.models import Order
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime
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
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

