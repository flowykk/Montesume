import openpyxl
from openpyxl.styles import PatternFill
from openpyxl.styles.borders import Border, Side

def WriteIn(data, id):
    filepath = "HelloFlask/static/excel_history/RequestHistory_"+id+".xlsx"
    wb = openpyxl.Workbook()
    ws = wb.active

    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

    ws["A1"] = "Номер запроса"
    ws.column_dimensions['A'].width = 15
    ws['A1'].fill = PatternFill(start_color="FFDF59", fill_type="solid")
    ws["B1"] = "Номер способа"
    ws.column_dimensions['B'].width = 15
    ws['B1'].fill = PatternFill(start_color="FFDF59", fill_type="solid")
    ws["C1"] = "Бизнес, привлекающий трафик"
    ws.column_dimensions['C'].width = 29
    ws['C1'].fill = PatternFill(start_color="FFDF59", fill_type="solid")
    ws["D1"] = "Бизнес конкурентов"
    ws.column_dimensions['D'].width = 19
    ws['D1'].fill = PatternFill(start_color="FFDF59", fill_type="solid")
    ws["E1"] = "Радиус окружностей"
    ws.column_dimensions['E'].width = 20
    ws['E1'].fill = PatternFill(start_color="FFDF59", fill_type="solid")
    ws["F1"] = "Адреса зафиксированных точек"
    ws.column_dimensions['F'].width = 31
    ws['F1'].fill = PatternFill(start_color="FFDF59", fill_type="solid")
    ws["G1"] = "Координаты зафиксированных точек"
    ws.column_dimensions['G'].width = 35
    ws['G1'].fill = PatternFill(start_color="FFDF59", fill_type="solid")
    ws["H1"] = "Время сделанного запроса(UTC+3:00)"
    ws.column_dimensions['H'].width = 35
    ws['H1'].fill = PatternFill(start_color="FFDF59", fill_type="solid")
    ws.cell(row=1, column=1).border = thin_border
    ws.cell(row=1, column=2).border = thin_border
    ws.cell(row=1, column=3).border = thin_border
    ws.cell(row=1, column=4).border = thin_border
    ws.cell(row=1, column=5).border = thin_border
    ws.cell(row=1, column=6).border = thin_border
    ws.cell(row=1, column=7).border = thin_border
    ws.cell(row=1, column=8).border = thin_border

    for i in range(len(data.keys())):
        ws.cell(row=i + 2, column=1).border = thin_border
        ws.cell(row=i + 2, column=2).border = thin_border
        ws.cell(row=i + 2, column=3).border = thin_border
        ws.cell(row=i + 2, column=4).border = thin_border
        ws.cell(row=i + 2, column=5).border = thin_border
        ws.cell(row=i + 2, column=6).border = thin_border
        ws.cell(row=i + 2, column=7).border = thin_border
        ws.cell(row=i + 2, column=8).border = thin_border
        ws["A" + str(i + 2)] = i + 1
        ws["B" + str(i + 2)] = int(data[str(i + 1)]["md_number"])
        ws["C" + str(i + 2)] = data[str(i + 1)]["your_business"]
        ws["D" + str(i + 2)] = data[str(i + 1)]["conc_business"]
        if data[str(i + 1)]["radius"] != "": ws["E" + str(i + 2)] = int(data[str(i + 1)]["radius"])
        ws["F" + str(i + 2)] = data[str(i + 1)]["stopped_points_adress"]
        ws["G" + str(i + 2)] = data[str(i + 1)]["stopped_points_coords"]
        ws["H" + str(i + 2)] = data[str(i + 1)]["time"]
    print("success")

    wb.save(filepath)
