import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- ΡΥΘΜΙΣΕΙΣ ΣΕΛΙΔΑΣ ---
st.set_page_config(
    page_title="Greece House Price Index (GHPI)",
    page_icon="🏛️",
    layout="wide"
)

# --- CSS STYLE (THEME AWARE & CUSTOM BUTTONS) ---
st.markdown("""
<style>
    /* Γενικά Κείμενα */
    .main-title { 
        font-size: 3rem; 
        color: var(--text-color); 
        font-weight: 800; 
        margin-bottom: 0; 
        line-height: 1.2;
    }
    .subtitle { 
        font-size: 1.5rem; 
        color: #3B82F6; 
        font-weight: 600; 
        margin-top: 0; 
        margin-bottom: 10px; 
    }
    .intro { 
        font-size: 1.1rem; 
        color: var(--text-color); 
        opacity: 0.8;
        margin-bottom: 30px; 
        font-style: italic;
    }
    
    /* Language Toggle Styling */
    div.stRadio > div[role="radiogroup"] {
        flex-direction: row;
        justify-content: flex-end;
    }
    
    /* Boxes */
    .source-box { 
        background-color: var(--secondary-background-color); 
        padding: 15px; 
        border-radius: 8px; 
        border-left: 5px solid #3B82F6; 
        margin-bottom: 10px;
        border: 1px solid rgba(128, 128, 128, 0.2);
    }
    
    /* HERO SECTION */
    .hero-container {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: white; 
        padding: 40px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 40px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .hero-title { font-size: 1.8rem; font-weight: 800; color: #ffffff; margin-bottom: 10px; }
    .hero-subtitle { font-size: 1.2rem; font-weight: 600; color: #60A5FA; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 1px;}
    .hero-text { font-size: 1.1rem; line-height: 1.6; color: #e2e8f0; max-width: 800px; margin: 0 auto;}

    /* SERVICE CARDS */
    .service-card {
        background-color: var(--secondary-background-color);
        padding: 25px;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.2);
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        height: 100%;
        text-align: center;
        transition: transform 0.2s;
    }
    .service-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px rgba(0,0,0,0.1);
        border-color: #3B82F6;
    }
    .service-icon { font-size: 2.5rem; margin-bottom: 15px; }
    .service-title { font-size: 1.2rem; font-weight: 700; color: var(--text-color); margin-bottom: 10px; }
    .service-desc { font-size: 0.95rem; color: var(--text-color); opacity: 0.8; line-height: 1.5; }

    /* Metric Box */
    div[data-testid="stMetric"] { 
        background-color: var(--secondary-background-color); 
        border: 1px solid rgba(128, 128, 128, 0.2); 
        padding: 15px; 
        border-radius: 5px; 
        box-shadow: 0 1px 3px rgba(0,0,0,0.05); 
    }
    
    a { color: #3B82F6; text-decoration: none; }
    a:hover { text-decoration: underline; }
</style>
""", unsafe_allow_html=True)

# --- HEADER LAYOUT (LOGO + LANGUAGE SWITCHER) ---
# Χωρίζουμε την κορυφή σε 2 στήλες: Λογότυπο (Αριστερά) - Γλώσσα (Δεξιά)
top_col1, top_col2 = st.columns([4, 1])

with top_col2:
    # Language Switcher ως Segmented Control (Pills) - Πολύ πιο εύχρηστο
    lang_selection = st.radio(
        "Language / Γλώσσα",
        ["🇬🇷 GR", "🇬🇧 EN"],
        horizontal=True,
        label_visibility="collapsed" # Κρύβει την ετικέτα για καθαρό look
    )

# Καθορισμός γλώσσας με βάση την επιλογή
lang = 'el' if lang_selection == "🇬🇷 GR" else 'en'

# --- ΛΕΞΙΚΟ ΜΕΤΑΦΡΑΣΕΩΝ ---
content = {
    'el': {
        'title': 'Greece House Price Index (GHPI)',
        'subtitle': 'by Giakoumakis Real Estate',
        'intro_text': 'Ο επίσημος σύνθετος δείκτης για την πορεία της Ελληνικής Κτηματαγοράς.',
        'tab_data': '📊 Δεδομένα & Στατιστικά',
        'tab_methodology': '📘 Μεθοδολογία & Πηγές',
        'tab_about': '🏢 Η Εταιρεία',
        
        # Stats
        'stat_current': 'Τρέχουσα Τιμή (2025)',
        'stat_yoy': 'Ετήσια Μεταβολή (1Y)',
        'stat_5y': 'Μεταβολή 5ετίας (5Y)',
        'stat_ath': 'Ιστορικό Υψηλό (ATH)',
        'ath_desc': 'από το peak του 2008',
        
        'chart_compare_title': 'Σύγκριση Πηγών: GHPI vs Επιμέρους Δείκτες',
        'chart_yoy_title': 'Ετήσια Ποσοστιαία Μεταβολή (%)',
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
        
        # --- ABOUT US TEXT ---
        'hero_title': 'GIAKOUMAKIS REAL ESTATE & PROPERTY DEVELOPER',
        'hero_subtitle': '50+ Χρόνια Εμπειρίας στην Ανάπτυξη Ακινήτων',
        'hero_desc': """
            Η εταιρεία **Μ.ΓΙΑΚΟΥΜΑΚΗΣ ΕΠΕ** ξεκίνησε την πορεία της το **1970** στην Ανατολική Κρήτη. 
            Από ένα παραδοσιακό κτηματομεσιτικό γραφείο, εξελίχθηκε σε έναν καθετοποιημένο όμιλο παροχής υπηρεσιών.
            Σήμερα, προσφέρουμε **360° λύσεις** γύρω από το ακίνητο: από τη σύλληψη της ιδέας και τη μελέτη, 
            μέχρι την κατασκευή, τη διαχείριση και την εμπορική εκμετάλλευση.
        """,
        'services_main_title': 'Οι Υπηρεσίες μας',
        's1_t': 'Real Estate', 's1_d': 'Πωλήσεις, Ενοικιάσεις και Εκτιμήσεις παντός τύπου ακινήτων.',
        's2_t': 'Μελέτες Μηχανικού', 's2_d': 'Τοπογραφικά, Αρχιτεκτονικά, Στατικά και Ηλεκτρομηχανολογικά.',
        's3_t': 'Κατασκευές', 's3_d': 'Ανέγερση πολυτελών κατοικιών, ξενοδοχείων και εμπορικών κτιρίων.',
        's4_t': 'Project Management', 's4_d': 'Συμβουλευτική, διοίκηση έργων και επενδυτικός σχεδιασμός.',
        's5_t': 'Ενέργεια', 's5_d': 'Ενεργειακές αναβαθμίσεις και λύσεις εξοικονόμησης.',
        's6_t': 'Business Operations', 's6_d': 'Λειτουργία ξενοδοχείων, εστίασης και θεματικών πάρκων.',
        'visit_button': 'Επισκεφθείτε το giakoumakis.gr',
        'footer': '© 2025 Giakoumakis Real Estate. All rights reserved.'
    },
    'en': {
        'title': 'Greece House Price Index (GHPI)',
        'subtitle': 'by Giakoumakis Real Estate',
        'intro_text': 'The official composite index tracking the Greek Real Estate Market.',
        'tab_data': '📊 Data & Statistics',
        'tab_methodology': '📘 Methodology & Sources',
        'tab_about': '🏢 About Us',
        
        # Stats
        'stat_current': 'Current Value (2025)',
        'stat_yoy': '1-Year Change (YoY)',
        'stat_5y': '5-Year Change',
        'stat_ath': 'All-Time High (ATH)',
        'ath_desc': 'from 2008 peak',

        'chart_compare_title': 'Source Comparison: GHPI vs Sub-Indices',
        'chart_yoy_title': 'Annual Percentage Change (%)',
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
        
        # --- ABOUT US TEXT ---
        'hero_title': 'GIAKOUMAKIS REAL ESTATE & PROPERTY DEVELOPER',
        'hero_subtitle': '50+ Years of Experience in Property Development',
        'hero_desc': """
            **M. GIAKOUMAKIS LTD** began its journey in **1970** in Eastern Crete. 
            From a traditional real estate agency, it has evolved into a vertically integrated service group.
            Today, we offer **360° solutions** for real estate: from concept and design, 
            to construction, management, and commercial operation.
        """,
        'services_main_title': 'Our Services',
        's1_t': 'Real Estate', 's1_d': 'Sales, Rentals, and Valuations of all property types.',
        's2_t': 'Engineering Studies', 's2_d': 'Topographical, Architectural, Structural, and Electromechanical.',
        's3_t': 'Construction', 's3_d': 'Development of luxury residences, hotels, and commercial buildings.',
        's4_t': 'Project Management', 's4_d': 'Consulting, project administration, and investment planning.',
        's5_t': 'Energy Solutions', 's5_d': 'Energy upgrades and efficiency solutions.',
        's6_t': 'Business Operations', 's6_d': 'Operation of hotels, catering, and theme parks.',
        'visit_button': 'Visit giakoumakis.gr',
        'footer': '© 2025 Giakoumakis Real Estate. All rights reserved.'
    }
}

text = content[lang]

# --- MAIN HEADER ---
with top_col1:
    # Προσπάθεια φόρτωσης λογοτύπου
    logo_col, title_col = st.columns([1, 6])
    with logo_col:
        try:
            st.image("logo.png", use_container_width=True)
        except:
            pass 
    with title_col:
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

# Extra Stats Calculation
latest_val = df['GHPI'].iloc[-1]
prev_year_val = df['GHPI'].iloc[-2]
five_years_ago_val = df['GHPI'].iloc[-6] 
yoy_diff = latest_val - prev_year_val
yoy_pct = df['YoY_Change'].iloc[-1]
five_y_diff = latest_val - five_years_ago_val
five_y_pct = ((latest_val - five_years_ago_val) / five_years_ago_val) * 100
ath_val = df['GHPI'].max()
diff_from_ath = latest_val - ath_val 

# --- TABS ---
tab1, tab2, tab3 = st.tabs([f"{text['tab_data']}", f"{text['tab_methodology']}", f"{text['tab_about']}"])

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
    
    # Chart with Theme Aware Colors
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Scatter(x=df['Year'], y=df['BoG_Index'], name='Bank of Greece (Valuations)', line=dict(dash='dot', width=1.5, color='#3B82F6'))) 
    fig_comp.add_trace(go.Scatter(x=df['Year'], y=df['SPI_Index'], name='Market Asking Prices', line=dict(dash='dot', width=1.5, color='#EF4444'))) 
    fig_comp.add_trace(go.Scatter(x=df['Year'], y=df['ELSTAT_Cost'], name='Construction Costs', line=dict(dash='dot', width=1.5, color='#10B981'))) 
    
    # GHPI Line
    fig_comp.add_trace(go.Scatter(x=df['Year'], y=df['GHPI'], name='GHPI (Composite)', line=dict(color='#7C3AED', width=4))) 

    fig_comp.update_layout(
        hovermode="x unified", 
        height=450, 
        legend=dict(orientation="h", y=1.1), 
        margin=dict(l=20, r=20, t=20, b=20), 
        dragmode=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=None) 
    )
    st.plotly_chart(fig_comp, use_container_width=True, config={'displayModeBar': False})

    st.subheader(text['chart_yoy_title'])
    colors = ['#EF4444' if x < 0 else '#10B981' for x in df['YoY_Change']]
    fig_bar = go.Figure(go.Bar(x=df['Year'], y=df['YoY_Change'], marker_color=colors, text=df['YoY_Change'].apply(lambda x: f'{x:.1f}%'), textposition='outside'))
    fig_bar.update_layout(
        height=350, 
        showlegend=False, 
        margin=dict(l=20, r=20, t=20, b=20), 
        dragmode=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=None)
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
    
    with st.expander("📂 View Raw Data / Προβολή Πίνακα Δεδομένων"):
        st.dataframe(df.style.format("{:.1f}"), use_container_width=True)

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
    st.markdown("---")
    st.markdown("**Note:** Data sources are updated quarterly.")

# === TAB 3: ABOUT US ===
with tab3:
    st.markdown(f"""
    <div class="hero-container">
        <div class="hero-title">{text['hero_title']}</div>
        <div class="hero-subtitle">{text['hero_subtitle']}</div>
        <div class="hero-text">{text['hero_desc']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader(text['services_main_title'])
    
    # Row 1
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="service-card">
            <div class="service-icon">🏡</div>
            <div class="service-title">{text['s1_t']}</div>
            <div class="service-desc">{text['s1_d']}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="service-card">
            <div class="service-icon">📐</div>
            <div class="service-title">{text['s2_t']}</div>
            <div class="service-desc">{text['s2_d']}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="service-card">
            <div class="service-icon">🏗️</div>
            <div class="service-title">{text['s3_t']}</div>
            <div class="service-desc">{text['s3_d']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("") 
    
    # Row 2
    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown(f"""
        <div class="service-card">
            <div class="service-icon">🤝</div>
            <div class="service-title">{text['s4_t']}</div>
            <div class="service-desc">{text['s4_d']}</div>
        </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown(f"""
        <div class="service-card">
            <div class="service-icon">⚡</div>
            <div class="service-title">{text['s5_t']}</div>
            <div class="service-desc">{text['s5_d']}</div>
        </div>
        """, unsafe_allow_html=True)
    with col6:
        st.markdown(f"""
        <div class="service-card">
            <div class="service-icon">🏨</div>
            <div class="service-title">{text['s6_t']}</div>
            <div class="service-desc">{text['s6_d']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown(f"""
    <div style="text-align: center; margin-top: 30px;">
        <a href="https://www.giakoumakis.gr" target="_blank" style="background-color: #3B82F6; color: white; padding: 16px 40px; text-align: center; text-decoration: none; display: inline-block; font-size: 18px; border-radius: 50px; font-weight: bold; box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4); transition: all 0.3s ease;">
            {text['visit_button']} 🌐
        </a>
    </div>
    """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.markdown(f"<div style='text-align: center; color: grey; font-size: 0.8rem;'>{text['footer']}</div>", unsafe_allow_html=True)
