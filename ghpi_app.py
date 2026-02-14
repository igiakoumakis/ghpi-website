import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64
import requests

# --- 1. ΡΥΘΜΙΣΕΙΣ ΣΕΛΙΔΑΣ (ΠΡΕΠΕΙ ΝΑ ΕΙΝΑΙ ΠΡΩΤΟ) ---
st.set_page_config(
    page_title="Δείκτης Τιμών Ακινήτων Ελλάδας (GHPI)",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. META TAGS ΓΙΑ SOCIAL MEDIA (WHATSAPP, FACEBOOK, LINKEDIN) ---
# ΣΗΜΑΝΤΙΚΟ: Βάλε εδώ το RAW Link του λογοτύπου σου από το GitHub ή άλλο site
LOGO_URL = "https://github.com/igiakoumakis/ghpi-website/blob/main/logo.png?raw=true" 
# Αν δεν έχεις το link πρόχειρο, άσε αυτό το placeholder, αλλά δεν θα δείχνει εικόνα στο WhatsApp.

meta_tags = f"""
<head>
    <meta property="og:title" content="Δείκτης Τιμών Ακινήτων Ελλάδας (GHPI)">
    <meta property="og:description" content="Η επίσημη πορεία της Ελληνικής Κτηματαγοράς. Στατιστικά, Μακροοικονομικά και Αναλύσεις από την Giakoumakis Real Estate.">
    <meta property="og:image" content="{LOGO_URL}">
    <meta property="og:url" content="https://www.ghpi.gr">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary_large_image">
</head>
"""
st.markdown(meta_tags, unsafe_allow_html=True)

# --- 3. CSS STYLE ---
st.markdown("""
<style>
    /* Απόκρυψη στοιχείων Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div.block-container { padding-top: 1rem; }

    /* Τυπογραφία */
    .main-title { font-size: 2.5rem; color: #1f2937; font-weight: 800; margin-bottom: 0; line-height: 1.2; }
    .subtitle { font-size: 1.4rem; color: #0088C3; font-weight: 600; margin-top: 5px; margin-bottom: 10px; }
    .intro { font-size: 1.1rem; color: #4b5563; margin-bottom: 30px; font-style: italic; margin-top: 20px; }
    
    /* Header Layout */
    .header-container { display: flex; flex-direction: row; align-items: center; justify-content: flex-start; }
    .logo-img { height: 100px; margin-right: 25px; align-self: center; }
    
    /* Mobile Header */
    @media only screen and (max-width: 768px) {
        .header-container { flex-direction: column; align-items: center; text-align: center; margin-bottom: 20px; }
        .logo-img { height: 80px; margin-right: 0; margin-bottom: 15px; }
        .main-title { font-size: 1.8rem; }
        .subtitle { font-size: 1.1rem; }
    }
    
    /* Boxes & Cards */
    .source-box { background-color: #f8fafc; padding: 15px; border-radius: 8px; border-left: 5px solid #003B71; margin-bottom: 10px; border: 1px solid #e2e8f0; }
    .hero-container { background: linear-gradient(135deg, #003B71 0%, #001F3F 100%); color: white; padding: 30px; border-radius: 12px; text-align: center; margin-bottom: 40px; box-shadow: 0 4px 15px rgba(0, 59, 113, 0.3); }
    .service-card { background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #e2e8f0; box-shadow: 0 2px 4px rgba(0,0,0,0.05); height: 100%; text-align: center; transition: transform 0.2s; }
    .service-card:hover { transform: translateY(-3px); border-color: #0088C3; }
    
    /* Metrics */
    div[data-testid="stMetric"] { background-color: white; border: 1px solid #e2e8f0; padding: 15px; border-radius: 8px; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
</style>
""", unsafe_allow_html=True)

# --- 4. LANGUAGE LOGIC ---
if 'lang_initialized' not in st.session_state:
    st.session_state['lang_index'] = 0 # Default Greek
    st.session_state['lang_initialized'] = True

col_h1, col_h2 = st.columns([4, 1])
with col_h2:
    lang_sel = st.radio("Language", ["🇬🇷 GR", "🇬🇧 EN"], index=st.session_state['lang_index'], horizontal=True, label_visibility="collapsed")

lang = 'el' if lang_sel == "🇬🇷 GR" else 'en'
st.session_state['lang_index'] = 0 if lang == 'el' else 1

# --- 5. CONTENT DICTIONARY ---
content = {
    'el': {
        'title': 'Δείκτης Τιμών Ακινήτων Ελλάδας (GHPI)',
        'subtitle': 'από Γιακουμάκης Ακίνητα',
        'intro': 'Ο επίσημος σύνθετος δείκτης για την πορεία της Ελληνικής Κτηματαγοράς.',
        'tabs': ['📊 GHPI & Στατιστικά', '📘 Μεθοδολογία', '📈 Μακροοικονομικά', '🏢 Η Εταιρεία'],
        'kpi': ['Τρέχουσα Τιμή (2025)', 'Ετήσια Μεταβολή (1Y)', 'Μεταβολή 5ετίας (5Y)', 'Ιστορικό Υψηλό'],
        'charts': ['Σύγκριση Πηγών: GHPI vs Επιμέρους Δείκτες', 'Ετήσια Ποσοστιαία Μεταβολή (%)'],
        'table': ['Έτος', 'Δείκτης GHPI', 'Ετήσια Μεταβολή'],
        'full_table': 'Προβολή Πλήρων Δεδομένων (Όλοι οι Δείκτες)',
        'macro': {
            'intro': 'Συγκριτική ανάλυση βασικών δεικτών της Ελληνικής Οικονομίας σε σχέση με την Κτηματαγορά.',
            'titles': ['1. Γενική Οικονομία: ΑΕΠ vs Χρηματιστήριο', '2. Προσφορά & Ζήτηση: Άδειες vs Συναλλαγές', '3. Ρευστότητα: Ξένες Επενδύσεις vs Στεγαστικά', '4. Πληθωρισμός vs Ακίνητα'],
            'labels': ['ΑΕΠ (€ Δις)', 'Πληθωρισμός (%)', 'Δείκτης ΧΑΑ', 'GHPI Μεταβολή (%)', 'Οικοδ. Άδειες (χιλ.)', 'Ξένες Επενδύσεις (εκ. €)', 'Νέα Στεγαστικά (εκ. €)', 'Συναλλαγές (χιλ.)'],
            'table_t': 'Συγκεντρωτικός Πίνακας Μακροοικονομικών'
        },
        'method': {
            't': 'Αναλυτική Μεθοδολογία & Σκεπτικό',
            's1': 'Ο GHPI συνθέτει δεδομένα από τρεις διαφορετικές πηγές για να προσφέρει μια ολιστική εικόνα της αγοράς.',
            's2': 'Η Φόρμουλα: GHPI = (0.5 x Τράπεζες) + (0.3 x Αγορά) + (0.2 x Κόστος)',
            'src': ['1. Τραπεζικές Εκτιμήσεις (BoG)', 'Επίσημος δείκτης. Υψηλή αξιοπιστία, αλλά συντηρητικός.', '2. Ζητούμενες Τιμές (Market)', 'Άμεση αποτύπωση τάσης, αλλά περιέχει "καπέλο" διαπραγμάτευσης.', '3. Κόστος Κατασκευής (ELSTAT)', 'Αντικειμενικό δεδομένο κόστους αντικατάστασης.'],
            'links': 'Πηγές Δεδομένων: Τράπεζα της Ελλάδος, Spitogatos Network, ΕΛΣΤΑΤ.'
        },
        'about': {
            'hero_t': 'GIAKOUMAKIS REAL ESTATE', 'hero_s': '50+ Χρόνια Εμπειρίας', 'hero_d': 'Ολοκληρωμένες λύσεις ακινήτων από το 1970.',
            'srv': ['Real Estate', 'Πωλήσεις & Ενοικιάσεις', 'Μελέτες', 'Τοπογραφικά & Στατικά', 'Κατασκευές', 'Πολυτελείς κατοικίες', 'Management', 'Διοίκηση έργων', 'Ενέργεια', 'Αναβαθμίσεις', 'Business', 'Τουριστική εκμετάλλευση'],
            'btn': 'Επισκεφθείτε το giakoumakis.gr', 'foot': '© 2025 Giakoumakis Real Estate.'
        }
    },
    'en': {
        'title': 'Greece House Price Index (GHPI)',
        'subtitle': 'by Giakoumakis Real Estate',
        'intro': 'The official composite index tracking the Greek Real Estate Market.',
        'tabs': ['📊 GHPI & Stats', '📘 Methodology', '📈 Macro Analysis', '🏢 About Us'],
        'kpi': ['Current Value (2025)', '1-Year Change (YoY)', '5-Year Change', 'All-Time High'],
        'charts': ['Source Comparison: GHPI vs Sub-Indices', 'Annual Percentage Change (%)'],
        'table': ['Year', 'GHPI Value', 'YoY Change'],
        'full_table': 'View Full Source Data (All Indices)',
        'macro': {
            'intro': 'Comparative analysis of key Greek Economic indicators vs Real Estate market.',
            'titles': ['1. Economy: GDP vs Stock Market', '2. Supply & Demand: Permits vs Transactions', '3. Liquidity: FDI vs Mortgages', '4. Inflation vs Real Estate'],
            'labels': ['GDP (€ Bn)', 'Inflation (%)', 'ASE Index', 'GHPI Change (%)', 'Build. Permits (k)', 'FDI (Real Estate €M)', 'New Mortgages (€M)', 'Transactions (k)'],
            'table_t': 'Consolidated Macroeconomic Data Table'
        },
        'method': {
            't': 'Detailed Methodology',
            's1': 'GHPI synthesizes data from three sources to provide a holistic market view.',
            's2': 'Formula: GHPI = (0.5 x Banks) + (0.3 x Market) + (0.2 x Cost)',
            'src': ['1. Bank Valuations (BoG)', 'Official index. Reliable but conservative.', '2. Asking Prices (Market)', 'Fast sentiment check but includes premiums.', '3. Construction Cost (ELSTAT)', 'Objective replacement cost data.'],
            'links': 'Data Sources: Bank of Greece, Spitogatos Network, ELSTAT.'
        },
        'about': {
            'hero_t': 'GIAKOUMAKIS REAL ESTATE', 'hero_s': '50+ Years of Experience', 'hero_d': 'Integrated real estate solutions since 1970.',
            'srv': ['Real Estate', 'Sales & Rentals', 'Engineering', 'Topographical & Structural', 'Construction', 'Luxury development', 'Management', 'Project administration', 'Energy', 'Efficiency solutions', 'Business', 'Hospitality operations'],
            'btn': 'Visit giakoumakis.gr', 'foot': '© 2025 Giakoumakis Real Estate.'
        }
    }
}
t = content[lang]

# --- 6. DISPLAY HEADER ---
with col_h1:
    logo_html = ""
    try:
        with open("logo.png", "rb") as f:
            encoded_img = base64.b64encode(f.read()).decode()
        logo_html = f'<img src="data:image/png;base64,{encoded_img}" class="logo-img">'
    except: pass
    st.markdown(f"""<div class="header-container">{logo_html}<div class="title-container"><div class="main-title">{t["title"]}</div><div class="subtitle">{t["subtitle"]}</div></div></div>""", unsafe_allow_html=True)

st.markdown(f'<div class="intro">{t["intro"]}</div>', unsafe_allow_html=True)

# --- 7. DATA ENGINE ---
# GHPI Data
data = {
    'Year': list(range(2000, 2026)),
    'BoG_Index': [58, 66, 75, 80, 85, 92, 98, 102, 101, 97, 92, 87, 76, 68, 63, 60, 59.5, 59, 60, 64.5, 67, 72, 80, 91, 99.5, 105],
    'SPI_Index': [60, 68, 78, 85, 90, 96, 100, 105, 104, 100, 95, 90, 82, 75, 70, 68, 67, 66, 69, 75, 79, 85, 95, 109, 122, 134],
    'ELSTAT_Cost': [70, 72, 75, 78, 82, 86, 90, 93, 96, 98, 100, 101, 100, 98, 96, 95, 94, 95, 96, 97, 96.5, 100, 110, 118, 125, 129]
}
df = pd.DataFrame(data)
df['GHPI'] = (df['BoG_Index'] * 0.50) + (df['SPI_Index'] * 0.30) + (df['ELSTAT_Cost'] * 0.20)
df['GHPI'] = df['GHPI'].round(1)
df['YoY_Change'] = df['GHPI'].pct_change() * 100

# Macro Data
macro_data = {
    'Year': list(range(2000, 2026)),
    'GDP': [141, 152, 163, 178, 193, 199, 217, 232, 242, 237, 226, 207, 191, 180, 178, 176, 174, 177, 180, 183, 165, 181, 206, 220, 235, 245],
    'Inflation': [3.2, 3.4, 3.6, 3.5, 2.9, 3.5, 3.2, 2.9, 4.2, 1.2, 4.7, 3.3, 1.5, -0.9, -1.3, -1.7, -0.8, 1.1, 0.6, 0.3, -1.2, 1.2, 9.6, 3.5, 2.9, 2.5],
    'ASE': [3400, 2600, 1750, 2260, 2790, 3540, 4400, 5178, 1786, 2196, 1413, 680, 907, 1162, 826, 631, 643, 802, 613, 916, 809, 893, 929, 1293, 1420, 1510],
    'Permits': [75, 82, 85, 89, 82, 96, 88, 79, 65, 56, 48, 32, 25, 16, 13, 12, 12.5, 13, 15, 17, 19, 23, 25, 27, 29, 31],
    'FDI': [100, 150, 180, 250, 300, 450, 900, 1100, 950, 700, 300, 150, 100, 250, 400, 600, 800, 1100, 1300, 1450, 900, 1100, 1975, 2100, 2300, 2500],
    'Mortgages': [4500, 6000, 8500, 11000, 13500, 15000, 16000, 15500, 11000, 6000, 3500, 1500, 800, 500, 450, 400, 450, 500, 600, 750, 800, 1000, 1200, 1300, 1500, 1700],
    'Transactions': [150, 165, 170, 160, 155, 175, 160, 145, 110, 85, 70, 50, 40, 35, 30, 38, 45, 55, 65, 75, 60, 75, 85, 95, 100, 105]
}
df_m = pd.DataFrame(macro_data)

# KPI Calcs
cur_val = df['GHPI'].iloc[-1]
yoy_val = df['YoY_Change'].iloc[-1]
yoy_diff = cur_val - df['GHPI'].iloc[-2]
five_y_val = ((cur_val - df['GHPI'].iloc[-6]) / df['GHPI'].iloc[-6]) * 100
five_y_diff = cur_val - df['GHPI'].iloc[-6]
ath = df['GHPI'].max()

# --- 8. TABS ---
tab1, tab2, tab3, tab4 = st.tabs(t['tabs'])

# === TAB 1: DATA ===
with tab1:
    k1, k2, k3, k4 = st.columns(4)
    k1.metric(t['kpi'][0], f"{cur_val}")
    k2.metric(t['kpi'][1], f"{yoy_val:.1f}%", f"{yoy_diff:.1f}")
    k3.metric(t['kpi'][2], f"{five_y_val:.1f}%", f"{five_y_diff:.1f}")
    k4.metric(t['kpi'][3], f"{ath}", f"{cur_val-ath:.1f}")
    st.divider()

    st.subheader(t['charts'][0])
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Scatter(x=df['Year'], y=df['BoG_Index'], name='BoG', line=dict(dash='dot', width=1.5, color='#0088C3')))
    fig_comp.add_trace(go.Scatter(x=df['Year'], y=df['SPI_Index'], name='Market', line=dict(dash='dot', width=1.5, color='#EF4444')))
    fig_comp.add_trace(go.Scatter(x=df['Year'], y=df['ELSTAT_Cost'], name='Cost', line=dict(dash='dot', width=1.5, color='#10B981')))
    fig_comp.add_trace(go.Scatter(x=df['Year'], y=df['GHPI'], name='GHPI', line=dict(color='#003B71', width=4)))
    fig_comp.update_layout(hovermode="x unified", height=450, margin=dict(l=20,r=20,t=20,b=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_comp, use_container_width=True)

    st.subheader(t['charts'][1])
    colors = ['#EF4444' if x < 0 else '#10B981' for x in df['YoY_Change']]
    fig_bar = go.Figure(go.Bar(x=df['Year'], y=df['YoY_Change'], marker_color=colors))
    fig_bar.update_layout(height=350, margin=dict(l=20,r=20,t=20,b=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_bar, use_container_width=True)

    with st.expander(t['full_table']):
        st.dataframe(df.sort_values(by='Year', ascending=False), use_container_width=True, hide_index=True)

# === TAB 2: METHODOLOGY ===
with tab2:
    st.header(t['method']['t'])
    st.info(t['method']['s1'])
    st.latex(r'''GHPI_t = (0.5 \times I_{Bank}) + (0.3 \times I_{Market}) + (0.2 \times I_{Cost})''')
    
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"#### {t['method']['src'][0]}")
    c1.success(t['method']['src'][1])
    c2.markdown(f"#### {t['method']['src'][2]}")
    c2.warning(t['method']['src'][3])
    c3.markdown(f"#### {t['method']['src'][4]}")
    c3.info(t['method']['src'][5])
    
    st.markdown("---")
    st.caption(t['method']['links'])

# === TAB 3: MACRO ===
with tab3:
    st.header(t['tabs'][2])
    st.markdown(f"*{t['macro']['intro']}*")

    # Chart 1
    st.subheader(t['macro']['titles'][0])
    f1 = make_subplots(specs=[[{"secondary_y": True}]])
    f1.add_trace(go.Bar(x=df_m['Year'], y=df_m['GDP'], name=t['macro']['labels'][0], marker_color='#003B71', opacity=0.7), secondary_y=False)
    f1.add_trace(go.Scatter(x=df_m['Year'], y=df_m['ASE'], name=t['macro']['labels'][2], line=dict(color='#FFA500', width=3)), secondary_y=True)
    f1.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(f1, use_container_width=True)

    # Chart 2
    st.subheader(t['macro']['titles'][1])
    f2 = go.Figure()
    f2.add_trace(go.Bar(x=df_m['Year'], y=df_m['Transactions'], name=t['macro']['labels'][7], marker_color='#60A5FA'))
    f2.add_trace(go.Scatter(x=df_m['Year'], y=df_m['Permits'], name=t['macro']['labels'][4], line=dict(color='#0088C3', width=3)))
    f2.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(f2, use_container_width=True)

    # Chart 3
    st.subheader(t['macro']['titles'][2])
    f3 = go.Figure()
    f3.add_trace(go.Bar(x=df_m['Year'], y=df_m['FDI'], name=t['macro']['labels'][5], marker_color='#059669'))
    f3.add_trace(go.Scatter(x=df_m['Year'], y=df_m['Mortgages'], name=t['macro']['labels'][6], line=dict(color='#F43F5E', width=3)))
    f3.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(f3, use_container_width=True)
    
    # Chart 4
    st.subheader(t['macro']['titles'][3])
    f4 = go.Figure()
    f4.add_trace(go.Scatter(x=df_m['Year'], y=df_m['Inflation'], name=t['macro']['labels'][1], line=dict(color='#EF4444', dash='dot')))
    f4.add_trace(go.Bar(x=df['Year'], y=df['YoY_Change'], name=t['macro']['labels'][3], marker_color='#10B981'))
    f4.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(f4, use_container_width=True)
    
    with st.expander(t['macro']['table_t']):
        st.dataframe(df_m.sort_values(by='Year', ascending=False), use_container_width=True, hide_index=True)

# === TAB 4: ABOUT ===
with tab4:
    st.markdown(f"""<div class="hero-container"><div class="hero-title">{t['about']['hero_t']}</div><div class="hero-subtitle">{t['about']['hero_s']}</div><div class="hero-text">{t['about']['hero_d']}</div></div>""", unsafe_allow_html=True)
    
    cols = st.columns(3) + st.columns(3)
    icons = ["🏡", "📐", "🏗️", "🤝", "⚡", "🏨"]
    for i, col in enumerate(cols):
        col.markdown(f"""<div class="service-card"><div class="service-icon">{icons[i]}</div><div class="service-title">{t['about']['srv'][i*2]}</div><div class="service-desc">{t['about']['srv'][i*2+1]}</div></div>""", unsafe_allow_html=True)
        
    st.markdown(f"""<div style="text-align: center; margin-top: 30px;"><a href="https://www.giakoumakis.gr" target="_blank" style="background-color: #0088C3; color: white; padding: 16px 40px; text-decoration: none; border-radius: 50px; font-weight: bold;">{t['about']['btn']} 🌐</a></div>""", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.markdown(f"<div style='text-align: center; color: grey;'>{t['about']['foot']}</div>", unsafe_allow_html=True)
