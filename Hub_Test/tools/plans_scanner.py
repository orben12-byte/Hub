"""
============================================================
 סורק תוכניות - Plans Scanner Tool
 tools/plans_scanner.py
============================================================
 כלי לסריקה וניתוח תוכניות בנייה / מפרטים.

 📌 הוראות לחבר הצוות שמפתח כלי זה:
    - ערוך את הפונקציה render() בקובץ זה
    - אל תשנה את שמה (render) כדי שהמערכת תטען אותה
    - ניתן להוסיף קבצי עזר נוספים ולייבא אותם כאן
============================================================
"""

import streamlit as st
import pandas as pd
import io


def render():
    """פונקציה ראשית של כלי סורק התוכניות"""

    # ---- כותרת ----
    st.markdown("""
    <div class="main-header">
        <h1>🏗️ סורק תוכניות</h1>
        <p>העלה תוכנית בנייה וקבל ניתוח מיידי של הנתונים המרכזיים</p>
    </div>
    """, unsafe_allow_html=True)

    # ---- העלאת קובץ ----
    st.markdown("""
    <div style="direction:rtl; color:rgba(255,255,255,0.7); font-size:15px; margin-bottom:12px;">
        📁 &nbsp;העלאת קובץ תוכנית
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "בחר קובץ לסריקה",
        type=["pdf", "xlsx", "csv", "dwg", "png", "jpg"],
        label_visibility="collapsed",
    )

    if uploaded is None:
        # הצג placeholder כשאין קובץ
        st.markdown("""
        <div style="
            border: 2px dashed rgba(99,102,241,0.35);
            border-radius: 16px;
            padding: 60px 40px;
            text-align: center;
            direction: rtl;
            margin-top: 12px;
        ">
            <div style="font-size:48px; margin-bottom:16px;">📋</div>
            <div style="color:rgba(255,255,255,0.5); font-size:15px;">
                טרם הועלה קובץ לסריקה
            </div>
            <div style="color:rgba(255,255,255,0.3); font-size:12px; margin-top:8px;">
                פורמטים נתמכים: PDF, Excel, CSV, DWG, תמונות
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # ---- עיבוד הקובץ ----
    st.success(f"✅ הקובץ '{uploaded.name}' הועלה בהצלחה")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stats-card" style="text-align:right;">
            <div style="color:rgba(255,255,255,0.5); font-size:12px;">שם קובץ</div>
            <div style="color:white; font-weight:600; margin-top:4px;">{uploaded.name}</div>
            <div style="color:rgba(255,255,255,0.5); font-size:12px; margin-top:10px;">גודל</div>
            <div style="color:white; font-weight:600; margin-top:4px;">{uploaded.size / 1024:.1f} KB</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stats-card" style="text-align:right;">
            <div style="color:rgba(255,255,255,0.5); font-size:12px;">סוג קובץ</div>
            <div style="color:white; font-weight:600; margin-top:4px;">{uploaded.type}</div>
            <div style="color:rgba(255,255,255,0.5); font-size:12px; margin-top:10px;">סטטוס</div>
            <div style="color:#4ade80; font-weight:600; margin-top:4px;">✅ ממתין לעיבוד</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- CSV / Excel ----
    if uploaded.name.endswith(".csv"):
        df = pd.read_csv(uploaded)
        st.markdown("**📊 תצוגת נתונים:**")
        st.dataframe(df, use_container_width=True)

    elif uploaded.name.endswith((".xlsx", ".xls")):
        df = pd.read_excel(uploaded)
        st.markdown("**📊 תצוגת נתונים:**")
        st.dataframe(df, use_container_width=True)

    elif uploaded.name.endswith((".png", ".jpg", ".jpeg")):
        st.markdown("**🖼️ תצוגה מקדימה:**")
        st.image(uploaded, use_column_width=True)

    else:
        st.info("📌 ניתוח קבצי PDF ו-DWG ייתמך בגרסה הבאה.")

    # ---- כפתור ניתוח ----
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔍 נתח קובץ"):
        with st.spinner("מנתח..."):
            import time; time.sleep(1.5)
        st.success("✅ הניתוח הושלם! (פיצ'ר זה בפיתוח — כאן יופיעו תוצאות הניתוח)")
