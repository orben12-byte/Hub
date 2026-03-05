"""
============================================================
 לוח בקרה - Dashboard
 tools/dashboard.py
============================================================
 לוח בקרה ארגוני עם גרפים וסטטיסטיקות כלליות.

 📌 הוראות לחבר הצוות שמפתח כלי זה:
    - ערוך את הפונקציה render() בקובץ זה
    - השתמש ב-Plotly לגרפים דינמיים
    - ניתן לחבר APIs חיצוניים לנתונים בזמן אמת
============================================================
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import random


# ---- נתוני דוגמה ----
def _sample_monthly_data():
    months = ["ינואר", "פברואר", "מרץ", "אפריל", "מאי", "יוני",
              "יולי", "אוגוסט", "ספטמבר", "אוקטובר", "נובמבר", "דצמבר"]
    income  = [42000, 55000, 48000, 62000, 71000, 58000,
                66000, 74000, 52000, 83000, 91000, 78000]
    expense = [28000, 31000, 35000, 40000, 38000, 42000,
                36000, 44000, 39000, 48000, 52000, 45000]
    return months, income, expense


def _sample_projects():
    return pd.DataFrame({
        "פרויקט":  ["בית מגורים - רמת גן", "משרדים - תל אביב", "מסחרי - חיפה", "מגורים - ירושלים"],
        "שלב":     ["תכנון", "ביצוע", "סיום", "ביצוע"],
        "התקדמות": [30, 65, 90, 45],
        "תקציב":   [850000, 2100000, 750000, 1350000],
    })


def render():
    """פונקציה ראשית של לוח הבקרה"""

    # ---- כותרת ----
    st.markdown("""
    <div class="main-header">
        <h1>📊 לוח בקרה</h1>
        <p>תמונת מצב כוללת של המשרד — פרויקטים, כספים וביצועים</p>
    </div>
    """, unsafe_allow_html=True)

    # ---- KPIs ----
    kpis = [
        ("🏗️", "פרויקטים פעילים", "12", "#6366f1"),
        ("💰", "הכנסות החודש",     "₪91,000", "#4ade80"),
        ("📋", "חשבוניות פתוחות", "7", "#fbbf24"),
        ("👥", "לקוחות פעילים",   "34", "#818cf8"),
    ]

    cols = st.columns(4)
    for col, (icon, label, value, color) in zip(cols, kpis):
        with col:
            st.markdown(f"""
            <div class="stats-card">
                <div style="font-size:28px; margin-bottom:6px;">{icon}</div>
                <div class="stats-number" style="color:{color}; font-size:26px;">{value}</div>
                <div class="stats-label">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- גרף הכנסות/הוצאות ----
    months, income, expense = _sample_monthly_data()

    fig_income = go.Figure()
    fig_income.add_trace(go.Scatter(
        x=months, y=income,
        mode="lines+markers",
        name="הכנסות",
        line=dict(color="#6366f1", width=3),
        fill="tozeroy",
        fillcolor="rgba(99,102,241,0.1)",
    ))
    fig_income.add_trace(go.Scatter(
        x=months, y=expense,
        mode="lines+markers",
        name="הוצאות",
        line=dict(color="#f87171", width=3),
        fill="tozeroy",
        fillcolor="rgba(248,113,113,0.1)",
    ))
    fig_income.update_layout(
        title="📈 הכנסות vs הוצאות — 2025",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Rubik, Arial", color="rgba(255,255,255,0.7)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickprefix="₪"),
        margin=dict(l=0, r=0, t=50, b=0),
    )
    st.plotly_chart(fig_income, use_container_width=True)

    # ---- פרויקטים ----
    col_left, col_right = st.columns([3, 2])

    with col_left:
        proj_df = _sample_projects()
        st.markdown("""
        <div style="color:rgba(255,255,255,0.6); font-size:14px; margin-bottom:10px;">
            🏗️ &nbsp;פרויקטים פעילים
        </div>
        """, unsafe_allow_html=True)

        for _, row in proj_df.iterrows():
            progress = row["התקדמות"]
            color = "#4ade80" if progress >= 80 else "#fbbf24" if progress >= 40 else "#f87171"
            st.markdown(f"""
            <div style="
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 12px;
                padding: 16px 20px;
                margin-bottom: 10px;
                direction: rtl;
            ">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div style="color:white; font-weight:600; font-size:14px;">{row['פרויקט']}</div>
                    <div style="color:{color}; font-size:13px;">{progress}%</div>
                </div>
                <div style="
                    background: rgba(255,255,255,0.08);
                    border-radius: 20px;
                    height: 6px;
                    margin-top: 10px;
                    overflow: hidden;
                ">
                    <div style="
                        width: {progress}%;
                        height: 100%;
                        background: linear-gradient(90deg, #6366f1, #8b5cf6);
                        border-radius: 20px;
                    "></div>
                </div>
                <div style="color:rgba(255,255,255,0.4); font-size:12px; margin-top:6px;">
                    {row['שלב']} · תקציב: ₪{row['תקציב']:,.0f}
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_right:
        st.markdown("""
        <div style="color:rgba(255,255,255,0.6); font-size:14px; margin-bottom:10px;">
            📊 &nbsp;התפלגות לפי שלב
        </div>
        """, unsafe_allow_html=True)

        proj_df = _sample_projects()
        stage_counts = proj_df["שלב"].value_counts()
        fig_pie = px.pie(
            values=stage_counts.values,
            names=stage_counts.index,
            color_discrete_sequence=["#6366f1", "#8b5cf6", "#4ade80", "#fbbf24"],
            hole=0.55,
        )
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Rubik, Arial", color="rgba(255,255,255,0.7)"),
            showlegend=True,
            legend=dict(orientation="v"),
            margin=dict(l=0, r=0, t=0, b=0),
        )
        st.plotly_chart(fig_pie, use_container_width=True)
