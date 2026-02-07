import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- ΡΥΘΜΙΣΕΙΣ ΣΕΛΙΔΑΣ (MOBILE OPTIMIZED) ---
st.set_page_config(
    page_title="GHPI Index",
    page_icon="🏛️",
    layout="centered", # Αλλαγή σε centered για να εστιάζει καλύτερα σε κινητά
    initial_sidebar_state="collapsed" # Κλειστή sidebar για περισσότερο χώρο
)

# --- ΛΕΞΙΚΟ ΜΕΤΑΦΡΑΣΕΩΝ ---
content = {
    'el': {
        'sidebar_lang': 'Γλώσσα / Language',
        'title': 'GHPI Index', # Πιο σύντομος τίτλος για mobile
        'subtitle': 'by Giakoumakis Real Estate',
        'intro_text': 'Ο επίσημος σύνθετος δείκτης για την πορεία της Ελληνικής Κτηματαγοράς.',
        'tab_data': '📊 Δεδομένα',
        'tab_methodology': '📘 Μεθοδολογία',
        'chart_compare_title': 'Σύγκριση Πηγών & GHPI',
        'chart_yoy_title': 'Ετήσια Μεταβολή (%)',
        'kpi_current': 'Τρέχουσα Τιμή (2025)',
        'method_title': 'Μεθοδολογία',
        'method_intro': 'Ο GHPI σταθμίζει τρεις κρίσιμους παράγοντες:',
        'method_p1': '1. Τράπεζες (50%)',
        'method_p2': '2. Αγορά (30%)',
        'method_p3': '3. Κόστος (20%)',
        'sources_title': '📚 Πηγές',
        'source_1': '🏦 **ΤτΕ:** Εκτιμήσεις Τραπεζών.',
        'source_2': '📈 **SPI:** Ζητούμενες Τιμές.',
        'source_3': '🏗️ **ΕΛΣΤΑΤ:** Κόστος Υλικών.',
        'footer': '© 2025 Giakoumakis Real Estate.'
    },
    'en': {
        'sidebar_lang': 'Language / Γλώσσα',
        'title': 'GHPI Index',
        'subtitle': 'by Giakoumakis Real Estate',
        'intro_text': 'The official composite index tracking the Greek Real Estate Market.',
        'tab_data': '📊 Data',
        'tab_methodology': '📘 Methodology',
        'chart_compare_title': 'Source Comparison',
        'chart_yoy_title': 'Yearly Change (%)',
        'kpi_current': 'Current Value (2025)',
        'method_title': 'Methodology',
        'method_intro': 'GHPI weights three critical factors:',
        'method_p1': '1. Banks (50%)',
        'method_p2': '2. Market (30%)',
        'method_p3': '3. Costs (20%)',
        'sources_title': '📚 Sources',
        'source_1': '🏦 **BoG:** Bank Valuations.',
        'source_2': '📈 **SPI:** Asking Prices.',
        'source_3': '🏗️ **ELSTAT:** Material Costs.',
        'footer': '© 2025 Giakoumakis Real Estate.'
    }
}

# --- SIDEBAR & ΓΛΩΣΣΑ ---
lang_option = st.sidebar.radio("🌍 Language", ('Ελληνικά', 'English'))
lang = 'el' if lang_option == 'Ελληνικά' else 'en'
text = content[lang]

# --- CSS ΓΙΑ ΚΙΝΗΤΑ (TOUCH FRIENDLY) ---
st.markdown("""
<style>
    .main-title { font-size: 2.2rem; color: #0F172A; font-weight: 800; margin-bottom: 0; line-height: 1.2; text-align: center;}
    .subtitle { font-size: 1.0rem; color: #3B82F6; font-weight: 600; margin-top: 5px; margin-bottom: 15px; text-align: center;}
    .intro { font-size: 0.95rem; color: #64748B; margin-bottom: 20px; font-style: italic; text-align: center;}
    /* Μεγαλύτερα Tabs για εύκολο πάτημα */
    .stTabs [data-baseweb="tab"] { font-size: 1.1rem; padding: 10px 20px; }
    /* Πιο καθαροί πίνακες */
    .stDataFrame { font-size: 0.9rem; }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
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
    # 1. KPI (Κεντραρισμένο)
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    diff = latest['GHPI'] - prev['GHPI']
    
    # Χρήση container για καλύτερο alignment
    with st.container():
        st.metric(label=text['kpi_current'], value=f"{latest['GHPI']}", delta=f"{diff:.1f} ({latest['YoY_Change']:.1f}%)")
    
    st.divider()

    # 2. CHART: COMPARISON (MOBILE OPTIMIZED)
    st.subheader(text['chart_compare_title'])
    
    fig_comp = go.Figure()
    
    # Λεπτές γραμμές για τα επιμέρους
    fig_comp.add_trace(go.Scatter(x=df['Year'], y=df['BoG_Index'], name='Banks', line=dict(dash='dot', width=1, color='blue')))
    fig_comp.add_trace(go.Scatter(x=df['Year'], y=df['SPI_Index'], name='Market', line=dict(dash='dot', width=1, color='red')))
    fig_comp.add_trace(go.Scatter(x=df['Year'], y=df['ELSTAT_Cost'], name='Costs', line=dict(dash='dot', width=1, color='green')))
    
    # Παχιά γραμμή για GHPI
    fig_comp.add_trace(go.Scatter(x=df['Year'], y=df['GHPI'], name='GHPI', line=dict(color='black', width=3)))

    # Ρυθμίσεις για κινητά (Legend κάτω, όχι Zoom)
    fig_comp.update_layout(
        height=400,
        margin=dict(l=10, r=10, t=30, b=0), # Μικρά περιθώρια
        legend=dict(
            orientation="h",    # Οριζόντιο υπόμνημα
            yanchor="bottom", 
            y=-0.3,             # Κάτω από το γράφημα
            xanchor="center", 
            x=0.5
        ),
        dragmode=False, # Απενεργοποίηση zoom για να μην κολλάει το scroll
        hovermode="x unified"
    )
    # Απόκρυψη του ModeBar (εργαλεία zoom κλπ)
    st.plotly_chart(fig_comp, use_container_width=True, config={'displayModeBar': False})

    # 3. CHART: YoY CHANGE
    st.subheader(text['chart_yoy_title'])
    colors = ['#EF4444' if x < 0 else '#10B981' for x in df['YoY_Change']]
    
    fig_bar = go.Figure(go.Bar(
        x=df['Year'], 
        y=df['YoY_Change'], 
        marker_color=colors
    ))
    fig_bar.update_layout(
        height=300, 
        margin=dict(l=10, r=10, t=30, b=30),
        showlegend=False,
        dragmode=False
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
    
    # 4. ΠΙΝΑΚΑΣ (DATA TABLE)
    with st.expander("📂 " + text['tab_data'] + " (Table)"):
        # Format των αριθμών για να πιάνουν λίγο χώρο
        st.dataframe(
            df.style.format("{:.1f}"), 
            use_container_width=True, 
            hide_index=True, # Κρύβουμε την αρίθμηση για χώρο
            height=300 # Σταθερό ύψος με scroll
        )

# === TAB 2: METHODOLOGY ===
with tab2:
    st.header(text['method_title'])
    st.markdown(text['method_intro'])
    
    # Κάθετα Cards αντί για στήλες στα κινητά
    st.info(f"**{text['method_p1']}**")
    st.warning(f"**{text['method_p2']}**")
    st.success(f"**{text['method_p3']}**")
    
    st.markdown("### Formula")
    st.latex(r'''GHPI = 0.5 I_{Bank} + 0.3 I_{Mkt} + 0.2 I_{Cost}''')
    
    st.subheader(text['sources_title'])
    st.markdown(f"""
    - {text['source_1']}
    - {text['source_2']}
    - {text['source_3']}
    """)

# --- FOOTER ---
st.markdown("---")
st.markdown(f"<div style='text-align: center; color: grey; font-size: 0.8rem;'>{text['footer']}</div>", unsafe_allow_html=True)
