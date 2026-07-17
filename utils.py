import pandas as pd
from io import BytesIO

def generate_excel_report(selections, student_name):
    """יצירת דוח מרוכז באקסל נקי, מקודד לעברית ומימין לשמאל"""
    report_rows = []
    for key, val in selections.items():
        cat, sub_cat, skill = key.split(" - ")
        # הסרת אמוג'י הצבעים לצורך דוח נקי
        clean_val = val.replace("🔴", "").replace("🟠", "").replace("🟡", "").replace("🟢", "").strip()
        report_rows.append({"קטגוריה": cat, "תת קטגוריה": sub_cat, "מיומנות": skill, "היגד שנבחר": clean_val})
    
    df_report = pd.DataFrame(report_rows)
    buffer = BytesIO()
    
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df_report.to_excel(writer, index=False, sheet_name="דוח מרוכז")
        workbook  = writer.book
        worksheet = writer.sheets['דוח מרוכז']
        worksheet.right_to_left()  # הגדרת כיוון הדף מימין לשמאל
        
    return buffer.getvalue()

def generate_community_text(selections):
    """שכתוב הנתונים לפיסקה רציפה עבור מצגת פאוור פוינט לקהילה"""
    paragraphs = []
    for key, val in selections.items():
        cat_info = key.split(" - ")
        clean_val = val.replace("🔴", "").replace("🟠", "").replace("🟡", "").replace("🟢", "").strip()
        paragraphs.append(f"בתחום {cat_info[0]} ובהקשר של {cat_info[2]}, נצפה כי {clean_val}.")
    
    # חיבור משפטים עם מילות קישור בסיסיות וסימני פיסוק
    full_text = " כמו כן, ".join(paragraphs)
    # הסרת דוגמאות במידה וקיימות בסוגריים
    if "(" in full_text and ")" in full_text:
        full_text = full_text.split("(")[0] + full_text.split(")")[-1]
        
    return full_text

def create_sample_excel():
    """יצירת קובץ אקסל לדוגמה להעלאת תלמידים חדשים למערכת"""
    sample_data = pd.DataFrame([{
        "שם פרטי": "ישראל", "שם משפחה": "ישראלי", "זכר/נקבה": "זכר", "תאריך לידה": "2015-01-01",
        "שם האם": "שרה", "שם האב": "משה", "סטטוס הורים": "נשואים", "עיר מגורים": "ירושלים",
        "שם המורה": "ישראל", "הכיתה": "א'1", "קריאה": "בסיסית", "חשבון": "בסיסי", "הנגשה קוגנטיבית": "תיווך חזותי", "מטרות": "יעדים שנתיים"
    }])
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        sample_data.to_excel(writer, index=False)
    return buffer.getvalue()
