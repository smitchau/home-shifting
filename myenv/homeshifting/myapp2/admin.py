from django.contrib import admin
from .models import *
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table,TableStyle
# Register your models here.

# admin.site.register(Truckpartner)
# admin.site.register(Rides)
# admin.site.register(Transactions)
# admin.site.register(Contact)


def export_to_pdf(modeladmin, request, queryset):
# Create a new PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # Generate the report using ReportLab

    # Custom page size (width, height)
    custom_page_size = (900, 600)
    doc = SimpleDocTemplate(response, pagesize=custom_page_size)
    elements = []

    # Define the style for the table
    style = TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.grey),
    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 14),
    ('BOTTOMPADDING', (0,0), (-1,0), 12),
    ('BACKGROUND', (0,1), (-1,-1), colors.beige),
    ('GRID', (0,0), (-1,-1), 1, colors.black),
    ])


    # Create the table headers
    
    #headers = ['Name', 'email', 'Contact No','Package','start_date','end_date']
    #headers = ['name', 'email', 'contact_number','message']
    #headers = ['truckpartner', 'account_holder_name', 'account_number','ifsc_code','date','amount']
    headers = ['truckpartner', 'total_trip', 'today_earning','total_earning']

    #Create the table data
    data = []
    for obj in queryset:
        # data.append([obj.t_name, obj.t_email,
        # obj.t_contact,obj.package_type, obj.start_date,obj.end_date])

        # data.append([obj.htype,obj.bname,
        # obj.movefrom,obj.moveto,obj.state,obj.zipcode,obj.price,obj.razorpay_order_id,obj.razorpay_payment_id,obj.date])
           
        # data.append([obj.name, obj.email,
        # obj.number,obj.message])

        # data.append([obj.truckpartner, obj.account_holder_name,
        # obj.account_number,obj.ifsc_code, obj.date,obj.amount])

        data.append([obj.truckpartner, obj.total_trip,
        obj.today_earning,obj.total_earning])
        
    # Create the table
    t = Table([headers] + data, style=style)
    # Add the table to the elements array
    elements.append(t)
    # Build the PDF document
    doc.build(elements)
    return response

export_to_pdf.short_description = "Export to PDF"



class ShowTruckpartner(admin.ModelAdmin):
    list_display = ['t_name', 't_email', 't_contact', 'package_type','start_date','end_date']
    actions = [export_to_pdf]

admin.site.register(Truckpartner, ShowTruckpartner)

class ShowTransactions(admin.ModelAdmin):
    list_display = ['truckpartner', 'account_holder_name', 'account_number', 'ifsc_code', 'date', 'amount']
    actions = [export_to_pdf]

admin.site.register(Transactions, ShowTransactions)

class ShowTcontact(admin.ModelAdmin):
    list_display = ['name', 'email', 'number', 'message']
    actions = [export_to_pdf]

admin.site.register(Tcontact, ShowTcontact)


class ShowRides(admin.ModelAdmin):
    list_display = ['truckpartner', 'total_trip', 'today_earning', 'total_earning']
    actions = [export_to_pdf]

admin.site.register(Rides, ShowRides)