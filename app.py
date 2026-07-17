import streamlit as st
import pandas as pd
from config import init_styles, init_session_state
from utils import generate_excel_report, generate_community_text, create_sample_excel

# טעינת הגדרות בסיסיות ועיצובים
init_styles()
init_session_state()

# ==========================================
# מנגנון התחברות (Login) לפי אפיון הרשאות
# ==========================================
if not st.session_state.logged_in:
    st.title("🔐 התחברות למערכת המיפוי הבית ספרית")
    username = st.text_input("שם משתמש")
    password = st.text_input("סיסמה", type="password")
    
    if st.button("התחבר למערכת 🚀"):
        user_found = next((u for u in st.session_state.users if u["שם משתמש"] == username and u["סיסמה"] == password), None)
        if user_found:
            st.session_state.logged_in = True
            st.session_state.user_role = user_found["סוג"]
            st.session_state.user_class = user_found["כיתה"]
            st.success(f"ברוך הבא! התחברת בהצלחה בתפקיד: {st.session_state.user_role}")
            st.rerun()
        else:
            st.error("פרטי התחברות שגויים ❌")
else:
    # סרגל צדדי להתנתקות מהמערכת
    st.sidebar.title(f"👤 מחובר: {st.session_state.user_role}")
    if st.sidebar.button("🚪 התנתק"):
        st.session_state.logged_in = False
        st.rerun()

    role = st.session_state.user_role

    # דינמיות של לשוניות בהתאם לסוג המשתמש שמופיע באפיון
    tabs_mapping = {
        "מנהל": ["🏠 דף הבית", "👥 תלמידים", "⚙️ עריכת מיפוי", "👤 משתמשים", "📝 הזנת מיפוי"],
        "רכז": ["🏠 דף הבית", "👥 תלמידים", "⚙️ עריכת מיפוי", "📝 הזנת מיפוי"],
        "מורה": ["🏠 דף הבית", "👥 תלמידים", "📝 הזנת מיפוי"],
        "מחנך": ["🏠 דף הבית", "📝 הזנת מיפוי"]
    }
    
    tabs_to_show = tabs_mapping.get(role, ["🏠 דף הבית"])
    active_tabs = st.tabs(tabs_to_show)

    # ------------------------------------------
    # לשונית 1: דף הבית + דשבורד
    # ------------------------------------------
    if "🏠 דף הבית" in tabs_to_show:
        with active_tabs[tabs_to_show.index("🏠 דף הבית")]:
            st.title("🏠 דשבורד וניהול מהיר")
            
            if role in ["מנהל", "רכז"]:
                c1, c2 = st.columns(2)
                with c1: st.button("💾 גיבוי נתונים מלא לענן Google Drive")
                with c2: st.button("🔄 שחזור נתונים מגרסה קודמת")

            st.write("---")
            df_stud = pd.DataFrame(st.session_state.students)
            st.metric("סה\"כ תלמידים רשומים בבית הספר", len(df_stud))

            st.subheader("📋 רשימת תלמידים ופעולות הזנה")
            filtered_students = st.session_state.students if role != "מחנך" else [s for s in st.session_state.students if s["כיתה"] == st.session_state.user_class]
            
            for s in filtered_students:
                col_s1, col_s2 = st.columns([3, 1])
                with col_s1:
                    st.write(f"🔹 **{s['שם פרטי']} {s['שם משפחה']}** (כיתה {s['כיתה']}) — עדכון אחרון: {s['תאריך עדכון']}")
                with col_s2:
                    st.file_uploader("העלאת אקסל אישי לתלמיד", key=f"file_{s['id']}")

    # ------------------------------------------
    # לשונית 2: תלמידים
    # ------------------------------------------
    if "👥 תלמידים" in tabs_to_show:
        with active_tabs[tabs_to_show.index("👥 תלמידים")]:
            st.title("👥 ניהול תלמידים")
            
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                with st.expander("➕ הוספת תלמיד חדש"):
                    with st.form("add_student"):
                        f_name = st.text_input("שם פרטי")
                        l_name = st.text_input("שם משפחה")
                        gender = st.selectbox("מגדר", ["זכר", "נקבה"])
                        s_class = st.text_input("כיתה")
                        if st.form_submit_button("שמור תלמיד"):
                            st.session_state.students.append({"id": len(st.session_state.students)+1, "שם פרטי": f_name, "שם משפחה": l_name, "מגדר": gender, "כיתה": s_class, "תאריך עדכון": "2026-07-17"})
                            st.success("התלמיד נוסף!")
                            st.rerun()
            with col_t2:
                st.download_button("📥 הורד קובץ אקסל לדוגמה להעלאת תלמידים", data=create_sample_excel(), file_name="sample_students.xlsx")

    # ------------------------------------------
    # לשונית 3: עריכת מיפוי
    # ------------------------------------------
    if "⚙️ עריכת מיפוי" in tabs_to_show:
        with active_tabs[tabs_to_show.index("⚙️ עריכת מיפוי")]:
            st.title("⚙️ הגדרת מיומנויות")
            st.file_uploader("העלאת מיפוי קיים מקובץ אקסל לבניית קטגוריות אוטומטית")
            st.json(st.session_state.mapping_structure)

    # ------------------------------------------
    # לשונית 4: משתמשים
    # ------------------------------------------
    if "👤 משתמשים" in tabs_to_show:
        with active_tabs[tabs_to_show.index("👤 משתמשים")]:
            st.title("👤 ניהול צוות והרשאות")
            st.write(pd.DataFrame(st.session_state.users))

    # ------------------------------------------
    # לשונית 5: הזנת מיפוי (חווית משתמש מלאה)
    # ------------------------------------------
    if "📝 הזנת מיפוי" in tabs_to_show:
        with active_tabs[tabs_to_show.index("📝 הזנת מיפוי")]:
            st.title("📝 מסך הזנת מיפוי פעיל")
            
            student_list = st.session_state.students if role != "מחנך" else [s for s in st.session_state.students if s["כיתה"] == st.session_state.user_class]
            student_names = [f"{s['שם פרטי']} {s['שם משפחה']}" for s in student_list]
            selected_student = st.selectbox("בחר תלמיד למיפוי", student_names)
            
            curr_student = next(s for s in student_list if f"{s['שם פרטי']} {s['שם משפחה']}" == selected_student)
            gender_key = "זכר" if curr_student["מגדר"] == "זכר" else "נקבה"
            
            # הצגת המיומנויות ובחירה ייחודית (תא אחד בלבד)
            for cat, sub_cats in st.session_state.mapping_structure.items():
                st.subheader(f"📂 {cat}")
                for sub_cat, skills in sub_cats.items():
                    for skill_name, ratings in skills.items():
                        options = ratings[gender_key]
                        selected_option = st.radio(f"🎯 מיומנות: {skill_name}", options, key=f"map_{curr_student['id']}_{skill_name}")
                        st.session_state.current_selections[f"{cat} - {sub_cat} - {skill_name}"] = selected_option
            
            st.write("---")
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                excel_data = generate_excel_report(st.session_state.current_selections, selected_student)
                st.download_button("📥 הורד קובץ אקסל - 'דוח מרוכז' (RTL)", data=excel_data, file_name=f"דווח_מרוכז_{curr_student['שם פרטי']}.xlsx")
            with col_d2:
                if st.button("🤝 הפק 'דוח לקהילה' לפאוור פוינט"):
                    text_report = generate_community_text(st.session_state.current_selections)
                    st.info(text_report)
