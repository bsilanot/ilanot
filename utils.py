import pandas as pd
from io import BytesIO

def generate_excel_report(selections, student_name):
    """יצירת דוח מרוכז באקסל RTL נקי ומסודר"""
    report_rows = []
    for key, val in selections.items():
        cat, sub_cat, skill = key.split(" - ")
        # הסרת אמוג'י הצבעים
        clean_val = val.replace("🔴", "").replace("🟠", "").replace("🟡", "").replace("🟢", "").strip()
        report_rows.append({"קטגוריה": cat, "תת קטגוריה": sub_cat, "מיומנות": skill, "היגד שנבחר": clean_val})
    
    df_report = pd.DataFrame(report_rows)
    buffer = BytesIO()
    
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df_report.to_excel(writer, index=False, sheet_name="דוח מרוכז")
        workbook  = writer.book
        worksheet = writer.sheets['דוח מרוכז']
        worksheet.right_to_left()
        
    return buffer.getvalue()

def generate_community_text(selections):
    """שכתוב הדוח לפסקאות קריאות ותקניות עבור פאוור פוינט לקהילה"""
    paragraphs = []
    for key, val in selections.items():
        clean_val = val.replace("🔴", "").replace("🟠", "").replace("🟡", "").replace("🟢", "").strip()
        paragraphs.append(f"בתחום {key.split(' - ')[0]}, נצפה כי התלמיד/ה {clean_val}.")
    
    full_text = " כמו כן, ".join(paragraphs)
    return full_text

def create_sample_excel():
    """יצירת תבנית אקסל לדוגמה"""
    sample_data = pd.DataFrame([{
        "שם פרטי": "ישראל", "שם משפחה": "ישראלי", "זכר/נקבה": "זכר", "תאריך לידה": "2015-01-01",
        "שם האם": "שרה", "שם האב": "משה", "סטטוס הורים": "נשואים", "עיר מגורים": "ירושלים",
        "שם המורה": "ישראל", "הכיתה": "א'1", "קריאה": "בסיסית", "חשבון": "בסיסי", "הנגשה קוגנטיבית": "תיווך חזותי", "מטרות": "יעדים"
    }])
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        sample_data.to_excel(writer, index=False)
    return buffer.getvalue()
