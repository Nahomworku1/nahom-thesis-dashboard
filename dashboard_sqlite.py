"""
=============================================================================
Nahom Thesis AI — Financial Performance Dashboard
File  : dashboard_pro.py
RUN   : python -m streamlit run dashboard_pro.py
=============================================================================
"""
import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3, os

st.set_page_config(
    page_title="Nahom Thesis AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

# ══════════════════════════════════════════════════════════════════════════════
# THEME
# ══════════════════════════════════════════════════════════════════════════════
def apply_theme():
    dk = st.session_state.dark_mode
    if dk:
        bg0,bg1,bg2,bg3,bg4 = "#020409","#070d1a","#0a1122","#0f172a","#1e293b"
        line = "#1e293b"
        text,text2,text3 = "#cbd5e1","#64748b","#334155"
        c1,c2,c3,c4,c5   = "#00f0ff","#7c3aed","#10b981","#f59e0b","#ef4444"
        plot_bg  = "rgba(7,13,26,0.95)"
        paper_bg = "rgba(0,0,0,0)"
    else:
        bg0,bg1,bg2,bg3,bg4 = "#f0f4f8","#e8edf3","#ffffff","#f0f4f8","#dde3ec"
        line = "#dde3ec"
        text,text2,text3 = "#1e293b","#475569","#94a3b8"
        c1,c2,c3,c4,c5   = "#0284c7","#7c3aed","#059669","#d97706","#dc2626"
        plot_bg  = "rgba(240,244,248,0.95)"
        paper_bg = "rgba(240,244,248,0)"

    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;600;700&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');
*,*::before,*::after{{box-sizing:border-box;}}
html,body,[class*="css"],.stApp{{background:{bg0}!important;color:{text}!important;font-family:'IBM Plex Sans',sans-serif!important;}}
[data-testid="stSidebar"]{{background:{bg1}!important;border-right:1px solid {line}!important;}}
[data-testid="stSidebar"] *{{color:{text}!important;}}
[data-testid="stMetric"]{{background:{bg2}!important;border:1px solid {line}!important;border-radius:8px!important;padding:14px 18px!important;position:relative;overflow:hidden;}}
[data-testid="stMetric"]:hover{{border-color:{c1}!important;}}
[data-testid="stMetricLabel"]{{color:{text2}!important;font-family:'IBM Plex Mono',monospace!important;font-size:9px!important;text-transform:uppercase;letter-spacing:2px;}}
[data-testid="stMetricValue"]{{color:{text}!important;font-family:'IBM Plex Mono',monospace!important;font-size:22px!important;font-weight:600!important;}}
[data-testid="stMetricDelta"]{{font-size:11px!important;font-family:'IBM Plex Mono',monospace!important;}}
.stTabs [data-baseweb="tab-list"]{{background:{bg2}!important;border:1px solid {line}!important;border-radius:6px!important;padding:3px!important;gap:2px!important;}}
.stTabs [data-baseweb="tab"]{{background:transparent!important;color:{text2}!important;border-radius:4px!important;font-family:'IBM Plex Mono',monospace!important;font-size:10px!important;text-transform:uppercase;letter-spacing:1px;padding:7px 14px!important;border:none!important;}}
.stTabs [aria-selected="true"]{{background:{bg4}!important;color:{c1}!important;border:1px solid {c1}!important;}}
.stSelectbox [data-baseweb="select"]>div,.stMultiSelect [data-baseweb="select"]>div{{background:{bg2}!important;border:1px solid {line}!important;border-radius:6px!important;color:{text}!important;}}
[data-testid="stRadio"]>label{{display:none!important;}}
[data-testid="stRadio"] input[type="radio"]{{display:none!important;}}
[data-testid="stRadio"] label{{background:transparent!important;border:none!important;border-left:2px solid transparent!important;border-radius:0 6px 6px 0!important;padding:9px 12px!important;cursor:pointer!important;display:flex!important;align-items:center!important;gap:8px!important;margin:1px 0!important;}}
[data-testid="stRadio"] label:hover{{background:{bg3}!important;}}
[data-testid="stRadio"] label p{{display:block!important;font-family:'IBM Plex Mono',monospace!important;font-size:11px!important;color:{text2}!important;margin:0!important;}}
[data-testid="stRadio"] label>div:first-child{{display:none!important;}}
[data-testid="stRadio"] label:has(input:checked){{background:linear-gradient(90deg,{c1}18,transparent)!important;border-left:2px solid {c1}!important;}}
[data-testid="stRadio"] label:has(input:checked) p{{color:{c1}!important;font-weight:600!important;}}
.stDataFrame{{border-radius:8px!important;border:1px solid {line}!important;overflow:hidden;}}
.block-container{{padding:1.2rem 2rem 2rem!important;max-width:100%!important;}}
#MainMenu,footer,header{{visibility:hidden!important;height:0!important;}}
::-webkit-scrollbar{{width:3px;height:3px;}}
::-webkit-scrollbar-track{{background:{bg1};}}
::-webkit-scrollbar-thumb{{background:{bg4};border-radius:2px;}}
hr{{border:none;border-top:1px solid {line}!important;margin:10px 0!important;}}
.stButton>button{{background:{bg2}!important;border:1px solid {line}!important;color:{text}!important;font-family:'IBM Plex Mono',monospace!important;font-size:10px!important;border-radius:6px!important;padding:6px 14px!important;width:100%;}}
.stButton>button:hover{{border-color:{c1}!important;color:{c1}!important;}}
</style>""", unsafe_allow_html=True)

    return dict(bg0=bg0,bg1=bg1,bg2=bg2,bg3=bg3,bg4=bg4,line=line,
                text=text,text2=text2,text3=text3,
                c1=c1,c2=c2,c3=c3,c4=c4,c5=c5,
                plot_bg=plot_bg,paper_bg=paper_bg,dk=dk)

# ══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════
INDUSTRY_COLORS = {
    "Technology":"#00f0ff","Finance":"#f59e0b","Healthcare":"#10b981",
    "Consumer":"#a78bfa","Energy":"#ef4444","Industrial":"#6366f1","Telecom":"#fb923c",
}
COLOR_SEQ = list(INDUSTRY_COLORS.values())
MODEL_COLORS = {
    "Linear Regression":"#00f0ff","Random Forest":"#f59e0b",
    "XGBoost":"#10b981","LSTM":"#ef4444",
}
MODEL_STATS = {
    "Linear Regression":{"rmse":17.51,"mae":10.16,"mape":6.1, "rank":"#1 Revenue"},
    "Random Forest":    {"rmse":36.80,"mae":22.18,"mape":8.8, "rank":"#3 Ensemble"},
    "XGBoost":          {"rmse":27.92,"mae":16.74,"mape":8.8, "rank":"#2 Profit"},
    "LSTM":             {"rmse":41.97,"mae":33.70,"mape":25.0,"rank":"#4 Deep Learning"},
}

def BL(T, height=400, title="", **extra):
    base = dict(
        paper_bgcolor=T["paper_bg"], plot_bgcolor=T["plot_bg"],
        font=dict(family="IBM Plex Mono",color=T["text2"],size=11),
        title=dict(text=title,font=dict(family="IBM Plex Mono",color=T["text"],size=13)),
        legend=dict(bgcolor="rgba(0,0,0,0.3)",bordercolor=T["line"],borderwidth=1,
                    font=dict(size=10,color=T["text2"])),
        margin=dict(l=16,r=16,t=48,b=16),
        xaxis=dict(gridcolor=T["bg3"],linecolor=T["line"],tickfont=dict(size=9,color=T["text2"])),
        yaxis=dict(gridcolor=T["bg3"],linecolor=T["line"],tickfont=dict(size=9,color=T["text2"])),
        hoverlabel=dict(bgcolor=T["bg2"],bordercolor=T["line"],
                        font=dict(family="IBM Plex Mono",size=11,color=T["text"])),
        height=height,
    )
    base.update(extra)
    return base

# ══════════════════════════════════════════════════════════════════════════════
# DATA — SQLite (works locally AND on Streamlit Cloud)
# ══════════════════════════════════════════════════════════════════════════════
DB_PATH = "thesis.db"   # same folder as dashboard_pro.py

@st.cache_data(show_spinner=False)
def load_all_data():
    if not os.path.exists(DB_PATH):
        st.error(f"thesis.db not found! Run convert_to_sqlite.py first.")
        st.stop()

    conn = sqlite3.connect(DB_PATH)

    fin = pd.read_sql("""
        SELECT c.name company, c.industry, fr.year,
               fr.total_revenue revenue, fr.net_profit profit, fr.total_cost cost
        FROM financial_report fr JOIN company c ON c.company_id=fr.company_id
        ORDER BY c.name, fr.year
    """, conn)
    fin["profit_margin"] = fin["profit"] / fin["revenue"] * 100
    fin["cost_ratio"]    = fin["cost"]   / fin["revenue"] * 100
    fin["rev_b"]  = fin["revenue"] / 1e9
    fin["prof_b"] = fin["profit"]  / 1e9
    fin["cost_b"] = fin["cost"]    / 1e9

    rev = pd.read_sql("""
        SELECT c.name company, c.industry, fr.year, rs.source_name, rs.amount
        FROM revenue_source rs
        JOIN financial_report fr ON fr.report_id=rs.report_id
        JOIN company c ON c.company_id=fr.company_id
    """, conn)

    exp = pd.read_sql("""
        SELECT c.name company, c.industry, fr.year, e.category, e.amount
        FROM expense e
        JOIN financial_report fr ON fr.report_id=e.report_id
        JOIN company c ON c.company_id=fr.company_id
    """, conn)

    kpi = pd.read_sql("""
        SELECT c.name company, c.industry, fr.year, k.kpi_name, ROUND(k.value,2) value
        FROM kpi k
        JOIN financial_report fr ON fr.report_id=k.report_id
        JOIN company c ON c.company_id=fr.company_id
    """, conn)

    fcast = pd.read_sql("""
        SELECT c.name company, c.industry, fm.year,
               fm.predicted_revenue pred_rev, fm.predicted_profit pred_prof,
               fm.model_type, fm.rmse, fm.mae
        FROM forecast_model fm JOIN company c ON c.company_id=fm.company_id
    """, conn)

    conn.close()
    return fin, rev, exp, kpi, fcast

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def fmt(v, d=1):
    if pd.isna(v): return "N/A"
    s = "-" if v < 0 else ""
    a = abs(v)
    if a >= 1e12: return f"{s}${a/1e12:.{d}f}T"
    if a >= 1e9:  return f"{s}${a/1e9:.{d}f}B"
    if a >= 1e6:  return f"{s}${a/1e6:.{d}f}M"
    return f"{s}${a:,.0f}"

def filt(df, ind, yr, ic="industry", yc="year"):
    d = df.copy()
    if ind != "All Industries": d = d[d[ic] == ind]
    return d[(d[yc] >= yr[0]) & (d[yc] <= yr[1])]

def sec_hdr(title, subtitle, T, accent=None):
    acc = accent or T["c1"]
    st.markdown(f"""
<div style="margin-bottom:20px;padding-bottom:12px;border-bottom:1px solid {T['line']}">
  <h1 style="font-family:'IBM Plex Mono';font-size:22px;color:{T['text']};font-weight:600;margin:0">{title}</h1>
  <p style="color:{T['text2']};font-size:12px;margin-top:4px;font-family:'IBM Plex Mono'">{subtitle}</p>
  <div style="width:40px;height:2px;background:{acc};margin-top:10px;border-radius:1px"></div>
</div>""", unsafe_allow_html=True)

def ticker_html(label, val, up, T):
    c = T["c3"] if up else T["c5"]
    arr = "▲" if up else "▼"
    return (f'<span style="display:inline-flex;align-items:center;gap:5px;background:{T["bg2"]};'
            f'border:1px solid {T["line"]};border-radius:4px;padding:3px 8px;'
            f'font-family:\'IBM Plex Mono\';font-size:10px;margin:2px">'
            f'<span style="color:{T["text2"]}">{label}</span>'
            f'<span style="color:{c}">{arr} {val}</span></span>')

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
def render_sidebar(fin, T):
    with st.sidebar:
        moon = "☀️  Day Mode" if st.session_state.dark_mode else "🌙 Night Mode"
        st.markdown(f"""
<div style="padding:18px 16px 14px;border-bottom:1px solid {T['line']}">
  <div style="display:flex;align-items:center;gap:10px">
    <div style="width:36px;height:36px;background:linear-gradient(135deg,{T['c1']},{T['c2']});
                border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:18px">📊</div>
    <div>
      <div style="font-family:'IBM Plex Mono';font-size:14px;font-weight:700;color:{T['text']}">Nahom Thesis AI</div>
      <div style="font-size:8px;color:{T['text2']};letter-spacing:2px;text-transform:uppercase;font-family:'IBM Plex Mono'">Financial Dashboard</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        if st.button(moon, key="theme_btn"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-family:IBM Plex Mono;font-size:8px;color:{T['text3']};text-transform:uppercase;letter-spacing:3px;margin-bottom:6px'>Navigation</div>", unsafe_allow_html=True)

        page = st.radio("nav", [
            "⬡  Market Overview",
            "📈  Financial Analysis",
            "💵  Revenue & Expenses",
            "🤖  AI Forecasting",
            "🔬  Company Deep Dive",
            "📋  Data Explorer",
        ], label_visibility="collapsed")

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-family:IBM Plex Mono;font-size:8px;color:{T['text3']};text-transform:uppercase;letter-spacing:3px;margin-bottom:6px'>Filters</div>", unsafe_allow_html=True)

        industries = ["All Industries"] + sorted(fin["industry"].unique().tolist())
        sel_ind = st.selectbox("Sector", industries, label_visibility="collapsed")
        yr = st.slider("Year Range", 2015, 2024, (2015, 2024))
        companies = sorted(fin["company"].unique().tolist())
        if sel_ind != "All Industries":
            companies = sorted(fin[fin.industry == sel_ind]["company"].unique().tolist())
        sel_co = st.selectbox("Company", companies, label_visibility="collapsed")

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f"""
<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px">
  <div style="background:{T['bg2']};border:1px solid {T['line']};border-radius:6px;padding:10px">
    <div style="font-size:8px;color:{T['text2']};font-family:'IBM Plex Mono';text-transform:uppercase">Companies</div>
    <div style="font-size:20px;color:{T['c1']};font-family:'IBM Plex Mono';font-weight:700">25</div>
  </div>
  <div style="background:{T['bg2']};border:1px solid {T['line']};border-radius:6px;padding:10px">
    <div style="font-size:8px;color:{T['text2']};font-family:'IBM Plex Mono';text-transform:uppercase">Years</div>
    <div style="font-size:20px;color:{T['c3']};font-family:'IBM Plex Mono';font-weight:700">10</div>
  </div>
  <div style="background:{T['bg2']};border:1px solid {T['line']};border-radius:6px;padding:10px">
    <div style="font-size:8px;color:{T['text2']};font-family:'IBM Plex Mono';text-transform:uppercase">Records</div>
    <div style="font-size:20px;color:{T['c4']};font-family:'IBM Plex Mono';font-weight:700">3K+</div>
  </div>
  <div style="background:{T['bg2']};border:1px solid {T['line']};border-radius:6px;padding:10px">
    <div style="font-size:8px;color:{T['text2']};font-family:'IBM Plex Mono';text-transform:uppercase">ML Models</div>
    <div style="font-size:20px;color:{T['c2']};font-family:'IBM Plex Mono';font-weight:700">4</div>
  </div>
</div>
<div style="margin-top:8px;font-size:8px;color:{T['text3']};text-align:center;font-family:'IBM Plex Mono'">SEC EDGAR XBRL API · 2015–2024</div>
""", unsafe_allow_html=True)

    return page, sel_ind, yr, sel_co

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
def pg_overview(fin, fcast, ind, yr, T):
    sec_hdr("Market Overview",
            f"AI-Enhanced Financial Performance · {yr[0]}–{yr[1]} · 25 Companies · 7 Sectors", T)
    df = filt(fin, ind, yr)

    co24 = fin[fin.year == 2024].sort_values("revenue", ascending=False).head(8)
    tickers = ""
    for _, r in co24.iterrows():
        prev = fin[(fin.company == r.company) & (fin.year == 2023)]
        if not prev.empty:
            chg = (r.revenue - prev.revenue.values[0]) / prev.revenue.values[0] * 100
            tickers += ticker_html(r.company[:6].upper(), f"{chg:+.1f}%", chg >= 0, T)
    st.markdown(f"""
<div style="background:{T['bg2']};border:1px solid {T['line']};border-radius:6px;
            padding:8px 14px;margin-bottom:16px;display:flex;flex-wrap:wrap;gap:4px;align-items:center">
  <span style="font-family:'IBM Plex Mono';font-size:8px;color:{T['c1']};text-transform:uppercase;letter-spacing:2px;margin-right:8px">2024 YoY ▸</span>
  {tickers}
</div>""", unsafe_allow_html=True)

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    with c1: st.metric("Total Revenue",     fmt(df.revenue.sum()))
    with c2: st.metric("Net Profit",        fmt(df.profit.sum()))
    with c3: st.metric("Avg Profit Margin", f"{df.profit_margin.mean():.1f}%")
    with c4: st.metric("Avg Cost Ratio",    f"{df.cost_ratio.mean():.1f}%")
    with c5: st.metric("Companies",         str(df.company.nunique()))
    with c6: st.metric("Data Points",       f"{len(df):,}")

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        grp = df.groupby(["industry","year"])["revenue"].sum().reset_index()
        fig = go.Figure()
        for nm, clr in INDUSTRY_COLORS.items():
            d2 = grp[grp.industry == nm]
            if d2.empty: continue
            rgb = bytes.fromhex(clr.lstrip("#"))
            fig.add_trace(go.Scatter(
                x=d2.year, y=d2.revenue/1e9, name=nm,
                line=dict(color=clr,width=2), mode="lines+markers", marker=dict(size=5),
                fill="tozeroy", fillcolor=f"rgba({rgb[0]},{rgb[1]},{rgb[2]},0.04)",
                hovertemplate=f"<b>{nm}</b><br>%{{x}}: $%{{y:.1f}}B<extra></extra>",
            ))
        fig.update_layout(**BL(T, 320, "Total Revenue by Industry (USD Billions)"))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    with col2:
        share = df.groupby("industry")["revenue"].sum().reset_index()
        fig2 = go.Figure(go.Pie(
            labels=share.industry, values=share.revenue, hole=0.7,
            marker=dict(colors=[INDUSTRY_COLORS.get(i,"#555") for i in share.industry],
                        line=dict(color=T["bg0"],width=3)),
            textinfo="none",
            hovertemplate="<b>%{label}</b><br>%{percent}<extra></extra>",
        ))
        fig2.add_annotation(text=f"${df.revenue.sum()/1e12:.1f}T", x=0.5, y=0.5,
                            showarrow=False,font=dict(size=14,color=T["text"],family="IBM Plex Mono"))
        fig2.update_layout(**BL(T, 320, "Revenue Mix", margin=dict(l=0,r=0,t=48,b=0)))
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    col3, col4 = st.columns(2)
    with col3:
        top = df.groupby(["company","industry"])["revenue"].mean().reset_index()
        top = top.nlargest(10,"revenue").sort_values("revenue")
        fig3 = go.Figure(go.Bar(
            x=top.revenue/1e9, y=top.company, orientation="h",
            marker=dict(color=[INDUSTRY_COLORS.get(i,"#555") for i in top.industry],
                        line=dict(color="rgba(0,0,0,0)"),opacity=0.85),
            text=[fmt(v,0) for v in top.revenue],
            textposition="outside",textfont=dict(size=9,color=T["text2"]),
            hovertemplate="<b>%{y}</b><br>$%{x:.1f}B avg<extra></extra>",
        ))
        fig3.update_layout(**BL(T, 340, "Top 10 Companies — Avg Revenue",
                                margin=dict(l=140,r=60,t=48,b=16)))
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
    with col4:
        cdf = df.groupby(["company","industry"]).agg(
            rev=("revenue","mean"),margin=("profit_margin","mean")).reset_index()
        fig4 = go.Figure()
        for nm, clr in INDUSTRY_COLORS.items():
            d2 = cdf[cdf.industry == nm]
            if d2.empty: continue
            fig4.add_trace(go.Scatter(
                x=d2.rev/1e9, y=d2.margin, mode="markers+text", name=nm,
                marker=dict(size=10,color=clr,opacity=0.8,line=dict(color=clr,width=1)),
                text=d2.company.str[:5], textposition="top center",
                textfont=dict(size=7,color=T["text2"]),
                hovertemplate="<b>%{text}</b><br>$%{x:.0f}B · %{y:.1f}%<extra></extra>",
            ))
        fig4.add_hline(y=0, line_color=T["c5"], line_dash="dot", opacity=0.5)
        fig4.update_layout(**BL(T, 340, "Revenue vs Profit Margin"))
        st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — FINANCIAL ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
def pg_financial(fin, ind, yr, T):
    sec_hdr("Financial Analysis","Profit margins · Cost ratios · YoY growth · Rankings",T,T["c3"])
    df = filt(fin, ind, yr)
    t1,t2,t3,t4,t5 = st.tabs(["🔥 Margin Heatmap","📉 YoY Growth","⚖️ Cost Analysis","🏆 Rankings","📊 Multi-Metric"])

    with t1:
        pivot = df.pivot_table(index="company",columns="year",values="profit_margin")
        pivot = pivot.loc[pivot.mean(axis=1).sort_values(ascending=False).index]
        fig = go.Figure(go.Heatmap(
            z=np.round(pivot.values,1), x=[str(c) for c in pivot.columns], y=pivot.index.tolist(),
            colorscale=[[0,"#7f1d1d"],[0.3,"#dc2626"],[0.5,T["bg3"]],[0.7,"#059669"],[1,"#064e3b"]],
            zmid=0,
            text=[[f"{v:.0f}%" if not np.isnan(v) else "" for v in row] for row in pivot.values],
            texttemplate="%{text}", textfont=dict(size=8,color="rgba(255,255,255,0.85)"),
            hovertemplate="<b>%{y}</b> %{x}<br>Margin: %{z:.1f}%<extra></extra>",
            colorbar=dict(title=dict(text="Margin %",font=dict(color=T["text2"],size=10)),
                         tickfont=dict(color=T["text2"],size=9),thickness=10),
        ))
        fig.update_layout(**BL(T, 660, "Profit Margin % Heatmap — All 25 Companies",
                               margin=dict(l=180,r=80,t=50,b=20),
                               xaxis=dict(gridcolor=T["bg3"],linecolor=T["line"],
                                          tickfont=dict(size=9,color=T["text2"]),side="top")))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with t2:
        grp = df.sort_values(["company","year"]).copy()
        grp["yoy"] = grp.groupby("company")["revenue"].pct_change() * 100
        grp = grp.dropna(subset=["yoy"])
        sel = st.multiselect("Companies", sorted(grp.company.unique()),
                             default=sorted(grp.company.unique())[:7], key="yoy_sel")
        fig = go.Figure()
        for i, co in enumerate(sel or []):
            d2 = grp[grp.company == co]
            clr = INDUSTRY_COLORS.get(d2.industry.iloc[0], COLOR_SEQ[i%7])
            fig.add_trace(go.Scatter(x=d2.year, y=d2.yoy, name=co,
                line=dict(color=clr,width=2), mode="lines+markers", marker=dict(size=6),
                hovertemplate=f"<b>{co}</b> %{{x}}: %{{y:.1f}}%<extra></extra>"))
        fig.add_hline(y=0, line_color=T["c5"], line_dash="dot", opacity=0.5)
        fig.add_vrect(x0=2019.5,x1=2020.5,fillcolor=T["c4"],opacity=0.05,line_width=0,
                      annotation_text="COVID-19",annotation_font_color=T["c4"],annotation_font_size=9)
        fig.update_layout(**BL(T, 420, "Year-over-Year Revenue Growth %"))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with t3:
        cdf = df.groupby(["company","industry"]).agg(
            avg_cost_ratio=("cost_ratio","mean"),avg_revenue=("revenue","mean"),
            avg_margin=("profit_margin","mean")).reset_index()
        col1,col2 = st.columns(2)
        with col1:
            cs = cdf.sort_values("avg_cost_ratio")
            fig = go.Figure(go.Bar(
                x=cs.avg_cost_ratio, y=cs.company, orientation="h",
                marker=dict(color=[INDUSTRY_COLORS.get(i,"#555") for i in cs.industry],
                            line=dict(color="rgba(0,0,0,0)"),opacity=0.85),
                text=[f"{v:.0f}%" for v in cs.avg_cost_ratio],
                textposition="outside",textfont=dict(size=9,color=T["text2"])))
            fig.add_vline(x=100,line_color=T["c5"],line_dash="dash",opacity=0.5)
            fig.update_layout(**BL(T, 580, "Avg Cost Ratio % by Company",
                                   margin=dict(l=150,r=60,t=48,b=16)))
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        with col2:
            fig2 = px.scatter(cdf, x="avg_cost_ratio", y="avg_margin",
                size="avg_revenue", color="industry", text="company",
                color_discrete_map=INDUSTRY_COLORS, size_max=45,
                labels={"avg_cost_ratio":"Cost Ratio %","avg_margin":"Profit Margin %"})
            fig2.update_traces(textposition="top center",textfont=dict(size=7,color=T["text2"]))
            fig2.add_vline(x=100,line_color=T["c5"],line_dash="dot",opacity=0.4)
            fig2.add_hline(y=0,line_color=T["c5"],line_dash="dot",opacity=0.4)
            fig2.update_layout(**BL(T, 580, "Cost vs Margin Bubble Chart"))
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    with t4:
        r = df.groupby(["company","industry"]).agg(
            avg_margin=("profit_margin","mean"),avg_revenue=("revenue","mean"),
            avg_cost_r=("cost_ratio","mean"),total_revenue=("revenue","sum"),
        ).reset_index().sort_values("avg_margin",ascending=False).reset_index(drop=True)
        r.index += 1
        d = r.copy()
        d["avg_revenue"]   = d["avg_revenue"].apply(fmt)
        d["total_revenue"] = d["total_revenue"].apply(fmt)
        d["avg_margin"]    = d["avg_margin"].apply(lambda x: f"{x:.1f}%")
        d["avg_cost_r"]    = d["avg_cost_r"].apply(lambda x: f"{x:.1f}%")
        d.columns = ["Company","Industry","Avg Margin","Avg Revenue","Avg Cost Ratio","Total Revenue"]
        st.dataframe(d, use_container_width=True, height=560)

    with t5:
        sel2 = st.multiselect("Companies", sorted(df.company.unique()),
                              default=sorted(df.company.unique())[:5], key="mm_sel")
        if sel2:
            d2 = df[df.company.isin(sel2)]
            fig = make_subplots(rows=2,cols=2,shared_xaxes=False,
                subplot_titles=["Revenue ($B)","Net Profit ($B)","Profit Margin %","Cost Ratio %"],
                vertical_spacing=0.14,horizontal_spacing=0.08)
            for i, co in enumerate(sel2):
                dc = d2[d2.company == co].sort_values("year")
                clr = INDUSTRY_COLORS.get(dc.industry.iloc[0], COLOR_SEQ[i%7])
                kw = dict(x=dc.year,name=co,line=dict(color=clr,width=2),
                          mode="lines+markers",marker=dict(size=5),
                          hovertemplate=f"<b>{co}</b> %{{x}}: %{{y:.1f}}<extra></extra>")
                fig.add_trace(go.Scatter(y=dc.rev_b,         **kw,showlegend=True),  1,1)
                fig.add_trace(go.Scatter(y=dc.prof_b,        **kw,showlegend=False), 1,2)
                fig.add_trace(go.Scatter(y=dc.profit_margin, **kw,showlegend=False), 2,1)
                fig.add_trace(go.Scatter(y=dc.cost_ratio,    **kw,showlegend=False), 2,2)
            ax = dict(gridcolor=T["bg3"],linecolor=T["line"],tickfont=dict(size=8,color=T["text2"]))
            fig.update_layout(paper_bgcolor=T["paper_bg"],plot_bgcolor=T["plot_bg"],
                font=dict(family="IBM Plex Mono",color=T["text2"]),height=560,
                legend=dict(bgcolor="rgba(0,0,0,0.3)",bordercolor=T["line"],
                            borderwidth=1,font=dict(size=10,color=T["text2"])),
                xaxis=ax,xaxis2=ax,xaxis3=ax,xaxis4=ax,yaxis=ax,yaxis2=ax,yaxis3=ax,yaxis4=ax)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — REVENUE & EXPENSES
# ══════════════════════════════════════════════════════════════════════════════
def pg_rev_exp(fin, rev, exp, ind, yr, T):
    sec_hdr("Revenue & Expense Breakdown","Source analysis · Category distribution · Industry comparison",T,T["c4"])
    rv = filt(rev, ind, yr); ep = filt(exp, ind, yr); df = filt(fin, ind, yr)
    t1,t2,t3,t4 = st.tabs(["💵 Revenue Sources","💸 Expense Categories","🌐 Industry View","⏱️ Time Series"])

    with t1:
        col1,col2 = st.columns(2)
        with col1:
            grp = rv.groupby(["industry","source_name"])["amount"].sum().reset_index()
            grp["pct"] = grp.groupby("industry")["amount"].transform(lambda x: x/x.sum()*100)
            fig = px.bar(grp,x="industry",y="pct",color="source_name",barmode="stack",
                color_discrete_sequence=COLOR_SEQ,
                text=grp["pct"].apply(lambda x: f"{x:.0f}%" if x>8 else ""),
                labels={"pct":"% of Revenue","source_name":"Source","industry":""})
            fig.update_traces(textposition="inside",textfont=dict(size=9,color="white"))
            fig.update_layout(**BL(T,380,"Revenue Source Mix % by Industry"))
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
        with col2:
            ts = rv.groupby("source_name")["amount"].sum().reset_index()
            fig2 = go.Figure(go.Pie(labels=ts.source_name,values=ts.amount,hole=0.55,
                marker=dict(colors=COLOR_SEQ[:len(ts)],line=dict(color=T["bg0"],width=3)),
                textinfo="label+percent",textfont=dict(size=9,color=T["text"])))
            fig2.update_layout(**BL(T,380,"Revenue Source Share",showlegend=False,margin=dict(l=10,r=10,t=48,b=10)))
            st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})
        sb = rv.groupby(["industry","source_name"])["amount"].sum().reset_index()
        fig3 = px.sunburst(sb,path=["industry","source_name"],values="amount",
                           color="industry",color_discrete_map=INDUSTRY_COLORS)
        fig3.update_layout(**BL(T,420,"Revenue Hierarchy",margin=dict(l=0,r=0,t=48,b=0)))
        st.plotly_chart(fig3,use_container_width=True,config={"displayModeBar":False})

    with t2:
        col1,col2 = st.columns(2)
        with col1:
            grp = ep.groupby(["industry","category"])["amount"].sum().reset_index()
            grp["pct"] = grp.groupby("industry")["amount"].transform(lambda x: x/x.sum()*100)
            fig = px.bar(grp,x="industry",y="pct",color="category",barmode="stack",
                color_discrete_sequence=COLOR_SEQ,
                text=grp["pct"].apply(lambda x: f"{x:.0f}%" if x>8 else ""),
                labels={"pct":"% of Expenses","category":"Category","industry":""})
            fig.update_traces(textposition="inside",textfont=dict(size=9,color="white"))
            fig.update_layout(**BL(T,380,"Expense Category Mix % by Industry"))
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
        with col2:
            te = ep.groupby("category")["amount"].sum().reset_index().sort_values("amount")
            fig2 = go.Figure(go.Bar(x=te.amount/1e9,y=te.category,orientation="h",
                marker=dict(color=COLOR_SEQ[:len(te)],line=dict(color="rgba(0,0,0,0)")),
                text=[fmt(v) for v in te.amount],textposition="outside",textfont=dict(size=9,color=T["text2"])))
            fig2.update_layout(**BL(T,380,"Total by Category ($B)",margin=dict(l=160,r=80,t=48,b=16)))
            st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})

    with t3:
        comp = df.groupby("industry").agg(rev=("revenue","sum"),cost=("cost","sum"),prof=("profit","sum")).reset_index()
        fig = go.Figure()
        for name,clr,col in [("Revenue",T["c1"],"rev"),("Cost",T["c5"],"cost"),("Profit",T["c3"],"prof")]:
            fig.add_trace(go.Bar(name=name,x=comp.industry,y=comp[col]/1e9,marker_color=clr,opacity=0.85))
        fig.update_layout(**BL(T,400,"Revenue vs Cost vs Profit by Industry ($B)",barmode="group"))
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

    with t4:
        col1,col2 = st.columns(2)
        with col1:
            rt = rv.groupby(["year","source_name"])["amount"].sum().reset_index()
            fig = px.area(rt,x="year",y="amount",color="source_name",color_discrete_sequence=COLOR_SEQ,
                          labels={"amount":"Revenue ($)","source_name":"Source"})
            fig.update_layout(**BL(T,340,"Revenue Sources Over Time"))
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
        with col2:
            et = ep.groupby(["year","category"])["amount"].sum().reset_index()
            fig2 = px.area(et,x="year",y="amount",color="category",color_discrete_sequence=COLOR_SEQ,
                           labels={"amount":"Expense ($)","category":"Category"})
            fig2.update_layout(**BL(T,340,"Expense Categories Over Time"))
            st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — AI FORECASTING
# ══════════════════════════════════════════════════════════════════════════════
def pg_ml(fin, fcast, ind, yr, T):
    sec_hdr("AI Forecasting Results","4 Models · Linear Regression · Random Forest · XGBoost · LSTM · 2025",T,T["c2"])
    fc = fcast[fcast.industry == ind].copy() if ind != "All Industries" else fcast.copy()
    t1,t2,t3,t4 = st.tabs(["🏅 Model Performance","🔮 2025 Forecasts","📊 Model Comparison","📋 Forecast Table"])

    with t1:
        cols = st.columns(4)
        for col,(model,stats) in zip(cols,MODEL_STATS.items()):
            clr = MODEL_COLORS[model]
            mc  = T["c3"] if stats["mape"]<10 else T["c4"] if stats["mape"]<20 else T["c5"]
            col.markdown(f"""
<div style="background:{T['bg2']};border:1px solid {T['line']};border-radius:8px;padding:16px;border-top:2px solid {clr}">
  <div style="font-family:'IBM Plex Mono';font-size:8px;color:{clr};text-transform:uppercase;letter-spacing:2px">{model}</div>
  <div style="font-size:9px;color:{T['text2']};margin:4px 0 12px;font-family:'IBM Plex Mono'">{stats['rank']}</div>
  <div style="display:grid;gap:8px">
    <div style="background:{T['bg3']};border-radius:4px;padding:8px">
      <div style="font-size:8px;color:{T['text2']};font-family:'IBM Plex Mono'">RMSE</div>
      <div style="font-size:18px;color:{T['text']};font-family:'IBM Plex Mono';font-weight:600">${stats['rmse']:.1f}B</div>
    </div>
    <div style="background:{T['bg3']};border-radius:4px;padding:8px">
      <div style="font-size:8px;color:{T['text2']};font-family:'IBM Plex Mono'">MAE</div>
      <div style="font-size:18px;color:{T['text']};font-family:'IBM Plex Mono';font-weight:600">${stats['mae']:.1f}B</div>
    </div>
    <div style="background:{T['bg3']};border-radius:4px;padding:8px">
      <div style="font-size:8px;color:{T['text2']};font-family:'IBM Plex Mono'">MAPE</div>
      <div style="font-size:18px;color:{mc};font-family:'IBM Plex Mono';font-weight:600">{stats['mape']:.1f}%</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        fig = go.Figure()
        cats = ["RMSE Score","MAE Score","MAPE Score","Stability","Interpretability"]
        interp = {"Linear Regression":95,"Random Forest":70,"XGBoost":65,"LSTM":40}
        stab   = {"Linear Regression":80,"Random Forest":85,"XGBoost":88,"LSTM":55}
        mr,mm,mp = (max(s[k] for s in MODEL_STATS.values()) for k in ["rmse","mae","mape"])
        for model,clr in MODEL_COLORS.items():
            s = MODEL_STATS[model]
            v = [(1-s["rmse"]/mr)*100,(1-s["mae"]/mm)*100,(1-s["mape"]/mp)*100,stab[model],interp[model]]
            v.append(v[0])
            rgb = bytes.fromhex(clr.lstrip("#"))
            fig.add_trace(go.Scatterpolar(r=v,theta=cats+[cats[0]],name=model,fill="toself",
                line=dict(color=clr,width=2),fillcolor=f"rgba({rgb[0]},{rgb[1]},{rgb[2]},0.08)"))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True,range=[0,100],gridcolor=T["line"],
                                       linecolor=T["line"],tickfont=dict(color=T["text2"],size=8)),
                       angularaxis=dict(gridcolor=T["line"],linecolor=T["line"],
                                        tickfont=dict(color=T["text"],size=10)),bgcolor=T["plot_bg"]),
            paper_bgcolor=T["paper_bg"],font=dict(family="IBM Plex Mono",color=T["text2"]),
            title=dict(text="Model Capability Radar",font=dict(color=T["text"],size=13)),
            legend=dict(bgcolor="rgba(0,0,0,0.3)",bordercolor=T["line"],borderwidth=1,font=dict(size=10,color=T["text2"])),
            height=420)
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

    with t2:
        sel_m = st.selectbox("Model",sorted(fc.model_type.unique()),
            index=list(sorted(fc.model_type.unique())).index("XGBoost")
            if "XGBoost" in fc.model_type.unique() else 0)
        dfc  = fc[fc.model_type==sel_m].sort_values("pred_rev",  ascending=True)
        dfc2 = fc[fc.model_type==sel_m].sort_values("pred_prof", ascending=True)
        col1,col2 = st.columns(2)
        with col1:
            fig = go.Figure(go.Bar(x=dfc.pred_rev/1e9,y=dfc.company,orientation="h",
                marker=dict(color=[INDUSTRY_COLORS.get(i,"#555") for i in dfc.industry],
                            line=dict(color="rgba(0,0,0,0)"),opacity=0.85),
                text=[fmt(v,0) for v in dfc.pred_rev],textposition="outside",textfont=dict(size=9,color=T["text2"]),
                hovertemplate="<b>%{y}</b> 2025: $%{x:.1f}B<extra></extra>"))
            fig.update_layout(**BL(T,580,f"2025 Revenue — {sel_m}",margin=dict(l=160,r=80,t=48,b=16)))
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
        with col2:
            bc = [T["c5"] if v<0 else T["c3"] for v in dfc2.pred_prof]
            fig2 = go.Figure(go.Bar(x=dfc2.pred_prof/1e9,y=dfc2.company,orientation="h",
                marker=dict(color=bc,line=dict(color="rgba(0,0,0,0)"),opacity=0.85),
                text=[fmt(v,0) for v in dfc2.pred_prof],textposition="outside",textfont=dict(size=9,color=T["text2"]),
                hovertemplate="<b>%{y}</b> 2025 Profit: $%{x:.1f}B<extra></extra>"))
            fig2.add_vline(x=0,line_color=T["c5"],line_dash="dot",opacity=0.5)
            fig2.update_layout(**BL(T,580,f"2025 Profit — {sel_m}",margin=dict(l=160,r=80,t=48,b=16)))
            st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})

    with t3:
        mg = fcast.groupby("model_type").agg(avg_rmse=("rmse","mean"),avg_mae=("mae","mean")).reset_index()
        fig = make_subplots(rows=1,cols=2,subplot_titles=["RMSE ($B)","MAE ($B)"],horizontal_spacing=0.12)
        for _,row in mg.iterrows():
            clr = MODEL_COLORS.get(row.model_type,"#555")
            fig.add_trace(go.Bar(x=[row.model_type],y=[row.avg_rmse/1e9],name=row.model_type,
                marker_color=clr,opacity=0.85,showlegend=True,
                text=[f"${row.avg_rmse/1e9:.1f}B"],textposition="outside",textfont=dict(size=10,color=T["text2"])),row=1,col=1)
            fig.add_trace(go.Bar(x=[row.model_type],y=[row.avg_mae/1e9],name=row.model_type,
                marker_color=clr,opacity=0.55,showlegend=False,
                text=[f"${row.avg_mae/1e9:.1f}B"],textposition="outside",textfont=dict(size=10,color=T["text2"])),row=1,col=2)
        ax = dict(gridcolor=T["bg3"],linecolor=T["line"],tickfont=dict(size=9,color=T["text2"]))
        fig.update_layout(paper_bgcolor=T["paper_bg"],plot_bgcolor=T["plot_bg"],
            font=dict(family="IBM Plex Mono",color=T["text2"]),height=380,
            legend=dict(bgcolor="rgba(0,0,0,0.3)",bordercolor=T["line"],borderwidth=1,font=dict(size=10,color=T["text2"])),
            xaxis=ax,xaxis2=ax,yaxis=ax,yaxis2=ax)
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

    with t4:
        piv = fcast.pivot_table(index=["company","industry"],columns="model_type",
                                values="pred_rev",aggfunc="first").reset_index()
        piv.columns.name = None
        for m in MODEL_COLORS:
            if m in piv.columns: piv[m] = piv[m].apply(lambda x: fmt(x,0) if pd.notna(x) else "—")
        piv.rename(columns={"company":"Company","industry":"Industry"},inplace=True)
        st.markdown("**2025 Revenue Forecasts — All 4 Models**")
        st.dataframe(piv,use_container_width=True,height=520)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — COMPANY DEEP DIVE
# ══════════════════════════════════════════════════════════════════════════════
def pg_company(fin, rev, exp, kpi, fcast, sel_co, T):
    dfc = fin[fin.company==sel_co].sort_values("year")
    rvc = rev[rev.company==sel_co]; exc = exp[exp.company==sel_co]
    kic = kpi[kpi.company==sel_co]; fcc = fcast[fcast.company==sel_co]
    if dfc.empty: st.warning("No data."); return

    ind_nm = dfc.industry.iloc[0]; clr = INDUSTRY_COLORS.get(ind_nm,T["c1"])
    latest = dfc.iloc[-1]; prev_yr = dfc.iloc[-2] if len(dfc)>1 else latest
    rev_d  = (latest.revenue-prev_yr.revenue)/abs(prev_yr.revenue)*100
    prof_d = (latest.profit-prev_yr.profit)/abs(prev_yr.profit)*100 if prev_yr.profit!=0 else 0
    badge_clr = T["c3"] if latest.profit>0 else T["c5"]
    badge_txt = "📈 Profitable" if latest.profit>0 else "📉 Net Loss"

    st.markdown(f"""
<div style="background:linear-gradient(90deg,{clr}0a,transparent);border:1px solid {clr}33;
            border-radius:10px;padding:20px 24px;margin-bottom:20px;display:flex;align-items:center;gap:20px">
  <div style="width:56px;height:56px;border-radius:10px;background:{clr}15;border:1px solid {clr}44;
              display:flex;align-items:center;justify-content:center;font-size:24px;flex-shrink:0">🏢</div>
  <div style="flex:1">
    <h1 style="font-family:'IBM Plex Mono';font-size:24px;color:{T['text']};margin:0;font-weight:600">{sel_co}</h1>
    <div style="display:flex;gap:8px;margin-top:6px;flex-wrap:wrap">
      <span style="font-family:'IBM Plex Mono';font-size:9px;color:{clr};background:{clr}15;border:1px solid {clr}33;border-radius:4px;padding:2px 8px;text-transform:uppercase;letter-spacing:2px">{ind_nm}</span>
      <span style="font-family:'IBM Plex Mono';font-size:9px;color:{T['text2']};background:{T['bg3']};border:1px solid {T['line']};border-radius:4px;padding:2px 8px">2015–2024</span>
      <span style="font-family:'IBM Plex Mono';font-size:9px;color:{badge_clr};background:{badge_clr}15;border:1px solid {badge_clr}33;border-radius:4px;padding:2px 8px">{badge_txt}</span>
    </div>
  </div>
  <div style="text-align:right">
    <div style="font-family:'IBM Plex Mono';font-size:10px;color:{T['text2']}">2024 Revenue</div>
    <div style="font-family:'IBM Plex Mono';font-size:26px;color:{T['text']};font-weight:700">{fmt(latest.revenue)}</div>
    <div style="font-family:'IBM Plex Mono';font-size:10px;color:{'#10b981' if rev_d>=0 else '#ef4444'}">
      {'▲' if rev_d>=0 else '▼'} {abs(rev_d):.1f}% vs 2023</div>
  </div>
</div>""", unsafe_allow_html=True)

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    with c1: st.metric("2024 Revenue",    fmt(latest.revenue),   f"{rev_d:+.1f}% vs 2023")
    with c2: st.metric("2024 Net Profit", fmt(latest.profit),    f"{prof_d:+.1f}% vs 2023")
    with c3: st.metric("Profit Margin",   f"{latest.profit_margin:.1f}%")
    with c4: st.metric("Cost Ratio",      f"{latest.cost_ratio:.1f}%")
    with c5: st.metric("10Y Avg Revenue", fmt(dfc.revenue.mean()))
    with c6: st.metric("Best Margin",     f"{dfc.profit_margin.max():.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)
    col1,col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Revenue",x=dfc.year,y=dfc.rev_b,marker=dict(color=clr,opacity=0.6,line=dict(color="rgba(0,0,0,0)"))))
        fig.add_trace(go.Bar(name="Cost",x=dfc.year,y=dfc.cost_b,marker=dict(color=T["c5"],opacity=0.5,line=dict(color="rgba(0,0,0,0)"))))
        fig.add_trace(go.Scatter(name="Net Profit",x=dfc.year,y=dfc.prof_b,line=dict(color=T["c3"],width=2.5),mode="lines+markers",marker=dict(size=7)))
        fig.update_layout(**BL(T,340,f"{sel_co} — Revenue · Cost · Profit",barmode="overlay"))
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    with col2:
        fig2 = go.Figure()
        mc = T["c3"] if dfc.profit_margin.mean()>0 else T["c5"]
        fig2.add_trace(go.Scatter(x=dfc.year,y=dfc.profit_margin,name="Profit Margin %",
            fill="tozeroy",line=dict(color=mc,width=2.5),fillcolor="rgba(16,185,129,0.08)"))
        fig2.add_trace(go.Scatter(x=dfc.year,y=dfc.cost_ratio,name="Cost Ratio %",
            line=dict(color=T["c4"],width=2,dash="dot")))
        fig2.add_hline(y=0,line_dash="dot",line_color=T["c5"],opacity=0.4)
        fig2.update_layout(**BL(T,340,"Margin & Cost Ratio Trend"))
        st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})

    col3,col4 = st.columns(2)
    with col3:
        rg = rvc.groupby(["year","source_name"])["amount"].sum().reset_index()
        fig3 = px.bar(rg,x="year",y="amount",color="source_name",barmode="stack",
                      color_discrete_sequence=COLOR_SEQ,labels={"amount":"Revenue ($)","source_name":"Source"})
        fig3.update_layout(**BL(T,300,"Revenue Sources 2015–2024"))
        st.plotly_chart(fig3,use_container_width=True,config={"displayModeBar":False})
    with col4:
        eg = exc.groupby(["year","category"])["amount"].sum().reset_index()
        fig4 = px.bar(eg,x="year",y="amount",color="category",barmode="stack",
                      color_discrete_sequence=COLOR_SEQ,labels={"amount":"Expense ($)","category":"Category"})
        fig4.update_layout(**BL(T,300,"Expense Breakdown 2015–2024"))
        st.plotly_chart(fig4,use_container_width=True,config={"displayModeBar":False})

    if not kic.empty:
        st.markdown(f"<div style='font-family:IBM Plex Mono;font-size:12px;color:{T['text2']};margin:12px 0 6px'>KPI History</div>",unsafe_allow_html=True)
        kp = kic.pivot_table(index="kpi_name",columns="year",values="value").round(2)
        st.dataframe(kp,use_container_width=True,height=180)

    if not fcc.empty:
        st.markdown(f"<div style='font-family:IBM Plex Mono;font-size:12px;color:{T['text2']};margin:16px 0 8px'>2025 Forecasts — All Models</div>",unsafe_allow_html=True)
        fc_cols = st.columns(4)
        for col,(_,row) in zip(fc_cols,fcc.iterrows()):
            mc=MODEL_COLORS.get(row.model_type,"#555"); pc=T["c3"] if row.pred_prof>=0 else T["c5"]
            col.markdown(f"""
<div style="background:{T['bg2']};border:1px solid {T['line']};border-radius:8px;padding:14px;border-top:2px solid {mc}">
  <div style="font-family:'IBM Plex Mono';font-size:8px;color:{mc};text-transform:uppercase;letter-spacing:2px;margin-bottom:10px">{row.model_type}</div>
  <div style="font-size:10px;color:{T['text2']};font-family:'IBM Plex Mono'">Revenue 2025</div>
  <div style="font-family:'IBM Plex Mono';font-size:18px;color:{T['text']};font-weight:600">{fmt(row.pred_rev)}</div>
  <div style="font-size:10px;color:{T['text2']};font-family:'IBM Plex Mono';margin-top:8px">Profit 2025</div>
  <div style="font-family:'IBM Plex Mono';font-size:18px;color:{pc};font-weight:600">{fmt(row.pred_prof)}</div>
  <div style="font-family:'IBM Plex Mono';font-size:9px;color:{T['text3']};margin-top:8px">RMSE: {fmt(row.rmse,0)}</div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — DATA EXPLORER
# ══════════════════════════════════════════════════════════════════════════════
def pg_explorer(fin, rev, exp, kpi, fcast, ind, yr, T):
    sec_hdr("Data Explorer","Browse all tables with live filters",T,T["c3"])
    table = st.selectbox("Table",["financial_report","revenue_source","expense","kpi","forecast_model"])
    c1,c2,c3 = st.columns(3)
    with c1: syr = st.selectbox("Year",["All"]+list(range(2024,2014,-1)))
    with c2: si  = st.selectbox("Industry",["All"]+sorted(fin.industry.unique()),key="ex_i")
    with c3: sc  = st.selectbox("Company", ["All"]+sorted(fin.company.unique()),key="ex_c")
    dm = {"financial_report":fin,"revenue_source":rev,"expense":exp,"kpi":kpi,"forecast_model":fcast}
    ds = dm[table].copy()
    if syr!="All" and "year"     in ds.columns: ds=ds[ds.year==int(syr)]
    if si !="All" and "industry" in ds.columns: ds=ds[ds.industry==si]
    if sc !="All" and "company"  in ds.columns: ds=ds[ds.company==sc]
    for c in ds.select_dtypes(include="number").columns:
        if ds[c].abs().max()>1e6: ds[c]=ds[c].apply(lambda x: fmt(x) if pd.notna(x) else "—")
    ca,cb,cc = st.columns(3)
    ca.metric("Rows",f"{len(ds):,}"); cb.metric("Columns",str(len(ds.columns))); cc.metric("Table",table)
    st.dataframe(ds,use_container_width=True,height=500)

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    T = apply_theme()
    try:
        fin, rev, exp, kpi, fcast = load_all_data()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()
    page, ind, yr, sel_co = render_sidebar(fin, T)
    if   "Overview"  in page: pg_overview(fin, fcast, ind, yr, T)
    elif "Financial" in page: pg_financial(fin, ind, yr, T)
    elif "Revenue"   in page: pg_rev_exp(fin, rev, exp, ind, yr, T)
    elif "AI"        in page: pg_ml(fin, fcast, ind, yr, T)
    elif "Deep Dive" in page: pg_company(fin, rev, exp, kpi, fcast, sel_co, T)
    elif "Explorer"  in page: pg_explorer(fin, rev, exp, kpi, fcast, ind, yr, T)

if __name__ == "__main__":
    main()
