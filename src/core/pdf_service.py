from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from src.config import FONTS_DIR


class PDFService:
    def __init__(self):
        pdfmetrics.registerFont(TTFont('DejaVuSans', FONTS_DIR / 'DejaVuSans.ttf'))
        pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', FONTS_DIR / 'DejaVuSans-Bold.ttf'))
        self.styles = {
            'title': ParagraphStyle(
                name='Title',
                fontName='DejaVuSans',
                fontSize=12,
                alignment=1,
                spaceAfter=20
            ),
            'heading': ParagraphStyle(
                name='Heading',
                fontName='DejaVuSans',
                fontSize=10,
                spaceAfter=10,
            ),
            'normal': ParagraphStyle(
                name='Normal',
                fontName='DejaVuSans',
                fontSize=8,
            ),
            'wrap': ParagraphStyle(
                name='WrapText',
                fontName='DejaVuSans',
                fontSize=8,
                leading=12,
                spaceBefore=0,
                spaceAfter=0,
            )
        }

    def generate_purchase_order(self, service, responsible, client, vehicle, maintenance_record):
        pdf_elements = list()

        pdf_elements.append(Paragraph('ЗАКАЗ-НАРЯД НА ТЕХНИЧЕСКОЕ ОБСЛУЖИВАНИЕ АВТОМОБИЛЯ', self.styles['title']))

        pdf_elements.append(Paragraph('Данные сервисной организации:', self.styles['heading']))
        service_data = [
            ['Наименование:', service.name],
            ['Коммерческое обозначение:', service.commercial_name],
            ['ИНН:', service.inn],
            ['ОГРН (ОГРНИП):', service.ogrn],
            ['Фактический адрес:', service.address]
        ]
        wrapped_data = []
        for row in service_data:
            wrapped_row = []
            for cell in row:
                if isinstance(cell, str):
                    wrapped_row.append(Paragraph(cell, self.styles.get('wrap')))
                else:
                    wrapped_row.append(cell)
            wrapped_data.append(wrapped_row)
        service_table = Table(wrapped_data, colWidths=[160, 300])
        service_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('LEADING', (0, 0), (-1, -1), 12),
        ]))
        pdf_elements.append(service_table)

        pdf_elements.append(Spacer(1, 10))

        pdf_elements.append(Paragraph('Данные клиента:', self.styles['heading']))
        vehicle_data = [
            ['ФИО:',
             f'{client.last_name} {client.first_name}{" " + patronymic if (patronymic := client.patronymic) else ""}'],
            ['Адрес эл. почты:', client.email],
            ['Номер телефона:', client.phone]
        ]
        vehicle_table = Table(vehicle_data, colWidths=[160, 300])
        vehicle_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        pdf_elements.append(vehicle_table)

        pdf_elements.append(Spacer(1, 10))

        pdf_elements.append(Paragraph('Данные автомобиля клиента:', self.styles['heading']))
        vehicle_data = [
            ['Марка и модель:', f'{vehicle.make.name} {vehicle.model.name}'],
            ['Цвет:', vehicle.color],
            ['Год выпуска:', vehicle.manufacture_year],
            ['Регистрационный знак:', vehicle.registration_plate],
            ['VIN:', vehicle.vin],
            ['Пробег на момент ТО:', maintenance_record.mileage]
        ]
        vehicle_table = Table(vehicle_data, colWidths=[160, 300])
        vehicle_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        pdf_elements.append(vehicle_table)

        pdf_elements.append(Spacer(1, 40))

        works_data = [
            ['Выполненные работы', 'Дата'],
            [maintenance_record.title, maintenance_record.date],
        ]
        works_table = Table(works_data, colWidths=[360, 100])
        works_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        pdf_elements.append(works_table)

        pdf_elements.append(Spacer(1, 20))

        costs_data = [
            ['Наименование', 'Стоимость'],
            ['Запчасти и расходные материалы', f'{maintenance_record.parts_cost} руб'],
            ['Работа', f'{maintenance_record.labor_cost} руб'],
        ]
        costs_table = Table(costs_data, colWidths=[360, 100])
        costs_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        pdf_elements.append(costs_table)

        total_data = [['Итого:', f'{maintenance_record.total_cost} руб']]
        total_table = Table(total_data, colWidths=[360, 100])
        total_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans-Bold'),
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        pdf_elements.append(total_table)

        pdf_elements.append(Spacer(1, 30))

        signs_data = [
            ['Подпись мастера:',
             f'__________________/ {responsible.last_name} {responsible.first_name[0]}.' +
             f'{" " + patronymic[0] + "." if (patronymic := responsible.patronymic) else ""}'],
            ['Подпись клиента:',
             f'__________________/ {client.last_name} {client.first_name[0]}.' +
             f'{" " + patronymic[0] + "." if (patronymic := client.patronymic) else ""}'],
        ]
        signs_table = Table(signs_data, colWidths=[100, 360])
        signs_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
        ]))
        pdf_elements.append(signs_table)

        buffer = BytesIO()
        pdf = SimpleDocTemplate(buffer, pagesize=A4)
        pdf.build(pdf_elements)
        buffer.seek(0)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
