"""
============================================================
 AI Hub - מרכז הכלים הארגוני
 קובץ ראשי (main.py)
============================================================
 הפעלה: streamlit run main.py

 הוראות להגדרת Google OAuth:
 1. צור פרויקט ב-Google Cloud Console
 2. הפעל את Google+ API
 3. צור OAuth 2.0 Credentials
 4. העתק Client ID ו-Client Secret ל-config.yaml
============================================================
"""

import streamlit as st
import importlib
import os
import yaml
from pathlib import Path

# ============================================================
# טעינת הגדרות מ-config.yaml
# ============================================================

CONFIG_FILE = "config.yaml"

def load_config():
    """טוען את ההגדרות מקובץ config.yaml"""
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        st.error(f"⚠️ קובץ ההגדרות {CONFIG_FILE} לא נמצא!")
        return None
    except Exception as e:
        st.error(f"❌ שגיאה בטעינת ההגדרות: {e}")
        return None

config = load_config()

# ============================================================
# הגדרות עיצוב ו-CSS �גלובלי (RTL + עיצוב בסגנון Etsy עם סגול)
# ============================================================

def inject_css():
    """מחדיר CSS מותאם אישית - עיצוב בסגנון Etsy עם סגול"""
    st.markdown("""
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;600;700;800&family=Assistant:wght@400;500;600;700&display=swap');

        /* איקונים */
        .material-icons {
            font-family: 'Material Icons';
            font-size: 24px;
            vertical-align: middle;
        }
        
        .material-icons.large {
            font-size: 48px;
        }
        
        .material-icons.small {
            font-size: 18px;
        }

        html, body, [class*="css"] {
            font-family: 'Heebo', 'Assistant', sans-serif !important;
            direction: rtl;
        }

        /* רקע כללי - בהיר כמו Etsy */
        .stApp {
            background: #f5f5f3;
        }

        /* סיידבר - רקע לבן */
        [data-testid="stSidebar"] {
            background: #ffffff;
            border-left: 1px solid #e8e8e8;
            box-shadow: 2px 0 8px rgba(0,0,0,0.05);
        }

        [data-testid="stSidebar"] > div:first-child {
            padding-top: 0 !important;
        }

        /* קונטיינר לוגו */
        .logo-container {
            background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%);
            padding: 24px 20px 20px 20px;
            text-align: center;
            margin-bottom: 16px;
            border-radius: 0 0 16px 16px;
        }

        .logo-title {
            color: white;
            font-size: 24px;
            font-weight: 800;
            letter-spacing: 0.5px;
            margin: 0;
        }

        .logo-subtitle {
            color: rgba(255,255,255,0.85);
            font-size: 13px;
            font-weight: 500;
            margin-top: 4px;
        }

        /* כפתורי ניווט בסיידבר */
        [data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label {
            display: flex !important;
            background: transparent;
            border: none;
            border-radius: 12px;
            padding: 14px 18px;
            cursor: pointer;
            color: #000000;
            font-size: 15px;
            font-weight: 500;
            width: 100%;
            transition: all 0.2s ease;
            flex-direction: row-reverse;
            justify-content: flex-start;
            gap: 12px;
            margin: 4px 8px;
        }

        [data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label:hover {
            background: #f8eef8;
            color: #9b59b6;
        }

        [data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label[data-checked="true"],
        [data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label[aria-checked="true"] {
            background: #9b59b6;
            color: white;
            box-shadow: 0 2px 8px rgba(155, 89, 182, 0.3);
        }

        /* כותרת ראשית - בסגנון Etsy */
        .main-header {
            background: white;
            border-radius: 16px;
            padding: 32px 36px;
            margin-bottom: 28px;
            direction: rtl;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
            border: 1px solid #e8e8e8;
        }

        .main-header h1 {
            color: #2d2d2d;
            font-size: 34px;
            font-weight: 700;
            margin: 0;
        }

        .main-header p {
            color: #777777;
            font-size: 16px;
            margin: 10px 0 0 0;
        }

        /* כרטיסיות כלים - בסגנון Etsy */
        .tool-card {
            background: white;
            border-radius: 16px;
            padding: 24px 22px;
            text-align: right;
            direction: rtl;
            transition: all 0.25s ease;
            height: 100%;
            position: relative;
            border: 1px solid #e8e8e8;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }

        .tool-card:hover {
            border-color: #d4a5d9;
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(155, 89, 182, 0.15);
        }

        .tool-card-icon {
            font-size: 48px;
            margin-bottom: 16px;
            display: block;
        }

        .tool-card-title {
            color: #2d2d2d;
            font-size: 20px;
            font-weight: 700;
            margin-bottom: 10px;
        }

        .tool-card-desc {
            color: #666666;
            font-size: 14px;
            line-height: 1.6;
            margin-bottom: 20px;
        }

        /* סטטוס כרטיס */
        .tool-card-status {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            margin-bottom: 16px;
        }

        .status-active {
            background: #e8f8e8;
            color: #27ae60;
        }

        .status-dev {
            background: #fef3e2;
            color: #d68910;
        }

        /* כפתור הפעלה - סגול כמו Etsy */
        .launch-btn {
            background: #9b59b6 !important;
            color: white !important;
            border: none !important;
            border-radius: 24px !important;
            font-family: 'Heebo', sans-serif !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            padding: 10px 24px !important;
            width: 100% !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 2px 6px rgba(155, 89, 182, 0.3) !important;
        }

        .launch-btn:hover {
            background: #8e44ad !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(155, 89, 182, 0.4) !important;
        }

        /* כפתורי Streamlit */
        .stButton > button {
            background: #9b59b6 !important;
            color: white !important;
            border: none !important;
            border-radius: 24px !important;
            font-family: 'Heebo', sans-serif !important;
            font-weight: 600 !important;
            font-size: 15px !important;
            padding: 12px 28px !important;
            width: 100% !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 2px 8px rgba(155, 89, 182, 0.3) !important;
        }

        .stButton > button:hover {
            background: #8e44ad !important;
            box-shadow: 0 4px 12px rgba(155, 89, 182, 0.4) !important;
        }

        /* שדות קלט */
        .stTextInput > div > div > input {
            background: white !important;
            border: 1px solid #e0e0e0 !important;
            border-radius: 12px !important;
            color: #333333 !important;
            font-family: 'Heebo', sans-serif !important;
            direction: rtl !important;
            text-align: right !important;
            padding: 14px 18px !important;
            font-size: 15px !important;
        }

        .stTextInput > div > div > input:focus {
            border-color: #9b59b6 !important;
            box-shadow: 0 0 0 3px rgba(155, 89, 182, 0.15) !important;
        }

        .stTextInput > div > div > input::placeholder {
            color: #999999 !important;
        }

        /* מסך כניסה */
        .login-container {
            max-width: 400px;
            margin: 100px auto;
            background: white;
            border-radius: 20px;
            padding: 48px 40px;
            text-align: center;
            direction: rtl;
            box-shadow: 0 4px 24px rgba(0,0,0,0.08);
            border: 1px solid #e8e8e8;
        }

        .login-logo {
            font-size: 64px;
            margin-bottom: 8px;
        }

        .login-title {
            color: #2d2d2d;
            font-size: 28px;
            font-weight: 800;
            margin-bottom: 8px;
        }

        .login-subtitle {
            color: #777777;
            font-size: 14px;
            margin-bottom: 32px;
        }

        /* הודעות שגיאה */
        .stError {
            background: #fdeaea;
            color: #c0392b;
            border-radius: 12px;
            padding: 12px 16px;
        }

        /* כותרות */
        h1, h2, h3, h4 {
            font-family: 'Heebo', sans-serif !important;
            color: #2d2d2d !important;
        }

        /* הסתרת סרגל עליון */
        #MainMenu, footer, header {
            visibility: hidden;
        }

        /* קו מפריד */
        hr {
            border-color: #eeeeee;
        }

        /* פרטי משתמש בסיידבר */
        .user-info {
            background: #f8eef8;
            border-radius: 12px;
            padding: 14px 18px;
            margin: 0 8px 16px 8px;
        }

        .user-name {
            color: #2d2d2d;
            font-size: 14px;
            font-weight: 600;
        }

        .user-method {
            color: #9b59b6;
            font-size: 12px;
            margin-top: 2px;
        }

        /* כפתור התנתק */
        .logout-btn {
            background: #f5f5f5 !important;
            color: #666666 !important;
            border: 1px solid #e0e0e0 !important;
            border-radius: 12px !important;
            font-size: 14px !important;
            padding: 10px 20px !important;
            box-shadow: none !important;
        }

        .logout-btn:hover {
            background: #eeeeee !important;
            color: #333333 !important;
        }

        /* מספרים בסטטיסטיקות */
        .stats-card {
            background: white;
            border: 1px solid #e8e8e8;
            border-radius: 16px;
            padding: 24px 28px;
            text-align: center;
            direction: rtl;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }

        .stats-number {
            font-size: 40px;
            font-weight: 800;
            color: #9b59b6;
        }

        .stats-label {
            color: #777777;
            font-size: 14px;
            margin-top: 6px;
        }

        /* כפתור תפריט צד */
        .sidebar-toggle {
            position: fixed;
            top: 14px;
            right: 14px;
            z-index: 9999;
            background: #9b59b6;
            color: white;
            border: none;
            border-radius: 12px;
            padding: 10px 18px;
            cursor: pointer;
            font-family: 'Heebo', sans-serif;
            font-size: 14px;
            font-weight: 600;
            box-shadow: 0 2px 8px rgba(155, 89, 182, 0.3);
        }
        .sidebar-toggle:hover {
            background: #8e44ad;
            box-shadow: 0 4px 12px rgba(155, 89, 182, 0.4);
        }

    </style>
    """, unsafe_allow_html=True)


# ============================================================
# מסך כניסה עם סיסמה + Google OAuth
# ============================================================

def show_login():
    """מציג את מסך הכניסה למערכת"""
    st.markdown("""
    <div class="login-container">
        <div class="login-logo">🏢</div>
        <div class="login-title">מרכז הכלים הארגוני</div>
        <div class="login-subtitle">AI Hub — גישה מורשית בלבד</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # בדיקה אם Google OAuth מוגדר
        google_configured = False
        if config and 'google' in config:
            client_id = config['google'].get('client_id', '')
            if client_id and 'YOUR_CLIENT_ID' not in client_id:
                google_configured = True

        # אפשרות 1: כניסה עם סיסמה
        password = st.text_input("🔑 סיסמה", type="password", placeholder="הזן סיסמה...")
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("כניסה למערכת ←"):
            if validate_password(password):
                st.session_state["authenticated"] = True
                st.session_state["user_name"] = "משתמש"
                st.session_state["login_method"] = "סיסמה"
                st.session_state["page"] = "🏠 דף הבית"
                st.rerun()
            else:
                st.error("❌ סיסמה שגויה. נסה שוב.")

        # אפשרות 2: כניסה עם Google (אם מוגדר)
        if google_configured:
            st.markdown('<div class="oauth-divider"><span>או</span></div>', unsafe_allow_html=True)
            
            if st.button("🔵 התחבר עם Google", key="google_login"):
                initiate_google_login()
        
        # הודעת עזרה
        st.markdown("""
        <div style="text-align:center; color:rgba(255,255,255,0.3); font-size:12px; margin-top:24px;">
            לשכחת הסיסמה? פנה למנהל המערכת
        </div>
        """, unsafe_allow_html=True)


def validate_password(password: str) -> bool:
    """מאמת סיסמה מול ההגדרות"""
    if not config or 'credentials' not in config:
        return password == "Hub2025!"  # סיסמה בטוחה
    
    import bcrypt
    usernames = config['credentials'].get('usernames', {})
    
    for username, user_data in usernames.items():
        stored_hash = user_data.get('password', '')
        if stored_hash and '$2b$' in stored_hash:
            try:
                if bcrypt.checkpw(password.encode(), stored_hash.encode()):
                    return True
            except Exception:
                pass
    
    return False


def initiate_google_login():
    """מתחיל תהליך כניסה דרך Google"""
    if not config or 'google' not in config:
        st.error("⚠️ Google OAuth לא מוגדר")
        return
    
    google_config = config['google']
    client_id = google_config.get('client_id', '')
    redirect_uri = google_config.get('redirect_uri', '')
    
    if 'YOUR_CLIENT_ID' in client_id:
        st.error("⚠️ יש להגדיר Client ID של Google בקובץ config.yaml")
        return

    # בניית URL לכניסת Google
    import urllib.parse
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': 'openid email profile',
        'access_type': 'offline',
        'prompt': 'consent'
    }
    auth_url = 'https://accounts.google.com/o/oauth2/v2/auth?' + urllib.parse.urlencode(params)
    
    # שמירת ה-state לשימוש אחרי החזרה
    st.session_state['oauth_state'] = 'initiated'
    st.session_state['oauth_redirect'] = redirect_uri
    
    # הצגת לינק לכניסת Google
    st.markdown(f"""
    <div style="text-align:center; margin:20px 0; padding:20px; background:rgba(255,255,255,0.05); border-radius:12px;">
        <p style="color:rgba(255,255,255,0.7); margin-bottom:15px;">לחץ על הקישור למטה לכניסה דרך Google:</p>
        <a href="{auth_url}" target="_self" style="
            display:inline-block;
            padding:12px 24px;
            background:#4285f4;
            color:white;
            text-decoration:none;
            border-radius:8px;
            font-weight:600;
        ">🔵 התחבר עם Google</a>
        <p style="color:rgba(255,255,255,0.4); font-size:11px; margin-top:15px;">
            לאחר הכניסה, תועבר אוטומטית בחזרה לאפליקציה
        </p>
    </div>
    """, unsafe_allow_html=True)


def handle_google_callback():
    """מטפל בחזרה מ-Google לאחר כניסה"""
    # בדיקת פרמטרים ב-URL
    query_params = st.query_params
    
    if 'code' in query_params and 'state' in query_params:
        code = query_params['code']
        
        try:
            import requests
            from google.oauth2 import credentials
            from google_auth_oauthlib.flow import Flow
            
            google_config = config['google']
            client_config = {
                'web': {
                    'client_id': google_config['client_id'],
                    'client_secret': google_config['client_secret'],
                    'redirect_uri': google_config['redirect_uri']
                }
            }
            
            flow = Flow.from_client_config(
                client_config,
                scopes=['openid', 'email', 'profile']
            )
            
            flow.fetch_token(code=code)
            credentials_obj = flow.credentials
            
            # קבלת מידע על המשתמש
            import requests
            userinfo_response = requests.get(
                'https://www.googleapis.com/oauth2/v3/userinfo',
                headers={'Authorization': f'Bearer {credentials_obj.token}'}
            )
            
            if userinfo_response.status_code == 200:
                userinfo = userinfo_response.json()
                
                # רישום משתמש
                st.session_state["authenticated"] = True
                st.session_state["user_name"] = userinfo.get('name', 'משתמש Google')
                st.session_state["user_email"] = userinfo.get('email', '')
                st.session_state["login_method"] = "Google"
                st.session_state["page"] = "🏠 דף הבית"
                
                # ניקוי הפרמטרים מה-URL
                st.query_params.clear()
                st.rerun()
                
        except Exception as e:
            st.error(f"❌ שגיאה באימות Google: {e}")
            st.query_params.clear()


# ============================================================
# תפריט צד (Sidebar Navigation)
# ============================================================

# ➕ להוסיף כלי חדש? הוסף אותו לרשימה הזו!
# פורמט: ("<span class='material-icons'>icon</span> שם הכלי", "tool_filename")
TOOLS_REGISTRY = [
    ("<span class='material-icons'>home</span> דף הבית",           "home"),
    ("<span class='material-icons'>architecture</span> סורק תוכניות",     "plans_scanner"),
    ("<span class='material-icons'>description</span> ניהול חשבוניות",    "invoices"),
    ("<span class='material-icons'>dashboard</span> לוח בקרה",          "dashboard"),
    # ➕ הוסף כאן את הכלי החדש שלך:
    # ("<span class='material-icons'>icon</span> שם הכלי", "my_tool_file"),
]


def show_sidebar():
    """מציג את תפריט הניווט בצד"""
    with st.sidebar:
        # ---- לוגו ושם החברה ----
        use_image = config.get('app', {}).get('use_image_logo', False) if config else False
        logo_icon = config.get('app', {}).get('logo_icon', 'business') if config else 'business'
        
        if use_image and os.path.exists('assets/logo.png'):
            from PIL import Image
            logo = Image.open('assets/logo.png')
            st.image(logo, use_column_width=True)
        else:
            st.markdown(f"""
            <div class="logo-container">
                <span class="material-icons" style="font-size:42px; margin-bottom:4px; color:white;">{logo_icon}</span>
                <div class="logo-title">AI Hub</div>
                <div class="logo-subtitle">מרכז הכלים הארגוני</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # ---- פרטי משתמש מחובר ----
        if st.session_state.get('authenticated'):
            user_name = st.session_state.get('user_name', 'משתמש')
            login_method = st.session_state.get('login_method', '')
            
            st.markdown(f"""
            <div class="user-info">
                <div class="user-name"><span class="material-icons small">person</span> {user_name}</div>
                <div class="user-method"><span class="material-icons small">link</span> {login_method}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(
            "<div style='color:#000000; font-size:11px; text-align:right; padding:0 16px; margin-bottom:6px;'>ניווט</div>",
            unsafe_allow_html=True
        )

        # ---- כפתורי ניווט ----
        tool_names = [t[0] for t in TOOLS_REGISTRY]
        
        # מיפוי משמות תצוגה לשמות פנימיים (ללא האייקון)
        name_to_key = {t[0]: t[1] for t in TOOLS_REGISTRY}
        
        # נרמול שם הדף הנוכחי (בלי אייקון)
        current = st.session_state.get("page", "דף הבית")
        # נסה להתאים גם עם אייקון
        if "דף הבית" in current:
            current = "דף הבית"

        # מצא את האינדקס הנכון
        display_names = ["<span class='material-icons'>home</span> דף הבית", 
                        "<span class='material-icons'>architecture</span> סורק תוכניות",
                        "<span class='material-icons'>description</span> ניהול חשבוניות",
                        "<span class='material-icons'>dashboard</span> לוח בקרה"]
        
        selected = st.radio(
            "ניווט",
            options=display_names,
            index=0,
            key="nav_radio",
            label_visibility="collapsed",
        )

        if selected != st.session_state.get("nav_selected"):
            # שמור את הבחירה החדשה
            st.session_state["nav_selected"] = selected
            # מפה בחזרה לשם הפנימי
            for name, key in TOOLS_REGISTRY:
                if name == selected:
                    st.session_state["page"] = name
                    break
            st.rerun()

        # ---- כפתור יציאה ----
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<hr style='border-color:#eeeeee;'>", unsafe_allow_html=True)
        col_a, col_b = st.columns([1, 2])
        with col_b:
            if st.button("התנתק", key="logout_btn"):
                st.session_state.clear()
                st.rerun()

        st.markdown("""
        <div style="text-align:center; color:rgba(255,255,255,0.2); font-size:10px; padding: 16px 0 8px 0;">
            v1.1 · AI Hub
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# טעינה דינמית של כלים (Dynamic Tool Loading)
# ============================================================

def load_tool(tool_key: str):
    """
    טוענת את הכלי המתאים מתיקיית tools/ לפי שם הקובץ.

    ➕ כדי להוסיף כלי חדש:
       1. צור קובץ Python חדש בתיקיית tools/ (למשל: my_tool.py)
       2. הוסף פונקציה בשם render() בתוך הקובץ
       3. הוסף רשומה ל-TOOLS_REGISTRY למעלה
       זהו! האפליקציה תטען אותו אוטומטית.
    """
    try:
        module = importlib.import_module(f"tools.{tool_key}")
        if hasattr(module, "render"):
            module.render()
        else:
            st.warning(f"⚠️ הכלי '{tool_key}' אינו מכיל פונקציית render()")
    except ModuleNotFoundError:
        st.error(f"❌ הקובץ tools/{tool_key}.py לא נמצא.")
    except Exception as e:
        st.error(f"❌ שגיאה בטעינת הכלי: {e}")


# ============================================================
# ריצה ראשית (Main Entry Point)
# ============================================================

def main():
    st.set_page_config(
        page_title="AI Hub | מרכז הכלים הארגוני",
        page_icon="🏢",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    inject_css()

    # אתחול session state
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "page" not in st.session_state:
        st.session_state["page"] = "🏠 דף הבית"
    if "sidebar_collapsed" not in st.session_state:
        st.session_state["sidebar_collapsed"] = False

    # בדיקת callback מ-Google
    if st.query_params.get('code'):
        handle_google_callback()
        return

    # בדיקת פרמטר דף מה-URL (מכרטיסיות) - לפני הכל
    if st.query_params.get('page'):
        selected_page = st.query_params.get('page')
        for name, _ in TOOLS_REGISTRY:
            if name == selected_page:
                st.session_state["page"] = selected_page
                break
        st.query_params.clear()

    # הצג מסך כניסה אם לא מחובר
    if not st.session_state["authenticated"]:
        show_login()
        return

    # כפתור קבוע לפתיחת הסיידבר - משתמש בקישור JavaScript
    st.markdown("""
    <button class="sidebar-toggle" onclick="document.querySelector('[data-testid=\\'stSidebar\\']').style.display='block'; document.querySelector('[data-testid=\\'stSidebar\\']').style.width='300px';">
        ☰ תפריט
    </button>
    """, unsafe_allow_html=True)

    # הצג תפריט צד
    show_sidebar()

    # הצג את הכלי הנבחר
    current_page = st.session_state.get("page", "🏠 דף הבית")

    # מצא את מפתח הקובץ לפי שם הכרטיסייה
    tool_key = None
    for name, key in TOOLS_REGISTRY:
        if name == current_page:
            tool_key = key
            break

    if tool_key:
        load_tool(tool_key)
    else:
        st.error("❌ עמוד לא נמצא")


if __name__ == "__main__":
    main()
