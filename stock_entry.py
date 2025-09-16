import frappe
import json
import calendar
from datetime import datetime

@frappe.whitelist()
def data(doc):
    doc = json.loads(doc)
    result = []  
    for row in doc.get('custom_labour_details', []):
        salary = frappe.get_value(
            'Salary Structure Assignment',
            {"employee": row["employee"]},
            ["base","from_date"],
            as_dict=True
        )
        if salary:
            base = salary["base"]
            from_date = salary["from_date"]
            if isinstance(from_date, str):
                from_date = datetime.strptime(from_date, "%Y-%m-%d")

            month_name = from_date.strftime("%B")
            total_days = calendar.monthrange(from_date.year, from_date.month)[1]
            day_salary = base / total_days
            per_hours_salary = day_salary / 8
            # frappe.msgprint(f"Employee {row['employee']} per_hours_salary: {per_hours_salary}")
            result.append({
                "employee": row["employee"],
                "base": base,
                "month_name": month_name,
                "total_days": total_days,
                "day_salary": day_salary,
                "per_hours_salary": per_hours_salary
            })
    return result

            
            


    
