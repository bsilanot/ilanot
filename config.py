import streamlit as st

def init_styles():
    """הגדרת עיצוב חזותי רגוע ונגיש עם טקסט גדול ומקרא צבעים"""
    st.set_page_config(page_title="מערכת מיפוי מיומנויות - חינוך מיוחד", layout="wide")
    st.markdown("""
        <style>
        body { background-color: #f4f7f6; color: #2c3e50; font-size: 18px; direction: rtl; text-align: right; }
        .stButton>button { background-color: #a8dadc; color: #1d3557; font-size: 16px; border-radius: 8px; font-weight: bold; }
        .stTabs [data-baseweb="tab"] { font-size: 20px; font-weight: bold; color: #457b9d; }
        h1, h2, h3 { color: #1d3557; }
        .rating-box { padding: 10px; border-radius: 5px; margin: 5px 0; font-weight: bold; text-align: center; }
        </style>
    """, unsafe_allow_html=True)

def init_session_state():
    """אתחול נתוני המערכת בזיכרון (יוחלף בחיבור לגוגל דרייב בהמשך)"""
    if 'students' not in st.session_state:
        st.session_state.students = [
            {"id": 1, "שם פרטי": "נועם", "שם משפחה": "כהן", "מגדר": "זכר", "כיתה": "א'1", "מורה": "ישראל", "תאריך עדכון": "2026-07-15", "קריאה": "מזהה אותיות", "חשבון": "סופר עד 10", "הנגשה קוגנטיבית": "תיווך חזותי", "מטרות": "לשפר קריאה רציפה"},
            {"id": 2, "שם פרטי": "שירה", "שם משפחה": "לוי", "מגדר": "נקבה", "כיתה": "ב'3", "מורה": "רחל", "תאריך עדכון": "2026-07-16", "קריאה": "קוראת מילים", "חשבון": "חיבור עד 5", "הנגשה קוגנטיבית": "הקראה", "מטרות": "עצמאות בפתרון תרגילים"}
        ]

    if 'users' not in st.session_state:
        st.session_state.users = [
            {"שם פרטי": "אדמין", "שם משפחה": "ראשי", "סוג": "מנהל", "כיתה": "הכל", "שם משתמש": "admin", "סיסמה": "admin"},
            {"שם פרטי": "רחל", "שם משפחה": "מורה", "סוג": "מחנך", "כיתה": "ב'3", "שם משתמש": "rachel", "סיסמה": "1234"}
        ]

    if 'mapping_structure' not in st.session_state:
        st.session_state.mapping_structure = {
            "מוטוריקה עדינה": {
                "אחיזת עיפרון": {
                    "אחיזה פונקציונלית": {
                        "זכר": ["לא אוחז 🔴", "אוחז עם קושי 🟠", "אוחז חלקית 🟡", "אוחז באופן עצמאי ומדויק 🟢"],
                        "נקבה": ["לא אוחזת 🔴", "אוחזת עם קושי 🟠", "אוחזת חלקית 🟡", "אוחזת באופן עצמאי ומדויק 🟢"]
                    }
                }
            }
        }

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_role = None
        st.session_state.user_class = None
        st.session_state.current_selections = {}
