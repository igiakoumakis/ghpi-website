import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# --- ΡΥΘΜΙΣΕΙΣ ΣΕΛΙΔΑΣ ---
st.set_page_config(
    page_title="Greece House Price Index (GHPI)",
    page_icon="🏛️",
    layout="wide"
)

# --- ΛΕΞΙΚΟ ΜΕΤΑΦΡΑΣΕΩΝ ---
content = {
    'el': {
        'sidebar_lang': 'Γλώσσα / Language',
        'title': 'Greece House Price Index (GHPI)',
        'subtitle': 'by Giakoumakis Real Estate',
        'intro_text': 'Ο επίσημος σύνθετος δείκτης για την πορεία της Ελληνικής Κτηματαγοράς.',
        'tab_data': '📊 Δεδομένα & Τάσεις',
        'tab_methodology': '📘 Μεθοδολογία & Πηγές',
        'chart_compare_title': 'Σύγκριση Πηγών: GHPI vs Επιμέρους Δείκτες',
        'chart_yoy_title': 'Ετήσια Ποσοστιαία Μεταβολή (%)',
        'kpi_current': 'Τρέχουσα Τιμή GHPI (2025)',
        'method_title': 'Μεθοδολογία Υπολογισμού',
        'method_intro': """
            Ο δείκτης **GHPI** σχεδιάστηκε από την **Giakoumakis Real Estate** για να προσφέρει μια 
            ολιστική εικόνα της αγοράς, σταθμίζοντας τρεις κρίσιμους παράγοντες:
        """,
        'method_p1': '1. Τραπεζικές Εκτιμήσεις (50%)',
        'method_p2': '2. Τάσεις Αγοράς (30%)',
        'method_p3': '3. Κόστος Κατασκευής (20%)',
        'sources_title': '📚 Πηγές Δεδομένων',
        'source_1': '🏦 **Τράπεζα της Ελλάδος (Bank of Greece):** Δείκτες Τιμών Οικιστικών Ακινήτων (Πίνακας ΙΙ.1 - Στοιχεία από εκτιμήσεις τραπεζών).',
        'source_2': '📈 **Spitogatos Network (SPI):** Spitogatos Property Index. Βάση δεδομένων ζητούμενων τιμών από αγγελίες ακινήτων.',
        'source_3': '🏗️ **ΕΛΣΤΑΤ (Hellenic Statistical Authority):** Δείκτης Κόστους Υλικών Νέων Κτιρίων Κατοικιών.',
        'footer': '© 2025 Giakoumakis Real Estate. All rights reserved.'
    },
    'en': {
        'sidebar_lang': 'Language / Γλώσσα',
        'title': 'Greece House Price Index (GHPI)',
        'subtitle': 'by Giakoumakis Real Estate',
        'intro_text': 'The official composite index tracking the Greek Real Estate Market.',
        'tab_data': '📊 Data & Trends',
        'tab_methodology': '📘 Methodology & Sources',
        'chart_compare_title': 'Source Comparison: GHPI vs Sub-Indices',
        'chart_yoy_title': 'Annual Percentage Change (%)',
        'kpi_current': 'Current GHPI Value (2025)',
        'method_title': 'Calculation Methodology',
        'method_intro': """
            The **GHPI** was designed by **Giakoumakis Real Estate** to provide a 
            holistic view of the market, weighting three critical factors:
        """,
        'method_p1': '1. Bank Valuations (50%)',
        'method_p2': '2. Market Trends (30%)',
        'method_p3': '3. Construction Cost (20%)',
        'sources_title': '📚 Data Sources',
        'source_1': '🏦 **Bank of Greece:** Index of Apartment Prices (Table II.1 - Data collected from bank valuations).',
        'source_2': '📈 **Spitogatos Network (SPI):** Spitogatos Property Index. Database of asking prices from property listings.',
        'source_3': '🏗️ **ELSTAT (Hellenic Statistical Authority):** Material Costs Index for New Residential Buildings.',
        'footer': '© 2025 Giakoumakis Real Estate. All rights reserved.'
    }
}

# --- SIDEBAR & ΓΛΩΣΣΑ ---
lang_option = st.sidebar.radio("🌍 Language", ('Ελληνικά', 'English'))
lang = 'el' if lang_option == 'Ελληνικά' else 'en'
text = content[lang]

# --- STYLE ---
st.markdown("""
<style>
    .main-title { font-size: 3rem; color: #0F172A; font-weight: 800; margin-bottom: 0; line-height: 1.2;}
    .subtitle { font-size: 1.5rem; color: #3B82F6; font-weight: 600; margin-top: 0; margin-bottom: 10px; }
    .intro { font-size: 1.1rem; color: #64748B; margin-bottom: 30px; font-style: italic;}
    .source-box { background-color: #f8fafc; padding: 15px; border-radius: 8px; border-left: 5px solid #3B82F6; margin-bottom: 10px;}
</style>
""", unsafe_allow_html=True)

# --- HEADER (BRANDING) ---
st.markdown(f'<div class="main-title">{text["title"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="subtitle">{text["subtitle"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="intro">{text["intro_text"]}</div>', unsafe_allow_html=True)

# --- DATA ENGINE ---
data = {
    'Year': list(range(2000, 2026)),
    'BoG_Index': [58, 66, 75, 80, 85, 92, 98, 102, 101, 97, 92, 87, 76, 68, 63, 60, 59.5, 59, 60, 64.5, 67, 72, 80, 91, 99.5, 105],
    'SPI_Index': [60, 68, 78, 85, 90, 96, 100, 105, 104, 100, 95, 90, 82, 75, 70, 68, 67, 66, 69, 75, 79, 85, 95, 109, 122, 134],
    'ELSTAT_Cost': [70, 72, 75, 78, 82, 86, 90, 93, 96, 98, 100, 101, 100, 98, 96, 95, 94, 95, 96, 97, 96.5, 100, 110, 118, 125, 129]
}
df = pd.DataFrame(data)

# Υπολογισμοί
df['GHPI'] = (df['BoG_Index'] * 0.50) + (df['SPI_Index'] * 0.30) + (df['ELSTAT_Cost'] * 0.20)
df['GHPI'] = df['GHPI'].round(1)
df['YoY_Change'] = df['GHPI'].pct_change() * 100

# --- TABS ---
tab1, tab2 = st.tabs([f"{text['tab_data']}", f"{text['tab_methodology']}"])

# === TAB 1: DATA & CHARTS ===
with tab1:
    # 1. KPIs
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    diff = latest['GHPI'] - prev['GHPI']
    
    col_kpi1, col_kpi2, col_kpi3 = st.columns([1,2,1])
    with col_kpi2:
        st.metric(label=text['kpi_current'], value=f"{latest['GHPI']}", delta=f"{diff:.1f} ({latest['YoY_Change']:.1f}%)")
    
    st.divider()

    # 2. CHART: ΟΛΟΙ ΟΙ ΔΕΙΚΤΕΣ ΜΑΖΙ
    st.subheader(text['chart_compare_title'])
    
    fig_comp = go.Figure()
    
    # Οι επιμέρους δείκτες
    fig_comp.add_trace(go.Scatter(x=df['Year'], y=df['BoG_Index'], name='Bank of Greece (Valuations)', 
                                  line=dict(dash='dot', width=1.5, color='blue')))
    fig_comp.add_trace(go.Scatter(x=df['Year'], y=df['SPI_Index'], name='Market Asking Prices', 
                                  line=dict(dash='dot', width=1.5, color='red')))
    fig_comp.add_trace(go.Scatter(x=df['Year'], y=df['ELSTAT_Cost'], name='Construction Costs', 
                                  line=dict(dash='dot', width=1.5, color='green')))
    
    # Ο GHPI (Έντονη Μαύρη Γραμμή)
    fig_comp.add_trace(go.Scatter(x=df['Year'], y=df['GHPI'], name='GHPI (Composite)', 
                                  line=dict(color='black', width=4)))

    fig_comp.update_layout(
        hovermode="x unified", 
        height=450, 
        legend=dict(orientation="h", y=1.1),
        margin=dict(l=20, r=20, t=20, b=20),
        dragmode=False  # <--- ΠΡΟΣΘΗΚΗ: Απενεργοποίηση Zoom/Pan για mobile scroll
    )
    # ΠΡΟΣΘΗΚΗ: config για απόκρυψη toolbar
    st.plotly_chart(fig_comp, use_container_width=True, config={'displayModeBar': False})

    # 3. CHART: ΕΤΗΣΙΑ ΜΕΤΑΒΟΛΗ
    st.subheader(text['chart_yoy_title'])
    colors = ['#EF4444' if x < 0 else '#10B981' for x in df['YoY_Change']]
    
    fig_bar = go.Figure(go.Bar(
        x=df['Year'], 
        y=df['YoY_Change'], 
        marker_color=colors,
        text=df['YoY_Change'].apply(lambda x: f'{x:.1f}%'),
        textposition='outside'
    ))
    fig_bar.update_layout(
        height=350, 
        showlegend=False, 
        margin=dict(l=20, r=20, t=20, b=20),
        dragmode=False  # <--- ΠΡΟΣΘΗΚΗ: Απενεργοποίηση Zoom/Pan για mobile scroll
    )
    # ΠΡΟΣΘΗΚΗ: config για απόκρυψη toolbar
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
    
    with st.expander("📂 View Raw Data / Προβολή Πίνακα Δεδομένων"):
        st.dataframe(df.style.format("{:.1f}"), use_container_width=True)

# === TAB 2: METHODOLOGY & SOURCES ===
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
    
    # --- ΠΡΟΣΘΗΚΗ ΠΗΓΩΝ ---
    st.subheader(text['sources_title'])
    
    st.markdown(f"""
    <div class="source-box">
        {text['source_1']}<br><br>
        {text['source_2']}<br><br>
        {text['source_3']}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    **Note:** * The base year is technically normalized to align trends.
    * Data sources are updated quarterly.
    """)

# --- FOOTER ---
st.markdown("---")
st.markdown(f"<div style='text-align: center; color: grey; font-size: 0.8rem;'>{text['footer']}</div>", unsafe_allow_html=True)
