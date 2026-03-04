"""
============================================================
 ניהול חשבוניות - Invoices Management Tool
 tools/invoices.py
============================================================
 כלי לניהול חשבוניות נכנסות ויוצאות.

 📌 הוראות לחבר הצוות שמפתח כלי זה:
    - ערוך את הפונקציה render() בקובץ זה
    - שמור נתונים ב-session_state או בקובץ CSV חיצוני
    - ניתן לחבר בסיס נתונים (Supabase / Firebase) לפי הצורך
============================================================
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date


# ============================================================
# אתחול נתוני חשבוניות לדוגמה
# ============================================================
def _init_data():
    """מאתחל נתוני דוגמה אם אין עדיין נתונים ב-session"""
    if "invoices_df" not in st.session_state:
        st.session_state["invoices_df"] = pd.DataFrame([
            {"מספר":  "INV-001", "לקוח": "חברה א׳",   "סכום": 12500, "תאריך": "2025-01-15", "סטטוס": "שולם"},
            {"מספר":  "INV-002", "לקוח": "חברה ב׳",   "סכום":  8300, "תאריך": "2025-02-03", "סטטוס": "ממתין"},
            {"מספר":  "INV-003", "לקוח": "חברה ג׳",   "סכום": 21000, "תאריך": "2025-02-20", "סטטוס": "שולם"},
            {"מספר":  "INV-004", "לקוח": "חברה ד׳",   "סכום":  4750, "תאריך": "2025-03-01", "סטטוס": "באיחור"},
        ])


def render():
    """פונקציה ראשית של כלי ניהול החשבוניות"""
    _init_data()
    df: pd.DataFrame = st.session_state["invoices_df"]

    # ---- כותרת ----
    st.markdown("""
    <div class="main-header">
        <h1>📄 ניהול חשבוניות</h1>
        <p>עקוב אחר חשבוניות נכנסות ויוצאות, מצב תשלומים ויצוא נתונים</p>
    </div>
    """, unsafe_allow_html=True)

    # ---- סטטיסטיקות ----
    total_sum  = df["סכום"].sum()
    paid       = df[df["סטטוס"] == "שולם"]["סכום"].sum()
    pending    = df[df["סטטוס"] == "ממתין"]["סכום"].sum()
    overdue    = df[df["סטטוס"] == "באיחור"]["סכום"].sum()

    c1, c2, c3, c4 = st.columns(4)
    for col, label, value, color in [
        (c1, "סה\"כ חשבוניות",  f"₪{total_sum:,.0f}", "#6366f1"),
        (c2, "שולם",            f"₪{paid:,.0f}",       "#4ade80"),
        (c3, "ממתין לתשלום",    f"₪{pending:,.0f}",    "#fbbf24"),
        (c4, "באיחור",          f"₪{overdue:,.0f}",    "#f87171"),
    ]:
        with col:
            st.markdown(f"""
            <div class="stats-card">
                <div class="stats-number" style="color:{color}; font-size:24px;">{value}</div>
                <div class="stats-label">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- טאבים ----
    tab1, tab2 = st.tabs(["📋 רשימת חשבוניות", "➕ הוסף חשבונית"])

    with tab1:
        # צבע שורות לפי סטטוס
        def color_status(val):
            colors = {"שולם": "color: #4ade80", "ממתין": "color: #fbbf24", "באיחור": "color: #f87171"}
            return colors.get(val, "")

        styled = df.style.applymap(color_status, subset=["סטטוס"])
        st.dataframe(styled, use_container_width=True, hide_index=True)

        # כפתור יצוא CSV
        csv = df.to_csv(index=False, encoding="utf-8-sig")
        st.download_button(
            label="📥 ייצוא ל-CSV",
            data=csv,
            file_name=f"חשבוניות_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )

    with tab2:
        with st.form("add_invoice_form", clear_on_submit=True):
            st.markdown("<div style='direction:rtl'>", unsafe_allow_html=True)
            col_a, col_b = st.columns(2)
            with col_a:
                inv_num    = st.text_input("מספר חשבונית", placeholder="INV-005")
                inv_client = st.text_input("לקוח", placeholder="שם הלקוח")
            with col_b:
                inv_amount = st.number_input("סכום (₪)", min_value=0, step=100)
                inv_status = st.selectbox("סטטוס", ["ממתין", "שולם", "באיחור"])

            inv_date = st.date_input("תאריך", value=date.today())
            submitted = st.form_submit_button("➕ הוסף חשבונית")
            st.markdown("</div>", unsafe_allow_html=True)

            if submitted:
                if not inv_num or not inv_client:
                    st.error("❌ יש למלא מספר חשבונית ושם לקוח")
                else:
                    new_row = pd.DataFrame([{
                        "מספר": inv_num,
                        "לקוח": inv_client,
                        "סכום": inv_amount,
                        "תאריך": str(inv_date),
                        "סטטוס": inv_status,
                    }])
                    st.session_state["invoices_df"] = pd.concat(
                        [df, new_row], ignore_index=True
                    )
                    st.success(f"✅ חשבונית {inv_num} נוספה בהצלחה!")
                    st.rerun()
