# 🏢 AI Hub — מרכז הכלים הארגוני

פרויקט Streamlit מודולרי עבור מרכז כלים ארגוני בעברית, עם תמיכה ב-Google OAuth ועיצוב RTL.

---

## 🚀 הפעלה מהירה

```bash
cd Hub_Test
pip install -r requirements.txt
streamlit run main.py
```

**סיסמת ברירת מחדל:** `Hub2025!`  
(יש לשנות ב-`config.yaml` לפני פריסה)

---

## 📁 מבנה הפרויקט

```
Hub_Test/
│
├── main.py                  ← קובץ ראשי (הפעלה + ניווט + login)
├── config.yaml              ← קובץ הגדרות (סיסמאות, Google OAuth)
├── requirements.txt         ← ספריות Python נדרשות
├── README.md                ← קובץ זה
│
├── assets/                  ← תיקייה ללוגו החברה
│   └── logo.png            ← (אופציונלי) לוגו תמונה
│
└── tools/                   ← תיקיית הכלים (כל כלי = קובץ נפרד)
    ├── __init__.py
    ├── home.py              ← דף הבית עם כרטיסיות
    ├── plans_scanner.py     ← סורק תוכניות (דוגמה)
    ├── invoices.py          ← ניהול חשבוניות (דוגמה)
    └── dashboard.py         ← לוח בקרה (דוגמה)
```

---

## 🔐 הגדרת התחברות (Login)

### אפשרות 1: סיסמה בלבד (פשוט)
ערוך את `config.yaml` ושנה את הסיסמאות:

```yaml
credentials:
  usernames:
    admin:
      email: "admin@company.com"
      name: "מנהל מערכת"
      password: "$2b$12$..."  # סיסמה מקודדת
```

**ליצירת סיסמה מקודדת:**
```python
import bcrypt
hashed = bcrypt.hashpw("הסיסמה_שלך".encode(), bcrypt.gensalt())
print(hashed.decode())
```

### אפשרות 2: Google OAuth (מומלץ)

1. **צור פרויקט ב-Google Cloud Console:**
   - עבור אל https://console.cloud.google.com/
   - צור פרויקט חדש

2. **הפעל את ה-API:**
   - Google+ API או People API

3. **צור OAuth Credentials:**
   - Credentials → Create Credentials → OAuth client ID
   - Application type: Web application
   - **Authorized JavaScript origins:**
     - `http://localhost:8501` (פיתוח מקומי)
     - `https://your-app.replit.app` (פרודקשן)
   - **Authorized redirect URIs:**
     - `http://localhost:8501/`
     - `https://your-app.replit.app/`

4. **העתק ל-`config.yaml`:**
   ```yaml
   google:
     client_id: "YOUR_CLIENT_ID.apps.googleusercontent.com"
     client_secret: "YOUR_CLIENT_SECRET"
     redirect_uri: "http://localhost:8501/"
   ```

5. **בפריסה ל-Replit:** שנה את ה-redirect_uri לכתובת שלך

---

## 🖼️ הוספת לוגו החברה

1. שים קובץ לוגו ב-`assets/logo.png` (מומלץ 200x200px)
2. ערוך `config.yaml`:
   ```yaml
   app:
     use_image_logo: true
   ```

---

## ➕ איך מוסיפים כלי חדש?

**3 שלבים בלבד:**

### שלב 1 — צור קובץ Python חדש ב-`tools/`

```python
# tools/my_new_tool.py
"""
============================================================
 שם הכלי החדש
 tools/my_new_tool.py
============================================================

 הוראות לחבר הצוות:
 - ערוך את הפונקציה render() בקובץ זה
 - אל תשנה את שמה (render) כדי שהמערכת תטען אותה
 - ניתן להוסיף קבצי עזר נוספים ולייבא אותם כאן
============================================================
"""

import streamlit as st

def render():
    """פונקציה ראשית של הכלי"""
    
    st.markdown("""
    <div class="main-header">
        <h1>🎯 שם הכלי החדש</h1>
        <p>תיאור קצר של הכלי</p>
    </div>
    """, unsafe_allow_html=True)
    
    # כאן יבוא הקוד של הכלי...
    st.write("תוכן הכלי יופיע כאן...")
```

### שלב 2 — רשום את הכלי ב-`main.py`

מצא את `TOOLS_REGISTRY` (בערך שורה 280) והוסף:

```python
TOOLS_REGISTRY = [
    ("🏠 דף הבית",           "home"),
    ("🏗️ סורק תוכניות",     "plans_scanner"),
    ("📄 ניהול חשבוניות",    "invoices"),
    ("📊 לוח בקרה",          "dashboard"),
    # ➕ הוסף כאן את הכלי החדש שלך:
    ("🎯 שם הכלי שלי", "my_new_tool"),
]
```

### שלב 3 — הוסף כרטיסייה ב-`tools/home.py`

מצא את `TOOLS_CARDS` והוסף:

```python
TOOLS_CARDS = [
    # ... כרטיסיות קיימות ...
    
    # ➕ הוסף כאן כרטיסייה עבור הכלי החדש:
    {
        "icon": "🎯",
        "title": "שם הכלי החדש",
        "desc": "תיאור קצר של הכלי החדש.",
        "page": "🎯 שם הכלי שלי",
        "status": "פעיל",
        "status_class": "status-active",
    },
]
```

**זהו!** הכלי יופיע אוטומטית בתפריט ובדף הבית.

---

## 🛠️ עקרונות פיתוח לצוות

1. **עבודה במקביל:** כל חבר צוות עובד על קובץ נפרד ב-`tools/` — אין התנגשויות ב-Git
2. **מודולריות:** כל כלי = קובץ עצמאי עם פונקציית `render()`
3. **RTL:** תמיד השתמש ב-CSS הקיים או ב-`direction="rtl"` ב-markdown
4. **עברית:** כל הטקסט בממשק — כותרות, כפתורים, הודעות

---

## 🖥️ פריסה ב-Replit

1. צור Replit חדש מסוג Python
2. העלה את כל הקבצים (כולל `config.yaml`)
3. הגדר ב-`.replit`:
   ```
   run = "streamlit run main.py --server.port 8080"
   ```
4. התקן תלויות: `pip install -r requirements.txt`
5. **ל-Google OAuth:** עדכן את ה-redirect_uri ב-`config.yaml` לכתובת ה-Replit שלך

---

## 📝 הערות למפתחים

- `config.yaml` מכיל מידע רגיש — הוסף ל-`.gitignore` אם אתה משתף פרויקט ציבורי
- הסיסמאות מאוחסנות כ-hash עם bcrypt — לעולם אל תשמור סיסמאות טקסט
- הוסף הערות בעברית בכל קובץ כלי חדש לטובת חברי הצוות

---

**נהנו! 🎉**
