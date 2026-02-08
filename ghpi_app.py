import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64
import requests
from datetime import timedelta # Χρήσιμο για μικρο-διορθώσεις στα όρια

# --- ΡΥΘΜΙΣΕΙΣ ΣΕΛΙΔΑΣ ---
st.set_page_config(
    page_title="Δείκτης Τιμών Ακινήτων Ελλάδας (GHPI)",
    page_icon="🏛️",
    layout="wide"
)

# --- CSS STYLE ---
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div.block-container { padding-top: 1rem; }

    .main-title { font-size: 2.8rem; color: var(--text-color); font-weight: 800; margin-bottom: 0; line-height: 1.2; }
    .subtitle { font-size: 1.5rem; color: #0088C3; font-weight: 600; margin-top: 5px; margin-bottom: 10px; }
    .intro { font-size: 1.1rem; color: var(--text-color); opacity: 0.8; margin-bottom: 30px; font-style: italic; margin-top: 20px; }
    
    .header-container { display: flex; flex-direction: row; align-items: center; justify-content: flex-start; }
    .logo-img { height: 110px; margin-right: 25px; align-self: center; }
    .title-container { display: flex; flex-direction: column; justify-content: center; text-align: left; }

    @media only screen and (max-width: 768px) {
        .header-container { flex-direction: column; align-items: center; text-align: center; margin-bottom: 20px; }
        .logo-img { height: 90px; margin-right: 0; margin-bottom: 15px; }
        .title-container { text-align: center; align-items: center; }
        .main-title { font-size: 1.8rem; }
        .subtitle { font-size: 1.1rem; }
        div.stRadio > div[role="radiogroup"] { justify-content: center !important; margin-bottom: 15px; }
    }
    
    div.stRadio > div[role="radiogroup"] { flex-direction: row; justify-content: flex-end; }
    
    .source-box { background-color: var(--secondary-background-color); padding: 15px; border-radius: 8px; border-left: 5px solid #003B71; margin-bottom: 10px; border: 1px solid rgba(128, 128, 128, 0.2); }
    
    .hero-container { background: linear-gradient(135deg, #003B71 0%, #001F3F 100%); color: white; padding: 40px; border-radius: 15px; text-align: center; margin-bottom: 40px; box-shadow: 0 4px 15px rgba(0, 59, 113, 0.3); border: 1px solid rgba(255,255,255,0.1); }
    .hero-title { font-size: 1.8rem; font-weight: 800; color: #ffffff; margin-bottom: 10px; }
    .hero-subtitle { font-size: 1.2rem; font-weight: 600; color: #0088C3; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 1px;}
    .hero-text { font-size: 1.1rem; line-height: 1.6; color: #e2e8f0; max-width: 800px; margin: 0 auto;}

    .service-card { background-color: var(--secondary-background-color); padding: 25px; border-radius: 12px; border: 1px solid rgba(128, 128, 128, 0.2); box-shadow: 0 4px 6px rgba(0,0,0,0.05); height: 100%; text-align: center; transition: transform 0.2s; }
    .service-card:hover { transform: translateY(-5px); box-shadow: 0 10px 15px rgba(0, 136, 195, 0.2); border-color: #0088C3; }
    .service-icon { font-size: 2.5rem; margin-bottom: 15px; }
    .service-title { font-size: 1.2rem; font-weight: 700; color: var(--text-color); margin-bottom: 10px; }
    .service-desc { font-size: 0.95rem; color: var(--text-color); opacity: 0.8; line-height: 1.5; }

    div[data-testid="stMetric"] { background-color: var(--secondary-background-color); border: 1px solid rgba(128, 128, 128, 0.2); padding: 15px; border-radius: 5px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    
    a { color: #0088C3; text-decoration: none; }
    a:hover { text-decoration: underline; }
</style>
""", unsafe_allow_html=True)

# --- LANGUAGE LOGIC ---
if 'lang_initialized' not in st.session_state:
    detected_index = 1 
    try:
        response = requests.get('http://ip-api.com/json/', timeout=2)
        if response.status_code == 200:
            data = response.json()
            if data.get('countryCode') == 'GR': detected_index = 0
            else: detected_index = 1
    except: pass
    st.session_state['lang_index'] = detected_index
    st.session_state['lang_initialized'] = True

top_col1, top_col2 = st.columns([4, 1])
with top_col2:
    lang_selection = st.radio("Language / Γλώσσα", ["🇬🇷 GR", "🇬🇧 EN"], index=st.session_state.get('lang_index', 1), horizontal=True, label_visibility="collapsed", key="lang_radio")

if lang_selection == "🇬🇷 GR":
    lang = 'el'
    st.session_state['lang_index'] = 0
else:
    lang = 'en'
    st.session_state['lang_index'] = 1

# --- CONTENTS ---
content = {
    'el': {
        'title': 'Δείκτης Τιμών Ακινήτων Ελλάδας (GHPI)',
        'subtitle': 'από Γιακουμάκης Ακίνητα',
        'intro_text': 'Ο επίσημος σύνθετος δείκτης για την πορεία της Ελληνικής Κτηματαγοράς.',
        'tab_data': '📊 GHPI & Στατιστικά',
        'tab_methodology': '📘 Μεθοδολογία',
        'tab_macro': '📈 Μακροοικονομικά',
        'tab_about': '🏢 Η Εταιρεία',
        
        # Stats & Charts
        'stat_current': 'Τρέχουσα Τιμή (2025)', 'stat_yoy': 'Ετήσια Μεταβολή (1Y)', 'stat_5y': 'Μεταβολή 5ετίας (5Y)', 'stat_ath': 'Ιστορικό Υψηλό (ATH)', 'ath_desc': 'από το peak του 2008',
        'chart_compare_title': 'Σύγκριση Πηγών: GHPI vs Επιμέρους Δείκτες', 'chart_yoy_title': 'Ετήσια Ποσοστιαία Μεταβολή (%)',
        'table_title': 'Συνοπτικός Πίνακας', 'col_year': 'Έτος', 'col_ghpi': 'Δείκτης GHPI', 'col_yoy': 'Ετήσια Μεταβολή',
        'full_table_title': 'Προβολή Πλήρων Δεδομένων (Όλοι οι Δείκτες)',
        
        # Macro Tab
        'macro_intro': 'Συγκριτική ανάλυση βασικών δεικτών της Ελληνικής Οικονομίας σε σχέση με την Κτηματαγορά.',
        'macro_c1_title': '1. Γενική Οικονομία: ΑΕΠ vs Χρηματιστήριο',
        'macro_c2_title': '2. Προσφορά & Ζήτηση: Άδειες vs Συναλλαγές',
        'macro_c3_title': '3. Ρευστότητα: Ξένες Επενδύσεις vs Στεγαστικά Δάνεια',
        'macro_c4_title': '4. Πληθωρισμός vs Ακίνητα (Real Returns)',
        'lbl_gdp': 'ΑΕΠ (Δις €)', 'lbl_inf': 'Πληθωρισμός (%)', 'lbl_ase': 'Γεν. Δείκτης ΧΑΑ', 'lbl_ghpi_yoy': 'Μεταβολή GHPI (%)',
        'lbl_permits': 'Οικοδ. Άδειες (χιλ.)', 'lbl_fdi': 'Ξένες Επενδύσεις (FDI - εκ. €)', 'lbl_mort': 'Νέα Στεγαστικά (εκ. €)', 'lbl_trans': 'Συναλλαγές (χιλ.)',
        'macro_table_title': 'Συγκεντρωτικός Πίνακας Μακροοικονομικών Δεικτών',

        # Methodology & About
        'method_title': 'Μεθοδολογία Υπολογισμού', 'method_intro': 'Ο δείκτης GHPI σταθμίζει τρεις κρίσιμους παράγοντες:', 'method_p1': '1. Τραπεζικές Εκτιμήσεις (50%)', 'method_p2': '2. Τάσεις Αγοράς (30%)', 'method_p3': '3. Κόστος Κατασκευής (20%)',
        'sources_title': '📚 Πηγές Δεδομένων', 'source_1': '🏦 **Τράπεζα της Ελλάδος:** Δείκτες Τιμών Οικιστικών Ακινήτων.', 'source_2': '📈 **Spitogatos Network:** Βάση δεδομένων ζητούμενων τιμών.', 'source_3': '🏗️ **ΕΛΣΤΑΤ:** Δείκτης Κόστους Υλικών Νέων Κτιρίων.',
        'hero_title': 'GIAKOUMAKIS REAL ESTATE', 'hero_subtitle': '50+ Χρόνια Εμπειρίας', 'hero_desc': 'Ολοκληρωμένες λύσεις ακινήτων από το 1970.',
        'services_main_title': 'Οι Υπηρεσίες μας', 's1_t': 'Real Estate', 's1_d': 'Πωλήσεις & Ενοικιάσεις.', 's2_t': 'Μελέτες', 's2_d': 'Τοπογραφικά & Αρχιτεκτονικά.', 's3_t': 'Κατασκευές', 's3_d': 'Πολυτελείς κατοικίες.', 's4_t': 'Management', 's4_d': 'Διοίκηση έργων.', 's5_t': 'Ενέργεια', 's5_d': 'Αναβαθμίσεις.', 's6_t': 'Business', 's6_d': 'Τουριστική εκμετάλλευση.', 'visit_button': 'Επισκεφθείτε το giakoumakis.gr', 'footer': '© 2025 Giakoumakis Real Estate.'
    },
    'en': {
        'title': 'Greece House Price Index (GHPI)',
        'subtitle': 'by Giakoumakis Real Estate',
        'intro_text': 'The official composite index tracking the Greek Real Estate Market.',
        'tab_data': '📊 GHPI & Stats',
        'tab_methodology': '📘 Methodology',
        'tab_macro': '📈 Macro Analysis',
        'tab_about': '🏢 About Us',
        
        # Stats & Charts
        'stat_current': 'Current Value (2025)', 'stat_yoy': '1-Year Change (YoY)', 'stat_5y': '5-Year Change', 'stat_ath': 'All-Time High (ATH)', 'ath_desc': 'from 2008 peak',
        'chart_compare_title': 'Source Comparison: GHPI vs Sub-Indices', 'chart_yoy_title': 'Annual Percentage Change (%)',
        'table_title': 'Summary Table', 'col_year': 'Year', 'col_ghpi': 'GHPI Value', 'col_yoy': 'YoY Change',
        'full_table_title': 'View Full Source Data (All Indices)',
        
        # Macro Tab
        'macro_intro': 'Comparative analysis of key Greek Economic indicators vs Real Estate market.',
        'macro_c1_title': '1. General Economy: GDP vs Stock Market',
        'macro_c2_title': '2. Supply & Demand: Permits vs Transactions',
        'macro_c3_title': '3. Liquidity: Foreign Investment (FDI) vs Mortgages',
        'macro_c4_title': '4. Inflation vs Real Estate (Real Returns)',
        'lbl_gdp': 'GDP (Billion €)', 'lbl_inf': 'Inflation (%)', 'lbl_ase': 'ASE Index', 'lbl_ghpi_yoy': 'GHPI Change (%)',
        'lbl_permits': 'Build. Permits (thous.)', 'lbl_fdi': 'FDI (Real Estate - M€)', 'lbl_mort': 'New Mortgages (M€)', 'lbl_trans': 'Transactions (thous.)',
        'macro_table_title': 'Consolidated Macroeconomic Data Table',

        # Methodology & About
        'method_title': 'Calculation Methodology', 'method_intro': 'The GHPI weights three critical factors:', 'method_p1': '1. Bank Valuations (50%)', 'method_p2': '2. Market Trends (30%)', 'method_p3': '3. Construction Cost (20%)',
        'sources_title': '📚 Data Sources', 'source_1': '🏦 **Bank of Greece:** Index of Apartment Prices.', 'source_2': '📈 **Spitogatos Network:** Asking prices database.', 'source_3': '🏗️ **ELSTAT:** Material Costs Index.',
        'hero_title': 'GIAKOUMAKIS REAL ESTATE', 'hero_subtitle': '50+ Years of Experience', 'hero_desc': 'Integrated real estate solutions since 1970.',
        'services_main_title': 'Our Services', 's1_t': 'Real Estate', 's1_d': 'Sales & Rentals.', 's2_t': 'Engineering', 's2_d': 'Topographical & Structural.', 's3_t': 'Construction', 's3_d': 'Luxury development.', 's4_t': 'Management', 's4_d': 'Project administration.', 's5_t': 'Energy', 's5_d': 'Efficiency solutions.', 's6_t': 'Business', 's6_d': 'Hospitality operations.', 'visit_button': 'Visit giakoumakis.gr', 'footer': '© 2025 Giakoumakis Real Estate.'
    }
}
text = content[lang]

# --- HEADER ---
with top_col1:
    logo_html = ""
    try:
        with open("logo.png", "rb") as f:
            encoded_img = base64.b64encode(f.read()).decode()
        logo_html = f'<img src="data:image/png;base64,{encoded_img}" class="logo-img">'
    except: pass
    st.markdown(f"""<div class="header-container">{logo_html}<div class="title-container"><div class="main-title">{text["title"]}</div><div class="subtitle">{text["subtitle"]}</div></div></div>""", unsafe_allow_html=True)

st.markdown(f'<div class="intro">{text["intro_text"]}</div>', unsafe_allow_html=True)

# --- DATA ENGINE (GHPI) ---
data = {
    'Year': list(range(2000, 2026)),
    'BoG_Index': [58, 66, 75, 80, 85, 92, 98, 102, 101, 97, 92, 87, 76, 68, 63, 60, 59.5, 59, 60, 64.5, 67, 72, 80, 91, 99.5, 105],
    'SPI_Index': [60, 68, 78, 85, 90, 96, 100, 105, 104, 100, 95, 90, 82, 75, 70, 68, 67, 66, 69, 75, 79, 85, 95, 109, 122, 134],
    'ELSTAT_Cost': [70, 72, 75, 78, 82, 86, 90, 93, 96, 98, 100, 101, 100, 98, 96, 95, 94, 95, 96, 97, 96.5, 100, 110, 118, 125, 129]
}
df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Year'], format='%Y')

df['GHPI'] = (df['BoG_Index'] * 0.50) + (df['SPI_Index'] * 0.30) + (df['ELSTAT_Cost'] * 0.20)
df['GHPI'] = df['GHPI'].round(1)
df['YoY_Change'] = df['GHPI'].pct_change() * 100

# --- DATA ENGINE (MACROECONOMIC) ---
macro_data = {
    'Year': list(range(2000, 2026)),
    'GDP_Billion': [141, 152, 163, 178, 193, 199, 217, 232, 242, 237, 226, 207, 191, 180, 178, 176, 174, 177, 180, 183, 165, 181, 206, 220, 235, 245],
    'Inflation': [3.2, 3.4, 3.6, 3.5, 2.9, 3.5, 3.2, 2.9, 4.2, 1.2, 4.7, 3.3, 1.5, -0.9, -1.3, -1.7, -0.8, 1.1, 0.6, 0.3, -1.2, 1.2, 9.6, 3.5, 2.9, 2.5],
    'ASE_Index': [3400, 2600, 1750, 2260, 2790, 3540, 4400, 5178, 1786, 2196, 1413, 680, 907, 1162, 826, 631, 643, 802, 613, 916, 809, 893, 929, 1293, 1420, 1510],
    'Permits_Thous': [75, 82, 85, 89, 82, 96, 88, 79, 65, 56, 48, 32, 25, 16, 13, 12, 12.5, 13, 15, 17, 19, 23, 25, 27, 29, 31],
    'FDI_RealEstate_M': [100, 150, 180, 250, 300, 450, 900, 1100, 950, 700, 300, 150, 100, 250, 400, 600, 800, 1100, 1300, 1450, 900, 1100, 1975, 2100, 2300, 2500],
    'Mortgages_New_M': [4500, 6000, 8500, 11000, 13500, 15000, 16000, 15500, 11000, 6000, 3500, 1500, 800, 500, 450, 400, 450, 500, 600, 750, 800, 1000, 1200, 1300, 1500, 1700],
    'Transactions_Thous': [150, 165, 170, 160, 155, 175, 160, 145, 110, 85, 70, 50, 40, 35, 30, 38, 45, 55, 65, 75, 60, 75, 85, 95, 100, 105]
}
df_macro = pd.DataFrame(macro_data)
df_macro['Date'] = pd.to_datetime(df_macro['Year'], format='%Y')
df_macro['GHPI_YoY'] = df['YoY_Change']

# Υπολογισμός ορίων για να κλειδώσουμε το zoom
min_date = df['Date'].min()
max_date = df['Date'].max()

# KPI Calcs
latest_val, prev_year_val = df['GHPI'].iloc[-1], df['GHPI'].iloc[-2]
yoy_pct, yoy_diff = df['YoY_Change'].iloc[-1], latest_val - prev_year_val
five_years_ago_val = df['GHPI'].iloc[-6]
five_y_pct, five_y_diff = ((latest_val - five_years_ago_val) / five_years_ago_val) * 100, latest_val - five_years_ago_val
ath_val = df['GHPI'].max()
diff_from_ath = latest_val - ath_val 

# --- COMMON CHART SETTINGS ---
common_xaxis = dict(
    type="date",
    range=[min_date, max_date], # Σκληρό όριο αρχικής προβολής (αποτρέπει το υπερβολικό zoom out αρχικά)
    rangeselector=dict(
        buttons=list([
            dict(count=5, label="5Y", step="year", stepmode="backward"),
            dict(count=10, label="10Y", step="year", stepmode="backward"),
            dict(step="all", label="MAX")
        ]),
        bgcolor='rgba(255, 255, 255, 0.9)',
        x=1, # ΤΕΡΜΑ ΔΕΞΙΑ
        y=1.2,
        xanchor='right' # ΕΥΘΥΓΡΑΜΜΙΣΗ ΔΕΞΙΑ
    )
)

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs([f"{text['tab_data']}", f"{text['tab_methodology']}", f"{text['tab_macro']}", f"{text['tab_about']}"])

# === TAB 1: DATA & CHARTS ===
with tab1:
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1: st.metric(label=text['stat_current'], value=f"{latest_val}", delta=None)
    with kpi2: st.metric(label=text['stat_yoy'], value=f"{yoy_pct:.1f}%", delta=f"{yoy_diff:.1f}")
    with kpi3: st.metric(label=text['stat_5y'], value=f"{five_y_pct:.1f}%", delta=f"{five_y_diff:.1f}")
    with kpi4: st.metric(label=text['stat_ath'], value=f"{ath_val}", delta=f"{diff_from_ath:.1f}", delta_color="normal")
    st.caption(f"* {text['stat_ath']}: {text['ath_desc']}")
    st.divider()

    st.subheader(text['chart_compare_title'])
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Scatter(x=df['Date'], y=df['BoG_Index'], name='Bank of Greece', line=dict(dash='dot', width=1.5, color='#0088C3'))) 
    fig_comp.add_trace(go.Scatter(x=df['Date'], y=df['SPI_Index'], name='Market Prices', line=dict(dash='dot', width=1.5, color='#EF4444'))) 
    fig_comp.add_trace(go.Scatter(x=df['Date'], y=df['ELSTAT_Cost'], name='Construction Cost', line=dict(dash='dot', width=1.5, color='#10B981'))) 
    fig_comp.add_trace(go.Scatter(x=df['Date'], y=df['GHPI'], name='GHPI', line=dict(color='#003B71', width=4))) 
    
    fig_comp.update_layout(
        hovermode="x unified", 
        height=450, 
        legend=dict(orientation="h", y=1.2), 
        margin=dict(l=20, r=20, t=20, b=20), 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', 
        font=dict(color=None),
        dragmode='pan',
        xaxis=common_xaxis # Εφαρμογή των ρυθμίσεων (δεξιά κουμπιά + όρια)
    )
    st.plotly_chart(fig_comp, use_container_width=True, config={'displayModeBar': False, 'scrollZoom': True})

    st.subheader(text['chart_yoy_title'])
    colors = ['#EF4444' if x < 0 else '#10B981' for x in df['YoY_Change']]
    fig_bar = go.Figure(go.Bar(x=df['Date'], y=df['YoY_Change'], marker_color=colors, text=df['YoY_Change'].apply(lambda x: f'{x:.1f}%' if pd.notnull(x) else ''), textposition='outside'))
    fig_bar.update_layout(
        height=350, 
        showlegend=False, 
        margin=dict(l=20, r=20, t=20, b=20), 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', 
        font=dict(color=None),
        dragmode='pan',
        xaxis=common_xaxis
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False, 'scrollZoom': True})
    
    st.divider()
    st.subheader(text['table_title'])
    table_df = df[['Year', 'GHPI', 'YoY_Change']].sort_values(by='Year', ascending=False)
    st.dataframe(table_df, column_config={"Year": st.column_config.NumberColumn(text['col_year'], format="%d"), "GHPI": st.column_config.NumberColumn(text['col_ghpi'], format="%.1f"), "YoY_Change": st.column_config.NumberColumn(text['col_yoy'], format="%.1f%%")}, use_container_width=True, hide_index=True, height=400)
    
    with st.expander(f"📂 {text['full_table_title']}"):
        full_df_display = df.sort_values(by='Year', ascending=False)
        st.dataframe(
            full_df_display,
            column_config={
                "Year": st.column_config.NumberColumn("Year / Έτος", format="%d"),
                "BoG_Index": st.column_config.NumberColumn("Bank of Greece", format="%.1f"),
                "SPI_Index": st.column_config.NumberColumn("Market Prices", format="%.1f"),
                "ELSTAT_Cost": st.column_config.NumberColumn("Constr. Cost", format="%.1f"),
                "GHPI": st.column_config.NumberColumn("GHPI", format="%.1f"),
                "YoY_Change": st.column_config.NumberColumn("YoY %", format="%.1f%%")
            },
            use_container_width=True,
            hide_index=True
        )

# === TAB 2: METHODOLOGY ===
with tab2:
    st.header(text['method_title'])
    st.markdown(text['method_intro'])
    c1, c2, c3 = st.columns(3)
    c1.info(f"**{text['method_p1']}**")
    c2.warning(f"**{text['method_p2']}**")
    c3.success(f"**{text['method_p3']}**")
    st.markdown("### The Formula")
    st.latex(r'''GHPI_t = (0.5 \times I_{Bank}) + (0.3 \times I_{Market}) + (0.2 \times I_{Cost})''')
    st.divider()
    st.subheader(text['sources_title'])
    st.markdown(f"""<div class="source-box">{text['source_1']}<br><br>{text['source_2']}<br><br>{text['source_3']}</div>""", unsafe_allow_html=True)

# === TAB 3: MACROECONOMIC ANALYSIS ===
with tab3:
    st.header(f"📊 {text['tab_macro']}")
    st.markdown(f"*{text['macro_intro']}*")
    
    # --- CHART 1 ---
    st.subheader(text['macro_c1_title'])
    fig_macro1 = make_subplots(specs=[[{"secondary_y": True}]])
    fig_macro1.add_trace(go.Bar(x=df_macro['Date'], y=df_macro['GDP_Billion'], name=text['lbl_gdp'], marker_color='#003B71', opacity=0.7), secondary_y=False)
    fig_macro1.add_trace(go.Scatter(x=df_macro['Date'], y=df_macro['ASE_Index'], name=text['lbl_ase'], line=dict(color='#FFA500', width=3)), secondary_y=True)
    fig_macro1.update_layout(
        height=400, hovermode="x unified", legend=dict(orientation="h", y=1.2), 
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color=None),
        dragmode='pan', xaxis=common_xaxis
    )
    fig_macro1.update_yaxes(title_text="GDP (€ Bn)", secondary_y=False)
    fig_macro1.update_yaxes(title_text="ASE Index Points", secondary_y=True)
    st.plotly_chart(fig_macro1, use_container_width=True, config={'displayModeBar': False, 'scrollZoom': True})
    
    st.divider()

    # --- CHART 2 ---
    st.subheader(text['macro_c2_title'])
    fig_macro_act = go.Figure()
    fig_macro_act.add_trace(go.Bar(x=df_macro['Date'], y=df_macro['Transactions_Thous'], name=text['lbl_trans'], marker_color='#60A5FA', opacity=0.6))
    fig_macro_act.add_trace(go.Scatter(x=df_macro['Date'], y=df_macro['Permits_Thous'], name=text['lbl_permits'], line=dict(color='#0088C3', width=3)))
    fig_macro_act.update_layout(
        height=400, hovermode="x unified", legend=dict(orientation="h", y=1.2), 
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color=None), 
        yaxis_title="Units (Thousands)",
        dragmode='pan', xaxis=common_xaxis
    )
    st.plotly_chart(fig_macro_act, use_container_width=True, config={'displayModeBar': False, 'scrollZoom': True})

    st.divider()

    # --- CHART 3 ---
    st.subheader(text['macro_c3_title'])
    fig_macro_liq = go.Figure()
    fig_macro_liq.add_trace(go.Bar(x=df_macro['Date'], y=df_macro['FDI_RealEstate_M'], name=text['lbl_fdi'], marker_color='#059669', opacity=0.7))
    fig_macro_liq.add_trace(go.Scatter(x=df_macro['Date'], y=df_macro['Mortgages_New_M'], name=text['lbl_mort'], line=dict(color='#F43F5E', width=3)))
    fig_macro_liq.update_layout(
        height=400, hovermode="x unified", legend=dict(orientation="h", y=1.2), 
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color=None), 
        yaxis_title="Amount (Million €)",
        dragmode='pan', xaxis=common_xaxis
    )
    st.plotly_chart(fig_macro_liq, use_container_width=True, config={'displayModeBar': False, 'scrollZoom': True})
    
    st.divider()

    # --- CHART 4 ---
    st.subheader(text['macro_c4_title'])
    fig_macro2 = go.Figure()
    fig_macro2.add_trace(go.Scatter(x=df_macro['Date'], y=df_macro['Inflation'], name=text['lbl_inf'], line=dict(color='#EF4444', width=2, dash='dot')))
    fig_macro2.add_trace(go.Bar(x=df_macro['Date'], y=df_macro['GHPI_YoY'], name=text['lbl_ghpi_yoy'], marker_color='#10B981', opacity=0.8))
    fig_macro2.update_layout(
        height=400, hovermode="x unified", legend=dict(orientation="h", y=1.2), 
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color=None), 
        yaxis_title="Percentage (%)",
        dragmode='pan', xaxis=common_xaxis
    )
    st.plotly_chart(fig_macro2, use_container_width=True, config={'displayModeBar': False, 'scrollZoom': True})

    # --- TABLE ---
    with st.expander(f"📂 {text['macro_table_title']}", expanded=False):
        macro_display = df_macro.drop(columns=['Date']).sort_values(by='Year', ascending=False)
        st.dataframe(
            macro_display,
            column_config={
                "Year": st.column_config.NumberColumn(text['col_year'], format="%d"),
                "GDP_Billion": st.column_config.NumberColumn("GDP (€Bn)", format="€ %.0f B"),
                "Inflation": st.column_config.NumberColumn("Inflation", format="%.1f%%"),
                "ASE_Index": st.column_config.NumberColumn("ASE", format="%d"),
                "Transactions_Thous": st.column_config.NumberColumn("Trans.", format="%.0f k"),
                "Permits_Thous": st.column_config.NumberColumn("Permits", format="%.1f k"),
                "FDI_RealEstate_M": st.column_config.NumberColumn("FDI (RE)", format="€ %.0f M"),
                "Mortgages_New_M": st.column_config.NumberColumn("Mortgages", format="€ %.0f M"),
            },
            use_container_width=True,
            hide_index=True
        )

# === TAB 4: ABOUT US ===
with tab4:
    st.markdown(f"""<div class="hero-container"><div class="hero-title">{text['hero_title']}</div><div class="hero-subtitle">{text['hero_subtitle']}</div><div class="hero-text">{text['hero_desc']}</div></div>""", unsafe_allow_html=True)
    st.subheader(text['services_main_title'])
    col1, col2, col3 = st.columns(3)
    with col1: st.markdown(f"""<div class="service-card"><div class="service-icon">🏡</div><div class="service-title">{text['s1_t']}</div><div class="service-desc">{text['s1_d']}</div></div>""", unsafe_allow_html=True)
    with col2: st.markdown(f"""<div class="service-card"><div class="service-icon">📐</div><div class="service-title">{text['s2_t']}</div><div class="service-desc">{text['s2_d']}</div></div>""", unsafe_allow_html=True)
    with col3: st.markdown(f"""<div class="service-card"><div class="service-icon">🏗️</div><div class="service-title">{text['s3_t']}</div><div class="service-desc">{text['s3_d']}</div></div>""", unsafe_allow_html=True)
    st.write("") 
    col4, col5, col6 = st.columns(3)
    with col4: st.markdown(f"""<div class="service-card"><div class="service-icon">🤝</div><div class="service-title">{text['s4_t']}</div><div class="service-desc">{text['s4_d']}</div></div>""", unsafe_allow_html=True)
    with col5: st.markdown(f"""<div class="service-card"><div class="service-icon">⚡</div><div class="service-title">{text['s5_t']}</div><div class="service-desc">{text['s5_d']}</div></div>""", unsafe_allow_html=True)
    with col6: st.markdown(f"""<div class="service-card"><div class="service-icon">🏨</div><div class="service-title">{text['s6_t']}</div><div class="service-desc">{text['s6_d']}</div></div>""", unsafe_allow_html=True)
    st.divider()
    st.markdown(f"""<div style="text-align: center; margin-top: 30px;"><a href="https://www.giakoumakis.gr" target="_blank" style="background-color: #0088C3; color: white; padding: 16px 40px; text-align: center; text-decoration: none; display: inline-block; font-size: 18px; border-radius: 50px; font-weight: bold; box-shadow: 0 4px 15px rgba(0, 136, 195, 0.4); transition: all 0.3s ease;">{text['visit_button']} 🌐</a></div>""", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.markdown(f"<div style='text-align: center; color: grey; font-size: 0.8rem;'>{text['footer']}</div>", unsafe_allow_html=True)
