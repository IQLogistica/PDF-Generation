from io import BytesIO
from datetime import datetime

from reportlab.platypus import SimpleDocTemplate, Table, Spacer, Paragraph, Image, PageBreak
from reportlab.platypus.flowables import KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import mm, inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter

from table_styles import table_style_gen_info, table_style, table_style_bold, table_style_premium, table_style_premium_total, table_style_premium_total, contact_style

from get_data import fetch_json


def generate_quote(quote_number: str, filepath: str):

    data = fetch_json(quote_number)

    scale_factor = (297 * mm) / 1399

    doc = SimpleDocTemplate(filepath, pagesize=landscape(A4))

    doc.leftMargin = 16 * scale_factor
    doc.rightMargin = 16 * scale_factor
    doc.topMargin = 8
    doc.bottomMargin = 8

    pdfmetrics.registerFont(TTFont('Calibri', 'calibri-font-family/calibri-regular.ttf'))
    pdfmetrics.registerFont(TTFont('Calibri-Bold', 'calibri-font-family/calibri-bold.ttf'))
    pdfmetrics.registerFont(TTFont('Calibri-Italic', 'calibri-font-family/calibri-italic.ttf'))



    # Create an empty list to hold the tables
    elements = []

    styles = getSampleStyleSheet()

    heading = ParagraphStyle(
        'Heading',
        fontName='Calibri-Bold',
        fontSize=16, 
        spaceAfter=19
    )

    general_information = ParagraphStyle(
        'General Information',
        fontName='Calibri-Bold',
        fontSize=10,
        spaceAfter=4
    )

    text_normal = ParagraphStyle(
        'text',
        fontName='Calibri',
        fontSize=9,
        spaceAfter=4
    )

    text_italics = ParagraphStyle(
        'text',
        fontName='Calibri-Italic',
        fontSize=9,
        spaceAfter=4
    )


    paragraph = Paragraph("Summary of Cover\n", heading)

    elements.append(paragraph)


    paragraph = Paragraph("General Information", general_information)
    elements.append(paragraph)

    # Extract data
    quote_number = data['quote']['quoteNumber']
    policy_number = data['quote']['policyNumber']
    product_name = data['quote']['product']['productName']
    product_code = data['quote']['product']['productCode']
    expiry_date = data['quote']['expiryDate']
    insurance_policies = data['quote']['insurancePolicy']
    premium_collection = data['quote']['premiumCollection']
    payment_date = data['quote']['premiumCollection']['paymentDate']
    finalization_date = data['quote']['finalizationDate']

    broker = data['quote']['broker']
    
    broker_name = 'null' #broker['firstName'] + ' ' + broker['lastName']
    brokerage_name = 'null' # broker['brokerage']['registeredName']

    organisation = data['quote']['organisation']
    
    organisation_name = 'null' #organisation['organisationName']

    commission = str(premium_collection['commission']) + '%'

    title = 'Quote ' + organisation_name + " " + quote_number
    

    issued_date = datetime.now().strftime('%Y-%m-%d')

    # Create table data
    table_data = [
        ['Application number', policy_number],
        ['Insured', organisation_name],
        ['Product', f'{product_name} ({product_code})'],
        ['Issued Date', issued_date],
        ['Expiry Date', expiry_date]
    ]

    col_widths_info = [177, 242]
    col_widths_info = [(x * scale_factor) - 4*16/14 for x in col_widths_info]

    # Create the table and add it to the elements list
    table = Table(table_data, colWidths=col_widths_info, hAlign='LEFT')
    table.setStyle(table_style_gen_info)
    elements.append(table)

    elements.append(Spacer(1, 12))

    # Create a list for the policy details in the desired order
    policy_data = [
        ['INSURABLE INTEREST (Calculates Insured Value)', '', '', '', '', '', '', '', 'STRUCTURE', '', '', '', '', 'PREMIUM'],
        ['\n\nFields', '\n\nGridCell', '\n\nCrop', '\n\nInsured area (ha)', '\n\nExpected\nPrice\n(ZAR/ha)',
        '\n\nExpected Production Value\n(ZAR)', '\n\nInsured\nPortion (%)','\n\nInsured Value -\nPAYOUT LIMIT\n(ZAR)',
        '\n\nStart of Risk\nperiod', '\n\nLength of\nRisk Period\n(days)', '\nSoil Moisture\nDepth (20cm for\nplanting season,\n40cm for mid-\nsummer drought)', '\n\nSeverity\n(years)',
        '\n\nInsurance\nRate (%)','\n\nGross Premium - \nExcl VAT (ZAR)\n\n']
    ]

    # Define column widths
    col_widths_policy = [84, 93, 61, 181, 83, 173, 85, 111, 79, 79, 117, 69, 75, 109]
    col_widths_policy = [(x * scale_factor) - 2*16/14 for x in col_widths_policy]

    # Add the policy details to the elements list as a separate table with the heading style and specified column widths
    heading_table = Table(policy_data, colWidths=col_widths_policy)
    heading_table.setStyle(table_style_premium)
    elements.append(heading_table)

    # Initialize group counter
    group_counter = 1

    # Initialize totals
    total_insured_area = 0
    total_expected_production_value = 0
    total_insured_portion = 0
    total_insured_value = 0
    total_gross_premium = 0

    # For each insurance policy
    for policy in insurance_policies:
        # Get the policy components as a dictionary for easy access
        components = {component['componentCode']: component['componentValue'] for component in policy['policyComponents']}

        # Calculate the expected price and production
        hectares = float(components['Hectares'])
        insured_amount = policy['insuredAmount']
        expected_price = "{:.2f}".format((insured_amount * 100) / hectares if hectares != 0 else 0, 2)
        expected_production = "{:.2f}".format(insured_amount * 100, 2)

        expected_price = float(expected_price)
        expected_production = float(expected_production)

        # Update totals
        total_insured_area += hectares
        total_expected_production_value += expected_production
        total_insured_portion += 100  # Assuming this is always 100%
        total_insured_value += float(expected_production)
        total_gross_premium += float(policy['insuredPremium'])

        # Format the float as currency with commas and spaces

        expected_price = "{:,.2f}".format(expected_price)
        expected_price = expected_price.replace(",", " ")

        expected_production = "{:,.2f}".format(expected_production)
        expected_production = expected_production.replace(",", " ")

        # Create a list for the policy values in the corresponding order
        policy_values = [
            f'Group {group_counter}', 
            components.get('GridCell', ''), 
            'T.B.C', 
            hectares,
            expected_price,
            expected_production,
            '100.00%',
            expected_production,
            policy['policyEndDate'],
            components.get('Duration', ''),
            components.get('Depth', ''),
            components.get('ClaimFrequency', ''),
            "{:.2f}".format(policy['insuredRate']) + '%',
            "{:,.2f}".format(policy['insuredPremium'])
        ]

        policy_values[13] = policy_values[13].replace(",", " ")

        # Add the policy values to a table and add it to the elements list
        table = Table([policy_values], colWidths=col_widths_policy)
        table.setStyle(table_style)
        elements.append(table)

        # Increment group counter
        group_counter += 1
    # Create a list for the totals in the corresponding order
    totals = [
        '', 
        '', 
        '', 
        total_insured_area,
        '',
        "{:,.2f}".format(total_expected_production_value),
        "{:.2f}".format(total_insured_portion/(group_counter-1))+'%',
        "{:,.2f}".format(total_insured_value),
        '', 
        '', 
        '', 
        '',
        '',
        "{:,.2f}".format(total_gross_premium)
    ]

    totals[5] = totals[5].replace(",", " ")
    totals[7] = totals[7].replace(",", " ")
    totals[13] = totals[13].replace(",", " ")

    table = Table([totals], colWidths=col_widths_policy)
    table.setStyle(table_style_premium_total)
    elements.append(table)

    # Add a spacer before the premium collection table
    elements.append(PageBreak())

    paragraph = Paragraph("Summary of Cover\n", heading)

    elements.append(paragraph)

    elements.append(Spacer(1,42))

    brokerage_values = [
        ['Premium Payment Date', payment_date],
        ['Nominated Brokerage', brokerage_name],
        ['Default Broker Commission', commission],
        ['Policy Finalization Date', finalization_date]
    ]

    col_widths_brokerage = [238, 258]
    col_widths_brokerage = [(x * scale_factor) - 2*16/14 for x in col_widths_brokerage]
    col_widths_brokerage[0] = col_widths_brokerage[0] - 4*16/14

    # Create the table and add it to the elements list
    table_brokerage = Table(brokerage_values, colWidths=col_widths_brokerage, hAlign='LEFT')
    table_brokerage.setStyle(table_style_gen_info)

    # Create a table for the premium collection details in a two-column format
    premium_data = [
        ['Gross Premium - Excl VAT','', "{:,.2f}".format(premium_collection['grossPremium'])],
        ['VAT @','15,00%', "{:,.2f}".format(premium_collection['vat'])],
        ['Total Premium','', "{:,.2f}".format(premium_collection['totalPremium'])]
    ]

    
    for row in premium_data:
        row[2] = row[2].replace(",", " ")

    col_widths_premium = [sum(col_widths_policy[6:12]),col_widths_policy[12],col_widths_policy[13]]

    # Create the premium collection table with right alignment and add it to the elements list
    table_premium = Table(premium_data, colWidths=col_widths_premium, hAlign='RIGHT')
    table_premium.setStyle(table_style_bold)


    # Empty table to fix the allignemnt of the merged table
    table_empty_len = (sum(col_widths_policy))- sum(col_widths_brokerage) - sum(col_widths_premium) - 21*16/14
    col_widths_temp = [col_widths_brokerage, table_empty_len, col_widths_premium]
    table_empty = Table([''], colWidths=table_empty_len)

    # Merged table
    table = Table([[table_brokerage, table_empty, table_premium]])

    elements.append(table)


    elements.append(Spacer(1,12))

    text = "JG Shields: "
    paragraph = Paragraph(text, text_normal)
    date_text = "Datum Date: " + issued_date 
    paragraph_date = Paragraph(date_text, text_normal)

    # Add the image
    signature_image = Image('images/JG_Signature.png')

    signature_image.drawHeight =  0.5*inch
    signature_image.drawWidth = 0.5*inch

    data = [[paragraph, signature_image, paragraph_date, '']]
    table = Table(data, colWidths=[0.1*doc.width, 0.1*doc.width, 0.25*doc.width, 0.7*doc.width])


    elements.append(table)
    elements.append(Spacer(1,1))

    text = "(For and on behalf of Guardrisk Insurance Company Ltd, FSP 75 and Agnovate (Pty) Ltd, FSP 48802) "
    paragraph = Paragraph(text, text_italics)

    elements.append(paragraph)

    elements.append(Spacer(1,3))

    contact = "Kontak besonderhede"
    paragraph = Paragraph(contact, text_normal)
    contact_italics = "Contact details"
    paragraph_italics = Paragraph(contact_italics, text_italics)

    table_empty = Table([''], colWidths=([doc.width/1.2]))

    data = [[paragraph, paragraph_italics, table_empty]]

    table = Table(data)

    elements.append(table)

    table_empty = Table([''], colWidths=([doc.width/1.5]))

    contact_data = [
        ["Polis Administrasie", Paragraph("Policy administration:", text_italics), "Carl Cronje - 072 905 8989", table_empty],
        ["Produk ondersteuning", Paragraph("Product support:", text_italics), "Armand Jacobs - 061 316 3972", table_empty],
        ["Tussenganger", Paragraph("Intermediary:", text_italics), broker_name, table_empty]
    ]

    # Create the table
    table = Table(contact_data)

    table.setStyle(contact_style)

    table = KeepTogether(table)

    elements.append(table)


    # Build the PDF
    doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)


    # Create a new PDF with Reportlab
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=landscape(A4))

    # Adjust the size of the image
    image_width = 300
    image_height = 70

    # Calculate the position of the image
    x = landscape(A4)[0] - image_width - 16
    y = landscape(A4)[1] - image_height - 16

    can.drawImage("images/merged_gap.png", x=x, y=y, width=image_width, height=image_height)
    can.save()

    # Move to the beginning of the StringIO buffer
    packet.seek(0)
    watermark_pdf = PdfReader(packet)

    # Read your existing PDF
    existing_pdf = PdfReader(open(filepath, "rb"))
    output = PdfWriter()

    # Loop through all the pages of the existing PDF
    for i, page in enumerate(existing_pdf.pages):
        # Add the watermark only on the first page

        page.merge_page(watermark_pdf.pages[0])
        # Add the page to the output
        output.add_page(page)

    # Finally, write "output" to a real file
    outputStream = open(filepath, "wb")
    output.write(outputStream)
    outputStream.close()

    return title

def add_page_number(canvas, doc):

    canvas.setFont('Calibri', 10)
    canvas.drawRightString(11.5 * inch, 0.2 * inch, 'Page %d' % canvas.getPageNumber())