from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import shutil


def pdf_printer(datalist, id):



    if len(datalist[0]) > 4:
        doc = SimpleDocTemplate(str(id), pagesize=landscape(letter))
        elements = list()
        t = Table(datalist, 100, 40)
        t._argW[1] = 25
        t._argW[2] = 80
        t._argW[3] = 200
        t._argW[4] = 130
    else:
        doc = SimpleDocTemplate(str(id))
        elements = list()
        t = Table(datalist,100,40)
    t._argW[0] = 25
    t.setStyle(TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
                           ('VALIGN', (0, 0), (0, -1), 'TOP'),
                           ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                           ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                           ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                           ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                           ]))
    elements.append(t)
    doc.build(elements)
    shutil.move(str(id), 'pdf/' + str(id))
    return ('pdf/' + str(id))
