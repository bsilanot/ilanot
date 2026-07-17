import streamlit as st

def init_styles():
    """הזרקת הנדסת עיצוב מתקדמת - כרטיסיות אינטראקטיביות, פונטים גדולים ומקרא צבעים פסטלי"""
    st.set_page_config(page_title="מערכת מיפוי מיומנויות דיגיטלית", layout="wide", initial_sidebar_state="expanded")
    
    st.markdown("""
        <style>
        @import url('https://googleapis.com');
        
        /* הגדרות גופן וכיווניות גלובליות */
        html, body, [data-testid="stAppViewContainer"] {
            font-family: 'Assistant', sans-serif !important;
            background-color: #f4f6f9 !important;
            direction: rtl !important;
            text-align: right !important;
        }
        
        /* שיפור הלשוניות העליונות (Tabs) */
        .stTabs [data-baseweb="tab"] {
            font-size: 20px !important;
            font-weight: 800 !important;
            color: #64748b !important;
            padding: 14px 28px !important;
            border-radius: 12px 12px 0 0 !important;
            transition: all 0.2s ease-in-out;
        }
        .stTabs [data-baseweb="tab"]:hover { color: #2563eb !important; background-color: #ea580c10 !important; }
        .stTabs [aria-selected="true"] { color: #2563eb !important; border-bottom: 4px solid #2563eb !important; background-color: #ffffff !important; }
        
        /* עיצוב כרטיסיות מידע (Cards) */
        .dashboard-card {
            background: white;
            padding: 24px;
            border-radius: 20px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.02);
            border-top: 5px solid #2563eb;
            margin-bottom: 20px;
            transition: transform 0.2s;
        }
        .dashboard-card:hover { transform: translateY(-3px); }
        
        /* הפיכת רכיב ה-Radio לכפתורי פרימיום מעוצבים צבעוניים */
        div[data-testid="stRadio"] div[role="radiogroup"] {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: wrap !important;
            gap: 15px !important;
            padding: 10px 0 !important;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] label {
            background-color: #ffffff !important;
            border: 2px solid #e2e8f0 !important;
            padding: 14px 24px !important;
            border-radius: 14px !important;
            font-size: 17px !important;
            font-weight: 600 !important;
            cursor: pointer !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.01) !important;
            transition: all 0.2s ease !important;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
            border-color: #cbd5e1 !important;
            background-color: #f8fafc !important;
        }
        /* התאמת צבע חזותי אקטיבי בעת סימון */
        div[data-testid="stRadio"] div[role="radiogroup"] [data-checked="true"] label {
            background-color: #eff6ff !important;
            border-color: #2563eb !important;
            color: #2563eb !important;
        }
        
        /* כפתורי מערכת גדולים ומזמינים */
        .stButton>button {
            width: 100% !important;
            padding: 12px 20px !important;
            border-radius: 12px !important;
            font-size: 16px !important;
            font-weight: bold !important;
            transition: all 0.2s;
        }
        </style>
    """, unsafe_allow_html=True)

def init_session_state():
    """בסיס הנתונים המשודרג הכולל תמונות הסבר ומבנה קטגוריות מלא"""
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
            "👋 מוטוריקה עדינה": {
                "✏️ אחיזת עיפרון": {
                    "🎯 אחיזה פונקציונלית": {
                        "זכר": ["🔴 לא אוחז פונקציונלית", "🟠 אוחז בקושי ומתעייף", "🟡 אוחז חלקית עם תזכורת", "🟢 אוחז עצמאי ומדויק"],
                        "נקבה": ["🔴 לא אוחזת פונקציונלית", "🟠 אוחזת בקושי ומתעייפת", "🟡 אוחזת חלקית עם תזכורת", "🟢 אוחזת עצמאי ומדויקת"]
                    }
                }
            }
        }

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_role = None
        st.session_state.user_class = None
        st.session_state.current_selections = {}
