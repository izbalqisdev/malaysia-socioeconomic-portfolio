import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

st.set_page_config(
    page_title="Malaysia Socioeconomic Portrait",
    page_icon="🇲🇾",
    layout="wide",
    initial_sidebar_state="expanded"
)

dark = True


def get_css():
    return """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800;900&family=Albert+Sans:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap');

        :root {
            --bg:           #080C10;
            --bg2:          #0E1318;
            --bg3:          #151B22;
            --bg4:          #1C242D;
            --border:       rgba(255,255,255,0.07);
            --border2:      rgba(255,255,255,0.12);
            --accent:       #C8A96E;
            --accent2:      #E07B6A;
            --accent3:      #6DB89A;
            --accent4:      #7B9FD4;
            --text:         #ECE8E1;
            --text2:        #7D8A96;
            --text3:        #4A5561;
            --card-bg:      #0E1318;
            --card-sh:      0 4px 32px rgba(0,0,0,0.6), 0 1px 0 rgba(255,255,255,0.04) inset;
            --glow-gold:    rgba(200,169,110,0.15);
            --glow-teal:    rgba(109,184,154,0.12);
        }

        html, body,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"], .main {
            background-color: var(--bg) !important;
            color: var(--text) !important;
            font-family: 'Albert Sans', sans-serif !important;
        }

        [data-testid="stHeader"] {
            background: var(--bg) !important;
            border-bottom: 1px solid var(--border) !important;
        }

        section[data-testid="stSidebar"] {
            background: var(--bg2) !important;
            border-right: 1px solid var(--border) !important;
        }
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] a { color: var(--text) !important; }
        section[data-testid="stSidebar"] .stSelectbox > div > div {
            background: var(--bg3) !important;
            border-color: var(--border2) !important;
            color: var(--text) !important;
        }
        /* Dark sidebar button */
        section[data-testid="stSidebar"] .stButton > button {
            background: var(--bg4) !important;
            border: 1px solid var(--border2) !important;
            border-radius: 4px !important;
            transition: all 0.2s ease !important;
        }
        section[data-testid="stSidebar"] .stButton > button,
        section[data-testid="stSidebar"] .stButton > button *,
        section[data-testid="stSidebar"] .stButton > button p,
        section[data-testid="stSidebar"] .stButton > button span {
            color: var(--text2) !important;
            font-family: 'Space Mono', monospace !important;
            font-size: 0.72rem !important;
            letter-spacing: 0.06em !important;
            background: transparent !important;
        }
        section[data-testid="stSidebar"] .stButton > button:hover {
            border-color: var(--accent) !important;
            background: rgba(200,169,110,0.08) !important;
        }
        section[data-testid="stSidebar"] .stButton > button:hover *,
        section[data-testid="stSidebar"] .stButton > button:hover p,
        section[data-testid="stSidebar"] .stButton > button:hover span {
            color: var(--accent) !important;
            background: transparent !important;
        }

        .block-container { padding: 2.5rem 3rem 3rem !important; max-width: 1600px !important; }

        h1 {
            font-family: 'Playfair Display', serif !important;
            font-weight: 900 !important;
            font-size: 2.6rem !important;
            color: var(--text) !important;
            letter-spacing: -0.02em !important;
            line-height: 1.15 !important;
        }
        h2, h3 {
            font-family: 'Albert Sans', sans-serif !important;
            font-weight: 600 !important;
            color: var(--text) !important;
        }

        /* ── KPI Cards ── */
        [data-testid="stMetric"] {
            background: var(--card-bg) !important;
            border: 1px solid var(--border2) !important;
            border-top: 2px solid var(--accent) !important;
            border-radius: 4px !important;
            padding: 22px 20px 18px !important;
            box-shadow: var(--card-sh) !important;
            transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
            position: relative !important;
            overflow: hidden !important;
        }
        [data-testid="stMetric"]::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 100%;
            background: linear-gradient(135deg, var(--glow-gold) 0%, transparent 60%);
            pointer-events: none;
        }
        [data-testid="stMetric"]:hover {
            transform: translateY(-3px) !important;
            border-color: var(--accent) !important;
            box-shadow: 0 12px 40px rgba(0,0,0,0.7), 0 0 0 1px var(--accent) !important;
        }
        [data-testid="stMetricLabel"] p {
            font-family: 'Space Mono', monospace !important;
            font-size: 0.65rem !important;
            color: var(--accent) !important;
            text-transform: uppercase !important;
            letter-spacing: 0.12em !important;
            margin-bottom: 6px !important;
        }
        [data-testid="stMetricValue"] {
            font-family: 'Playfair Display', serif !important;
            font-size: 1.85rem !important;
            font-weight: 800 !important;
            color: var(--text) !important;
        }
        [data-testid="stMetricDelta"] {
            font-family: 'Space Mono', monospace !important;
            font-size: 0.7rem !important;
        }

        /* ── Plotly ── */
        .stPlotlyChart > div {
            border-radius: 6px !important;
            overflow: hidden !important;
            border: 1px solid var(--border) !important;
        }

        /* ── Info boxes ── */
        [data-testid="stAlert"] {
            background: var(--bg3) !important;
            border: 1px solid var(--border2) !important;
            border-left: 3px solid var(--accent) !important;
            border-radius: 4px !important;
            color: var(--text2) !important;
            font-family: 'Albert Sans', sans-serif !important;
        }

        /* ── Selectbox ── */
        [data-testid="stSelectbox"] > div,
        [data-testid="stMultiSelect"] > div {
            background: var(--bg3) !important;
            border-color: var(--border2) !important;
        }

        hr { border-color: var(--border) !important; }

        /* ── Page load animation ── */
        @keyframes fadeUp {
            from { opacity: 0; transform: translateY(20px); }
            to   { opacity: 1; transform: translateY(0); }
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-12px); }
            to   { opacity: 1; transform: translateX(0); }
        }
        .block-container > div > div {
            animation: fadeUp 0.5s ease both;
        }
        .block-container > div > div:nth-child(2) { animation-delay: 0.05s; }
        .block-container > div > div:nth-child(3) { animation-delay: 0.10s; }
        .block-container > div > div:nth-child(4) { animation-delay: 0.15s; }
        .block-container > div > div:nth-child(5) { animation-delay: 0.20s; }

        /* ── Divider ── */
        .section-rule {
            height: 1px;
            background: linear-gradient(90deg, var(--accent) 0%, transparent 60%);
            margin: 28px 0 20px;
        }

        /* ── Badge ── */
        .badge {
            display: inline-block;
            padding: 4px 11px;
            border-radius: 2px;
            font-family: 'Space Mono', monospace;
            font-size: 0.62rem;
            font-weight: 400;
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }
        .badge-gold   { background: rgba(200,169,110,0.12); color: #C8A96E; border: 1px solid rgba(200,169,110,0.35); }
        .badge-teal   { background: rgba(109,184,154,0.10); color: #6DB89A; border: 1px solid rgba(109,184,154,0.3); }
        .badge-coral  { background: rgba(224,123,106,0.10); color: #E07B6A; border: 1px solid rgba(224,123,106,0.3); }
        .badge-blue   { background: rgba(123,159,212,0.10); color: #7B9FD4; border: 1px solid rgba(123,159,212,0.3); }

        /* ── Section header ── */
        .sec-header {
            display: flex; align-items: center; gap: 14px; margin: 32px 0 20px;
        }
        .sec-num {
            font-family: 'Space Mono', monospace;
            font-size: 0.6rem; color: var(--accent);
            letter-spacing: 0.15em; text-transform: uppercase;
            white-space: nowrap;
        }
        .sec-line { flex:1; height:1px; background: linear-gradient(90deg, var(--border2) 0%, transparent 100%); }

        /* ── Story card ── */
        .story-card {
            background: var(--bg2);
            border: 1px solid var(--border2);
            border-radius: 6px;
            padding: 28px 26px;
            border-top: 2px solid;
            transition: transform 0.2s ease;
        }
        .story-card:hover { transform: translateY(-2px); }
        </style>
        """

def plt_theme():
    return dict(
        template='plotly_dark',
        paper_bgcolor='#0E1318',
        plot_bgcolor='#0E1318',
        font_color='#ECE8E1',
        font_family='Albert Sans',
        gridcolor='rgba(255,255,255,0.04)',
    )

def apply_plt(fig, height=460, title=None):
    t = plt_theme()
    upd = dict(
        paper_bgcolor=t['paper_bgcolor'],
        plot_bgcolor=t['plot_bgcolor'],
        font=dict(color=t['font_color'], family=t['font_family'], size=12),
        height=height,
        margin=dict(t=64, b=44, l=64, r=44),
        title_font=dict(size=13, family='Albert Sans', color=t['font_color']),
        hoverlabel=dict(
            bgcolor='#1C242D',
            font_color='#ECE8E1',
            font_family='Space Mono',
            font_size=11,
            bordercolor='rgba(0,0,0,0)',
        ),
    )
    if title:
        upd['title'] = dict(text=title, font=dict(size=13, family='Albert Sans'))
    fig.update_layout(**upd)
    fig.update_xaxes(
        gridcolor=t['gridcolor'],
        zerolinecolor=t['gridcolor'],
        tickfont=dict(family='Space Mono', size=10),
        linecolor='rgba(200,169,110,0.2)',
    )
    fig.update_yaxes(
        gridcolor=t['gridcolor'],
        zerolinecolor=t['gridcolor'],
        tickfont=dict(family='Space Mono', size=10),
        linecolor='rgba(200,169,110,0.2)',
    )
    return fig

palette = dict(
    primary='#C8A96E', red='#E07B6A', green='#6DB89A',
    blue='#7B9FD4', purple='#B8A0D4', amber='#D4A44C',
    teal='#5BC4C0', orange='#D4865A', coral='#E09080',
    fill_green='rgba(109,184,154,0.10)',
    fill_red='rgba(224,123,106,0.10)',
    fill_primary='rgba(200,169,110,0.10)',
    fill_blue='rgba(123,159,212,0.10)',
)

_cwd  = os.getcwd()
_here = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else _cwd
_candidates = [
    os.path.join(_here, '..', 'data', 'clean'),
    os.path.join(_here, 'data', 'clean'),
    os.path.join(_cwd,  '..', 'data', 'clean'),
    os.path.join(_cwd,  'data', 'clean'),
    os.path.join(_cwd,  '..', '..', 'data', 'clean'),
]
CLEAN_DIR = next(
    (os.path.normpath(p) for p in _candidates if os.path.isdir(p)),
    os.path.normpath(os.path.join(_here, '..', 'data', 'clean'))
)

@st.cache_data
def load(name):
    path = os.path.join(CLEAN_DIR, f'{name}.csv')
    if not os.path.exists(path):
        return None
    df = pd.read_csv(path)
    if 'year' not in df.columns and 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['year'] = df['date'].dt.year
    return df

pop_malaysia        = load('population_malaysia')
pop_state           = load('population_state')
fertility           = load('fertility')
fertility_state     = load('fertility_state')
births              = load('births_annual')
deaths              = load('deaths')
marriages           = load('marriages')
hh_income           = load('hh_income')
hh_income_state     = load('hh_income_state')
hh_inequality       = load('hh_inequality')
hh_inequality_state = load('hh_inequality_state')
hh_poverty          = load('hh_poverty')
hies_state          = load('hies_state')
cpi_inflation       = load('cpi_headline_inflation')

st.markdown(get_css(), unsafe_allow_html=True)

with st.sidebar:
    st.markdown(f"""
    <div style='padding:10px 0 28px'>
        <div style='font-family:"Playfair Display",serif;font-size:1.6rem;font-weight:900;
                    letter-spacing:-0.02em;color:#C8A96E;line-height:1.1;'>
            Malaysia
        </div>
        <div style='font-family:"Space Mono",monospace;font-size:0.6rem;
                    opacity:0.5;text-transform:uppercase;letter-spacing:0.16em;
                    margin-top:6px;color:#C8A96E;'>
            Socioeconomic Portrait
        </div>
        <div style='margin-top:14px;width:40px;height:2px;background:#C8A96E;opacity:0.4;border-radius:2px;'></div>
    </div>
    """, unsafe_allow_html=True)

    page = st.selectbox("Navigate", [
        "🏠  Overview",
        "📊  Tema 1 — The Ageing Nation",
        "💰  Tema 2 — Income & Inflation",
        "⚖️  Inequality Deep Dive",
    ], label_visibility="collapsed")

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div style='margin-top:32px;font-family:"Space Mono",monospace;font-size:0.6rem;
                opacity:0.35;line-height:2;color:#C8A96E;'>
    DATA SOURCE<br>
    <a href='https://open.dosm.gov.my/' style='color:inherit;'>open.dosm.gov.my</a><br><br>
    21 DATASETS · 2 THEMES<br>
    TEMA 1: DEMOGRAPHY<br>
    TEMA 2: COST OF LIVING
    </div>
    """, unsafe_allow_html=True)

def section_header(num, label):
    st.markdown(f"""
    <div class='sec-header'>
        <div class='sec-num'>{num} · {label}</div>
        <div class='sec-line'></div>
    </div>
    """, unsafe_allow_html=True)

def insight_box(text):
    st.info(f"💡  {text}")

if "Overview" in page:

    st.markdown(f"""
    <div style='margin-bottom:10px;display:flex;gap:8px;flex-wrap:wrap;align-items:center;'>
        <span class='badge badge-gold'>OpenDOSM · 21 Datasets</span>
        <span class='badge badge-teal'>Tema 1 · Demography</span>
        <span class='badge badge-coral'>Tema 2 · Cost of Living</span>
    </div>
    """, unsafe_allow_html=True)

    st.title("Malaysia Socioeconomic Portrait")
    sub_color = "#7D8A96"
    st.markdown(f"<p style='font-family:Albert Sans;color:{sub_color};font-size:1.05rem;margin-top:-6px;margin-bottom:28px;letter-spacing:0.01em;'>A data-driven narrative of population, income &amp; inequality — 1970 to present.</p>", unsafe_allow_html=True)

    _all_datasets = [pop_malaysia, fertility, hh_income, hh_inequality, hh_poverty, cpi_inflation]
    _missing = sum(1 for d in _all_datasets if d is None)
    if _missing > 0:
        _bg  = "#1C242D"
        _brd = "#C8A96E"
        _txt = "#ECE8E1"
        st.markdown(f"""
        <div style='background:{_bg};border:1px solid {_brd};border-left:3px solid {_brd};
                    border-radius:4px;padding:14px 18px;margin-bottom:20px;
                    font-family:"Space Mono",monospace;font-size:0.72rem;color:{_txt};'>
            ⚠ &nbsp; <b>{_missing} dataset(s) not loaded.</b> &nbsp; Data path: <code>{CLEAN_DIR}</code><br>
            <span style='opacity:0.7;'>Run notebooks 00 and 01 first, then restart the app.</span>
        </div>
        """, unsafe_allow_html=True)

    if all(df is not None for df in [pop_malaysia, fertility, hh_income, hh_inequality, hh_poverty, cpi_inflation]):
        pop_row  = pop_malaysia[(pop_malaysia['age']=='overall')&(pop_malaysia['sex']=='both')&(pop_malaysia['ethnicity']=='overall')].sort_values('year').iloc[-1]
        tfr_row  = fertility[fertility['age_group']=='tfr'].sort_values('year').iloc[-1]
        inc_row  = hh_income.sort_values('year').iloc[-1]
        gini_row = hh_inequality.sort_values('year').iloc[-1]
        pov_row  = hh_poverty.sort_values('year').iloc[-1]

        pop_mx  = pop_malaysia[(pop_malaysia['sex']=='both')&(pop_malaysia['ethnicity']=='overall')&(pop_malaysia['age']!='overall')].copy()
        young   = pop_mx[pop_mx['age'].isin(['0-4','5-9','10-14'])].groupby('year')['population'].sum()
        elderly = pop_mx[pop_mx['age'].isin(['60-64','65-69','70-74','75-79','80+'])].groupby('year')['population'].sum()
        ai      = (elderly/young*100).sort_index().iloc[-1]

        cpi_ov  = cpi_inflation[(cpi_inflation['division']=='overall')&(cpi_inflation['inflation_yoy'].notna())]
        cpi_val = cpi_ov.groupby('year')['inflation_yoy'].mean().sort_index().iloc[-1]

        section_header("01", "DEMOGRAPHIC SNAPSHOT")
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Population (thousands)", f"{pop_row['population']:,.0f}", f"Year {int(pop_row['year'])}")
        c2.metric("Fertility Rate (TFR)", f"{tfr_row['fertility_rate']:.2f}", "⚠ Sub-replacement" if tfr_row['fertility_rate']<2.1 else "✓ Above 2.1")
        c3.metric("Ageing Index", f"{ai:.1f}", "⚠ Aged nation" if ai>=100 else "Pre-aged (<100)")
        c4.metric("Latest TFR Year", str(int(tfr_row['year'])), "HIES cycle")

        section_header("02", "ECONOMIC SNAPSHOT")
        c5,c6,c7,c8 = st.columns(4)
        c5.metric("Median Income", f"RM {inc_row['income_median']:,.0f}/mo", f"Year {int(inc_row['year'])}")
        c6.metric("CPI Inflation", f"{cpi_val:+.1f}% YoY", "Latest annual avg")
        c7.metric("Gini Coefficient", f"{gini_row['gini']:.3f}", f"Year {int(gini_row['year'])}")
        c8.metric("Poverty Rate", f"{pov_row['poverty_absolute']:.1f}%", f"Year {int(pov_row['year'])}")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    section_header("03", "TREND OVERVIEW")
    col_l, col_r = st.columns(2)

    with col_l:
        if pop_malaysia is not None:
            pop_total = pop_malaysia[(pop_malaysia['age']=='overall')&(pop_malaysia['sex']=='both')&(pop_malaysia['ethnicity']=='overall')].sort_values('year')
            fig_pop = go.Figure()
            fig_pop.add_trace(go.Scatter(
                x=pop_total['year'], y=pop_total['population'],
                mode='lines', fill='tozeroy',
                fillcolor=palette['fill_primary'],
                line=dict(color=palette['primary'], width=2.5),
                hovertemplate='%{x}: <b>%{y:,.0f}k</b><extra></extra>'
            ))
            apply_plt(fig_pop, height=230)
            fig_pop.update_layout(showlegend=False, yaxis_title='Population (thousands)', title='Total Population 1970–Present')
            st.plotly_chart(fig_pop, use_container_width=True)

    with col_r:
        if hh_income is not None:
            inc_trend = hh_income.sort_values('year')
            fig_inc = go.Figure()
            fig_inc.add_trace(go.Scatter(
                x=inc_trend['year'], y=inc_trend['income_median'],
                mode='lines+markers', fill='tozeroy',
                fillcolor=palette['fill_green'],
                line=dict(color=palette['green'], width=2.5), marker=dict(size=6),
                hovertemplate='%{x}: <b>RM %{y:,.0f}</b><extra></extra>'
            ))
            apply_plt(fig_inc, height=230)
            fig_inc.update_layout(showlegend=False, yaxis_title='RM/month', title='Median Household Income')
            st.plotly_chart(fig_inc, use_container_width=True)

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    insight_box("Use the sidebar to navigate all 12 interactive charts across 4 analytical pages.")

elif "Tema 1" in page:

    st.markdown("<span class='badge badge-gold'>TEMA 1 · DEMOGRAPHY</span>", unsafe_allow_html=True)
    st.title("The Ageing Nation")
    sub_color = "#7D8A96"
    st.markdown(f"<p style='color:{sub_color};font-size:1.05rem;margin-top:-6px;margin-bottom:24px;'>Malaysia's population is ageing rapidly — fewer births, a narrowing base, more elderly.</p>", unsafe_allow_html=True)

    section_header("CHART 01", "POPULATION PYRAMID — ANIMATED")
    if pop_malaysia is not None:
        pyramid = pop_malaysia[
            (pop_malaysia['ethnicity']=='overall') &
            (pop_malaysia['sex'].isin(['male','female'])) &
            (~pop_malaysia['age'].isin(['overall','70+']))
        ].copy()
        age_order = ['0-4','5-9','10-14','15-19','20-24','25-29','30-34',
                     '35-39','40-44','45-49','50-54','55-59','60-64','65-69','70-74','75-79','80+']
        age_order = [a for a in age_order if a in pyramid['age'].unique()]
        pyramid   = pyramid[pyramid['age'].isin(age_order)].copy()
        pyramid['pop_plot'] = pyramid.apply(lambda r: -r['population'] if r['sex']=='male' else r['population'], axis=1)
        pyramid['age'] = pd.Categorical(pyramid['age'], categories=age_order, ordered=True)
        pyramid = pyramid.sort_values(['year','age'])

        male_col   = '#5BC4C0'
        female_col = '#E07B6A'

        fig1 = px.bar(
            pyramid, x='pop_plot', y='age', color='sex',
            animation_frame='year', orientation='h',
            color_discrete_map={'male': male_col, 'female': female_col},
            labels={'pop_plot':'Population (thousands)','age':'Age Group'},
            category_orders={'age': age_order},
            template='plotly_dark',
        )
        fig1.update_layout(
            bargap=0.06,
            xaxis_title='← Male (thousands)          Female (thousands) →',
            legend_title='Sex',
            legend=dict(x=0.82, y=0.99, font=dict(family='Space Mono', size=10)),
        )
        apply_plt(fig1, height=580, title='Population Pyramid — Drag the Year Slider ▶')
        st.plotly_chart(fig1, use_container_width=True)
        insight_box("The pyramid base is narrowing year by year — fewer young people, more elderly. This is the visual signature of demographic ageing.")
    else:
        st.warning("population_malaysia.csv not found in ../data/clean/")

    st.markdown("<div class='section-rule'></div>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        section_header("CHART 02", "TOTAL FERTILITY RATE")
        if fertility is not None:
            tfr    = fertility[fertility['age_group']=='tfr'].sort_values('year').copy()
            latest = tfr.iloc[-1]
            below_21 = tfr[tfr['fertility_rate']<2.1]
            first_below_yr = int(below_21.iloc[0]['year']) if len(below_21)>0 else None

            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=list(tfr['year'])+list(tfr['year'])[::-1],
                y=list(tfr['fertility_rate'])+[2.1]*len(tfr),
                fill='toself', fillcolor=palette['fill_red'],
                line=dict(color='rgba(0,0,0,0)'), showlegend=False, hoverinfo='skip'
            ))
            fig2.add_trace(go.Scatter(
                x=tfr['year'], y=tfr['fertility_rate'],
                mode='lines+markers', name='TFR',
                line=dict(color=palette['amber'], width=3), marker=dict(size=5),
                hovertemplate='%{x}: <b>%{y:.2f}</b> children/woman<extra></extra>'
            ))
            fig2.add_hline(y=2.1, line_dash='dash', line_color=palette['red'], line_width=2,
                           annotation_text='Replacement 2.1',
                           annotation_position='top right',
                           annotation_font_color=palette['red'])
            if first_below_yr:
                cr = below_21.iloc[0]
                bg_ann = 'rgba(30,14,8,0.9)'
                fig2.add_annotation(
                    x=cr['year'], y=cr['fertility_rate'],
                    text=f'Crossed below 2.1<br>in {first_below_yr}',
                    showarrow=True, arrowhead=2, ax=55, ay=-32,
                    font=dict(size=10, color=palette['red']),
                    bgcolor=bg_ann, bordercolor=palette['red']
                )
            bg_ann2 = 'rgba(212,164,76,0.15)'
            fig2.add_annotation(
                x=latest['year'], y=latest['fertility_rate'],
                text=f"<b>{latest['fertility_rate']:.2f}</b>",
                showarrow=True, arrowhead=2, ax=35, ay=-30,
                bgcolor=bg_ann2, bordercolor=palette['amber'], font_size=11
            )
            apply_plt(fig2, height=400, title=f"TFR {int(tfr['year'].min())}–{int(tfr['year'].max())}")
            fig2.update_layout(xaxis_title='Year', yaxis_title='Children per Woman', hovermode='x unified')
            st.plotly_chart(fig2, use_container_width=True)
            insight_box(f"TFR = **{latest['fertility_rate']:.2f}** ({int(latest['year'])}) — below the 2.1 replacement level needed to sustain population size.")
        else:
            st.warning("fertility.csv not found.")

    with col_b:
        section_header("CHART 03", "BIRTHS vs DEATHS")
        if births is not None and deaths is not None:
            # Handle sex column
            b = births.copy()
            d = deaths.copy()
            if 'sex' in b.columns:
                b = b[b['sex']=='both'].sort_values('year') if 'both' in b['sex'].unique() else b.sort_values('year')
            else:
                b = b.sort_values('year')
            if 'sex' in d.columns:
                d = d[d['sex']=='both'].sort_values('year') if 'both' in d['sex'].unique() else d.sort_values('year')
            else:
                d = d.sort_values('year')

            fig3 = go.Figure()
            common = sorted(set(b['year'])&set(d['year']))
            if common:
                b_c = b[b['year'].isin(common)].sort_values('year')
                d_c = d[d['year'].isin(common)].sort_values('year')
                fig3.add_trace(go.Scatter(
                    x=list(b_c['year'])+list(b_c['year'])[::-1],
                    y=list(b_c['abs'])+list(d_c['abs'])[::-1],
                    fill='toself', fillcolor=palette['fill_green'],
                    line=dict(color='rgba(0,0,0,0)'), showlegend=False, hoverinfo='skip'
                ))
            fig3.add_trace(go.Scatter(
                x=b['year'], y=b['abs'], mode='lines+markers', name='Live Births',
                line=dict(color=palette['green'], width=2.5), marker=dict(size=5),
                hovertemplate='%{x}: <b>%{y:,.0f}</b> births<extra></extra>'
            ))
            fig3.add_trace(go.Scatter(
                x=d['year'], y=d['abs'], mode='lines+markers', name='Deaths',
                line=dict(color=palette['red'], width=2.5), marker=dict(size=5),
                hovertemplate='%{x}: <b>%{y:,.0f}</b> deaths<extra></extra>'
            ))
            apply_plt(fig3, height=400, title='Births vs Deaths — Natural Growth Slowing')
            fig3.update_layout(xaxis_title='Year', yaxis_title='Count', hovermode='x unified',
                               legend=dict(x=0.01,y=0.99,font=dict(family='Space Mono',size=10)))
            st.plotly_chart(fig3, use_container_width=True)
            insight_box("The gap between births and deaths is **narrowing**. Fewer marriages → fewer births → decelerating natural growth.")
        else:
            st.warning("births_annual.csv or deaths.csv not found.")

    st.markdown("<div class='section-rule'></div>", unsafe_allow_html=True)

    section_header("CHART 04", "FERTILITY RATE BY STATE")
    if fertility_state is not None:
        tfr_st = fertility_state[fertility_state['age_group']=='tfr'].copy()
        for col in ['sex','ethnicity']:
            if col in tfr_st.columns:
                v = tfr_st[col].unique()
                if 'both' in v:      tfr_st = tfr_st[tfr_st[col]=='both']
                elif 'overall' in v: tfr_st = tfr_st[tfr_st[col]=='overall']
        latest_yr  = int(tfr_st['year'].max())
        tfr_latest = (tfr_st[tfr_st['year']==latest_yr]
                      .groupby('state',as_index=False)['fertility_rate'].mean()
                      .sort_values('fertility_rate', ascending=True))
        nat_avg = tfr_latest['fertility_rate'].mean()
        bar_cols = [palette['red'] if v<2.1 else palette['green'] for v in tfr_latest['fertility_rate']]
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            x=tfr_latest['fertility_rate'], y=tfr_latest['state'],
            orientation='h', marker_color=bar_cols, marker_cornerradius=3,
            text=[f' {v:.2f}' for v in tfr_latest['fertility_rate']],
            textposition='outside', textfont=dict(size=10, family='Space Mono'),
            hovertemplate='<b>%{y}</b>: %{x:.2f} children/woman<extra></extra>'
        ))
        fig4.add_vline(x=2.1, line_dash='dot', line_color=palette['amber'], line_width=2,
                       annotation_text='2.1 Replacement', annotation_position='top right',
                       annotation_font_color=palette['amber'])
        fig4.add_vline(x=nat_avg, line_dash='dash',
                       line_color='rgba(150,140,130,0.5)', line_width=1.5,
                       annotation_text=f'Avg {nat_avg:.2f}', annotation_position='bottom right')
        apply_plt(fig4, height=540, title=f'Fertility Rate by State ({latest_yr}) — Red = Below 2.1 | Green = Above 2.1')
        fig4.update_layout(xaxis_title='Children per Woman', margin=dict(l=155, r=120, t=64, b=44))
        st.plotly_chart(fig4, use_container_width=True)
        pct_below = len(tfr_latest[tfr_latest['fertility_rate']<2.1])/len(tfr_latest)*100
        insight_box(f"**{pct_below:.0f}%** of Malaysian states are below the 2.1 replacement level in {latest_yr}.")
    else:
        st.warning("fertility_state.csv not found.")

    st.markdown("<div class='section-rule'></div>", unsafe_allow_html=True)

    section_header("CHART 05", "AGEING INDEX  [DERIVED METRIC]")
    if pop_malaysia is not None:
        pop_mx  = pop_malaysia[(pop_malaysia['sex']=='both')&(pop_malaysia['ethnicity']=='overall')&(pop_malaysia['age']!='overall')].copy()
        y_s = pop_mx[pop_mx['age'].isin(['0-4','5-9','10-14'])].groupby('year')['population'].sum().reset_index()
        e_s = pop_mx[pop_mx['age'].isin(['60-64','65-69','70-74','75-79','80+'])].groupby('year')['population'].sum().reset_index()
        ageing = pd.merge(y_s, e_s, on='year', suffixes=('_young','_elderly'))
        ageing['ageing_index'] = (ageing['population_elderly']/ageing['population_young'])*100
        ageing = ageing.sort_values('year').reset_index(drop=True)
        latest_ai = ageing.iloc[-1]
        crossed   = ageing[ageing['ageing_index']>=100]
        cross_yr  = int(crossed.iloc[0]['year']) if len(crossed)>0 else None

        fig5 = go.Figure()
        fig5.add_trace(go.Scatter(
            x=ageing['year'], y=ageing['ageing_index'],
            mode='lines+markers', line=dict(color=palette['blue'], width=3),
            marker=dict(size=7, color=[palette['red'] if v>=100 else palette['blue'] for v in ageing['ageing_index']]),
            fill='tozeroy', fillcolor=palette['fill_blue'],
            name='Ageing Index',
            hovertemplate='%{x}: Ageing Index = <b>%{y:.1f}</b><extra></extra>'
        ))
        fig5.add_hline(y=100, line_dash='dash', line_color=palette['red'], line_width=2,
                       annotation_text='Index 100 = Equal elderly & children',
                       annotation_position='bottom right',
                       annotation_font_color=palette['red'])
        if cross_yr:
            fig5.add_vrect(x0=cross_yr, x1=int(ageing['year'].max()),
                           fillcolor=palette['fill_red'], layer='below', line_width=0)
        bg_ann = 'rgba(20,30,45,0.9)'
        fig5.add_annotation(
            x=latest_ai['year'], y=latest_ai['ageing_index'],
            text=f"<b>{int(latest_ai['year'])}: {latest_ai['ageing_index']:.1f}</b>",
            showarrow=True, arrowhead=2, ax=50, ay=-40,
            font=dict(color=palette['blue'], size=12),
            bgcolor=bg_ann, bordercolor=palette['blue']
        )
        apply_plt(fig5, height=440, title='Ageing Index = (Pop 60+) / (Pop 0–14) × 100')
        fig5.update_layout(xaxis_title='Year', yaxis_title='Ageing Index', hovermode='x unified')
        st.plotly_chart(fig5, use_container_width=True)
        if latest_ai['ageing_index'] >= 100:
            msg = f"Ageing Index = **{latest_ai['ageing_index']:.1f}** — Malaysia now has MORE elderly than children. The tipping point was {cross_yr}."
        else:
            msg = f"Ageing Index = **{latest_ai['ageing_index']:.1f}** — rapidly approaching the 100 threshold (aged-nation status)."
        insight_box(msg)
    else:
        st.warning("population_malaysia.csv not found.")

elif "Tema 2" in page:

    st.markdown("<span class='badge badge-teal'>TEMA 2 · COST OF LIVING</span>", unsafe_allow_html=True)
    st.title("Income & Inflation")
    sub_color = "#7D8A96"
    st.markdown(f"<p style='color:{sub_color};font-size:1.05rem;margin-top:-6px;margin-bottom:24px;'>Is Malaysia's rising income keeping pace with the cost of living? Who really wins?</p>", unsafe_allow_html=True)

    # CPI prep
    cpi_yr = None
    if cpi_inflation is not None:
        cpi_overall = cpi_inflation[(cpi_inflation['division']=='overall')&(cpi_inflation['inflation_yoy'].notna())].copy()
        cpi_yr = cpi_overall.groupby('year')['inflation_yoy'].mean().reset_index()
        cpi_yr.columns = ['year','cpi_yoy']

    income = hh_income.sort_values('year').copy() if hh_income is not None else None

    section_header("CHART 06 ⭐", "HERO — MEDIAN INCOME vs CPI INFLATION")
    if income is not None and cpi_yr is not None:
        fig6 = make_subplots(specs=[[{'secondary_y': True}]])
        fig6.add_trace(go.Scatter(
            x=income['year'], y=income['income_median'],
            mode='lines+markers', name='Median Income (RM/month)',
            line=dict(color=palette['green'], width=3.5), marker=dict(size=8),
            hovertemplate='%{x}: <b>RM %{y:,.0f}</b>/month<extra></extra>'
        ), secondary_y=False)
        fig6.add_trace(go.Scatter(
            x=income['year'], y=income['income_mean'],
            mode='lines+markers', name='Mean Income (RM/month)',
            line=dict(color=palette['teal'], width=2, dash='dot'), marker=dict(size=5),
            hovertemplate='%{x}: RM %{y:,.0f}<extra></extra>'
        ), secondary_y=False)
        fig6.add_trace(go.Scatter(
            x=cpi_yr['year'], y=cpi_yr['cpi_yoy'],
            mode='lines+markers', name='CPI Inflation % YoY',
            line=dict(color=palette['red'], width=2.5, dash='dash'),
            marker=dict(size=7, symbol='diamond'),
            hovertemplate='%{x}: <b>%{y:.1f}%</b> inflation<extra></extra>'
        ), secondary_y=True)

        first_inc, last_inc = income.iloc[0], income.iloc[-1]
        for row, ax, ay in [(first_inc, 40, -35), (last_inc, -50, -35)]:
            bg_a = 'rgba(30,14,8,0.9)'
            fig6.add_annotation(
                x=row['year'], y=row['income_median'],
                text=f"RM {row['income_median']:,.0f}",
                showarrow=True, arrowhead=1, ax=ax, ay=ay,
                font=dict(size=10, color=palette['green']), bgcolor=bg_a
            )
        apply_plt(fig6, height=500, title='⭐ HERO: Median Income vs CPI Inflation — Does Real Income Grow?')
        fig6.update_yaxes(title_text='Monthly Household Income (RM)', secondary_y=False,
                          tickprefix='RM ', tickformat=',')
        fig6.update_yaxes(title_text='CPI Inflation Rate (% YoY)', secondary_y=True, ticksuffix='%')
        fig6.update_layout(hovermode='x unified',
                           legend=dict(x=0.01, y=0.99, bgcolor='rgba(0,0,0,0.05)',
                                       font=dict(family='Space Mono', size=10)))
        st.plotly_chart(fig6, use_container_width=True)
        growth = ((last_inc['income_median']/first_inc['income_median'])-1)*100
        insight_box(f"Median income rose **RM {first_inc['income_median']:,.0f} → RM {last_inc['income_median']:,.0f}** (+{growth:.0f}% total). But inflation spikes in certain years erode real gains — see Chart 07.")
    else:
        st.warning("hh_income.csv or cpi_headline_inflation.csv not found.")

    st.markdown("<div class='section-rule'></div>", unsafe_allow_html=True)

    section_header("CHART 07", "REAL PURCHASING POWER  [DERIVED METRIC]")
    if income is not None and cpi_yr is not None:
        income_s = income.copy()
        income_s['income_growth_pct'] = income_s['income_median'].pct_change()*100
        real = pd.merge(income_s[['year','income_median','income_growth_pct']], cpi_yr, on='year', how='inner').dropna()
        real['real_growth'] = real['income_growth_pct'] - real['cpi_yoy']
        real = real.sort_values('year').reset_index(drop=True)

        fig7 = go.Figure()
        fig7.add_trace(go.Bar(
            x=real['year'], y=real['real_growth'],
            marker_color=[palette['green'] if v>=0 else palette['red'] for v in real['real_growth']],
            marker_line_color='rgba(0,0,0,0)', marker_cornerradius=3,
            text=[f'{v:+.1f}%' for v in real['real_growth'].round(1)],
            textposition='outside', textfont=dict(size=10, family='Space Mono'),
            name='Real Wage Growth',
            hovertemplate='%{x}: Real = <b>%{y:+.1f}%</b><extra></extra>',
            width=0.55
        ))
        fig7.add_hline(y=0, line_color='rgba(150,140,130,0.6)', line_width=2)
        apply_plt(fig7, height=400, title='Real Purchasing Power = Income Growth % − CPI Inflation %')
        fig7.update_layout(xaxis_title='Year', yaxis_title='Real Growth (%)',
                           yaxis_ticksuffix='%', xaxis=dict(type='category'))
        st.plotly_chart(fig7, use_container_width=True)
        bad  = real[real['real_growth']<0]['year'].astype(int).tolist()
        good = real[real['real_growth']>=0]['year'].astype(int).tolist()
        insight_box(f"Income **beat** inflation in: {good}  |  Inflation **won** in: {bad}")
    else:
        st.warning("Data not available for real purchasing power chart.")

    st.markdown("<div class='section-rule'></div>", unsafe_allow_html=True)

    col_c, col_d = st.columns(2)

    with col_c:
        section_header("CHART 08", "INCOME BY STATE")
        if hh_income_state is not None and hh_income is not None:
            latest_yr  = int(hh_income_state['year'].max())
            inc_state  = hh_income_state[hh_income_state['year']==latest_yr].dropna(subset=['income_median']).sort_values('income_median', ascending=True).copy()
            nat_vals   = hh_income[hh_income['year']==latest_yr]['income_median'].values
            nat_median = nat_vals[0] if len(nat_vals)>0 else inc_state['income_median'].median()
            fig8 = go.Figure(go.Bar(
                x=inc_state['income_median'], y=inc_state['state'],
                orientation='h', marker_cornerradius=3,
                marker_color=[palette['green'] if v>=nat_median else palette['red'] for v in inc_state['income_median']],
                text=[f'RM {v:,.0f}' for v in inc_state['income_median']],
                textposition='outside', textfont=dict(size=9, family='Space Mono'),
                hovertemplate='<b>%{y}</b>: RM %{x:,.0f}/month<extra></extra>'
            ))
            fig8.add_vline(x=nat_median, line_dash='dash', line_color=palette['purple'], line_width=2,
                           annotation=dict(text=f'National RM {nat_median:,.0f}',
                                           font=dict(size=9, color=palette['purple'])),
                           annotation_position='top')
            apply_plt(fig8, height=520, title=f'Income by State ({latest_yr}) — Green=Above / Red=Below Median')
            fig8.update_layout(
                xaxis=dict(tickprefix='RM ', tickformat=',', range=[0, inc_state['income_median'].max()*1.32]),
                margin=dict(l=155, r=110)
            )
            st.plotly_chart(fig8, use_container_width=True)
        else:
            st.warning("hh_income_state.csv not found.")

    with col_d:
        section_header("CHART 10", "POVERTY RATE TREND")
        if hh_poverty is not None:
            poverty_c = hh_poverty.sort_values('year').copy()
            hardcore  = poverty_c.dropna(subset=['poverty_hardcore']).copy() if 'poverty_hardcore' in poverty_c.columns else pd.DataFrame()
            fp, lp    = poverty_c.iloc[0], poverty_c.iloc[-1]
            fig10 = go.Figure()
            fig10.add_trace(go.Scatter(
                x=poverty_c['year'], y=poverty_c['poverty_absolute'],
                mode='lines+markers', name='Absolute Poverty (%)',
                line=dict(color=palette['amber'], width=3), marker=dict(size=8),
                fill='tozeroy', fillcolor=palette['fill_primary'],
                hovertemplate='%{x}: <b>%{y:.1f}%</b><extra></extra>'
            ))
            if len(hardcore)>0:
                fig10.add_trace(go.Scatter(
                    x=hardcore['year'], y=hardcore['poverty_hardcore'],
                    mode='lines+markers', name='Hardcore Poverty (%)',
                    line=dict(color=palette['red'], width=2, dash='dot'), marker=dict(size=6),
                    hovertemplate='%{x}: <b>%{y:.1f}%</b> hardcore<extra></extra>'
                ))
            for row, bg, bc, ax, ay in [
                (fp, 'rgba(212,164,76,0.15)', palette['amber'], 40, -32),
                (lp, 'rgba(109,184,154,0.15)', palette['green'], -45, -35)
            ]:
                fig10.add_annotation(
                    x=row['year'], y=row['poverty_absolute'],
                    text=f"<b>{row['poverty_absolute']:.1f}%</b>",
                    showarrow=True, arrowhead=2, ax=ax, ay=ay,
                    bgcolor=bg, bordercolor=bc, font_size=11
                )
            apply_plt(fig10, height=520, title=f'Poverty Rate — {fp["poverty_absolute"]:.0f}% → {lp["poverty_absolute"]:.1f}% 🎉')
            fig10.update_layout(xaxis_title='Year', yaxis_title='Poverty Rate (%)',
                                yaxis_ticksuffix='%',
                                legend=dict(x=0.6, y=0.99, font=dict(family='Space Mono', size=10)))
            st.plotly_chart(fig10, use_container_width=True)
        else:
            st.warning("hh_poverty.csv not found.")

    st.markdown("<div class='section-rule'></div>", unsafe_allow_html=True)

    section_header("CHART 11", "CPI INFLATION BY CATEGORY")
    if cpi_inflation is not None:
        division_map = {
            'overall':'Overall CPI', '01':'Food & Non-Alcoholic Beverages',
            '04':'Housing, Water & Energy', '07':'Transport',
            '06':'Health', '10':'Education'
        }
        color_map = {
            'Overall CPI':                   palette['blue'],
            'Food & Non-Alcoholic Beverages': palette['red'],
            'Housing, Water & Energy':        palette['teal'],
            'Transport':                      palette['amber'],
            'Health':                         palette['purple'],
            'Education':                      palette['green'],
        }
        cpi_c = cpi_inflation[cpi_inflation['division'].isin(division_map.keys())].copy()
        cpi_c['div_name'] = cpi_c['division'].map(division_map)
        cpi_c = cpi_c.dropna(subset=['div_name','inflation_yoy'])
        cpi_ann = cpi_c.groupby(['year','div_name'])['inflation_yoy'].mean().reset_index()

        all_cats = sorted(cpi_ann['div_name'].unique())
        selected = st.multiselect("Filter categories:", all_cats, default=all_cats)
        cpi_filt = cpi_ann[cpi_ann['div_name'].isin(selected)]

        fig11 = go.Figure()
        for div in cpi_filt['div_name'].unique():
            df_d = cpi_filt[cpi_filt['div_name']==div].sort_values('year')
            fig11.add_trace(go.Scatter(
                x=df_d['year'], y=df_d['inflation_yoy'],
                mode='lines+markers', name=div,
                line=dict(width=3 if div=='Overall CPI' else 2, color=color_map.get(div,'#94A3B8')),
                marker=dict(size=5),
                hovertemplate=div+'<br>%{x}: <b>%{y:.1f}%</b><extra></extra>'
            ))
        fig11.add_hline(y=0, line_color='rgba(150,140,130,0.5)', line_width=1)
        apply_plt(fig11, height=450, title='CPI Inflation by Category (% YoY) — Which Goods Cost More?')
        fig11.update_layout(
            xaxis_title='Year', yaxis_title='Inflation (% YoY)',
            yaxis_ticksuffix='%', hovermode='x unified',
            legend=dict(x=0.01, y=0.99, bgcolor='rgba(0,0,0,0.04)',
                        font=dict(family='Space Mono', size=10))
        )
        st.plotly_chart(fig11, use_container_width=True)
        insight_box("Food & beverage inflation hits B40 households hardest — they spend the largest share of income on food. Use the multiselect to compare categories.")
    else:
        st.warning("cpi_headline_inflation.csv not found.")

elif "Inequality" in page:

    st.markdown("<span class='badge badge-coral'>COMBINED · INEQUALITY</span>", unsafe_allow_html=True)
    st.title("Inequality Deep Dive")
    sub_color = "#7D8A96"
    st.markdown(f"<p style='color:{sub_color};font-size:1.05rem;margin-top:-6px;margin-bottom:24px;'>High income does not mean low inequality. Explore the gap between and within Malaysian states.</p>", unsafe_allow_html=True)

    section_header("CHART 09", "GINI COEFFICIENT HEATMAP  (STATE × YEAR)")
    if hh_inequality_state is not None:
        gini_pivot = hh_inequality_state.pivot_table(index='state', columns='year', values='gini')
        latest_col = gini_pivot.columns[-1]
        gini_pivot = gini_pivot.sort_values(latest_col, ascending=False)
        text_vals  = [[f'{v:.3f}' if not np.isnan(v) else '' for v in row] for row in gini_pivot.values]

        fig9 = go.Figure(go.Heatmap(
            z=gini_pivot.values,
            x=[str(int(c)) for c in gini_pivot.columns],
            y=gini_pivot.index.tolist(),
            colorscale='RdYlGn_r', zmin=0.30, zmax=0.55,
            hoverongaps=False,
            hovertemplate='<b>%{y}</b><br>Year: %{x}<br>Gini: <b>%{z:.3f}</b><extra></extra>',
            colorbar=dict(
                title=dict(text='Gini', side='right'),
                len=0.85,
                tickfont=dict(family='Space Mono', size=9)
            ),
            text=text_vals, texttemplate='%{text}',
            textfont=dict(size=9, family='Space Mono', color='#1A1410')
        ))
        apply_plt(fig9, height=590, title='Gini Heatmap — 🔴 High Inequality  |  🟢 More Equal  |  Hover for exact values')
        fig9.update_layout(xaxis_title='Year', yaxis_title='State', margin=dict(l=180, t=64))
        st.plotly_chart(fig9, use_container_width=True)
        most_unequal  = gini_pivot[latest_col].idxmax()
        least_unequal = gini_pivot[latest_col].idxmin()
        insight_box(f"Most unequal: **{most_unequal}** (Gini = {gini_pivot.loc[most_unequal,latest_col]:.3f}) | Most equal: **{least_unequal}** (Gini = {gini_pivot.loc[least_unequal,latest_col]:.3f})")
    else:
        st.warning("hh_inequality_state.csv not found.")

    st.markdown("<div class='section-rule'></div>", unsafe_allow_html=True)

    section_header("CHART 12", "BUBBLE CHART — INCOME × INEQUALITY × POPULATION")
    if hies_state is not None:
        hies_yr   = int(hies_state['year'].max())
        hies_data = hies_state[hies_state['year'] == hies_yr].copy()

        def get_total_pop_by_state(df):
            df = df.copy()
            str_cols = df.select_dtypes(include='object').columns
            df[str_cols] = df[str_cols].apply(lambda c: c.str.strip().str.lower())
            filters = {}
            if 'sex' in df.columns:
                both_vals = [v for v in df['sex'].unique() if 'both' in str(v)]
                if both_vals: filters['sex'] = both_vals[0]
            if 'age' in df.columns:
                overall_vals = [v for v in df['age'].unique()
                                if any(k in str(v) for k in ('overall', 'total', 'all'))]
                if overall_vals: filters['age'] = overall_vals[0]
            if 'ethnicity' in df.columns:
                overall_eth = [v for v in df['ethnicity'].unique()
                            if any(k in str(v) for k in ('overall', 'total', 'all'))]
                if overall_eth: filters['ethnicity'] = overall_eth[0]
            mask = pd.Series(True, index=df.index)
            for col, val in filters.items():
                mask &= (df[col] == val)
            result = df[mask].copy()
            if len(result) == 0:
                result = df.groupby(['state', 'year'])['population'].sum().reset_index()
            return result, filters

        bubble_size = 'income_median'
        size_label  = 'Median Income (RM/month)'

        if pop_state is not None:
            pop_st, _ = get_total_pop_by_state(pop_state)
            if len(pop_st) > 0 and pop_st['year'].notna().any():
                pop_yr       = int(pop_st['year'].max())
                pop_by_state = pop_st[pop_st['year'] == pop_yr][['state', 'population']].copy()
                pop_by_state['state'] = pop_by_state['state'].str.title()
                hies_data['state']    = hies_data['state'].str.strip()
                hies_data = pd.merge(hies_data, pop_by_state, on='state', how='left')
                if hies_data['population'].notna().sum() >= 3:
                    bubble_size = 'population'
                    size_label  = 'Population (thousands)'

        if bubble_size == 'income_median' and 'expenditure_mean' in hies_data.columns:
            if hies_data['expenditure_mean'].notna().sum() >= 3:
                bubble_size = 'expenditure_mean'
                size_label  = 'Mean Expenditure (RM/month)'

        bubble = hies_data.dropna(subset=['income_median', 'gini']).copy()
        if bubble_size != 'income_median':
            bubble = bubble.dropna(subset=[bubble_size])

        fig12 = px.scatter(
            bubble, x='income_median', y='gini',
            size=bubble_size, color='state',
            hover_name='state', size_max=68,
            labels={
                'income_median' : 'Median Household Income (RM/month)',
                'gini'          : 'Gini Coefficient (↑ = More Unequal)',
                bubble_size     : size_label
            },
            template='plotly_dark',
        )
        fig12.update_traces(
            text=bubble['state'].tolist(),  
            textposition='top center',
            textfont=dict(size=9, family='Space Mono', color='#ECE8E1'),
            marker=dict(opacity=0.80, line=dict(width=1.5, color='rgba(255,255,255,0.2)'))
        )
        apply_plt(fig12, height=580, title=f'Income vs Inequality by State ({hies_yr}) — X=Income | Y=Gini | Size={size_label}')
        fig12.update_layout(xaxis=dict(tickprefix='RM ', tickformat=','), showlegend=False)
        st.plotly_chart(fig12, use_container_width=True)

        richest  = bubble.loc[bubble['income_median'].idxmax()]
        most_une = bubble.loc[bubble['gini'].idxmax()]
        insight_box(f"Highest income: **{richest['state']}** (RM {richest['income_median']:,.0f}) | Most unequal: **{most_une['state']}** (Gini = {most_une['gini']:.3f}). High income ≠ low inequality.")
    else:
        st.warning("hies_state.csv not found.")

    st.markdown("<div class='section-rule'></div>", unsafe_allow_html=True)

    section_header("FINAL", "THE FULL STORY — SO WHAT DOES THIS MEAN?")

    if all(df is not None for df in [hh_income, hh_inequality, hh_poverty, fertility, pop_malaysia]):
        latest_income = hh_income.sort_values('year').iloc[-1]
        first_income  = hh_income.sort_values('year').iloc[0]
        latest_gini   = hh_inequality.sort_values('year').iloc[-1]
        first_gini    = hh_inequality.sort_values('year').iloc[0]
        latest_pov    = hh_poverty.sort_values('year').iloc[-1]
        first_pov     = hh_poverty.sort_values('year').iloc[0]
        latest_tfr    = fertility[fertility['age_group']=='tfr'].sort_values('year').iloc[-1]

        pop_mx2 = pop_malaysia[(pop_malaysia['sex']=='both')&(pop_malaysia['ethnicity']=='overall')&(pop_malaysia['age']!='overall')].copy()
        y2 = pop_mx2[pop_mx2['age'].isin(['0-4','5-9','10-14'])].groupby('year')['population'].sum()
        e2 = pop_mx2[pop_mx2['age'].isin(['60-64','65-69','70-74','75-79','80+'])].groupby('year')['population'].sum()
        ai_latest = (e2/y2*100).sort_index().iloc[-1]
        income_growth = ((latest_income['income_median']/first_income['income_median'])-1)*100
        gini_dir  = "✓ Improved" if latest_gini['gini']<first_gini['gini'] else "⚠ Worsened"
        pov_drop  = first_pov['poverty_absolute']-latest_pov['poverty_absolute']

        card_bg = "#0E1318"; border = "rgba(255,255,255,0.08)"
        txt = "#ECE8E1"; txt2 = "#7D8A96"
        acc1 = "#C8A96E"; acc2 = "#6DB89A"

        st.markdown(f"""
        <div style='display:grid;grid-template-columns:1fr 1fr;gap:20px;margin:16px 0 32px;'>

          <div class='story-card' style='background:{card_bg};border-color:{border};border-top-color:{acc1};'>
            <div style='font-family:"Albert Sans",sans-serif;font-size:0.62rem;
                        font-weight:600;color:{acc1};text-transform:uppercase;
                        letter-spacing:0.14em;margin-bottom:12px;'>
              📊 Tema 1 — Demographic Findings
            </div>
            <div style='font-family:"Albert Sans",sans-serif;font-size:0.9rem;color:{txt2};line-height:2.1;'>
              <b style='color:{txt};font-weight:600;'>TFR:</b> {latest_tfr['fertility_rate']:.2f} —
              {'⚠ BELOW' if latest_tfr['fertility_rate']<2.1 else '✓ Above'} the 2.1 replacement level<br>
              <b style='color:{txt};font-weight:600;'>Ageing Index:</b> {ai_latest:.1f} —
              {'officially an ageing nation' if ai_latest>=100 else 'approaching aged-nation status'}<br>
              <b style='color:{txt};font-weight:600;'>Key Risk:</b> Fewer workers supporting more retirees → pension, healthcare &amp; labour pressure
            </div>
          </div>

          <div class='story-card' style='background:{card_bg};border-color:{border};border-top-color:{acc2};'>
            <div style='font-family:"Albert Sans",sans-serif;font-size:0.62rem;
                        font-weight:600;color:{acc2};text-transform:uppercase;
                        letter-spacing:0.14em;margin-bottom:12px;'>
              💰 Tema 2 — Economic Findings
            </div>
            <div style='font-family:"Albert Sans",sans-serif;font-size:0.9rem;color:{txt2};line-height:2.1;'>
              <b style='color:{txt};font-weight:600;'>Income Growth:</b>
              RM {first_income['income_median']:,.0f} → RM {latest_income['income_median']:,.0f} (+{income_growth:.0f}%)<br>
              <b style='color:{txt};font-weight:600;'>Gini Coefficient:</b>
              {first_gini['gini']:.3f} → {latest_gini['gini']:.3f} ({gini_dir})<br>
              <b style='color:{txt};font-weight:600;'>Poverty:</b>
              {first_pov['poverty_absolute']:.0f}% → {latest_pov['poverty_absolute']:.1f}% (−{pov_drop:.1f}pp 🎉)<br>
              <b style='color:{txt};font-weight:600;'>Key Risk:</b>
              Inflation spikes erode real gains, especially for B40 households
            </div>
          </div>

        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Some datasets are missing. Run notebooks 00 and 01 first to generate clean CSVs.")