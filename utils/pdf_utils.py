import qrcode
import base64
from io import BytesIO
from django.utils import translation
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.utils.translation import gettext as _


def generar_qr(texto):
    qr = qrcode.make(texto)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return qr_base64


def generar_pdf(template_src, contexto={}):
    template = get_template(template_src)
    html = template.render(contexto)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="nota_ingreso.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("Error al generar PDF")
    return response

current_lang = translation.get_language()