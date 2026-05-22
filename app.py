import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import base64
import os
from PIL import Image
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE CONFIG & FAVICON
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
favicon_path = os.path.join(os.path.dirname(__file__), "assets", "Isotipo Ricardo Palma.png")
favicon = "🏥"
if os.path.exists(favicon_path):
    try:
        favicon = Image.open(favicon_path)
    except Exception:
        pass

st.set_page_config(
    page_title="Dashboard CRP – Centro de Operaciones",
    page_icon=favicon,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# BRAND TOKENS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TEAL   = "#115264"
CYAN   = "#00b2a9"
GREEN  = "#10b981"
GOLD   = "#f59e0b"
RED    = "#ef4444"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# INLINE SVG ICONS  (24×24, stroke-based, no external deps)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def _svg(path_d, color, size=20):
    return (
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{size}' height='{size}' "
        f"viewBox='0 0 24 24' fill='none' stroke='{color}' stroke-width='2' "
        f"stroke-linecap='round' stroke-linejoin='round' "
        f"style='vertical-align:middle;flex-shrink:0;'>{path_d}</svg>"
    )

# Lucide-style paths
ICON = {
    "dollar":    lambda c: _svg("<line x1='12' y1='1' x2='12' y2='23'/><path d='M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6'/>", c),
    "trending":  lambda c: _svg("<polyline points='22 7 13.5 15.5 8.5 10.5 2 17'/><polyline points='16 7 22 7 22 13'/>", c),
    "clipboard": lambda c: _svg("<rect x='8' y='2' width='8' height='4' rx='1' ry='1'/><path d='M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2'/>", c),
    "tag":       lambda c: _svg("<path d='M12 2H2v10l9.29 9.29a1 1 0 0 0 1.42 0l6.58-6.58a1 1 0 0 0 0-1.42L12 2Z'/><circle cx='7.5' cy='7.5' r='.5' fill='{c}'/>".replace("{c}", c), c),
    "bar_chart": lambda c: _svg("<line x1='18' y1='20' x2='18' y2='10'/><line x1='12' y1='20' x2='12' y2='4'/><line x1='6' y1='20' x2='6' y2='14'/>", c),
    "folder":    lambda c: _svg("<path d='M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z'/>", c),
    "file_text": lambda c: _svg("<path d='M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z'/><path d='M14 2v4a2 2 0 0 0 2 2h4'/><line x1='10' y1='12' x2='16' y2='12'/><line x1='10' y1='16' x2='16' y2='16'/>", c),
    "calendar":  lambda c: _svg("<rect x='3' y='4' width='18' height='18' rx='2'/><line x1='16' y1='2' x2='16' y2='6'/><line x1='8' y1='2' x2='8' y2='6'/><line x1='3' y1='10' x2='21' y2='10'/>", c),
    "hospital":  lambda c: _svg("<path d='M12 6v4'/><path d='M14 8h-4'/><rect width='20' height='18' x='2' y='4' rx='2'/><path d='M2 8h20'/><path d='M6 12v4'/><path d='M10 12v4'/><path d='M14 12v4'/><path d='M18 12v4'/>", c, 26),
    "check":     lambda c: _svg(f"<circle cx='12' cy='12' r='10' fill='{c}' stroke='{c}'/><polyline points='9 12 11 14 15 10' stroke='white' fill='none'/>", c, 14),
    "globe":     lambda c: _svg("<circle cx='12' cy='12' r='10'/><line x1='2' y1='12' x2='22' y2='12'/><path d='M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z'/>", c),
    "download":  lambda c: _svg("<path d='M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4'/><polyline points='7 10 12 15 17 10'/><line x1='12' y1='15' x2='12' y2='3'/>", c),
    "percent":   lambda c: _svg("<line x1='19' y1='5' x2='5' y2='19'/><circle cx='6.5' cy='6.5' r='2.5'/><circle cx='17.5' cy='17.5' r='2.5'/>", c),
    "wallet":    lambda c: _svg("<path d='M20 12V8H6a2 2 0 0 1-2-2c0-1.1.9-2 2-2h12v4'/><path d='M4 6v12a2 2 0 0 0 2 2h14v-4'/><path d='M18 12a2 2 0 0 0-2 2v2a2 2 0 0 0 2 2h4v-6Z'/>", c),
    "user":      lambda c: _svg("<path d='M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2'/><circle cx='12' cy='7' r='4'/>", c, 18),
    "award":     lambda c: _svg("<circle cx='12' cy='8' r='7'/><polyline points='8.21 13.89 7 23 12 20 17 23 15.79 13.88'/>", c, 18),
    "trophy":    lambda c: _svg("<path d='M6 9H4.5a2.5 2.5 0 0 1 0-5H6'/><path d='M18 9h1.5a2.5 2.5 0 0 0 0-5H18'/><path d='M4 22h16'/><path d='M10 14.66V17c0 .55-.45 1-1 1H4v2h16v-2h-5c-.55 0-1-.45-1-1v-2.34'/><path d='M12 2a6.45 6.45 0 0 1 6 6.4c0 3.22-2.58 5.8-5.8 5.8h-.4C8.58 14.2 6 11.62 6 8.4A6.45 6.45 0 0 1 12 2z'/>", c, 18),
    "activity":  lambda c: _svg("<polyline points='22 12 18 12 15 21 9 3 6 12 2 12'/>", c, 18),
}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SIDEBAR – Logo + Theme
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
logo_path = os.path.join(os.path.dirname(__file__), "assets", "LogoCompleto.svg")
logo_b64 = ""
if os.path.exists(logo_path):
    with open(logo_path, "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode()



# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PALETTE (Light Mode)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BG      = "#f8fafc"
SURFACE = "#ffffff"
BORDER  = "#e2e8f0"
TXT     = "#0f172a"
MUTED   = "#64748b"
ACCENT  = TEAL
PLT     = "plotly_white"
GRID    = "#f1f5f9"
INP_BG  = "#ffffff"
INP_TXT = "#0f172a"
INP_BRD = "#cbd5e1"
SEC_BG  = "#f1f5f9"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CSS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ---- base ---- */
html, body, .stApp {{
    background:{BG}!important;
    color:{TXT}!important;
    font-family:'Inter',sans-serif!important;
}}

/* ---- hide sidebar completely ---- */
[data-testid="stSidebar"],
[data-testid="collapsedSidebarCodegen"],
[data-testid="stSidebarCollapseButton"],
section[data-testid="stSidebar"] {{
    display: none !important;
}}

.block-container, .stMainBlockContainer {{
    max-width: 1400px !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    padding-top: 1.5rem !important;
    margin: 0 auto !important;
}}

/* Hide Streamlit Header, Main Menu and Footer */
header[data-testid="stHeader"] {{ display: none !important; }}
#MainMenu {{ visibility: hidden; }}
footer {{ visibility: hidden; }}

/* ---- inputs / selects / date / text ---- */
/* Control outer border and container */
div[data-baseweb="select"] > div,
div[data-testid="stDateInput"] > div > div,
div[data-testid="stTextInput"] > div > div {{
    background: {INP_BG} !important;
    border: 1px solid {INP_BRD} !important;
    border-radius: 10px !important;
    height: 38px !important;
    box-shadow: none !important;
    transition: all 0.2s ease-in-out !important;
}}
/* Remove all inner borders, outlines and background colors to prevent double lines */
div[data-baseweb="select"] > div *,
div[data-testid="stDateInput"] > div > div *,
div[data-testid="stTextInput"] > div > div * {{
    border: none !important;
    background: transparent !important;
    box-shadow: none !important;
    outline: none !important;
}}
/* Set input text paddings and height */
div[data-testid="stDateInput"] input,
div[data-testid="stTextInput"] input {{
    color: {INP_TXT} !important;
    font-size: 14px !important;
    padding: 0 12px !important;
    height: 36px !important;
}}
/* Select text color and font size */
[data-baseweb="select"] * {{
    color: {INP_TXT} !important;
    font-size: 14px !important;
}}
[data-baseweb="select"] svg {{
    fill: {INP_TXT} !important;
}}
/* Focus highlights on outer borders */
div[data-baseweb="select"] > div:focus-within,
div[data-testid="stDateInput"] > div > div:focus-within,
div[data-testid="stTextInput"] > div > div:focus-within {{
    border: 1px solid {ACCENT} !important;
    box-shadow: 0 0 0 1px {ACCENT} !important;
}}

/* dropdown / popover menu */
[data-baseweb="popover"] {{ background:{SURFACE}!important; border:1px solid {BORDER}!important; border-radius:10px!important; }}
[data-baseweb="calendar"], [data-baseweb="calendar"] * {{ background:{SURFACE}!important; color:{INP_TXT}!important; }}
[data-baseweb="menu"], ul[role="listbox"] {{ background:{SURFACE}!important; }}
[data-baseweb="menu"] li, ul[role="listbox"] li {{ color:{INP_TXT}!important; }}
[data-baseweb="menu"] li:hover, ul[role="listbox"] li:hover {{ background:{BORDER}!important; }}

label {{
    color:{MUTED}!important;
    font-weight:700!important;
    font-size:11px!important;
    text-transform:uppercase!important;
    letter-spacing:0.5px!important;
    margin-bottom:6px!important;
}}

/* ---- tabs ---- */
.stTabs [data-baseweb="tab-list"] {{
    background:{BG}!important;
    border-radius:10px; padding:4px;
    border:1px solid {BORDER};
}}
.stTabs [data-baseweb="tab"] {{
    color:{MUTED}!important; font-weight:600!important; border-radius:8px!important;
}}
.stTabs [aria-selected="true"] {{
    background:{SURFACE}!important; color:{ACCENT}!important;
    box-shadow:0 2px 6px rgba(0,0,0,.06)!important;
}}

/* ---- expander ---- */
details[data-testid="stExpander"] {{
    background:{SURFACE}!important;
    border:1px solid {BORDER}!important;
    border-radius:12px!important;
}}
details[data-testid="stExpander"] summary span {{ color:{TXT}!important; font-weight:600!important; }}

/* ---- dataframe ---- */
[data-testid="stDataFrame"] {{ border:1px solid {BORDER}!important; border-radius:10px!important; }}

/* ---- buttons ---- */
.stDownloadButton button {{
    background:transparent!important; color:{ACCENT}!important;
    border:1.5px solid {ACCENT}!important; border-radius:8px!important;
    font-weight:600!important; font-size:13px!important; transition:all .2s;
}}
.stDownloadButton button:hover {{ background:{ACCENT}!important; color:#fff!important; }}
.stLinkButton a {{
    background:{ACCENT}!important; color:#fff!important;
    border-radius:8px!important; font-weight:600!important; font-size:13px!important;
    text-decoration:none!important; transition:all .2s;
}}
.stLinkButton a:hover {{ opacity:.9; }}

/* ---- divider ---- */
hr {{ border-color:{BORDER}!important; }}

/* ---- KPI cards ---- */
.kpi {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 22px 24px;
    box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.03), 0 2px 4px -2px rgba(15, 23, 42, 0.02);
    transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.25s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.25s;
}}
.kpi:hover {{
    transform: translateY(-3px);
    box-shadow: 0 12px 24px -4px rgba(15, 23, 42, 0.08), 0 8px 16px -4px rgba(15, 23, 42, 0.04);
    border-color: {ACCENT};
}}
.kpi-head {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
}}
.kpi-icon-wrap {{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    border-radius: 8px;
    background: rgba(17, 82, 100, 0.06);
    color: {ACCENT};
    flex-shrink: 0;
}}
.kpi-lbl {{
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 700;
    color: {MUTED};
}}
.kpi-val {{
    font-size: 30px;
    font-weight: 800;
    line-height: 1.1;
}}
.kpi-sub {{
    font-size: 12px;
    color: {MUTED};
    margin-top: 8px;
}}

/* ---- section header ---- */
.sec {{
    display:flex; align-items:center; gap:10px;
    padding:12px 18px; margin:30px 0 18px;
    border-left:4px solid {ACCENT}; border-radius:8px;
    background:{SEC_BG};
    font-size:15px; font-weight:700; color:{ACCENT};
}}

/* ---- scrollbar ---- */
::-webkit-scrollbar {{ width:6px; }}
::-webkit-scrollbar-thumb {{ background:{BORDER}; border-radius:3px; }}

/* ---- insight operational box ---- */
.insight-row {{
    display: flex;
    gap: 16px;
    margin-top: 14px;
    margin-bottom: 24px;
    flex-wrap: wrap;
}}
.insight-box {{
    flex: 1;
    min-width: 240px;
    background: {SURFACE};
    border-radius: 16px;
    padding: 18px 22px;
    border: 1px solid {BORDER};
    border-left: 4px solid {ACCENT};
    box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.03), 0 2px 4px -2px rgba(15, 23, 42, 0.02);
    transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.25s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.25s;
}}
.insight-box:hover {{
    transform: translateY(-3px);
    box-shadow: 0 12px 24px -4px rgba(15, 23, 42, 0.08), 0 8px 16px -4px rgba(15, 23, 42, 0.04);
    border-color: {ACCENT};
}}
.insight-lbl-row {{
    display: flex;
    align-items: center;
    gap: 14px;
}}
.insight-icon-wrap {{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 38px;
    height: 38px;
    border-radius: 8px;
    background: rgba(17, 82, 100, 0.06);
    color: {ACCENT};
    flex-shrink: 0;
}}
.insight-lbl {{
    font-size: 11px;
    font-weight: 700;
    color: {MUTED};
    text-transform: uppercase;
    letter-spacing: 0.8px;
}}
.insight-val {{
    font-size: 16px;
    font-weight: 800;
    color: {TXT};
    line-height: 1.2;
    margin-top: 2px;
}}

/* ---- mobile responsiveness ---- */
@media (max-width: 768px) {{
    .block-container, .stMainBlockContainer {{
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }}
    .insight-box {{
        min-width: 100% !important;
    }}
    .kpi {{
        padding: 18px 20px !important;
    }}
    /* Stack all streamlit columns on mobile */
    div[data-testid="stHorizontalBlock"] {{
        flex-direction: column !important;
        gap: 16px !important;
    }}
    div[data-testid="column"] {{
        width: 100% !important;
        flex: 1 1 100% !important;
        min-width: 100% !important;
    }}
    /* Align header items better on mobile */
    div[style*="text-align:right"] {{
        text-align: left !important;
        padding-top: 10px !important;
    }}
}}
@media (max-width: 600px) {{
    .kpi-val {{
        font-size: 24px !important;
    }}
    .kpi-lbl {{
        font-size: 10px !important;
    }}
    .insight-val {{
        font-size: 15px !important;
    }}
}}
</style>
""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DATA LOADING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXCEL = os.path.join(os.path.dirname(__file__), "data", "Plantilla_Mensual_CRP.xlsx")
SHEET_ID = "1nFenhWcCDrqCG76VqOIGOuLLSptdFWRmwfbTa9ZdVsU"
URL_METAS = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"
URL_VENTAS = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=2061072924"
URL_AGENDAS = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=1426952662"

def clean_currency(val):
    if pd.isna(val):
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    val_str = str(val).strip().upper().replace("S/.", "").replace("S/", "").replace("$", "").strip()
    if "," in val_str and "." in val_str:
        if val_str.rfind(",") > val_str.rfind("."):
            val_str = val_str.replace(".", "").replace(",", ".")
        else:
            val_str = val_str.replace(",", "")
    elif "," in val_str:
        import re
        if re.search(r',\d{2}$', val_str):
            val_str = val_str.replace(",", ".")
        else:
            val_str = val_str.replace(",", "")
    val_str = val_str.replace(" ", "")
    try:
        return float(val_str)
    except:
        return 0.0

def parse_dates_custom(series):
    if pd.api.types.is_datetime64_any_dtype(series):
        return series
    def clean_date_str(val):
        if pd.isna(val):
            return val
        val_str = str(val).strip()
        import re
        if not re.search(r'\b(20\d{2})\b', val_str):
            val_str = f"{val_str}-2026"
        return val_str
    cleaned = series.apply(clean_date_str)
    months_es_en = {
        r'\bene\b': 'jan', r'\bfeb\b': 'feb', r'\bmar\b': 'mar', r'\babr\b': 'apr',
        r'\bmay\b': 'may', r'\bjun\b': 'jun', r'\bjul\b': 'jul', r'\bago\b': 'aug',
        r'\bsep\b': 'sep', r'\boct\b': 'oct', r'\bnov\b': 'nov', r'\bdic\b': 'dec'
    }
    for es, en in months_es_en.items():
        import re
        cleaned = cleaned.astype(str).str.replace(es, en, case=False, regex=True)
    return pd.to_datetime(cleaned, errors="coerce")

@st.cache_data(show_spinner="Cargando datos...")
def load_data():
    source = "Google Sheets (En Vivo)"
    try:
        df_metas = pd.read_csv(URL_METAS)
        df_ventas = pd.read_csv(URL_VENTAS)
        df_agendas = pd.read_csv(URL_AGENDAS)
    except Exception as gs_err:
        # Fallback to local
        df_metas = pd.read_excel(EXCEL, sheet_name="METAS")
        df_ventas = pd.read_excel(EXCEL, sheet_name="VENTAS")
        df_agendas = pd.read_excel(EXCEL, sheet_name="AGENDAS")
        source = "Local Excel (Offline)"

    # 1. Metas
    df_metas.columns = df_metas.columns.str.strip().str.upper()
    meta_global_row = df_metas[df_metas["CATEGORIA"].str.strip().str.upper() == "GLOBAL"]
    meta_global = int(meta_global_row["META"].iloc[0]) if not meta_global_row.empty else 360
    
    df_sups = df_metas[df_metas["CATEGORIA"].str.strip().str.upper() == "SUPERVISOR"]
    sup_targets = dict(zip(df_sups["NOMBRE"].str.strip().str.upper(), df_sups["META"].fillna(180).astype(int)))
    
    df_asesores = df_metas[df_metas["CATEGORIA"].str.strip().str.upper() == "ASESOR"]
    asesor_targets = dict(zip(df_asesores["NOMBRE"].str.strip().str.upper(), df_asesores["META"].fillna(13).astype(int)))

    # 2. Sales
    df_ventas.columns = df_ventas.columns.str.strip().str.upper()
    df_ventas = df_ventas.dropna(subset=["FECHA", "ASESOR"])
    df_ventas["FECHA"] = parse_dates_custom(df_ventas["FECHA"])
    for c in ["PRIMA", "COMISION", "COMISION SUPERVISOR"]:
        if c in df_ventas.columns:
            df_ventas[c] = df_ventas[c].apply(clean_currency)
            
    contrato_col = next((c for c in df_ventas.columns if "CONTRATO" in str(c)), None)
    if contrato_col and contrato_col != "CONTRATO":
        df_ventas = df_ventas.rename(columns={contrato_col: "CONTRATO"})
        
    df_ventas["SUPERVISOR"] = df_ventas["SUPERVISOR"].str.strip().str.upper()
    df_ventas["SUP_FULL"] = df_ventas["SUPERVISOR"].map({"FRANK": "FRANK ROSAS", "GONZALO": "GONZALO PAZ"}).fillna(df_ventas["SUPERVISOR"])

    # 3. Agendas
    df_agendas.columns = df_agendas.columns.str.strip().str.upper()
    marca_col = next((c for c in df_agendas.columns if "MARCA TEMPORAL" in str(c)), "MARCA TEMPORAL")
    asesor_col = next((c for c in df_agendas.columns if "ASESOR" in str(c)), "ASESOR COMERCIAL")
    
    df_agendas = df_agendas.dropna(subset=[marca_col, asesor_col])
    df_agendas[marca_col] = pd.to_datetime(df_agendas[marca_col], errors="coerce")
    df_agendas = df_agendas.rename(columns={marca_col: "Marca temporal", asesor_col: "ASESOR COMERCIAL"})

    return df_ventas, df_agendas, meta_global, sup_targets, asesor_targets, source


try:
    df_ventas, df_agendas, META_GLOBAL, SUP_TARGETS, ASESOR_TARGETS, DATA_SOURCE = load_data()
except Exception as e:
    st.error(f"No se pudo cargar los datos (Google Sheets / Excel local). Verifica el archivo o la conexión.\n\n`{e}`")
    st.stop()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HEADER (Brand & Status Row)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
head_cols = st.columns([3.5, 1.5])

with head_cols[0]:
    logo_html = ""
    if logo_b64:
        logo_html = f"<img src='data:image/svg+xml;base64,{logo_b64}' style='max-height:60px;width:auto;display:block;'/>"
    else:
        logo_html = f"<h1 style='color:{ACCENT};margin:0;font-weight:800;font-size:24px;'>CLINICA CRP</h1>"
    
    st.markdown(
        f"<div style='display:flex;align-items:center;height:75px;'>"
        f"  {logo_html}"
        f"</div>",
        unsafe_allow_html=True,
    )

with head_cols[1]:
    is_live = "Google Sheets" in DATA_SOURCE
    badge_bg = "rgba(16, 185, 129, 0.1)" if is_live else "rgba(245, 158, 11, 0.1)"
    badge_color = GREEN if is_live else GOLD
    badge_text = "NUBE" if is_live else "LOCAL"
    badge_title = "Google Sheets (En Vivo)" if is_live else "Excel Local (Offline)"

    st.markdown(
        f"<div style='text-align:right;height:75px;display:flex;flex-direction:column;justify-content:center;align-items:flex-end;'>"
        f"  <span style='font-size:10px;font-weight:700;color:{MUTED};letter-spacing:1px;text-transform:uppercase;'>Centro de Operaciones</span>"
        f"  <div style='display:flex;align-items:center;gap:6px;margin-top:2px;'>"
        f"    <span style='font-size:12px;color:{GREEN};font-weight:600;'>&bull; Campaña Mayo 2026</span>"
        f"    <span title='{badge_title}' style='font-size:10px;background:{badge_bg};color:{badge_color};padding:2px 8px;border-radius:12px;font-weight:700;border:1px solid {badge_color}50;text-transform:uppercase;cursor:help;'>{badge_text}</span>"
        f"  </div>"
        f"</div>",
        unsafe_allow_html=True
    )

st.markdown("<hr style='margin:10px 0 18px;border:0;border-top:1px solid #e2e8f0;'/>", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FILTERS PANEL
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
filter_cols = st.columns([1, 1, 1])

with filter_cols[0]:
    sup_opts = ["Todos"] + sorted(df_ventas["SUP_FULL"].dropna().unique().tolist())
    sel_sup = st.selectbox("Supervisor", sup_opts)

with filter_cols[1]:
    pool = df_ventas if sel_sup == "Todos" else df_ventas[df_ventas["SUP_FULL"] == sel_sup]
    sel_asesor = st.selectbox("Asesor Comercial", ["Todos"] + sorted(pool["ASESOR"].dropna().unique().tolist()))

with filter_cols[2]:
    if not df_ventas.empty and pd.notna(df_ventas["FECHA"].min()):
        d_min, d_max = df_ventas["FECHA"].min().date(), df_ventas["FECHA"].max().date()
        if d_min == d_max:
            date_range = st.date_input("Rango de Fechas", value=(d_min, d_min), min_value=d_min, max_value=d_min + pd.Timedelta(days=30))
        else:
            date_range = st.date_input("Rango de Fechas", value=(d_min, d_max), min_value=d_min, max_value=d_max)
    else:
        d_min = pd.Timestamp.now().date()
        d_max = d_min + pd.Timedelta(days=30)
        date_range = st.date_input("Rango de Fechas", value=(d_min, d_max), min_value=d_min, max_value=d_max)

st.markdown("<hr style='margin:16px 0 24px;border:0;border-top:1px solid #e2e8f0;'/>", unsafe_allow_html=True)

# Apply filters
fv = df_ventas.copy()
if sel_sup != "Todos":
    fv = fv[fv["SUP_FULL"] == sel_sup]
if sel_asesor != "Todos":
    fv = fv[fv["ASESOR"] == sel_asesor]
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    fv = fv[(fv["FECHA"].dt.date >= date_range[0]) & (fv["FECHA"].dt.date <= date_range[1])]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# KPI CARDS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
total_prima  = fv["PRIMA"].sum()
total_ventas = len(fv)
avance_pct   = (total_ventas / META_GLOBAL * 100) if META_GLOBAL else 0
ticket_prom  = fv["PRIMA"].mean() if total_ventas else 0
gap          = META_GLOBAL - total_ventas
total_comisiones = fv["COMISION"].sum() + fv["COMISION SUPERVISOR"].sum()

def kpi(icon_fn, label, value, sub, val_color=None):
    vc = val_color or TXT
    return (
        f"<div class='kpi'>"
        f"<div class='kpi-head'>"
        f"  <div class='kpi-icon-wrap'>{icon_fn(ACCENT)}</div>"
        f"  <span class='kpi-lbl'>{label}</span>"
        f"</div>"
        f"<div class='kpi-val' style='color:{vc}'>{value}</div>"
        f"<div class='kpi-sub'>{sub}</div>"
        f"</div>"
    )

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(kpi(ICON["dollar"], "Recaudacion Total", f"S/. {total_prima:,.0f}", f"{total_ventas} contratos"), unsafe_allow_html=True)
with k2:
    c = GREEN if avance_pct >= 80 else (GOLD if avance_pct >= 50 else RED)
    st.markdown(kpi(ICON["percent"], "Avance vs Meta", f"{avance_pct:.1f}%", f"Meta: {META_GLOBAL} &middot; Faltan {gap}", c), unsafe_allow_html=True)
with k3:
    st.markdown(kpi(ICON["clipboard"], "Operaciones", f"{total_ventas}", "Registradas en Mayo 2026"), unsafe_allow_html=True)
with k4:
    st.markdown(kpi(ICON["tag"], "Ticket Promedio", f"S/. {ticket_prom:,.0f}", f"Comisión prom: S/. {(fv['COMISION'].mean() if total_ventas else 0):,.0f}"), unsafe_allow_html=True)
with k5:
    st.markdown(kpi(ICON["wallet"], "Comisiones Totales", f"S/. {total_comisiones:,.0f}", f"Asesor + Supervisor"), unsafe_allow_html=True)

# Calculate secondary operational insights
if not fv.empty:
    top_adv_series = fv["ASESOR"].value_counts()
    top_adv_name = top_adv_series.index[0].strip().title() if not top_adv_series.empty else "N/A"
    top_adv_sales = top_adv_series.iloc[0] if not top_adv_series.empty else 0
    top_adv_txt = f"{top_adv_name} ({top_adv_sales} vts)"
    
    pref_plan_series = fv["PRIMA"].value_counts()
    pref_plan_val = pref_plan_series.index[0] if not pref_plan_series.empty else 0
    pref_plan_pct = (pref_plan_series.iloc[0] / len(fv) * 100) if not pref_plan_series.empty else 0
    pref_plan_txt = f"Plan S/. {pref_plan_val:,.0f} ({pref_plan_pct:.1f}%)"
    
    rec_day_series = fv.groupby("FECHA").size()
    rec_day_val = rec_day_series.max() if not rec_day_series.empty else 0
    rec_day_date = rec_day_series.idxmax().strftime("%d/%m") if not rec_day_series.empty else "N/A"
    rec_day_txt = f"{rec_day_date} ({rec_day_val} vts)"
    
    act_adv = fv["ASESOR"].nunique()
    avg_sales_adv = len(fv) / act_adv if act_adv else 0
    prod_txt = f"{act_adv} asesores ({avg_sales_adv:.1f} v/as)"
else:
    top_adv_txt = "N/A"
    pref_plan_txt = "N/A"
    rec_day_txt = "N/A"
    prod_txt = "N/A"

st.markdown(
    f"<div class='insight-row'>"
    f"  <div class='insight-box'>"
    f"    <div class='insight-lbl-row'>"
    f"      <div class='insight-icon-wrap'>{ICON['user'](ACCENT)}</div>"
    f"      <div style='display:flex;flex-direction:column;'>"
    f"        <span class='insight-lbl'>Top Asesor del Mes</span>"
    f"        <span class='insight-val'>{top_adv_txt}</span>"
    f"      </div>"
    f"    </div>"
    f"  </div>"
    f"  <div class='insight-box'>"
    f"    <div class='insight-lbl-row'>"
    f"      <div class='insight-icon-wrap'>{ICON['award'](ACCENT)}</div>"
    f"      <div style='display:flex;flex-direction:column;'>"
    f"        <span class='insight-lbl'>Plan Preferido</span>"
    f"        <span class='insight-val'>{pref_plan_txt}</span>"
    f"      </div>"
    f"    </div>"
    f"  </div>"
    f"  <div class='insight-box'>"
    f"    <div class='insight-lbl-row'>"
    f"      <div class='insight-icon-wrap'>{ICON['trophy'](ACCENT)}</div>"
    f"      <div style='display:flex;flex-direction:column;'>"
    f"        <span class='insight-lbl'>Día Récord de Ventas</span>"
    f"        <span class='insight-val'>{rec_day_txt}</span>"
    f"      </div>"
    f"    </div>"
    f"  </div>"
    f"  <div class='insight-box'>"
    f"    <div class='insight-lbl-row'>"
    f"      <div class='insight-icon-wrap'>{ICON['activity'](ACCENT)}</div>"
    f"      <div style='display:flex;flex-direction:column;'>"
    f"        <span class='insight-lbl'>Productividad Promedio</span>"
    f"        <span class='insight-val'>{prod_txt}</span>"
    f"      </div>"
    f"    </div>"
    f"  </div>"
    f"</div>",
    unsafe_allow_html=True
)



# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PLOTLY HELPER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def style_fig(fig, title="", h=350):
    fig.update_layout(
        template=PLT,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor=SURFACE,
        title=dict(text=title, font=dict(size=14, family="Inter", color=ACCENT), x=0.02),
        margin=dict(l=12, r=12, t=46, b=12),
        height=h,
        font=dict(family="Inter", color=TXT, size=11),
        hoverlabel=dict(bgcolor=SURFACE, font_color=TXT, font_size=12, bordercolor=BORDER),
        dragmode=False,
    )
    fig.update_xaxes(showgrid=True, gridcolor=GRID, zeroline=False, fixedrange=True)
    fig.update_yaxes(showgrid=True, gridcolor=GRID, zeroline=False, fixedrange=True)
    return fig


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 1 – ANALISIS DE RENDIMIENTO
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown(f"<div class='sec'>{ICON['bar_chart'](ACCENT)} ANALISIS DE RENDIMIENTO</div>", unsafe_allow_html=True)

# Row 1 ─ Avance Acumulado vs Meta | Tendencia Diaria
r1a, r1b = st.columns(2)

with r1a:
    # Get cumulative sales
    start_date = date_range[0] if isinstance(date_range, (list, tuple)) and len(date_range) == 2 else df_ventas["FECHA"].min().date()
    end_date = date_range[1] if isinstance(date_range, (list, tuple)) and len(date_range) == 2 else df_ventas["FECHA"].max().date()
    
    all_dates = pd.date_range(start=start_date, end=end_date)
    df_daily = fv.groupby("FECHA").size().reset_index(name="Ventas")
    df_daily = df_daily.sort_values("FECHA")
    df_daily = df_daily.set_index("FECHA").reindex(all_dates, fill_value=0).reset_index()
    df_daily = df_daily.rename(columns={"index": "Fecha"})
    df_daily["Acumulado"] = df_daily["Ventas"].cumsum()
    
    # Calculate target path
    if sel_asesor != "Todos":
        current_target = ASESOR_TARGETS.get(sel_asesor.strip().upper(), 13)
    elif sel_sup != "Todos":
        current_target = SUP_TARGETS.get(sel_sup.strip().upper(), 180)
    else:
        current_target = META_GLOBAL
        
    num_days = len(all_dates)
    df_daily["Meta_Acumulada"] = [round((i + 1) * (current_target / num_days), 1) for i in range(num_days)]
    
    fig_burn = go.Figure()
    fig_burn.add_trace(go.Scatter(
        x=df_daily["Fecha"], y=df_daily["Acumulado"],
        mode="lines+markers", name="Ventas Acumuladas",
        line=dict(color=TEAL, width=3),
        fill="tozeroy", fillcolor="rgba(17,82,100,0.06)",
        hovertemplate="<b>%{x|%d %b}</b><br>Avance: %{y} ventas<extra></extra>"
    ))
    fig_burn.add_trace(go.Scatter(
        x=df_daily["Fecha"], y=df_daily["Meta_Acumulada"],
        mode="lines", name="Trayectoria Meta",
        line=dict(color=MUTED, width=1.8, dash="dash"),
        hovertemplate="<b>%{x|%d %b}</b><br>Objetivo: %{y:.1f} ventas<extra></extra>"
    ))
    style_fig(fig_burn, f"Avance Acumulado vs Meta (Objetivo: {current_target} ventas)", h=290)
    fig_burn.update_layout(legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center"))
    st.plotly_chart(fig_burn, use_container_width=True, config={'displayModeBar': False})

with r1b:
    df_t = fv.groupby("FECHA").size().reset_index(name="Ventas")
    fig = go.Figure(go.Scatter(
        x=df_t["FECHA"], y=df_t["Ventas"], mode="lines+markers",
        line=dict(color=CYAN, width=2.5, shape="spline"),
        marker=dict(size=6, color=CYAN, line=dict(color=SURFACE, width=1.5)),
        fill="tozeroy", fillcolor="rgba(0,178,169,0.05)",
        hovertemplate="<b>%{x|%d %b}</b><br>Ventas: %{y}<extra></extra>",
    ))
    style_fig(fig, "Tendencia Diaria de Ventas", h=290)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# Row 2 ─ Primas por Supervisor | Ventas por Día de la Semana
r2a, r2b = st.columns(2)

with r2a:
    df_sp = fv.groupby("SUP_FULL").agg(Prima=("PRIMA", "sum"), N=("PRIMA", "count")).reset_index().sort_values("Prima", ascending=True)
    fig = go.Figure(go.Bar(
        y=df_sp["SUP_FULL"], x=df_sp["Prima"], orientation="h",
        marker=dict(color=[CYAN, TEAL][: len(df_sp)], cornerradius=6),
        text=df_sp.apply(lambda r: f"S/. {r['Prima']:,.0f}  ({int(r['N'])} ventas)", axis=1),
        textposition="auto", textfont=dict(color="#fff", size=12),
        hovertemplate="<b>%{y}</b><br>S/. %{x:,.0f}<extra></extra>",
    ))
    style_fig(fig, "Recaudacion por Supervisor", h=290)
    fig.update_xaxes(tickprefix="S/. ")
    fig.update_yaxes(showgrid=False)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with r2b:
    fv_temp = fv.copy()
    fv_temp["Dia_Semana"] = fv_temp["FECHA"].dt.day_name()
    day_mapping = {
        "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
        "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"
    }
    fv_temp["Dia_Esp"] = fv_temp["Dia_Semana"].map(day_mapping)
    df_days = fv_temp.groupby("Dia_Esp").size().reset_index(name="Ventas")
    days_order = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    df_days["Dia_Esp"] = pd.Categorical(df_days["Dia_Esp"], categories=days_order, ordered=True)
    df_days = df_days.sort_values("Dia_Esp")
    
    fig_days = go.Figure(go.Bar(
        x=df_days["Dia_Esp"], y=df_days["Ventas"],
        marker=dict(color=TEAL, cornerradius=5),
        text=df_days["Ventas"], textposition="auto",
        textfont=dict(color="#fff", size=11),
        hovertemplate="<b>%{x}</b><br>Ventas: %{y}<extra></extra>"
    ))
    style_fig(fig_days, "Ventas por Día de la Semana", h=290)
    fig_days.update_layout(showlegend=False)
    st.plotly_chart(fig_days, use_container_width=True, config={'displayModeBar': False})

# Row 3 ─ Desempeño de Asesores vs Meta | Donut de Distribución | Comisiones
r3a, r3b, r3c = st.columns([1.4, 1, 1.2])

with r3a:
    df_a_meta = fv.groupby("ASESOR").size().reset_index(name="Ventas")
    df_a_meta["Meta"] = df_a_meta["ASESOR"].map(lambda n: ASESOR_TARGETS.get(n.strip().upper(), 13))
    df_a_meta = df_a_meta.sort_values("Ventas", ascending=True).tail(8)
    
    fig_meta = go.Figure()
    fig_meta.add_trace(go.Bar(
        y=df_a_meta["ASESOR"].str.title(), x=df_a_meta["Ventas"],
        name="Ventas Reales", orientation="h",
        marker=dict(color=CYAN, cornerradius=5),
        text=df_a_meta["Ventas"], textposition="auto",
        hovertemplate="<b>%{y}</b><br>Ventas: %{x}<extra></extra>"
    ))
    fig_meta.add_trace(go.Bar(
        y=df_a_meta["ASESOR"].str.title(), x=df_a_meta["Meta"],
        name="Meta", orientation="h",
        marker=dict(color=TEAL, cornerradius=5),
        text=df_a_meta["Meta"], textposition="auto",
        hovertemplate="<b>%{y}</b><br>Meta: %{x}<extra></extra>"
    ))
    fig_meta.update_layout(barmode="group")
    style_fig(fig_meta, "Desempeño vs Meta por Asesor (Ventas)", h=340)
    fig_meta.update_layout(legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center"))
    st.plotly_chart(fig_meta, use_container_width=True, config={'displayModeBar': False})

with r3b:
    df_pie = fv.groupby("SUP_FULL")["PRIMA"].sum().reset_index()
    fig = go.Figure(go.Pie(
        labels=df_pie["SUP_FULL"], values=df_pie["PRIMA"], hole=0.55,
        marker=dict(colors=[TEAL, CYAN]),
        textinfo="percent+label", textfont=dict(size=11),
        hovertemplate="<b>%{label}</b><br>S/. %{value:,.0f}<br>%{percent}<extra></extra>",
    ))
    style_fig(fig, "Distribucion de Primas", h=340)
    fig.update_layout(
        annotations=[dict(text=f"S/. {total_prima:,.0f}", x=.5, y=.5, font_size=13, font_color=TXT, showarrow=False)],
        legend=dict(orientation="h", y=-0.05, x=.5, xanchor="center", font=dict(size=10, color=TXT)),
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with r3c:
    df_com = fv.groupby("SUP_FULL").agg(Asesor=("COMISION", "sum"), Supervisor=("COMISION SUPERVISOR", "sum")).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Com. Asesor", x=df_com["SUP_FULL"], y=df_com["Asesor"],
                         marker_color=CYAN, marker_cornerradius=5, hovertemplate="Asesor: S/. %{y:,.0f}<extra></extra>"))
    fig.add_trace(go.Bar(name="Com. Supervisor", x=df_com["SUP_FULL"], y=df_com["Supervisor"],
                         marker_color=TEAL, marker_cornerradius=5, hovertemplate="Supervisor: S/. %{y:,.0f}<extra></extra>"))
    fig.update_layout(barmode="stack")
    style_fig(fig, "Comisiones Generadas", h=340)
    fig.update_yaxes(tickprefix="S/. ")
    fig.update_layout(legend=dict(orientation="h", y=-0.15, x=.5, xanchor="center", font=dict(size=10, color=TXT)))
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 2 – TABLAS DE GESTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown(f"<div class='sec'>{ICON['folder'](ACCENT)} TABLAS DE GESTION</div>", unsafe_allow_html=True)

tab1,tab2,tab3 = st.tabs(["Resumen por Supervisor", "Desempeño por Asesor", "Mix de Productos (Primas)"])

with tab1:
    df_s = df_ventas.groupby("SUP_FULL").agg(
        Recaudacion=("PRIMA", "sum"), Ventas=("PRIMA", "count"),
        Com_Asesor=("COMISION", "sum"), Com_Supervisor=("COMISION SUPERVISOR", "sum"),
    ).reset_index()
    df_s["Meta"] = df_s["SUP_FULL"].map(lambda n: SUP_TARGETS.get(n.upper(), 180))
    df_s["Avance %"] = (df_s["Ventas"] / df_s["Meta"] * 100).round(1)
    df_s = df_s.rename(columns={"SUP_FULL": "Supervisor"})
    df_s = df_s[["Supervisor", "Recaudacion", "Ventas", "Meta", "Avance %", "Com_Asesor", "Com_Supervisor"]]

    st.dataframe(df_s, column_config={
        "Recaudacion": st.column_config.NumberColumn("Recaudacion", format="S/. %,.0f"),
        "Avance %": st.column_config.ProgressColumn("Avance %", format="%.1f%%", min_value=0, max_value=100),
        "Com_Asesor": st.column_config.NumberColumn("Com. Asesores", format="S/. %,.0f"),
        "Com_Supervisor": st.column_config.NumberColumn("Com. Supervisor", format="S/. %,.0f"),
    }, use_container_width=True, hide_index=True)

    st.download_button("Exportar Supervisores", df_s.to_csv(index=False).encode("utf-8"),
                        "supervisores_crp.csv", "text/csv", key="dl_s")

with tab2:
    df_a = df_ventas.groupby(["ASESOR", "SUP_FULL"]).agg(
        Recaudacion=("PRIMA", "sum"), Ventas=("PRIMA", "count"), Comision=("COMISION", "sum"),
    ).reset_index()
    df_a["Meta"] = df_a["ASESOR"].map(lambda n: ASESOR_TARGETS.get(n.strip().upper(), 13))
    df_a["Avance %"] = (df_a["Ventas"] / df_a["Meta"] * 100).round(1)
    df_a["Ticket"] = (df_a["Recaudacion"] / df_a["Ventas"]).round(0)
    df_a = df_a.rename(columns={"SUP_FULL": "Supervisor"}).sort_values("Recaudacion", ascending=False)
    df_a = df_a[["ASESOR", "Supervisor", "Recaudacion", "Ventas", "Meta", "Avance %", "Comision", "Ticket"]]

    st.dataframe(df_a, column_config={
        "ASESOR": st.column_config.TextColumn("Asesor", width="large"),
        "Recaudacion": st.column_config.NumberColumn("Recaudacion", format="S/. %,.0f"),
        "Avance %": st.column_config.ProgressColumn("Avance %", format="%.1f%%", min_value=0, max_value=100),
        "Comision": st.column_config.NumberColumn("Comision", format="S/. %,.0f"),
        "Ticket": st.column_config.NumberColumn("Ticket Prom.", format="S/. %,.0f"),
    }, use_container_width=True, hide_index=True)

    st.download_button("Exportar Asesores", df_a.to_csv(index=False).encode("utf-8"),
                        "asesores_crp.csv", "text/csv", key="dl_a")

with tab3:
    # Product/Premium Mix
    df_p = df_ventas.groupby("PRIMA").agg(
        Ventas=("PRIMA", "count"),
        Recaudacion=("PRIMA", "sum"),
        Com_Asesor=("COMISION", "sum"),
        Com_Supervisor=("COMISION SUPERVISOR", "sum")
    ).reset_index()
    total_p_ventas = df_p["Ventas"].sum()
    df_p["Mix %"] = (df_p["Ventas"] / total_p_ventas * 100).round(1) if total_p_ventas else 0
    df_p["Comisión Total"] = df_p["Com_Asesor"] + df_p["Com_Supervisor"]
    df_p = df_p.rename(columns={"PRIMA": "Plan (Prima S/.)"}).sort_values("Ventas", ascending=False)
    df_p = df_p[["Plan (Prima S/.)", "Ventas", "Mix %", "Recaudacion", "Comisión Total"]]

    st.dataframe(df_p, column_config={
        "Plan (Prima S/.)": st.column_config.NumberColumn("Plan (Prima S/.)", format="S/. %,.0f"),
        "Ventas": st.column_config.NumberColumn("Contratos Vendidos"),
        "Mix %": st.column_config.ProgressColumn("Cuota de Mix", format="%.1f%%", min_value=0, max_value=100),
        "Recaudacion": st.column_config.NumberColumn("Total Recaudado", format="S/. %,.0f"),
        "Comisión Total": st.column_config.NumberColumn("Comisiones Generadas", format="S/. %,.0f"),
    }, use_container_width=True, hide_index=True)

    st.download_button("Exportar Mix de Productos", df_p.to_csv(index=False).encode("utf-8"),
                        "mix_productos_crp.csv", "text/csv", key="dl_p")



# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 3 – DETALLE DE OPERACIONES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown(f"<div class='sec'>{ICON['file_text'](ACCENT)} DETALLE DE OPERACIONES</div>", unsafe_allow_html=True)

with st.expander("Ver registro detallado de ventas"):
    search = st.text_input("Buscar por afiliado, DNI, asesor o supervisor:", placeholder="Escribe para filtrar...", key="s_ops")
    dfd = fv.copy()
    if search:
        q = search.lower()
        dfd = dfd[
            dfd["NOMBRE AFILIADO"].astype(str).str.lower().str.contains(q, na=False) |
            dfd["DNI"].astype(str).str.lower().str.contains(q, na=False) |
            dfd["ASESOR"].astype(str).str.lower().str.contains(q, na=False) |
            dfd["SUP_FULL"].astype(str).str.lower().str.contains(q, na=False)
        ]
    dfs = dfd[["SUP_FULL", "FECHA", "ASESOR", "CONTRATO", "NOMBRE AFILIADO", "DNI", "PRIMA", "COMISION", "COMISION SUPERVISOR"]].rename(columns={
        "SUP_FULL": "Supervisor", "FECHA": "Fecha", "ASESOR": "Asesor",
        "CONTRATO": "Contrato", "NOMBRE AFILIADO": "Afiliado",
        "PRIMA": "Prima", "COMISION": "Comision", "COMISION SUPERVISOR": "Com. Sup."
    })
    dfs["Fecha"] = dfs["Fecha"].dt.strftime("%d/%m/%Y")
    st.dataframe(dfs, column_config={
        "Prima": st.column_config.NumberColumn("Prima", format="S/. %,.0f"),
        "Comision": st.column_config.NumberColumn("Comision", format="S/. %,.0f"),
        "Com. Sup.": st.column_config.NumberColumn("Com. Sup.", format="S/. %,.0f"),
    }, use_container_width=True, hide_index=True)
    st.download_button("Exportar Detalle", dfs.to_csv(index=False).encode("utf-8"),
                        "detalle_ventas_crp.csv", "text/csv", key="dl_d")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 4 – AGENDAS COMERCIALES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown(f"<div class='sec'>{ICON['calendar'](ACCENT)} AGENDAS COMERCIALES</div>", unsafe_allow_html=True)

# 4 KPIs for Agendas (Baseline Ene/Feb 2025)
total_agendas = len(df_agendas)
act_ag_asesores = df_agendas["ASESOR COMERCIAL"].nunique()
avg_ag_per_asesor = total_agendas / act_ag_asesores if act_ag_asesores else 0

top_ag_series = df_agendas["ASESOR COMERCIAL"].value_counts()
top_ag_name = top_ag_series.index[0].strip().title() if not top_ag_series.empty else "N/A"
top_ag_val = top_ag_series.iloc[0] if not top_ag_series.empty else 0

df_ag_temp = df_agendas.copy()
df_ag_temp["Dia_Semana"] = df_ag_temp["Marca temporal"].dt.day_name()
day_mapping_es = {
    "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
    "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"
}
df_ag_temp["Dia_Esp"] = df_ag_temp["Dia_Semana"].map(day_mapping_es)
peak_day_series = df_ag_temp["Dia_Esp"].value_counts()
peak_day_name = peak_day_series.index[0] if not peak_day_series.empty else "N/A"
peak_day_val = peak_day_series.iloc[0] if not peak_day_series.empty else 0

col_ag1, col_ag2, col_ag3, col_ag4 = st.columns(4)
with col_ag1:
    st.markdown(kpi(ICON["calendar"], "Total Agendas", f"{total_agendas}", "Registros en Ene/Feb 2025"), unsafe_allow_html=True)
with col_ag2:
    st.markdown(kpi(ICON["clipboard"], "Asesores Activos", f"{act_ag_asesores}", f"Promedio: {avg_ag_per_asesor:.1f} por asesor"), unsafe_allow_html=True)
with col_ag3:
    st.markdown(kpi(ICON["trending"], "Top Agendador", f"{top_ag_val}", f"Asesor: {top_ag_name}"), unsafe_allow_html=True)
with col_ag4:
    st.markdown(kpi(ICON["globe"], "Día Más Activo", f"{peak_day_name}", f"Pico de {peak_day_val} agendas"), unsafe_allow_html=True)

st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

# 2 side-by-side charts for agendas
col_ch1, col_ch2 = st.columns(2)

with col_ch1:
    df_ag_asesor = df_agendas.groupby("ASESOR COMERCIAL").size().reset_index(name="Agendas").sort_values("Agendas", ascending=True)
    fig_ag_a = go.Figure(go.Bar(
        y=df_ag_asesor["ASESOR COMERCIAL"].str.title(), x=df_ag_asesor["Agendas"],
        orientation="h",
        marker=dict(color=TEAL, cornerradius=5),
        text=df_ag_asesor["Agendas"], textposition="auto",
        textfont=dict(color="#fff", size=11),
        hovertemplate="<b>%{y}</b><br>Agendas: %{x}<extra></extra>"
    ))
    style_fig(fig_ag_a, "Distribución de Agendas por Asesor", h=280)
    fig_ag_a.update_yaxes(showgrid=False)
    st.plotly_chart(fig_ag_a, use_container_width=True, config={'displayModeBar': False})

with col_ch2:
    df_ag_daily = df_agendas.groupby(df_agendas["Marca temporal"].dt.date).size().reset_index(name="Agendas")
    df_ag_daily = df_ag_daily.sort_values("Marca temporal")
    fig_ag_t = go.Figure(go.Scatter(
        x=df_ag_daily["Marca temporal"], y=df_ag_daily["Agendas"],
        mode="lines+markers",
        line=dict(color=CYAN, width=2.5, shape="spline"),
        marker=dict(size=5, color=CYAN, line=dict(color=SURFACE, width=1)),
        fill="tozeroy", fillcolor="rgba(0,178,169,0.05)",
        hovertemplate="<b>%{x|%d %b %Y}</b><br>Agendas: %{y}<extra></extra>"
    ))
    style_fig(fig_ag_t, "Tendencia Diaria de Agendas (Histórico)", h=280)
    fig_ag_t.update_layout(showlegend=False)
    st.plotly_chart(fig_ag_t, use_container_width=True, config={'displayModeBar': False})

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

with st.expander("Ver registro detallado de agendas"):
    ag_q = st.text_input("Buscar cliente, DNI o asesor:", placeholder="Escribe para filtrar...", key="s_ag")
    dfag = df_agendas.copy()
    if ag_q:
        q = ag_q.lower()
        dfag = dfag[
            dfag["NOMBRE DEL CLIENTE"].astype(str).str.lower().str.contains(q, na=False) |
            dfag["DNI"].astype(str).str.lower().str.contains(q, na=False) |
            dfag["ASESOR COMERCIAL"].astype(str).str.lower().str.contains(q, na=False)
        ]
    dag = dfag.rename(columns={
        "Marca temporal": "Registro", "ASESOR COMERCIAL": "Asesor",
        "NOMBRE DEL CLIENTE": "Cliente", "NUMERO DE TELEFONO": "Telefono",
        "CORREO ELECTRONICO": "Email", "COMENTARIO": "Comentario",
    })[["Registro", "Asesor", "Cliente", "DNI", "Telefono", "Email", "Comentario"]]
    dag["Registro"] = dag["Registro"].dt.strftime("%d/%m/%Y %H:%M")
    st.dataframe(dag, use_container_width=True, hide_index=True)
    st.download_button("Exportar Agendas", dag.to_csv(index=False).encode("utf-8"),
                        "agendas_crp.csv", "text/csv", key="dl_ag")



# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FOOTER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("---")
st.markdown(
    f"<div style='text-align:center;padding:8px 0 20px;font-size:12px;color:{MUTED}'>"
    f"Clinica Ricardo Palma &middot; Dashboard de Operaciones &middot; Mayo 2026<br>"
    f"Streamlit &amp; Plotly &middot; Datos actualizados al 18 de Mayo"
    f"</div>",
    unsafe_allow_html=True,
)
