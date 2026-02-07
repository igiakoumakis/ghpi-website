import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- ΡΥΘΜΙΣΕΙΣ ΣΕΛΙΔΑΣ ---
st.set_page_config(
    page_title="GHPI Index",
    page_icon="🏛️",
    layout="wide", # Επιστροφή σε wide για να χωρέσει ο μεγάλος πίνακας
    initial_sidebar_state="collapsed"
)

# --- ΛΕΞΙΚΟ ΜΕΤΑΦΡΑΣΕΩΝ ---
content = {
    'el': {
        'sidebar_lang': 'Γλώσσα / Language',
        'title': 'GHPI Index',
        'subtitle': 'by Giakoumakis Real Estate',
        'intro_text': 'Ο επίσημος σύνθετος δείκτης για την πορεία της Ελληνικής Κτηματαγοράς.',
        'tab_data': '📊 Δεδομένα',
        'tab_methodology': '📘 Μεθοδολογία & Ανάλυση',
        'chart_compare_title': 'Σύγκριση Πηγών & GHPI',
        'chart_yoy_title': 'Ετήσια Ποσοστιαία Μεταβολή (%)',
        'kpi_current': 'Τρέχουσα Τιμή (2025)',
        'method_title': 'Μεθοδολογία Υπολογισμού',
        'method_intro': 'Ο GHPI αποτελεί ένα weighted index (σταθμισμένο δείκτη) που συνδυάζει τρεις πρωτογενείς πηγές δεδομένων:',
        'sources_title': '📚 Ανάλυση Πηγών Δεδομένων',
        
        # Αναλυτικές περιγραφές πηγών
        'source_1_title': '🏦 Τράπεζα της Ελλάδος (Βαρύτητα 50%)',
        'source_1_desc': 'Ο Δείκτης Τιμών Διαμερισμάτων της ΤτΕ βασίζεται σε δεδομένα εκτιμήσεων από τα τραπεζικά ιδρύματα. Θεωρείται η πιο "θεσμική" πηγή, καθώς φιλτράρει τις υπερβολικές προσδοκίες των πωλητών. Αντικατοπτρίζει την αξία που αναγνωρίζει το τραπεζικό σύστημα για δανειοδότηση.',
        
        'source_2_title': '📈 Spitogatos / Αγγελίες (Βαρύτητα 30%)',
        'source_2_desc': 'Ο δείκτης SPI (Spitogatos Property Index) καταγράφει τις ζητούμενες τιμές (Asking Prices). Είναι ο δείκτης που αντιδρά πιο γρήγορα στις τάσεις της αγοράς και στην ψυχολογία των ιδιοκτητών, λειτουργώντας συχνά ως προπομπός των μελλοντικών αυξήσεων.',
        
        'source_3_title': '🏗️ ΕΛΣΤΑΤ / Κόστος (Βαρύτητα 20%)',
        'source_3_desc': 'Ο Δείκτης Κόστους Υλικών Νέων Κτιρίων της Ελληνικής Στατιστικής Αρχής. Η συμμετοχή του στον GHPI είναι κρίσιμη, καθώς η άνοδος του κόστους κατασκευής συμπαρασύρει αναπόφευκτα τις τιμές των νεόδμητων αλλά και το κόστος ανακαίνισης των παλαιότερων ακινήτων.',
        
        'about_title': 'Σχετικά με την Giakoumakis Real Estate',
        'about_text': """
            Η **Giakoumakis Real Estate** ηγείται της κτηματομεσιτικής αγοράς στην Κρήτη και την Ελλάδα, 
            παρέχοντας υπηρεσίες υψηλού επιπέδου στην πώληση, ενοικίαση και διαχείριση ακινήτων. 
            Ο δείκτης GHPI δημιουργήθηκε από την ομάδα αναλυτών μας για να προσφέρει διαφάνεια 
            σε επενδυτές και ιδιώτες.
        """,
        'visit_site': 'Επισκεφθείτε την ιστοσελίδα μας: www.giakoumakis.gr',
        'footer': '© 2025 Giakoumakis Real Estate. All rights reserved.'
    },
    'en': {
        'sidebar_lang': 'Language / Γλώσσα',
        'title': 'GHPI Index',
        'subtitle': 'by Giakoumakis Real Estate',
        'intro_text': 'The official composite index tracking the Greek Real Estate Market.',
        'tab_data': '📊 Data',
        'tab_methodology': '📘 Methodology & Analysis',
        'chart_compare_title': 'Source Comparison',
        'chart_yoy_title': 'Yearly Change (%)',
        'kpi_current': 'Current Value (2025)',
        'method_title': 'Calculation Methodology',
        'method_intro': 'GHPI is a weighted index combining three primary data sources:',
        'sources_title': '📚 Data Source Analysis',
        
        'source_1_title': '🏦 Bank of Greece (Weight 50%)',
        'source_1_desc': 'The BoG Apartment Price Index is based on bank appraisal data. It is considered the most "institutional" source, filtering out excessive seller expectations. It reflects the value recognized by the banking system for lending purposes.',
        
        'source_2_title': '📈 Spitogatos / Listings (Weight 30%)',
        'source_2_desc': 'The SPI (Spitogatos Property Index) tracks Asking Prices. It is the most responsive index to market trends and owner sentiment, often acting as a leading indicator for future price increases.',
        
        'source_3_title': '🏗️ ELSTAT / Costs (Weight 20%)',
        'source_3_desc': 'The Material Costs Index for New Buildings by the Hellenic Statistical Authority. Its inclusion in GHPI is critical, as rising construction costs inevitably drive up new build prices and renovation costs for older properties.',
        
        'about_title': 'About Giakoumakis Real Estate',
        'about_text': """
            **Giakoumakis Real Estate** leads the property market in Crete and Greece, 
            providing top-tier services in sales, rentals, and property management. 
            The GHPI index was created by our analyst team to offer transparency 
            to investors and individuals.
        """,
        'visit_site': 'Visit our website: www.giakoumakis.gr',
        'footer': '© 2025 Giakoumakis Real Estate. All rights reserved.'
    }
}

# --- SIDEBAR & ΓΛΩΣΣΑ ---
lang_option = st.sidebar.radio("🌍 Language", ('Ελληνικά', 'English'))
lang = 'el' if lang_option == 'Ελληνικά' else 'en'
text = content[lang]

# --- CSS STYLING ---
st.markdown("""
<style>
    .main-title { font-size: 2.8rem; color: #0F172A; font-weight: 800; margin-bottom: 0; line-height: 1.1;}
    .subtitle { font-size: 1.2rem; color: #3B82F6; font-weight: 600; margin-top: 5px; margin-bottom: 10px; }
    .source-box { background-color: #f8fafc; padding: 20px; border-radius: 10px; border-left: 5px solid #3B82F6; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);}
    .about-section { background-color: #1E293B; color: white; padding: 30px; border-radius: 15px; margin-top: 40px; text-align: center;}
    .about-link { color: #3B82F6; font-weight: bold; font-size: 1.1rem; text-decoration: none;}
</style>
""", unsafe_allow_html=True)

# --- HEADER (LOGO & TITLE) ---
# Δημιουργία στηλών για Λογότυπο + Τίτλο
col_logo, col_title = st.columns([1, 4])

with col_logo:
    # ΠΡΟΣΟΧΗ: Ανέβασε ένα αρχείο 'logo.png' στο GitHub repository σου.
    # Αν δεν βρει το αρχείο, θα δείξει ένα κενό κουτί.
    try:
        st.image("logo.png", use_container_width=True)
    except:
        # Fallback αν δεν έχει ανέβει εικόνα ακόμα (εικονίδιο σπιτιού)
        st.markdown("🏠", unsafe_allow_html=True)

with col_title:
    st.markdown(f'<div class="main-title">{text["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">{text["subtitle"]}</div>', unsafe_allow_html=True)

st.divider()

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
    # 1. KPI
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    diff = latest['GHPI'] - prev['GHPI']
    
    with st.container():
        st.metric(label=text['kpi_current'], value=f"{latest['GHPI']}", delta=f"{diff:.1f} ({latest['YoY_Change']:.1f}%)")
    
    st.divider()

    # 2. CHART: COMPARISON
    st.subheader(text['chart_compare_title'])
    
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Scatter(x=df['Year'], y=df['BoG_Index'], name='Banks (BoG)', line=dict(dash='dot', width=1, color='blue')))
    fig_comp.add_trace(go.Scatter(x=df['Year'], y=df['SPI_Index'], name='Market (SPI)', line=dict(dash='dot', width=1, color='red')))
    fig_comp.add_trace(go.Scatter(x=df['Year'], y=df['ELSTAT_Cost'], name='Costs (ELSTAT)', line=dict(dash='dot', width=1, color='green')))
    fig_comp.add_trace(go.Scatter(x=df['Year'], y=df['GHPI'], name='GHPI (Composite)', line=dict(color='black', width=3)))

    fig_comp.update_layout(
        height=400,
        margin=dict(l=10, r=10, t=30, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
        dragmode=False,
        hovermode="x unified"
    )
    st.plotly_chart(fig_comp, use_container_width=True, config={'displayModeBar': False})

    # 3. CHART: YoY CHANGE
    st.subheader(text['chart_yoy_title'])
    colors = ['#EF4444' if x < 0 else '#10B981' for x in df['YoY_Change']]
    
    fig_bar = go.Figure(go.Bar(
        x=df['Year'], y=df['YoY_Change'], marker_color=colors
    ))
    fig_bar.update_layout(
        height=300, margin=dict(l=10, r=10, t=30, b=30), showlegend=False, dragmode=False
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
    
    # 4. ΠΙΝΑΚΑΣ (ΠΛΗΡΗΣ ΠΛΕΟΝ)
    st.markdown("### " + text['tab_data'] + " (Detailed Table)")
    # Εδώ εμφανίζουμε ΟΛΕΣ τις στήλες ξανά
    st.dataframe(
        df.style.format("{:.1f}"),
        use_container_width=True,
        hide_index=True,
        height=400
    )

# === TAB 2: METHODOLOGY & ANALYSIS ===
with tab2:
    st.header(text['method_title'])
    st.markdown(text['method_intro'])
    st.latex(r'''GHPI = 0.5 I_{Bank} + 0.3 I_{Mkt} + 0.2 I_{Cost}''')
    
    st.divider()
    
    st.subheader(text['sources_title'])
    
    # Αναλυτικά κουτιά για τις πηγές
    st.markdown(f"""
    <div class="source-box">
        <h4>{text['source_1_title']}</h4>
        <p>{text['source_1_desc']}</p>
    </div>
    <div class="source-box">
        <h4>{text['source_2_title']}</h4>
        <p>{text['source_2_desc']}</p>
    </div>
    <div class="source-box">
        <h4>{text['source_3_title']}</h4>
        <p>{text['source_3_desc']}</p>
    </div>
    """, unsafe_allow_html=True)

# --- FOOTER & BRANDING ---
st.markdown(f"""
<div class="about-section">
    <h3>{text['about_title']}</h3>
    <p>{text['about_text']}</p>
    <br>
    <a class="about-link" href="https://www.giakoumakis.gr" target="_blank">{text['visit_site']}</a>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown(f"<div style='text-align: center; color: grey; font-size: 0.8rem;'>{text['footer']}</div>", unsafe_allow_html=True)
