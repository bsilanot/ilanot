import streamlit as st
import pandas as pd
from config import init_styles, init_session_state
from utils import generate_excel_report, generate_community_text, create_sample_excel

init_styles()
init_session_state()

if not st.session_state.logged_in:
    # מסך התחברות יוקרתי וממורכז
    st.markdown('<div style="text-align:center; padding: 50px 0;"><h1>🏫 מערכת מיפוי מיומנויות דיגיטלית</h1><p style="color:#64748b; font-size:20px;">בית ספר לחינוך מיוחד - ממשק ניהול פדגוגי</p></div>', unsafe_allow_html=True)
    
    _, col_center, _ = st.columns([1, 2, 1])
    with col_center:
        st.markdown('<div class="dashboard-card" style="border-top-color:#2563eb;">', unsafe_allow_html=True)
        st.subheader("🔐 כניסת צוות מורשה")
        username = st.text_input("שם משתמש")
        password = st.text_input("סיסמה", type="password")
        if st.button("התחבר למערכת 🚀", use_container_width=True):
            user_found = next((u for u in st.session_state.users if u["שם משתמש"] == username and u["סיסמה"] == password), None)
            if user_found:
                st.session_state.logged_in = True
                st.session_state.user_role = user_found["סוג"]
                st.session_state.user_class = user_found["כיתה"]
                st.rerun()
            else:
                st.error("שם משתמש או סיסמה שגויים ❌")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    # סרגל צד מעוצב
    st.sidebar.markdown(f'<div style="background-color:#ffffff; padding:20px; border-radius:15px; box-shadow:0 4px 10px rgba(0,0,0,0.03); border-right: 5px solid #2563eb;">👋 שלום, <b>{st.session_state.user_role}</b><br><small style="color:#64748b;">מחובר כעת למערכת</small></div>', unsafe_allow_html=True)
    st.sidebar.write("")
    if st.sidebar.button("🚪 התנתק וצא", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    role = st.session_state.user_role
    tabs_mapping = {
        "מנהל": ["🏠 דף הבית", "👥 תלמידים", "⚙️ עריכת מיפוי", "👤 משתמשים", "📝 הזנת מיפוי"],
        "רכז": ["🏠 דף הבית", "👥 תלמידים", "⚙️ עריכת מיפוי", "📝 הזנת מיפוי"],
        "מורה": ["🏠 דף הבית", "👥 תלמידים", "📝 הזנת מיפוי"],
        "מחנך": ["🏠 דף הבית", "📝 הזנת מיפוי"]
    }
    
    tabs_to_show = tabs_mapping.get(role, ["🏠 דף הבית"])
    active_tabs = st.tabs(tabs_to_show)

    # ------------------------------------------
    # לשונית 1: דף הבית והדשבורד
    # ------------------------------------------
    if "🏠 דף הבית" in tabs_to_show:
        with active_tabs[tabs_to_show.index("🏠 דף הבית")]:
            st.markdown('<h2>📊 לוח בקרה וניהול פדגוגי</h2>', unsafe_allow_html=True)
            
            # כרטיסיות דשבורד צבעוניות
            df_stud = pd.DataFrame(st.session_state.students)
            m1, m2, m3 = st.columns(3)
            with m1: st.markdown(f'<div class="dashboard-card" style="border-top-color:#10b981;"><h3>👥 תלמידים רשומים</h3><h2>{len(df_stud)}</h2></div>', unsafe_allow_html=True)
            with m2: st.markdown('<div class="dashboard-card" style="border-top-color:#f59e0b;"><h3>📋 מיפויים בביצוע</h3><h2>4 החודש</h2></div>', unsafe_allow_html=True)
            with m3: st.markdown('<div class="dashboard-card" style="border-top-color:#8b5cf6;"><h3>🔒 אבטחת ענן</h3><p style="color:#10b981; font-weight:bold;">מחובר לגוגל דרייב</p></div>', unsafe_allow_html=True)

            # הוספת תמונת הסבר וסימני הדרכה כפי שביקשת באפיון
            st.markdown("""
            <div style="background-color: #eff6ff; padding: 20px; border-radius: 15px; border-right: 6px solid #3b82f6; margin-bottom: 25px;">
                <h4>💡 הוראות שימוש מהירות לצוות:</h4>
                <ul>
                    <li><b>שלב א':</b> לחץ על לשונית <b>'📝 הזנת מיפוי'</b> למעלה.</li>
                    <li><b>שלב ב':</b> בחר את התלמיד הרצוי ולחץ על רמות המיומנות (ההיגדים מותאמים מגדרית אוטומטית).</li>
                    <li><b>שלב ג':</b> בתחתית העמוד, לחץ על כפתור הייצוא כדי להפיק דוח אקסל או טקסט מוכן למצגת.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<h3>📋 כרטיסי תלמידים פעילים</h3>', unsafe_allow_html=True)
            filtered_students = st.session_state.students if role != "מחנך" else [s for s in st.session_state.students if s["כיתה"] == st.session_state.user_class]
            
            for s in filtered_students:
                with st.container():
                    st.markdown(f"""
                    <div class="dashboard-card" style="border-top:none; border-right: 5px solid #64748b; padding: 15px; margin-bottom: 10px;">
                        <span style="font-size: 18px;">👤 <b>{s['שם פרטי']} {s['שם משפחה']}</b> — כיתה {s['כיתה']}</span> | 
                        <span style="color:#64748b; font-size:14px;">📅 עדכון אחרון: {s['תאריך עדכון']}</span>
                    </div>
                    """, unsafe_allow_html=True)

    # ------------------------------------------
    # לשונית 5: מסך הזנת מיפוי (חווית משתמש משופרת)
    # ------------------------------------------
    if "📝 הזנת מיפוי" in tabs_to_show:
        with active_tabs[tabs_to_show.index("📝 הזנת מיפוי")]:
            st.markdown('<h2>📝 טופס הערכת מיומנויות והזנת מיפוי</h2>', unsafe_allow_html=True)
            
            student_list = st.session_state.students if role != "מחנך" else [s for s in st.session_state.students if s["כיתה"] == st.session_state.user_class]
            student_names = [f"{s['שם פרטי']} {s['שם משפחה']}" for s in student_list]
            
            selected_student = st.selectbox("🎯 בחר תלמיד/ה להתחלת תהליך המיפוי:", student_names)
            curr_student = next(s for s in student_list if f"{s['שם פרטי']} {s['שם משפחה']}" == selected_student)
            gender_key = "זכר" if curr_student["מגдер"] == "זכר" else "נקבה"
            
            # הצגת מבנה המיומנויות בכרטיסיות פרימיום
            for cat, sub_cats in st.session_state.mapping_structure.items():
                for sub_cat, skills in sub_cats.items():
                    for skill_name, ratings in skills.items():
                        st.markdown('<div class="dashboard-card" style="border-top-color:#3b82f6;">', unsafe_allow_html=True)
                        st.markdown(f'<h3>📌 {cat} &gt; {sub_cat}</h3>', unsafe_allow_html=True)
                        
                        options = ratings[gender_key]
                        # כפתורי הרדיו יוצגו כעת כריבועים לחיצים ומעוצבים
                        selected_option = st.radio(f"נקבע עבור: {skill_name} (ניתן לסמן רק תא אחד)", options, key=f"map_{curr_student['id']}_{skill_name}")
                        st.session_state.current_selections[f"{cat} - {sub_cat} - {skill_name}"] = selected_option
                        st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<h3>📥 פאנל הפקת מסמכים ודוחות קליניים</h3>', unsafe_allow_html=True)
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                excel_data = generate_excel_report(st.session_state.current_selections, selected_student)
                st.download_button("📊 ייצא 'דוח מרוכז' לקובץ אקסל (RTL)", data=excel_data, file_name=f"דווח_מרוכז_{curr_student['שם פרטי']}.xlsx", use_container_width=True)
            with col_d2:
                if st.button("🤝 שכתב אוטומטית ל'דוח קהילה' (מצגות)", use_container_width=True):
                    text_report = generate_community_text(st.session_state.current_selections)
                    st.markdown(f'<div style="background-color:#ffffff; padding:25px; border-radius:16px; border-right:6px solid #10b981; box-shadow: 0 4px 15px rgba(0,0,0,0.02); margin-top:15px;"><b>✍️ הניסוח האקדמי המשוכתב עבור שקופית פאוור פוינט:</b><br><br>{text_report}</div>', unsafe_allow_html=True)
