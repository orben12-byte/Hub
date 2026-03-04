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
# הגדרות עיצוב ו-CSS גלובלי (RTL + עיצוב ארגוני)
# ============================================================

def inject_css():
    """מחדיר CSS מותאם אישית לעיצוב RTL וקורפורטיבי"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Heebo', sans-serif !important;
            direction: rtl;
        }

        .stApp {
            background: linear-gradient(135deg, #0f1117 0%, #1a1f2e 50%, #0f1117 100%);
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #161b2e 0%, #1e2540 100%);
            border-left: 1px solid rgba(99, 102, 241, 0.3);
            border-right: none;
        }

        [data-testid="stSidebar"] > div:first-child {
            padding-top: 0 !important;
        }

        .logo-container {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            padding: 28px 20px 22px 20px;
            text-align: center;
            margin-bottom: 10px;
            border-bottom: 1px solid rgba(99, 102, 241, 0.4);
        }

        .logo-title {
            color: white;
            font-size: 22px;
            font-weight: 800;
            letter-spacing: 0.5px;
            margin: 0;
            text-shadow: 0 2px 8px rgba(0,0,0,0.3);
        }

        .logo-subtitle {
            color: rgba(255,255,255,0.75);
            font-size: 12px;
            font-weight: 400;
            margin-top: 4px;
        }

        .nav-btn {
            width: 100%;
            padding: 12px 18px;
            margin: 3px 0;
            background: transparent;
            border: none;
            border-radius: 10px;
            color: rgba(255,255,255,0.7);
            font-family: 'Heebo', sans-serif;
            font-size: 15px;
            font-weight: 500;
            text-align: right;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .nav-btn:hover {
            background: rgba(99, 102, 241, 0.2);
            color: white;
        }

        .nav-btn.active {
            background: linear-gradient(135deg, rgba(99,102,241,0.3), rgba(139,92,246,0.3));
            color: white;
            border-right: 3px solid #6366f1;
        }

        .main-header {
            background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(139,92,246,0.1));
            border: 1px solid rgba(99,102,241,0.3);
            border-radius: 16px;
            padding: 32px 36px;
            margin-bottom: 32px;
            direction: rtl;
        }

        .main-header h1 {
            color: white;
            font-size: 32px;
            font-weight: 800;
            margin: 0;
        }

        .main-header p {
            color: rgba(255,255,255,0.6);
            font-size: 15px;
            margin: 8px 0 0 0;
        }

        .tool-card {
            background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 16px;
            padding: 28px 24px;
            text-align: right;
            direction: rtl;
            transition: all 0.3s ease;
            height: 100%;
            position: relative;
            overflow: hidden;
        }

        .tool-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, #6366f1, #8b5cf6);
            border-radius: 16px 16px 0 0;
        }

        .tool-card:hover {
            border-color: rgba(99,102,241,0.5);
            background: linear-gradient(135deg, rgba(99,102,241,0.1), rgba(139,92,246,0.05));
            transform: translateY(-2px);
            box-shadow: 0 12px 40px rgba(99,102,241,0.2);
        }

        .tool-card-icon {
            font-size: 42px;
            margin-bottom: 14px;
            display: block;
        }

        .tool-card-title {
            color: white;
            font-size: 19px;
            font-weight: 700;
            margin-bottom: 10px;
        }

        .tool-card-desc {
            color: rgba(255,255,255,0.55);
            font-size: 13.5px;
            line-height: 1.6;
            margin-bottom: 20px;
        }

        .tool-card-status {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 600;
            margin-bottom: 16px;
        }

        .status-active {
            background: rgba(34,197,94,0.2);
            color: #4ade80;
            border: 1px solid rgba(34,197,94,0.3);
        }

        .status-dev {
            background: rgba(234,179,8,0.2);
            color: #fbbf24;
            border: 1px solid rgba(234,179,8,0.3);
        }

        .stats-card {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 12px;
            padding: 20px 24px;
            text-align: center;
            direction: rtl;
        }

        .stats-number {
            font-size: 36px;
            font-weight: 800;
            color: #6366f1;
        }

        .stats-label {
            color: rgba(255,255,255,0.5);
            font-size: 13px;
            margin-top: 4px;
        }

        .login-container {
            max-width: 420px;
            margin: 80px auto;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(99,102,241,0.3);
            border-radius: 24px;
            padding: 50px 44px;
            text-align: center;
            direction: rtl;
        }

        .login-logo {
            font-size: 52px;
            margin-bottom: 10px;
        }

        .login-title {
            color: white;
            font-size: 26px;
            font-weight: 800;
            margin-bottom: 6px;
        }

        .login-subtitle {
            color: rgba(255,255,255,0.45);
            font-size: 14px;
            margin-bottom: 36px;
        }

        .stTextInput > div > div > input {
            background: rgba(255,255,255,0.06) !important;
            border: 1px solid rgba(99,102,241,0.3) !important;
            border-radius: 10px !important;
            color: white !important;
            font-family: 'Heebo', sans-serif !important;
            direction: rtl !important;
            text-align: right !important;
            padding: 12px 16px !important;
        }

        .stTextInput > div > div > input:focus {
            border-color: #6366f1 !important;
            box-shadow: 0 0 0 3px rgba(99,102,241,0.2) !important;
        }

        .stButton > button {
            background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            font-family: 'Heebo', sans-serif !important;
            font-weight: 600 !important;
            font-size: 15px !important;
            padding: 12px 28px !important;
            width: 100% !important;
            transition: all 0.2s ease !important;
        }

        .stButton > button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 8px 25px rgba(99,102,241,0.45) !important;
        }

        .google-btn {
            background: white !important;
            color: #333 !important;
            border: 1px solid #ddd !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 10px !important;
        }

        .google-btn:hover {
            background: #f5f5f5 !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
        }

        #MainMenu, footer, header {
            visibility: hidden;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            direction: rtl;
        }

        h1, h2, h3, h4 {
            font-family: 'Heebo', sans-serif !important;
            color: white !important;
        }

        .stSuccess, .stError, .stWarning, .stInfo {
            direction: rtl;
            text-align: right;
        }

        hr {
            border-color: rgba(255,255,255,0.08);
        }

        .stRadio > div {
            direction: rtl;
        }

        [data-testid="stSidebar"] .stRadio > label {
            display: none;
        }

        [data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label {
            display: flex !important;
            background: transparent;
            border: none;
            border-radius: 10px;
            padding: 11px 16px;
            cursor: pointer;
            color: rgba(255,255,255,0.65);
            font-size: 15px;
            font-weight: 500;
            width: 100%;
            transition: all 0.2s;
            flex-direction: row-reverse;
            justify-content: flex-end;
            gap: 10px;
            margin: 2px 0;
        }

        [data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label:hover {
            background: rgba(99,102,241,0.18);
            color: white;
        }

        [data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label[data-checked="true"],
        [data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label[aria-checked="true"] {
            background: rgba(99,102,241,0.25);
            color: white;
            border-right: 3px solid #6366f1;
        }

        .oauth-divider {
            display: flex;
            align-items: center;
            margin: 20px 0;
            color: rgba(255,255,255,0.3);
            font-size: 12px;
        }

        .oauth-divider::before,
        .oauth-divider::after {
            content: '';
            flex: 1;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }

        .oauth-divider span {
            padding: 0 10px;
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
# פורמט: ("🔥 שם הכלי", "tool_filename")
TOOLS_REGISTRY = [
    ("🏠 דף הבית",           "home"),
    ("🏗️ סורק תוכניות",     "plans_scanner"),
    ("📄 ניהול חשבוניות",    "invoices"),
    ("📊 לוח בקרה",          "dashboard"),
    # ➕ הוסף כאן את הכלי החדש שלך:
    # ("🎯 שם הכלי שלי", "my_tool_file"),
]


def show_sidebar():
    """מציג את תפריט הניווט בצד"""
    with st.sidebar:
        # ---- לוגו ושם החברה ----
        use_image = config.get('app', {}).get('use_image_logo', False) if config else False
        logo_emoji = config.get('app', {}).get('logo_emoji', '🏢') if config else '🏢'
        
        if use_image and os.path.exists('assets/logo.png'):
            from PIL import Image
            logo = Image.open('assets/logo.png')
            st.image(logo, use_column_width=True)
        else:
            st.markdown(f"""
            <div class="logo-container">
                <div style="font-size:38px; margin-bottom:8px;">{logo_emoji}</div>
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
            <div style="background:rgba(99,102,241,0.1); border-radius:10px; padding:12px 16px; margin-bottom:16px;">
                <div style="color:white; font-size:14px; font-weight:600;">👤 {user_name}</div>
                <div style="color:rgba(255,255,255,0.5); font-size:11px;">🔗 {login_method}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(
            "<div style='color:rgba(255,255,255,0.35); font-size:11px; text-align:right; padding:0 16px; margin-bottom:6px;'>ניווט</div>",
            unsafe_allow_html=True
        )

        # ---- כפתורי ניווט ----
        tool_names = [t[0] for t in TOOLS_REGISTRY]
        current = st.session_state.get("page", "🏠 דף הבית")

        selected = st.radio(
            "ניווט",
            options=tool_names,
            index=tool_names.index(current) if current in tool_names else 0,
            key="nav_radio",
            label_visibility="collapsed",
        )

        if selected != current:
            st.session_state["page"] = selected
            st.rerun()

        # ---- כפתור יציאה ----
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        col_a, col_b = st.columns([1, 2])
        with col_b:
            if st.button("🚪 התנתק"):
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

    # הצג מסך כניסה אם לא מחובר
    if not st.session_state["authenticated"]:
        show_login()
        return

    # כפתור קבוע לפתיחת הסיידבר - משתמש בקישור JavaScript
    st.markdown("""
    <style>
        .sidebar-toggle {
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 9999;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 16px;
            cursor: pointer;
            font-family: 'Heebo', sans-serif;
            font-size: 14px;
            font-weight: 600;
        }
        .sidebar-toggle:hover {
            box-shadow: 0 4px 15px rgba(99,102,241,0.4);
        }
    </style>
    <button class="sidebar-toggle" onclick="document.querySelector('[data-testid=\"stSidebar\"]').style.display='block'; document.querySelector('[data-testid=\"stSidebar\"]').style.width='300px';">
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
