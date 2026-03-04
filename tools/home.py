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
# שימוש ב-Material Icons: https://fonts.google.com/icons
# ============================================================
TOOLS_CARDS = [
    {
        "icon": "architecture",
        "title": "סורק תוכניות",
        "desc": "סרוק ונתח תוכניות בנייה, חלץ מידע מרכזי ויצר דוחות מפורטים בלחיצת כפתור.",
        "page": "<span class='material-icons'>architecture</span> סורק תוכניות",
        "status": "פעיל",
        "status_class": "status-active",
    },
    {
        "icon": "description",
        "title": "ניהול חשבוניות",
        "desc": "טיפול בחשבוניות נכנסות ויוצאות, מעקב תשלומים ויצוא לאקסל בקלות.",
        "page": "<span class='material-icons'>description</span> ניהול חשבוניות",
        "status": "פעיל",
        "status_class": "status-active",
    },
    {
        "icon": "dashboard",
        "title": "לוח בקרה",
        "desc": "תמונת מצב כוללת של המשרד — נתוני פרויקטים, כספים וביצועים בזמן אמת.",
        "page": "<span class='material-icons'>dashboard</span> לוח בקרה",
        "status": "בפיתוח",
        "status_class": "status-dev",
    },
    # ➕ הוסף כאן עוד כרטיסיות:
    # {
    #     "icon": "icon_name",
    #     "title": "שם הכלי",
    #     "desc": "תיאור קצר של הכלי.",
    #     "page": "<span class='material-icons'>icon_name</span> שם הכלי",
    #     "status": "פעיל",
    #     "status_class": "status-active",
    # },
]


def render():
    """פונקציה ראשית של דף הבית"""

    # ---- כותרת עליונה ----
    st.markdown("""
    <div class="main-header">
        <h1><span class="material-icons">waving_hand</span> ברוכים הבאים ל-AI Hub</h1>
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
            <div class="stats-number" style="color:#27ae60;">{active}</div>
            <div class="stats-label">כלים פעילים</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number" style="color:#d68910;">{dev}</div>
            <div class="stats-label">בפיתוח</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="direction:rtl; color:#666666; font-size:15px; margin-bottom:16px; font-weight:600;">
        <span class="material-icons">construction</span>&nbsp;הכלים הזמינים
    </div>
    """, unsafe_allow_html=True)

    # ---- כרטיסיות הכלים ----
    cols = st.columns(3)

    for idx, tool in enumerate(TOOLS_CARDS):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="tool-card" id="card_{idx}" style="cursor:pointer;">
                <span class="material-icons large">{tool['icon']}</span>
                <div class="tool-card-title">{tool['title']}</div>
                <span class="tool-card-status {tool['status_class']}">{tool['status']}</span>
                <div class="tool-card-desc">{tool['desc']}</div>
            </div>
            <script>
                document.getElementById('card_{idx}').addEventListener('click', function() {{
                    window.location.href = '?page=' + encodeURIComponent('{tool["page"]}');
                }});
            </script>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
