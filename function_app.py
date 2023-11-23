import azure.functions as func
import logging

import tempfile
import os

from PyPDF2 import PdfReader

from pdfgen import generate_quote

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="quote_document")
def quote_document(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    quote_number = req.params.get('quote-number')
    if not quote_number:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            quote_number = req_body.get('quote-number')

    local_path = tempfile.gettempdir()
    filepath = os.path.join(local_path, 'output.pdf')

    title = generate_quote(quote_number, filepath)

    if quote_number:
        with open(filepath, "rb") as f:
            pdf_bytes = f.read()
     
        response = func.HttpResponse(pdf_bytes,  mimetype="application/pdf")
        response.headers['Content-Disposition'] = f'inline; filename="{title}.pdf"'
        return response
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the quote-number string in the request body    .",
             status_code=200
        )