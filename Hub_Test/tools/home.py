"""
============================================================
 דף הבית - Home Page
 tools/home.py
============================================================
 מציג את כרטיסיות הכלים הזמינים במרכז הכלים הארגוני.

 ➕ להוסיף כרטיסייה חדשה:
    1. הוסף רשומה ל-TOOLS_CARDS למטה
    2. ודא שקיים קובץ מתאים ב-tools/
    3. הוסף אותו ל-TOOLS_REGISTRY ב-main.py
============================================================
"""

import streamlit as st


# ============================================================
# רישום כל הכרטיסיות של הכלים
# ➕ הוסף כאן כרטיסייה עבור כל כלי חדש שאתה מוסיף
# ============================================================
TOOLS_CARDS = [
    {
        "icon": "🏗️",
        "title": "סורק תוכניות",
        "desc": "סרוק ונתח תוכניות בנייה, חלץ מידע מרכזי ויצר דוחות מפורטים בלחיצת כפתור.",
        "page": "🏗️ סורק תוכניות",
        "status": "פעיל",
        "status_class": "status-active",
    },
    {
        "icon": "📄",
        "title": "ניהול חשבוניות",
        "desc": "טיפול בחשבוניות נכנסות ויוצאות, מעקב תשלומים ויצוא לאקסל בקלות.",
        "page": "📄 ניהול חשבוניות",
        "status": "פעיל",
        "status_class": "status-active",
    },
    {
        "icon": "📊",
        "title": "לוח בקרה",
        "desc": "תמונת מצב כוללת של המשרד — נתוני פרויקטים, כספים וביצועים בזמן אמת.",
        "page": "📊 לוח בקרה",
        "status": "בפיתוח",
        "status_class": "status-dev",
    },
    # ➕ הוסף כאן עוד כרטיסיות:
    # {
    #     "icon": "🎯",
    #     "title": "שם הכלי",
    #     "desc": "תיאור קצר של הכלי.",
    #     "page": "🎯 שם הכלי",
    #     "status": "פעיל",
    #     "status_class": "status-active",
    # },
]


def render():
    """פונקציה ראשית של דף הבית"""

    # ---- כותרת עליונה ----
    st.markdown("""
    <div class="main-header">
        <h1>👋 ברוכים הבאים ל-AI Hub</h1>
        <p>מרכז הכלים הארגוני — כל הכלים שאתם צריכים, במקום אחד</p>
    </div>
    """, unsafe_allow_html=True)

    # ---- שורת סטטיסטיקות ----
    total  = len(TOOLS_CARDS)
    active = sum(1 for t in TOOLS_CARDS if t["status"] == "פעיל")
    dev    = total - active

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">{total}</div>
            <div class="stats-label">סה"כ כלים</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number" style="color:#4ade80;">{active}</div>
            <div class="stats-label">כלים פעילים</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number" style="color:#fbbf24;">{dev}</div>
            <div class="stats-label">בפיתוח</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="direction:rtl; color:rgba(255,255,255,0.5); font-size:14px; margin-bottom:16px;">
        🛠️ &nbsp;הכלים הזמינים
    </div>
    """, unsafe_allow_html=True)

    # ---- כרטיסיות הכלים ----
    cols = st.columns(3)

    for idx, tool in enumerate(TOOLS_CARDS):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="tool-card">
                <span class="tool-card-icon">{tool['icon']}</span>
                <div class="tool-card-title">{tool['title']}</div>
                <span class="tool-card-status {tool['status_class']}">{tool['status']}</span>
                <div class="tool-card-desc">{tool['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

            # כפתור הפעלה
            if st.button(f"הפעל ←  {tool['icon']}", key=f"launch_{idx}"):
                st.session_state["page"] = tool["page"]
                st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)
