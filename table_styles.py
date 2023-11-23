from reportlab.platypus import TableStyle
from reportlab.lib import colors
from reportlab.lib.units import mm

scale_factor = (297 * mm) / 1399

font_size = 14 * scale_factor
font_size_bold = 18 * scale_factor
    
table_style_gen_info = TableStyle([
    ('BOX', (0,0), (-1,-1), 1.0, colors.black),
    ('GRID', (0,0), (-1,-1), 1.0, colors.black),
    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('TEXTCOLOR', (0,0), (-1,-1), colors.black),
    ('FONTNAME', (0, 0), (-1, -1), 'Calibri'),
    ('FONTSIZE', (0, 0), (-1, -1), font_size)
])

table_style = TableStyle([
    ('BOX', (0,0), (-1,-1), 1.0, colors.black),
    ('GRID', (0,0), (-1,-1), 1.0, colors.black),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('TEXTCOLOR', (0,0), (-1,-1), colors.black),
    ('FONTNAME', (0, 0), (-1, -1), 'Calibri'),
    ('FONTSIZE', (0, 0), (-1, -1), font_size),
    ('ALIGN', (4, 0), (4, -1), 'RIGHT'),
    ('ALIGN', (5, 0), (5, -1), 'RIGHT'),
    ('ALIGN', (7, 0), (7, -1), 'RIGHT'),
    ('ALIGN', (13, 0), (13, -1), 'RIGHT')
])

table_style_bold = TableStyle([
    ('BOX', (0,0), (-1,-1), 1.0, colors.black),
    ('GRID', (0,0), (-1,-1), 1.0, colors.black),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('TEXTCOLOR', (0,0), (-1,-1), colors.black),
    ('FONTNAME', (0, 0), (-1, -1), 'Calibri-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), font_size),
    ('ALIGN', (2, 0), (2, -1), 'RIGHT')
])

table_style_premium = TableStyle([
    ('BOX', (0,0), (-1,-1), 1.0, colors.black),
    ('GRID', (0,0), (-1,-1), 1.0, colors.black),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('TEXTCOLOR', (0,0), (-1,-1), colors.black),
    ('FONTNAME', (0, 0), (-1, -1), 'Calibri'),
    ('FONTSIZE', (0, 0), (-1, -1), font_size),
    ('SPAN', (0,0), (7,0)),
    ('SPAN', (8,0), (12,0)),
    ('SPAN', (13,0), (13,0)),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'), 
    ('FONTNAME', (0, 0), (13, 0), 'Calibri-Bold'),
    ('FONTSIZE', (0, 0), (13, 0), font_size_bold)  
])

table_style_premium_total = TableStyle([
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('TEXTCOLOR', (0,0), (-1,-1), colors.black),
    ('FONTNAME', (0, 0), (-1, -1), 'Calibri-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), font_size),  
    ('ALIGN', (5, 0), (5, -1), 'RIGHT'),
    ('ALIGN', (7, 0), (7, -1), 'RIGHT'),
    ('ALIGN', (13, 0), (13, -1), 'RIGHT'),
    ('BOX', (3, 0), (3, 0), 1.0, colors.black), 
    ('BOX', (5, 0), (5, 0), 1.0, colors.black),
    ('BOX', (6, 0), (6, 0), 1.0, colors.black), 
    ('BOX', (7, 0), (7, 0), 1.0, colors.black), 
    ('BOX', (13, 0), (13, 0), 1.0, colors.black)
])

contact_style = TableStyle([
    ('INNERGRID', (0,0), (-1,-1), 0, colors.white), 
    ('BOX', (0,0), (-1,-1), 1, colors.black),
    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, -1), 'Calibri'),
    ('FONTSIZE', (0, 0), (-1, -1), font_size)
])