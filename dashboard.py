# dashboard.py
"""
NIFTY IT Analytics Dashboard
"""

import os
import sys
import subprocess
from datetime import datetime
from io import BytesIO

import pandas as pd
import plotly.express as px
import streamlit as st

# --------------------------------------------------------------------------
# Page configuration
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="NIFTY IT Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------------------------------
# Color palettes
#
# NOTE ON DARK MODE: the previous version toggled a `.dark-mode` wrapper div
# using two separate st.markdown() calls (one for the opening tag, one for
# the closing tag). That doesn't work in Streamlit — every st.markdown call
# renders into its own isolated container, so the tags never actually wrap
# the content in between and the `.dark-mode .stApp {...}` rules never
# matched anything.
#
# The fix: pick one palette per render based on session state, inject it as
# real CSS variables, and target Streamlit's actual structural elements
# (data-testid attributes) directly. No wrapper div required.
# --------------------------------------------------------------------------
LIGHT_COLORS = {
    "bg": "#F5F8F7",
    "card": "#FFFFFF",
    "text_primary": "#0B1F1B",
    "text_secondary": "#3F5D52",
    "text_muted": "#6B8478",
    "border": "#DCE7E1",
    "primary": "#155E4B",
    "secondary": "#1F7A5E",
    "accent": "#2FA37B",
    "chip_bg": "#E4F3EC",
    "positive": "#0F9D68",
    "negative": "#D64545",
    "chart_seq": ["#0B3B2E", "#155E4B", "#2FA37B", "#63C79A", "#9BDCBE", "#CDEEDD"],
}

DARK_COLORS = {
    "bg": "#0B120F",
    "card": "#121D19",
    "text_primary": "#EAF3EF",
    "text_secondary": "#BBD6C9",
    "text_muted": "#84A597",
    "border": "#233731",
    "primary": "#4FD9A6",
    "secondary": "#39B78C",
    "accent": "#7FE6BE",
    "chip_bg": "#17251F",
    "positive": "#3ADF9B",
    "negative": "#FF6B6B",
    "chart_seq": ["#CDEEDD", "#9BDCBE", "#63C79A", "#2FA37B", "#155E4B", "#0B3B2E"],
}

REQUIRED_NUMERIC_COLS = [
    "Current Revenue (Cr)",
    "Annual Revenue (Cr)",
    "Annual Profit (Cr)",
    "Total TCV",
    "Deal Wins",
    "Total Clients",
    "Profit Margin %",
]


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------
def to_numeric(series: pd.Series) -> pd.Series:
    """Coerce a column to numeric regardless of its current dtype."""
    if series.dtype == "object":
        return pd.to_numeric(series, errors="coerce")
    return series


def safe_sum(df: pd.DataFrame, col: str) -> float:
    if col not in df.columns:
        return 0.0
    s = to_numeric(df[col])
    return float(s.sum()) if s.notna().any() else 0.0


def safe_mean(df: pd.DataFrame, col: str) -> float:
    if col not in df.columns:
        return 0.0
    s = to_numeric(df[col])
    return float(s.mean()) if s.notna().any() else 0.0


def metric_card(label: str, value: str) -> str:
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """


def detail_card(label: str, value) -> str:
    return f"""
    <div class="company-detail-card">
        <div class="detail-label">{label}</div>
        <div class="detail-value">{value}</div>
    </div>
    """


def style_chart(fig, colors: dict, showlegend: bool = False, height: int = 400):
    """Apply consistent, theme-aware styling to a plotly figure."""
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=12, color=colors["text_secondary"]),
        title_font=dict(color=colors["text_primary"], size=14),
        height=height,
        margin=dict(l=40, r=40, t=50, b=40),
        showlegend=showlegend,
        legend=dict(font=dict(color=colors["text_secondary"])),
    )
    fig.update_xaxes(color=colors["text_secondary"], gridcolor=colors["border"])
    fig.update_yaxes(color=colors["text_secondary"], gridcolor=colors["border"])
    return fig


# --------------------------------------------------------------------------
# CSS
# --------------------------------------------------------------------------
def load_css(colors: dict):
    st.markdown(
        f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
            background-color: {colors['bg']};
        }}

        [data-testid="stAppViewContainer"],
        [data-testid="stAppViewContainer"] p,
        [data-testid="stAppViewContainer"] span,
        [data-testid="stAppViewContainer"] label,
        [data-testid="stMarkdownContainer"] {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: {colors['text_primary']};
        }}

        [data-testid="stHeader"] {{
            background-color: transparent;
        }}

        /* Sidebar */
        [data-testid="stSidebar"] {{
            background-color: {colors['card']};
            border-right: 1px solid {colors['border']};
        }}
        [data-testid="stSidebar"] * {{
            color: {colors['text_primary']};
        }}
        [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {{
            color: {colors['text_secondary']};
            font-weight: 500;
        }}

        .main-header {{
            font-weight: 700;
            font-size: 2.3rem;
            color: {colors['primary']};
            margin-bottom: 0.2rem;
            letter-spacing: -0.02em;
        }}

        .sub-header {{
            font-weight: 400;
            font-size: 1rem;
            color: {colors['text_secondary']};
            margin-bottom: 1.8rem;
        }}

        .metric-card {{
            background: {colors['card']};
            border-radius: 14px;
            padding: 1.1rem 1.4rem;
            border: 1px solid {colors['border']};
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            transition: transform 0.15s ease, box-shadow 0.15s ease;
            position: relative;
            overflow: hidden;
        }}
        .metric-card::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, {colors['secondary']}, {colors['accent']});
        }}
        .metric-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.12);
        }}
        .metric-label {{
            font-weight: 500;
            font-size: 0.75rem;
            color: {colors['text_muted']};
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }}
        .metric-value {{
            font-weight: 700;
            font-size: 1.7rem;
            color: {colors['text_primary']};
            margin-top: 0.25rem;
        }}

        .section-title {{
            font-weight: 600;
            font-size: 1.15rem;
            color: {colors['text_primary']};
            margin: 1.4rem 0 0.9rem 0;
            letter-spacing: -0.01em;
        }}

        .sidebar-section {{
            font-weight: 600;
            font-size: 0.75rem;
            color: {colors['text_muted']};
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin: 1.4rem 0 0.5rem 0;
        }}

        .company-detail-card {{
            background: {colors['card']};
            border-radius: 12px;
            padding: 1.3rem 1.4rem;
            border: 1px solid {colors['border']};
            margin-bottom: 0.9rem;
        }}
        .detail-label {{
            font-weight: 500;
            font-size: 0.75rem;
            color: {colors['text_muted']};
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}
        .detail-value {{
            font-weight: 600;
            font-size: 1.05rem;
            color: {colors['text_primary']};
            margin-top: 0.15rem;
        }}

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 2px;
            background-color: {colors['chip_bg']};
            border-radius: 12px;
            padding: 4px;
        }}
        .stTabs [data-baseweb="tab"] {{
            font-weight: 500;
            font-size: 0.85rem;
            border-radius: 8px;
            padding: 0.5rem 1.2rem;
            color: {colors['text_secondary']};
        }}
        .stTabs [aria-selected="true"] {{
            background-color: {colors['secondary']} !important;
            color: #ffffff !important;
        }}

        /* Buttons */
        .stButton > button, .stDownloadButton > button {{
            font-weight: 500;
            font-size: 0.85rem;
            background: {colors['secondary']};
            color: #ffffff;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1.2rem;
            transition: all 0.2s ease;
        }}
        .stButton > button:hover, .stDownloadButton > button:hover {{
            background: {colors['accent']};
            box-shadow: 0 4px 14px rgba(0,0,0,0.18);
            color: #ffffff;
        }}

        /* Dataframe */
        [data-testid="stDataFrame"] {{
            border: 1px solid {colors['border']};
            border-radius: 10px;
        }}

        /* Hide default Streamlit chrome */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        .positive {{ color: {colors['positive']}; }}
        .negative {{ color: {colors['negative']}; }}

        @media (max-width: 768px) {{
            .main-header {{ font-size: 1.5rem; }}
            .metric-value {{ font-size: 1.3rem; }}
        }}
    </style>
    """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------------------------------
# Data loading
# --------------------------------------------------------------------------
def load_data():
    """Load the most recent Excel export from the output directory."""
    output_dir = "output"
    if not os.path.exists(output_dir):
        return None

    excel_files = [
        f for f in os.listdir(output_dir)
        if f.endswith(".xlsx") and f.startswith("nifty_it_data_")
    ]
    if not excel_files:
        return None

    latest_file = sorted(excel_files)[-1]
    file_path = os.path.join(output_dir, latest_file)

    try:
        df = pd.read_excel(file_path, sheet_name="Summary")

        for col in ["Current Revenue (Cr)", "Annual Revenue (Cr)", "Annual Profit (Cr)"]:
            if col in df.columns:
                df[col] = (
                    df[col].astype(str).str.replace("₹", "", regex=False)
                    .str.replace(",", "", regex=False).str.strip()
                )
                df[col] = pd.to_numeric(df[col], errors="coerce")

        if "Total TCV" in df.columns:
            df["Total TCV"] = df["Total TCV"].astype(str).str.extract(r"([\d.]+)")[0]
            df["Total TCV"] = pd.to_numeric(df["Total TCV"], errors="coerce")

        for col in ["Deal Wins", "Total Clients", "Profit Margin %"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None


def to_excel_bytes(df: pd.DataFrame) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Summary", index=False)
    return output.getvalue()


# --------------------------------------------------------------------------
# Session state
# --------------------------------------------------------------------------
defaults = {"data": None, "dark_mode": False, "running": False}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

colors = DARK_COLORS if st.session_state.dark_mode else LIGHT_COLORS
load_css(colors)

# --------------------------------------------------------------------------
# Sidebar
# --------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        f'<p style="font-weight:700; font-size:1.3rem; color:{colors["primary"]}; '
        f'margin-bottom:0.1rem;">NIFTY IT</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<p style="font-weight:300; font-size:0.8rem; color:{colors["text_muted"]}; '
        f'margin-bottom:1.3rem;">Analytics Dashboard</p>',
        unsafe_allow_html=True,
    )

    dark_mode = st.toggle("🌙 Dark mode", value=st.session_state.dark_mode)
    if dark_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_mode
        st.rerun()

    st.markdown(f'<hr style="margin:1.3rem 0; border-color:{colors["border"]};">', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-section">Controls</p>', unsafe_allow_html=True)

    if st.button("🔄 Refresh data", use_container_width=True):
        st.session_state.running = True
        st.rerun()

    st.markdown('<p class="sidebar-section">Filters</p>', unsafe_allow_html=True)

    selected_companies = None
    rev_range = None
    deal_range = None

    if st.session_state.data is not None:
        df_full = st.session_state.data

        companies = df_full["Company Name"].unique().tolist()
        selected_companies = st.multiselect(
            "Companies", companies, default=companies, key="company_filter"
        )

        if "Current Revenue (Cr)" in df_full.columns:
            revenue_col = to_numeric(df_full["Current Revenue (Cr)"])
            min_rev = float(revenue_col.min()) if revenue_col.notna().any() else 0.0
            max_rev = float(revenue_col.max()) if revenue_col.notna().any() else 10000.0
            rev_range = st.slider(
                "Revenue range (Cr)",
                min_value=min_rev,
                max_value=max_rev,
                value=(min_rev, max_rev),
                step=100.0,
                key="rev_range",
            )

        if "Deal Wins" in df_full.columns:
            deals_col = to_numeric(df_full["Deal Wins"])
            min_deals = int(deals_col.min()) if deals_col.notna().any() else 0
            max_deals = int(deals_col.max()) if deals_col.notna().any() else 10
            deal_range = st.slider(
                "Deal wins",
                min_value=min_deals,
                max_value=max_deals,
                value=(min_deals, max_deals),
                key="deal_range",
            )

    st.markdown(f'<hr style="margin:1.3rem 0; border-color:{colors["border"]};">', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-section">Export</p>', unsafe_allow_html=True)

    if st.session_state.data is not None:
        export_df = st.session_state.data
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "📊 XLSX",
                data=to_excel_bytes(export_df),
                file_name=f"nifty_it_export_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
        with col2:
            st.download_button(
                "📄 CSV",
                data=export_df.to_csv(index=False).encode("utf-8"),
                file_name=f"nifty_it_export_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True,
            )

# --------------------------------------------------------------------------
# Main content
# --------------------------------------------------------------------------
st.markdown('<p class="main-header">NIFTY IT Index</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-header">Real-time analytics &amp; performance metrics of '
    "India's top IT companies</p>",
    unsafe_allow_html=True,
)

if st.session_state.running:
    with st.spinner("Running data pipeline... this may take a few minutes."):
        try:
            result = subprocess.run(
                [sys.executable, "main.py"], capture_output=True, text=True
            )
            if result.returncode == 0:
                st.session_state.data = load_data()
                st.success("✅ Data refreshed successfully!")
            else:
                st.error(f"❌ Pipeline failed: {result.stderr[:200]}")
        except Exception as e:
            st.error(f"❌ Error: {e}")
    st.session_state.running = False
    st.rerun()

if st.session_state.data is None:
    st.session_state.data = load_data()

if st.session_state.data is not None:
    df = st.session_state.data

    if selected_companies:
        df = df[df["Company Name"].isin(selected_companies)]
    if rev_range and "Current Revenue (Cr)" in df.columns:
        rc = to_numeric(df["Current Revenue (Cr)"])
        df = df[(rc >= rev_range[0]) & (rc <= rev_range[1])]
    if deal_range and "Deal Wins" in df.columns:
        dc = to_numeric(df["Deal Wins"])
        df = df[(dc >= deal_range[0]) & (dc <= deal_range[1])]

    if df.empty:
        st.warning("No companies match the current filters. Try widening your filter ranges.")
    else:
        tab1, tab2, tab3 = st.tabs(["📊 Overview", "🏢 Company Details", "📈 Analytics"])

        # ---------------- TAB 1: OVERVIEW ----------------
        with tab1:
            c1, c2, c3, c4, c5 = st.columns(5)
            with c1:
                st.markdown(metric_card("Total Revenue", f"₹{safe_sum(df, 'Current Revenue (Cr)'):,.0f} Cr"), unsafe_allow_html=True)
            with c2:
                st.markdown(metric_card("Average Revenue", f"₹{safe_mean(df, 'Current Revenue (Cr)'):,.0f} Cr"), unsafe_allow_html=True)
            with c3:
                st.markdown(metric_card("Total Deals", f"{safe_sum(df, 'Deal Wins'):,.0f}"), unsafe_allow_html=True)
            with c4:
                st.markdown(metric_card("Avg Margin", f"{safe_mean(df, 'Profit Margin %'):.1f}%"), unsafe_allow_html=True)
            with c5:
                st.markdown(metric_card("Total Clients", f"{safe_sum(df, 'Total Clients'):,.0f}"), unsafe_allow_html=True)

            st.markdown('<p class="section-title">Performance Overview</p>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)

            with col1:
                chart_df = df.dropna(subset=["Current Revenue (Cr)"])
                if not chart_df.empty:
                    fig = px.bar(
                        chart_df, x="Company Name", y="Current Revenue (Cr)",
                        title="Revenue by Company", color="Current Revenue (Cr)",
                        color_continuous_scale=colors["chart_seq"],
                        text="Current Revenue (Cr)",
                    )
                    fig.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
                    st.plotly_chart(style_chart(fig, colors), use_container_width=True)
                else:
                    st.info("No revenue data available for this selection.")

            with col2:
                if "Deal Wins" in df.columns:
                    scatter_df = df.dropna(subset=["Current Revenue (Cr)", "Deal Wins"])
                    if not scatter_df.empty:
                        fig = px.scatter(
                            scatter_df, x="Current Revenue (Cr)", y="Deal Wins",
                            size="Current Revenue (Cr)", color="Company Name",
                            text="Company Name", title="Revenue vs Deal Wins",
                            color_discrete_sequence=colors["chart_seq"],
                        )
                        fig.update_traces(textposition="top center")
                        st.plotly_chart(style_chart(fig, colors), use_container_width=True)
                    else:
                        st.info("No deal wins data available for this selection.")

        # ---------------- TAB 2: COMPANY DETAILS ----------------
        with tab2:
            st.markdown('<p class="section-title">Individual Company Analysis</p>', unsafe_allow_html=True)
            companies = df["Company Name"].unique().tolist()
            selected_company = st.selectbox("Select company", companies)

            if selected_company:
                row = df[df["Company Name"] == selected_company].iloc[0]

                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.markdown(detail_card("Current Revenue", f"₹{row.get('Current Revenue (Cr)', 0):,.0f} Cr"), unsafe_allow_html=True)
                with c2:
                    st.markdown(detail_card("Annual Revenue", f"₹{row.get('Annual Revenue (Cr)', 0):,.0f} Cr"), unsafe_allow_html=True)
                with c3:
                    st.markdown(detail_card("Profit Margin", f"{row.get('Profit Margin %', 0):.1f}%"), unsafe_allow_html=True)
                with c4:
                    st.markdown(detail_card("Deal Wins", f"{row.get('Deal Wins', 0):,.0f}"), unsafe_allow_html=True)

                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(detail_card("Financial Year", row.get("Financial Year", "N/A")), unsafe_allow_html=True)
                    st.markdown(detail_card("Total TCV", row.get("Total TCV", "N/A")), unsafe_allow_html=True)
                with c2:
                    clients = row.get("Total Clients", "N/A")
                    clients_display = f"{clients:,.0f}" if isinstance(clients, (int, float)) else clients
                    st.markdown(detail_card("Total Clients", clients_display), unsafe_allow_html=True)
                    st.markdown(detail_card("Service Categories", row.get("Service Categories", "N/A")), unsafe_allow_html=True)

                st.markdown('<p class="section-title">Services &amp; Products</p>', unsafe_allow_html=True)
                services = str(row.get("Services/Products", "No data available"))
                truncated = services[:1000] + ("..." if len(services) > 1000 else "")
                st.markdown(
                    f'<div class="company-detail-card">'
                    f'<div style="font-size:0.9rem; color:{colors["text_secondary"]}; white-space:pre-wrap;">'
                    f'{truncated}</div></div>',
                    unsafe_allow_html=True,
                )

        # ---------------- TAB 3: ANALYTICS ----------------
        with tab3:
            st.markdown('<p class="section-title">Advanced Analytics</p>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)

            with col1:
                fig = px.pie(
                    df, values="Current Revenue (Cr)", names="Company Name",
                    title="Revenue Distribution", color_discrete_sequence=colors["chart_seq"],
                )
                st.plotly_chart(style_chart(fig, colors, showlegend=True), use_container_width=True)

            with col2:
                if "Profit Margin %" in df.columns:
                    fig = px.scatter(
                        df, x="Current Revenue (Cr)", y="Profit Margin %",
                        size="Current Revenue (Cr)", color="Company Name",
                        text="Company Name", title="Margin vs Revenue",
                        color_discrete_sequence=colors["chart_seq"],
                    )
                    fig.update_traces(textposition="top center")
                    st.plotly_chart(style_chart(fig, colors), use_container_width=True)

            st.markdown('<p class="section-title">Complete Data</p>', unsafe_allow_html=True)

            display_cols = [
                "Company Name", "Current Revenue (Cr)", "Annual Revenue (Cr)",
                "Profit Margin %", "Total TCV", "Deal Wins", "Total Clients",
                "Service Categories",
            ]
            available_cols = [c for c in display_cols if c in df.columns]
            display_df = df[available_cols].copy()

            money_fmt = lambda x: f"₹{x:,.0f}" if pd.notna(x) else "N/A"
            for col in ["Current Revenue (Cr)", "Annual Revenue (Cr)"]:
                if col in display_df.columns:
                    display_df[col] = display_df[col].map(money_fmt)
            if "Profit Margin %" in display_df.columns:
                display_df["Profit Margin %"] = display_df["Profit Margin %"].map(
                    lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A"
                )
            if "Total TCV" in display_df.columns:
                display_df["Total TCV"] = display_df["Total TCV"].map(
                    lambda x: f"{x:,.0f}" if pd.notna(x) else "N/A"
                )
            if "Deal Wins" in display_df.columns:
                display_df["Deal Wins"] = display_df["Deal Wins"].map(
                    lambda x: f"{x:,.0f}" if pd.notna(x) else "0"
                )
            if "Total Clients" in display_df.columns:
                display_df["Total Clients"] = display_df["Total Clients"].map(
                    lambda x: f"{x:,.0f}" if pd.notna(x) else "N/A"
                )

            display_df = display_df.rename(columns={
                "Company Name": "Company",
                "Current Revenue (Cr)": "Revenue",
                "Annual Revenue (Cr)": "Annual",
                "Profit Margin %": "Margin",
                "Total TCV": "TCV",
                "Deal Wins": "Deals",
                "Total Clients": "Clients",
            })

            st.dataframe(display_df, use_container_width=True, hide_index=True)

else:
    st.info("📂 No data found. Click 'Refresh Data' in the sidebar to run the pipeline and fetch the latest data.")

st.markdown(
    f"""
    <hr style="margin:2rem 0 1rem 0; border-color:{colors['border']};">
    <p style="font-size:0.75rem; color:{colors['text_muted']}; text-align:center; letter-spacing:0.03em;">
        Data sourced from Screener.in &amp; Company Investor Relations | Updated: {datetime.now().strftime('%d %b %Y, %H:%M')}
    </p>
    """,
    unsafe_allow_html=True,
)

# # # # dashboard.py
# # # """
# # # NIFTY IT Analytics Dashboard
# # # """

# # # import os
# # # import sys
# # # import subprocess
# # # from datetime import datetime
# # # from io import BytesIO

# # # import pandas as pd
# # # import plotly.express as px
# # # import plotly.graph_objects as go
# # # import streamlit as st

# # # # --------------------------------------------------------------------------
# # # # Page configuration
# # # # --------------------------------------------------------------------------
# # # st.set_page_config(
# # #     page_title="NIFTY IT Analytics Dashboard",
# # #     page_icon="📊",
# # #     layout="wide",
# # #     initial_sidebar_state="expanded",
# # # )

# # # # --------------------------------------------------------------------------
# # # # Color palettes
# # # # --------------------------------------------------------------------------
# # # LIGHT_COLORS = {
# # #     "bg": "#F5F8F7",
# # #     "card": "#FFFFFF",
# # #     "text_primary": "#0B1F1B",
# # #     "text_secondary": "#3F5D52",
# # #     "text_muted": "#6B8478",
# # #     "border": "#DCE7E1",
# # #     "primary": "#155E4B",
# # #     "secondary": "#1F7A5E",
# # #     "accent": "#2FA37B",
# # #     "chip_bg": "#E4F3EC",
# # #     "positive": "#0F9D68",
# # #     "negative": "#D64545",
# # #     "chart_seq": ["#0B3B2E", "#155E4B", "#2FA37B", "#63C79A", "#9BDCBE", "#CDEEDD"],
# # # }

# # # DARK_COLORS = {
# # #     "bg": "#0B120F",
# # #     "card": "#121D19",
# # #     "text_primary": "#EAF3EF",
# # #     "text_secondary": "#BBD6C9",
# # #     "text_muted": "#84A597",
# # #     "border": "#233731",
# # #     "primary": "#4FD9A6",
# # #     "secondary": "#39B78C",
# # #     "accent": "#7FE6BE",
# # #     "chip_bg": "#17251F",
# # #     "positive": "#3ADF9B",
# # #     "negative": "#FF6B6B",
# # #     "chart_seq": ["#CDEEDD", "#9BDCBE", "#63C79A", "#2FA37B", "#155E4B", "#0B3B2E"],
# # # }


# # # # --------------------------------------------------------------------------
# # # # Helpers
# # # # --------------------------------------------------------------------------
# # # def to_numeric(series: pd.Series) -> pd.Series:
# # #     if series.dtype == "object":
# # #         return pd.to_numeric(series, errors="coerce")
# # #     return series


# # # def safe_sum(df: pd.DataFrame, col: str) -> float:
# # #     if col not in df.columns:
# # #         return 0.0
# # #     s = to_numeric(df[col])
# # #     return float(s.sum()) if s.notna().any() else 0.0


# # # def safe_mean(df: pd.DataFrame, col: str) -> float:
# # #     if col not in df.columns:
# # #         return 0.0
# # #     s = to_numeric(df[col])
# # #     return float(s.mean()) if s.notna().any() else 0.0


# # # def style_chart(fig, colors: dict, showlegend: bool = False, height: int = 400):
# # #     fig.update_layout(
# # #         plot_bgcolor="rgba(0,0,0,0)",
# # #         paper_bgcolor="rgba(0,0,0,0)",
# # #         font=dict(family="Inter, sans-serif", size=12, color=colors["text_secondary"]),
# # #         title_font=dict(color=colors["text_primary"], size=14),
# # #         height=height,
# # #         margin=dict(l=40, r=40, t=50, b=40),
# # #         showlegend=showlegend,
# # #         legend=dict(font=dict(color=colors["text_secondary"])),
# # #     )
# # #     fig.update_xaxes(color=colors["text_secondary"], gridcolor=colors["border"])
# # #     fig.update_yaxes(color=colors["text_secondary"], gridcolor=colors["border"])
# # #     return fig


# # # # --------------------------------------------------------------------------
# # # # CSS
# # # # --------------------------------------------------------------------------
# # # def load_css(colors: dict):
# # #     st.markdown(
# # #         f"""
# # #     <style>
# # #         @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

# # #         html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
# # #             background-color: {colors['bg']};
# # #         }}

# # #         [data-testid="stAppViewContainer"],
# # #         [data-testid="stAppViewContainer"] p,
# # #         [data-testid="stAppViewContainer"] span,
# # #         [data-testid="stAppViewContainer"] label,
# # #         [data-testid="stMarkdownContainer"] {{
# # #             font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
# # #             color: {colors['text_primary']};
# # #         }}

# # #         [data-testid="stHeader"] {{
# # #             background-color: transparent;
# # #         }}

# # #         [data-testid="stSidebar"] {{
# # #             background-color: {colors['card']};
# # #             border-right: 1px solid {colors['border']};
# # #         }}
# # #         [data-testid="stSidebar"] * {{
# # #             color: {colors['text_primary']};
# # #         }}
# # #         [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {{
# # #             color: {colors['text_secondary']};
# # #             font-weight: 500;
# # #         }}

# # #         .main-header {{
# # #             font-weight: 700;
# # #             font-size: 2.3rem;
# # #             color: {colors['primary']};
# # #             margin-bottom: 0.2rem;
# # #             letter-spacing: -0.02em;
# # #         }}

# # #         .sub-header {{
# # #             font-weight: 400;
# # #             font-size: 1rem;
# # #             color: {colors['text_secondary']};
# # #             margin-bottom: 1.8rem;
# # #         }}

# # #         .metric-card {{
# # #             background: {colors['card']};
# # #             border-radius: 14px;
# # #             padding: 1.1rem 1.4rem;
# # #             border: 1px solid {colors['border']};
# # #             box-shadow: 0 1px 3px rgba(0,0,0,0.08);
# # #             transition: transform 0.15s ease, box-shadow 0.15s ease;
# # #             position: relative;
# # #             overflow: hidden;
# # #         }}
# # #         .metric-card::before {{
# # #             content: '';
# # #             position: absolute;
# # #             top: 0; left: 0; right: 0;
# # #             height: 3px;
# # #             background: linear-gradient(90deg, {colors['secondary']}, {colors['accent']});
# # #         }}
# # #         .metric-card:hover {{
# # #             transform: translateY(-2px);
# # #             box-shadow: 0 8px 20px rgba(0,0,0,0.12);
# # #         }}
# # #         .metric-label {{
# # #             font-weight: 500;
# # #             font-size: 0.75rem;
# # #             color: {colors['text_muted']};
# # #             text-transform: uppercase;
# # #             letter-spacing: 0.06em;
# # #         }}
# # #         .metric-value {{
# # #             font-weight: 700;
# # #             font-size: 1.7rem;
# # #             color: {colors['text_primary']};
# # #             margin-top: 0.25rem;
# # #         }}

# # #         .section-title {{
# # #             font-weight: 600;
# # #             font-size: 1.15rem;
# # #             color: {colors['text_primary']};
# # #             margin: 1.4rem 0 0.9rem 0;
# # #             letter-spacing: -0.01em;
# # #         }}

# # #         .sidebar-section {{
# # #             font-weight: 600;
# # #             font-size: 0.75rem;
# # #             color: {colors['text_muted']};
# # #             text-transform: uppercase;
# # #             letter-spacing: 0.06em;
# # #             margin: 1.4rem 0 0.5rem 0;
# # #         }}

# # #         /* Tabs */
# # #         .stTabs [data-baseweb="tab-list"] {{
# # #             gap: 2px;
# # #             background-color: {colors['chip_bg']};
# # #             border-radius: 12px;
# # #             padding: 4px;
# # #         }}
# # #         .stTabs [data-baseweb="tab"] {{
# # #             font-weight: 500;
# # #             font-size: 0.85rem;
# # #             border-radius: 8px;
# # #             padding: 0.5rem 1.2rem;
# # #             color: {colors['text_secondary']};
# # #         }}
# # #         .stTabs [aria-selected="true"] {{
# # #             background-color: {colors['secondary']} !important;
# # #             color: #ffffff !important;
# # #         }}

# # #         .stButton > button, .stDownloadButton > button {{
# # #             font-weight: 500;
# # #             font-size: 0.85rem;
# # #             background: {colors['secondary']};
# # #             color: #ffffff;
# # #             border: none;
# # #             border-radius: 8px;
# # #             padding: 0.5rem 1.2rem;
# # #             transition: all 0.2s ease;
# # #         }}
# # #         .stButton > button:hover, .stDownloadButton > button:hover {{
# # #             background: {colors['accent']};
# # #             box-shadow: 0 4px 14px rgba(0,0,0,0.18);
# # #             color: #ffffff;
# # #         }}

# # #         [data-testid="stDataFrame"] {{
# # #             border: 1px solid {colors['border']};
# # #             border-radius: 10px;
# # #         }}

# # #         #MainMenu {{visibility: hidden;}}
# # #         footer {{visibility: hidden;}}

# # #         .positive {{ color: {colors['positive']}; }}
# # #         .negative {{ color: {colors['negative']}; }}

# # #         @media (max-width: 768px) {{
# # #             .main-header {{ font-size: 1.5rem; }}
# # #             .metric-value {{ font-size: 1.3rem; }}
# # #         }}
# # #     </style>
# # #     """,
# # #         unsafe_allow_html=True,
# # #     )


# # # # --------------------------------------------------------------------------
# # # # Data loading
# # # # --------------------------------------------------------------------------
# # # def load_excel_data():
# # #     """Load all sheets from the latest Excel file."""
# # #     output_dir = "output"
# # #     if not os.path.exists(output_dir):
# # #         return None

# # #     excel_files = [
# # #         f for f in os.listdir(output_dir)
# # #         if f.endswith(".xlsx") and f.startswith("nifty_it_data_")
# # #     ]
# # #     if not excel_files:
# # #         return None

# # #     latest_file = sorted(excel_files)[-1]
# # #     file_path = os.path.join(output_dir, latest_file)

# # #     try:
# # #         xl = pd.ExcelFile(file_path)
# # #         sheets = {}
# # #         for sheet_name in xl.sheet_names:
# # #             df = pd.read_excel(xl, sheet_name=sheet_name)
# # #             sheets[sheet_name] = df
# # #         return sheets
# # #     except Exception as e:
# # #         st.error(f"Error loading data: {e}")
# # #         return None


# # # def load_summary_data():
# # #     """Load only the summary sheet for metrics."""
# # #     sheets = load_excel_data()
# # #     if sheets and "Summary" in sheets:
# # #         df = sheets["Summary"]
# # #         # Clean numeric columns
# # #         for col in ["Current Revenue (Cr)", "Annual Revenue (Cr)", "Annual Profit (Cr)"]:
# # #             if col in df.columns:
# # #                 df[col] = (
# # #                     df[col].astype(str).str.replace("₹", "", regex=False)
# # #                     .str.replace(",", "", regex=False).str.strip()
# # #                 )
# # #                 df[col] = pd.to_numeric(df[col], errors="coerce")
        
# # #         for col in ["Total TCV", "Deal Wins", "Total Clients", "Profit Margin %"]:
# # #             if col in df.columns:
# # #                 df[col] = pd.to_numeric(df[col], errors="coerce")
        
# # #         return df
# # #     return None


# # # # --------------------------------------------------------------------------
# # # # Session state
# # # # --------------------------------------------------------------------------
# # # defaults = {"data": None, "dark_mode": False, "running": False}
# # # for key, value in defaults.items():
# # #     if key not in st.session_state:
# # #         st.session_state[key] = value

# # # colors = DARK_COLORS if st.session_state.dark_mode else LIGHT_COLORS
# # # load_css(colors)

# # # # --------------------------------------------------------------------------
# # # # Sidebar
# # # # --------------------------------------------------------------------------
# # # with st.sidebar:
# # #     st.markdown(
# # #         f'<p style="font-weight:700; font-size:1.3rem; color:{colors["primary"]}; '
# # #         f'margin-bottom:0.1rem;">NIFTY IT</p>',
# # #         unsafe_allow_html=True,
# # #     )
# # #     st.markdown(
# # #         f'<p style="font-weight:300; font-size:0.8rem; color:{colors["text_muted"]}; '
# # #         f'margin-bottom:1.3rem;">Analytics Dashboard</p>',
# # #         unsafe_allow_html=True,
# # #     )

# # #     dark_mode = st.toggle("Dark mode", value=st.session_state.dark_mode)
# # #     if dark_mode != st.session_state.dark_mode:
# # #         st.session_state.dark_mode = dark_mode
# # #         st.rerun()

# # #     st.markdown(f'<hr style="margin:1.3rem 0; border-color:{colors["border"]};">', unsafe_allow_html=True)
# # #     st.markdown('<p class="sidebar-section">Controls</p>', unsafe_allow_html=True)

# # #     if st.button("Refresh data", use_container_width=True):
# # #         st.session_state.running = True
# # #         st.rerun()

# # #     st.markdown('<p class="sidebar-section">Filters</p>', unsafe_allow_html=True)

# # #     selected_companies = None
# # #     rev_range = None
# # #     deal_range = None

# # #     if st.session_state.data is not None:
# # #         df_full = st.session_state.data.get("Summary")
# # #         if df_full is not None:
# # #             companies = df_full["Company Name"].unique().tolist()
# # #             selected_companies = st.multiselect(
# # #                 "Companies", companies, default=companies, key="company_filter"
# # #             )

# # #             if "Current Revenue (Cr)" in df_full.columns:
# # #                 revenue_col = to_numeric(df_full["Current Revenue (Cr)"])
# # #                 min_rev = float(revenue_col.min()) if revenue_col.notna().any() else 0.0
# # #                 max_rev = float(revenue_col.max()) if revenue_col.notna().any() else 10000.0
# # #                 rev_range = st.slider(
# # #                     "Revenue range (Cr)",
# # #                     min_value=min_rev,
# # #                     max_value=max_rev,
# # #                     value=(min_rev, max_rev),
# # #                     step=100.0,
# # #                     key="rev_range",
# # #                 )

# # #             if "Deal Wins" in df_full.columns:
# # #                 deals_col = to_numeric(df_full["Deal Wins"])
# # #                 min_deals = int(deals_col.min()) if deals_col.notna().any() else 0
# # #                 max_deals = int(deals_col.max()) if deals_col.notna().any() else 10
# # #                 deal_range = st.slider(
# # #                     "Deal wins",
# # #                     min_value=min_deals,
# # #                     max_value=max_deals,
# # #                     value=(min_deals, max_deals),
# # #                     key="deal_range",
# # #                 )

# # #     st.markdown(f'<hr style="margin:1.3rem 0; border-color:{colors["border"]};">', unsafe_allow_html=True)
# # #     st.markdown('<p class="sidebar-section">Export</p>', unsafe_allow_html=True)

# # #     if st.session_state.data is not None:
# # #         # Export all sheets as Excel
# # #         def export_all_sheets():
# # #             output = BytesIO()
# # #             with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
# # #                 for sheet_name, df in st.session_state.data.items():
# # #                     df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
# # #             return output.getvalue()

# # #         col1, col2 = st.columns(2)
# # #         with col1:
# # #             st.download_button(
# # #                 "XLSX",
# # #                 data=export_all_sheets(),
# # #                 file_name=f"nifty_it_export_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
# # #                 mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
# # #                 use_container_width=True,
# # #             )
# # #         with col2:
# # #             st.download_button(
# # #                 "CSV",
# # #                 data=st.session_state.data.get("Summary", pd.DataFrame()).to_csv(index=False).encode("utf-8"),
# # #                 file_name=f"nifty_it_export_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
# # #                 mime="text/csv",
# # #                 use_container_width=True,
# # #             )

# # # # --------------------------------------------------------------------------
# # # # Main content
# # # # --------------------------------------------------------------------------
# # # st.markdown('<p class="main-header">NIFTY IT Index</p>', unsafe_allow_html=True)
# # # st.markdown(
# # #     '<p class="sub-header">Real-time analytics and performance metrics of '
# # #     "India's top IT companies</p>",
# # #     unsafe_allow_html=True,
# # # )

# # # if st.session_state.running:
# # #     with st.spinner("Running data pipeline... this may take a few minutes."):
# # #         try:
# # #             result = subprocess.run(
# # #                 [sys.executable, "main.py"], capture_output=True, text=True
# # #             )
# # #             if result.returncode == 0:
# # #                 st.session_state.data = load_excel_data()
# # #                 st.success("Data refreshed successfully!")
# # #             else:
# # #                 st.error(f"Pipeline failed: {result.stderr[:200]}")
# # #         except Exception as e:
# # #             st.error(f"Error: {e}")
# # #     st.session_state.running = False
# # #     st.rerun()

# # # if st.session_state.data is None:
# # #     st.session_state.data = load_excel_data()

# # # if st.session_state.data is not None:
# # #     # Get summary data for metrics and filtering
# # #     summary_df = st.session_state.data.get("Summary")
    
# # #     if summary_df is not None:
# # #         # Apply filters
# # #         df = summary_df.copy()
# # #         if selected_companies:
# # #             df = df[df["Company Name"].isin(selected_companies)]
# # #         if rev_range and "Current Revenue (Cr)" in df.columns:
# # #             rc = to_numeric(df["Current Revenue (Cr)"])
# # #             df = df[(rc >= rev_range[0]) & (rc <= rev_range[1])]
# # #         if deal_range and "Deal Wins" in df.columns:
# # #             dc = to_numeric(df["Deal Wins"])
# # #             df = df[(dc >= deal_range[0]) & (dc <= deal_range[1])]

# # #         if df.empty:
# # #             st.warning("No companies match the current filters. Try widening your filter ranges.")
# # #         else:
# # #             # Metrics row
# # #             c1, c2, c3, c4, c5 = st.columns(5)
# # #             with c1:
# # #                 st.markdown(
# # #                     f"""
# # #                     <div class="metric-card">
# # #                         <div class="metric-label">Total Revenue</div>
# # #                         <div class="metric-value">₹{safe_sum(df, 'Current Revenue (Cr)'):,.0f} Cr</div>
# # #                     </div>
# # #                     """,
# # #                     unsafe_allow_html=True,
# # #                 )
# # #             with c2:
# # #                 st.markdown(
# # #                     f"""
# # #                     <div class="metric-card">
# # #                         <div class="metric-label">Average Revenue</div>
# # #                         <div class="metric-value">₹{safe_mean(df, 'Current Revenue (Cr)'):,.0f} Cr</div>
# # #                     </div>
# # #                     """,
# # #                     unsafe_allow_html=True,
# # #                 )
# # #             with c3:
# # #                 st.markdown(
# # #                     f"""
# # #                     <div class="metric-card">
# # #                         <div class="metric-label">Total Deals</div>
# # #                         <div class="metric-value">{safe_sum(df, 'Deal Wins'):,.0f}</div>
# # #                     </div>
# # #                     """,
# # #                     unsafe_allow_html=True,
# # #                 )
# # #             with c4:
# # #                 st.markdown(
# # #                     f"""
# # #                     <div class="metric-card">
# # #                         <div class="metric-label">Average Margin</div>
# # #                         <div class="metric-value">{safe_mean(df, 'Profit Margin %'):.1f}%</div>
# # #                     </div>
# # #                     """,
# # #                     unsafe_allow_html=True,
# # #                 )
# # #             with c5:
# # #                 st.markdown(
# # #                     f"""
# # #                     <div class="metric-card">
# # #                         <div class="metric-label">Total Clients</div>
# # #                         <div class="metric-value">{safe_sum(df, 'Total Clients'):,.0f}</div>
# # #                     </div>
# # #                     """,
# # #                     unsafe_allow_html=True,
# # #                 )

# # #             # Tabs matching Excel sheets
# # #             tab1, tab2, tab3, tab4, tab5 = st.tabs([
# # #                 "Summary", "Deal Wins", "Service Details", "Quarterly Details", "Comparison"
# # #             ])

# # #             # ------------------------------------------------------------------------
# # #             # TAB 1: SUMMARY
# # #             # ------------------------------------------------------------------------
# # #             with tab1:
# # #                 st.markdown('<p class="section-title">Performance Overview</p>', unsafe_allow_html=True)
                
# # #                 col1, col2 = st.columns(2)
# # #                 with col1:
# # #                     chart_df = df.dropna(subset=["Current Revenue (Cr)"])
# # #                     if not chart_df.empty:
# # #                         fig = px.bar(
# # #                             chart_df, x="Company Name", y="Current Revenue (Cr)",
# # #                             title="Revenue by Company", color="Current Revenue (Cr)",
# # #                             color_continuous_scale=colors["chart_seq"],
# # #                             text="Current Revenue (Cr)",
# # #                         )
# # #                         fig.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
# # #                         st.plotly_chart(style_chart(fig, colors), use_container_width=True)

# # #                 with col2:
# # #                     if "Profit Margin %" in df.columns:
# # #                         margin_df = df.dropna(subset=["Profit Margin %"])
# # #                         if not margin_df.empty:
# # #                             fig = px.bar(
# # #                                 margin_df, x="Company Name", y="Profit Margin %",
# # #                                 title="Profit Margin by Company", color="Profit Margin %",
# # #                                 color_continuous_scale="RdYlGn",
# # #                                 text="Profit Margin %",
# # #                             )
# # #                             fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
# # #                             st.plotly_chart(style_chart(fig, colors), use_container_width=True)

# # #                 # Full Summary Table
# # #                 st.markdown('<p class="section-title">Summary Data</p>', unsafe_allow_html=True)
# # #                 display_df = df.copy()
# # #                 for col in ["Current Revenue (Cr)", "Annual Revenue (Cr)"]:
# # #                     if col in display_df.columns:
# # #                         display_df[col] = display_df[col].map(
# # #                             lambda x: f"₹{x:,.0f}" if pd.notna(x) else "N/A"
# # #                         )
# # #                 if "Profit Margin %" in display_df.columns:
# # #                     display_df["Profit Margin %"] = display_df["Profit Margin %"].map(
# # #                         lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A"
# # #                     )
# # #                 if "Total TCV" in display_df.columns:
# # #                     display_df["Total TCV"] = display_df["Total TCV"].map(
# # #                         lambda x: f"{x:,.0f}" if pd.notna(x) else "N/A"
# # #                     )
# # #                 if "Deal Wins" in display_df.columns:
# # #                     display_df["Deal Wins"] = display_df["Deal Wins"].map(
# # #                         lambda x: f"{x:,.0f}" if pd.notna(x) else "0"
# # #                     )
# # #                 if "Total Clients" in display_df.columns:
# # #                     display_df["Total Clients"] = display_df["Total Clients"].map(
# # #                         lambda x: f"{x:,.0f}" if pd.notna(x) else "N/A"
# # #                     )
                
# # #                 st.dataframe(display_df, use_container_width=True, hide_index=True)

# # #             # ------------------------------------------------------------------------
# # #             # TAB 2: DEAL WINS
# # #             # ------------------------------------------------------------------------
# # #             with tab2:
# # #                 st.markdown('<p class="section-title">Deal Wins Detail</p>', unsafe_allow_html=True)
# # #                 deal_df = st.session_state.data.get("Deal Wins")
# # #                 if deal_df is not None and not deal_df.empty:
# # #                     # Filter by selected companies
# # #                     if selected_companies:
# # #                         deal_df = deal_df[deal_df["Company"].isin(selected_companies)]
                    
# # #                     # Deal Wins visualization
# # #                     col1, col2 = st.columns(2)
# # #                     with col1:
# # #                         deal_counts = deal_df.groupby("Company").size().reset_index(name="Count")
# # #                         if not deal_counts.empty:
# # #                             fig = px.bar(
# # #                                 deal_counts, x="Company", y="Count",
# # #                                 title="Deal Wins by Company",
# # #                                 color="Count", color_continuous_scale=colors["chart_seq"],
# # #                                 text="Count"
# # #                             )
# # #                             fig.update_traces(texttemplate="%{text}", textposition="outside")
# # #                             st.plotly_chart(style_chart(fig, colors), use_container_width=True)
                    
# # #                     with col2:
# # #                         # Deal values distribution
# # #                         if "Deal Value" in deal_df.columns:
# # #                             value_counts = deal_df["Deal Value"].value_counts().head(10)
# # #                             fig = px.pie(
# # #                                 values=value_counts.values, names=value_counts.index,
# # #                                 title="Deal Value Distribution",
# # #                                 color_discrete_sequence=colors["chart_seq"]
# # #                             )
# # #                             st.plotly_chart(style_chart(fig, colors, showlegend=True), use_container_width=True)
                    
# # #                     # Full Deal Wins table
# # #                     st.dataframe(deal_df, use_container_width=True, hide_index=True)
# # #                 else:
# # #                     st.info("No deal wins data available.")

# # #             # ------------------------------------------------------------------------
# # #             # TAB 3: SERVICE DETAILS
# # #             # ------------------------------------------------------------------------
# # #             with tab3:
# # #                 st.markdown('<p class="section-title">Service Details</p>', unsafe_allow_html=True)
# # #                 service_df = st.session_state.data.get("Services Detail")
# # #                 if service_df is not None and not service_df.empty:
# # #                     if selected_companies:
# # #                         service_df = service_df[service_df["Company"].isin(selected_companies)]
                    
# # #                     # Service category distribution
# # #                     if "Category" in service_df.columns:
# # #                         categories = service_df["Category"].value_counts().head(10)
# # #                         if not categories.empty:
# # #                             fig = px.bar(
# # #                                 x=categories.values, y=categories.index,
# # #                                 orientation='h', title="Top Service Categories",
# # #                                 color=categories.values, color_continuous_scale=colors["chart_seq"],
# # #                                 text=categories.values
# # #                             )
# # #                             fig.update_traces(texttemplate="%{text}", textposition="outside")
# # #                             fig.update_layout(
# # #                                 xaxis_title="Count",
# # #                                 yaxis_title="Category",
# # #                                 height=400
# # #                             )
# # #                             st.plotly_chart(style_chart(fig, colors), use_container_width=True)
                    
# # #                     st.dataframe(service_df, use_container_width=True, hide_index=True)
# # #                 else:
# # #                     st.info("No service details available.")

# # #             # ------------------------------------------------------------------------
# # #             # TAB 4: QUARTERLY DETAILS
# # #             # ------------------------------------------------------------------------
# # #             with tab4:
# # #                 st.markdown('<p class="section-title">Quarterly Details</p>', unsafe_allow_html=True)
# # #                 quarterly_df = st.session_state.data.get("Quarterly Details")
# # #                 if quarterly_df is not None and not quarterly_df.empty:
# # #                     if selected_companies:
# # #                         quarterly_df = quarterly_df[quarterly_df["Company"].isin(selected_companies)]
                    
# # #                     # Quarterly revenue trend
# # #                     if "Quarter" in quarterly_df.columns and "Revenue (Cr)" in quarterly_df.columns:
# # #                         # Get last 8 quarters for cleaner visualization
# # #                         recent_df = quarterly_df.tail(20)
# # #                         fig = px.line(
# # #                             recent_df, x="Quarter", y="Revenue (Cr)",
# # #                             color="Company", title="Quarterly Revenue Trend",
# # #                             color_discrete_sequence=colors["chart_seq"]
# # #                         )
# # #                         st.plotly_chart(style_chart(fig, colors, showlegend=True), use_container_width=True)
                    
# # #                     st.dataframe(quarterly_df, use_container_width=True, hide_index=True)
# # #                 else:
# # #                     st.info("No quarterly data available.")

# # #             # ------------------------------------------------------------------------
# # #             # TAB 5: COMPARISON
# # #             # ------------------------------------------------------------------------
# # #             with tab5:
# # #                 st.markdown('<p class="section-title">Company Comparison</p>', unsafe_allow_html=True)
                
# # #                 # Revenue vs Profit scatter
# # #                 col1, col2 = st.columns(2)
# # #                 with col1:
# # #                     scatter_df = df.dropna(subset=["Current Revenue (Cr)", "Annual Profit (Cr)"])
# # #                     if not scatter_df.empty:
# # #                         fig = px.scatter(
# # #                             scatter_df, x="Current Revenue (Cr)", y="Annual Profit (Cr)",
# # #                             size="Current Revenue (Cr)", color="Company Name",
# # #                             text="Company Name", title="Revenue vs Profit",
# # #                             color_discrete_sequence=colors["chart_seq"],
# # #                         )
# # #                         fig.update_traces(textposition="top center")
# # #                         st.plotly_chart(style_chart(fig, colors), use_container_width=True)
                
# # #                 with col2:
# # #                     # TCV vs Deals
# # #                     tcv_df = df.dropna(subset=["Total TCV", "Deal Wins"])
# # #                     if not tcv_df.empty:
# # #                         fig = px.scatter(
# # #                             tcv_df, x="Total TCV", y="Deal Wins",
# # #                             size="Total TCV", color="Company Name",
# # #                             text="Company Name", title="TCV vs Deal Wins",
# # #                             color_discrete_sequence=colors["chart_seq"],
# # #                         )
# # #                         fig.update_traces(textposition="top center")
# # #                         st.plotly_chart(style_chart(fig, colors), use_container_width=True)
                
# # #                 # Comparison table
# # #                 st.markdown('<p class="section-title">Comparison Data</p>', unsafe_allow_html=True)
# # #                 comparison_df = st.session_state.data.get("Comparison")
# # #                 if comparison_df is not None:
# # #                     st.dataframe(comparison_df, use_container_width=True, hide_index=True)

# # # else:
# # #     st.info("No data found. Click 'Refresh Data' in the sidebar to run the pipeline and fetch the latest data.")

# # # # Footer
# # # st.markdown(
# # #     f"""
# # #     <hr style="margin:2rem 0 1rem 0; border-color:{colors['border']};">
# # #     <p style="font-size:0.75rem; color:{colors['text_muted']}; text-align:center; letter-spacing:0.03em;">
# # #         Data sourced from Screener.in and Company Investor Relations | Updated: {datetime.now().strftime('%d %b %Y, %H:%M')}
# # #     </p>
# # #     """,
# # #     unsafe_allow_html=True,
# # # )

# # # dashboard.py (FIXED)
# # """
# # NIFTY IT Analytics Dashboard
# # """

# # import os
# # import sys
# # import subprocess
# # from datetime import datetime
# # from io import BytesIO

# # import pandas as pd
# # import plotly.express as px
# # import plotly.graph_objects as go
# # import streamlit as st

# # # --------------------------------------------------------------------------
# # # Page configuration
# # # --------------------------------------------------------------------------
# # st.set_page_config(
# #     page_title="NIFTY IT Analytics Dashboard",
# #     page_icon="📊",
# #     layout="wide",
# #     initial_sidebar_state="expanded",
# # )

# # # --------------------------------------------------------------------------
# # # Color palettes
# # # --------------------------------------------------------------------------
# # LIGHT_COLORS = {
# #     "bg": "#F5F8F7",
# #     "card": "#FFFFFF",
# #     "text_primary": "#0B1F1B",
# #     "text_secondary": "#3F5D52",
# #     "text_muted": "#6B8478",
# #     "border": "#DCE7E1",
# #     "primary": "#155E4B",
# #     "secondary": "#1F7A5E",
# #     "accent": "#2FA37B",
# #     "chip_bg": "#E4F3EC",
# #     "positive": "#0F9D68",
# #     "negative": "#D64545",
# #     "chart_seq": ["#0B3B2E", "#155E4B", "#2FA37B", "#63C79A", "#9BDCBE", "#CDEEDD"],
# # }

# # DARK_COLORS = {
# #     "bg": "#0B120F",
# #     "card": "#121D19",
# #     "text_primary": "#EAF3EF",
# #     "text_secondary": "#BBD6C9",
# #     "text_muted": "#84A597",
# #     "border": "#233731",
# #     "primary": "#4FD9A6",
# #     "secondary": "#39B78C",
# #     "accent": "#7FE6BE",
# #     "chip_bg": "#17251F",
# #     "positive": "#3ADF9B",
# #     "negative": "#FF6B6B",
# #     "chart_seq": ["#CDEEDD", "#9BDCBE", "#63C79A", "#2FA37B", "#155E4B", "#0B3B2E"],
# # }


# # # --------------------------------------------------------------------------
# # # Helpers
# # # --------------------------------------------------------------------------
# # def to_numeric_safe(series: pd.Series) -> pd.Series:
# #     """Safely convert series to numeric, handling strings with currency symbols."""
# #     if series.dtype in ['int64', 'float64']:
# #         return series
# #     # Remove currency symbols and commas, then convert
# #     cleaned = series.astype(str).str.replace('₹', '', regex=False).str.replace(',', '', regex=False).str.strip()
# #     cleaned = cleaned.replace('', 'NaN')
# #     return pd.to_numeric(cleaned, errors='coerce')


# # def safe_sum(df: pd.DataFrame, col: str) -> float:
# #     if col not in df.columns:
# #         return 0.0
# #     s = to_numeric_safe(df[col])
# #     return float(s.sum()) if s.notna().any() else 0.0


# # def safe_mean(df: pd.DataFrame, col: str) -> float:
# #     if col not in df.columns:
# #         return 0.0
# #     s = to_numeric_safe(df[col])
# #     return float(s.mean()) if s.notna().any() else 0.0


# # def format_currency(value) -> str:
# #     """Format a value as currency with ₹ symbol."""
# #     if pd.isna(value):
# #         return "N/A"
# #     try:
# #         return f"₹{float(value):,.0f}"
# #     except (ValueError, TypeError):
# #         return "N/A"


# # def format_percent(value) -> str:
# #     """Format a value as percentage."""
# #     if pd.isna(value):
# #         return "N/A"
# #     try:
# #         return f"{float(value):.1f}%"
# #     except (ValueError, TypeError):
# #         return "N/A"


# # def format_number(value) -> str:
# #     """Format a number with commas."""
# #     if pd.isna(value):
# #         return "N/A"
# #     try:
# #         return f"{float(value):,.0f}"
# #     except (ValueError, TypeError):
# #         return "N/A"


# # def style_chart(fig, colors: dict, showlegend: bool = False, height: int = 400):
# #     fig.update_layout(
# #         plot_bgcolor="rgba(0,0,0,0)",
# #         paper_bgcolor="rgba(0,0,0,0)",
# #         font=dict(family="Inter, sans-serif", size=12, color=colors["text_secondary"]),
# #         title_font=dict(color=colors["text_primary"], size=14),
# #         height=height,
# #         margin=dict(l=40, r=40, t=50, b=40),
# #         showlegend=showlegend,
# #         legend=dict(font=dict(color=colors["text_secondary"])),
# #     )
# #     fig.update_xaxes(color=colors["text_secondary"], gridcolor=colors["border"])
# #     fig.update_yaxes(color=colors["text_secondary"], gridcolor=colors["border"])
# #     return fig


# # # --------------------------------------------------------------------------
# # # CSS
# # # --------------------------------------------------------------------------
# # def load_css(colors: dict):
# #     st.markdown(
# #         f"""
# #     <style>
# #         @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

# #         html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
# #             background-color: {colors['bg']};
# #         }}

# #         [data-testid="stAppViewContainer"],
# #         [data-testid="stAppViewContainer"] p,
# #         [data-testid="stAppViewContainer"] span,
# #         [data-testid="stAppViewContainer"] label,
# #         [data-testid="stMarkdownContainer"] {{
# #             font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
# #             color: {colors['text_primary']};
# #         }}

# #         [data-testid="stHeader"] {{
# #             background-color: transparent;
# #         }}

# #         [data-testid="stSidebar"] {{
# #             background-color: {colors['card']};
# #             border-right: 1px solid {colors['border']};
# #         }}
# #         [data-testid="stSidebar"] * {{
# #             color: {colors['text_primary']};
# #         }}
# #         [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {{
# #             color: {colors['text_secondary']};
# #             font-weight: 500;
# #         }}

# #         .main-header {{
# #             font-weight: 700;
# #             font-size: 2.3rem;
# #             color: {colors['primary']};
# #             margin-bottom: 0.2rem;
# #             letter-spacing: -0.02em;
# #         }}

# #         .sub-header {{
# #             font-weight: 400;
# #             font-size: 1rem;
# #             color: {colors['text_secondary']};
# #             margin-bottom: 1.8rem;
# #         }}

# #         .metric-card {{
# #             background: {colors['card']};
# #             border-radius: 14px;
# #             padding: 1.1rem 1.4rem;
# #             border: 1px solid {colors['border']};
# #             box-shadow: 0 1px 3px rgba(0,0,0,0.08);
# #             transition: transform 0.15s ease, box-shadow 0.15s ease;
# #             position: relative;
# #             overflow: hidden;
# #         }}
# #         .metric-card::before {{
# #             content: '';
# #             position: absolute;
# #             top: 0; left: 0; right: 0;
# #             height: 3px;
# #             background: linear-gradient(90deg, {colors['secondary']}, {colors['accent']});
# #         }}
# #         .metric-card:hover {{
# #             transform: translateY(-2px);
# #             box-shadow: 0 8px 20px rgba(0,0,0,0.12);
# #         }}
# #         .metric-label {{
# #             font-weight: 500;
# #             font-size: 0.75rem;
# #             color: {colors['text_muted']};
# #             text-transform: uppercase;
# #             letter-spacing: 0.06em;
# #         }}
# #         .metric-value {{
# #             font-weight: 700;
# #             font-size: 1.7rem;
# #             color: {colors['text_primary']};
# #             margin-top: 0.25rem;
# #         }}

# #         .section-title {{
# #             font-weight: 600;
# #             font-size: 1.15rem;
# #             color: {colors['text_primary']};
# #             margin: 1.4rem 0 0.9rem 0;
# #             letter-spacing: -0.01em;
# #         }}

# #         .sidebar-section {{
# #             font-weight: 600;
# #             font-size: 0.75rem;
# #             color: {colors['text_muted']};
# #             text-transform: uppercase;
# #             letter-spacing: 0.06em;
# #             margin: 1.4rem 0 0.5rem 0;
# #         }}

# #         .stTabs [data-baseweb="tab-list"] {{
# #             gap: 2px;
# #             background-color: {colors['chip_bg']};
# #             border-radius: 12px;
# #             padding: 4px;
# #         }}
# #         .stTabs [data-baseweb="tab"] {{
# #             font-weight: 500;
# #             font-size: 0.85rem;
# #             border-radius: 8px;
# #             padding: 0.5rem 1.2rem;
# #             color: {colors['text_secondary']};
# #         }}
# #         .stTabs [aria-selected="true"] {{
# #             background-color: {colors['secondary']} !important;
# #             color: #ffffff !important;
# #         }}

# #         .stButton > button, .stDownloadButton > button {{
# #             font-weight: 500;
# #             font-size: 0.85rem;
# #             background: {colors['secondary']};
# #             color: #ffffff;
# #             border: none;
# #             border-radius: 8px;
# #             padding: 0.5rem 1.2rem;
# #             transition: all 0.2s ease;
# #         }}
# #         .stButton > button:hover, .stDownloadButton > button:hover {{
# #             background: {colors['accent']};
# #             box-shadow: 0 4px 14px rgba(0,0,0,0.18);
# #             color: #ffffff;
# #         }}

# #         [data-testid="stDataFrame"] {{
# #             border: 1px solid {colors['border']};
# #             border-radius: 10px;
# #         }}

# #         #MainMenu {{visibility: hidden;}}
# #         footer {{visibility: hidden;}}

# #         .positive {{ color: {colors['positive']}; }}
# #         .negative {{ color: {colors['negative']}; }}

# #         @media (max-width: 768px) {{
# #             .main-header {{ font-size: 1.5rem; }}
# #             .metric-value {{ font-size: 1.3rem; }}
# #         }}
# #     </style>
# #     """,
# #         unsafe_allow_html=True,
# #     )


# # # --------------------------------------------------------------------------
# # # Data loading
# # # --------------------------------------------------------------------------
# # def load_excel_data():
# #     """Load all sheets from the latest Excel file."""
# #     output_dir = "output"
# #     if not os.path.exists(output_dir):
# #         return None

# #     excel_files = [
# #         f for f in os.listdir(output_dir)
# #         if f.endswith(".xlsx") and f.startswith("nifty_it_data_")
# #     ]
# #     if not excel_files:
# #         return None

# #     latest_file = sorted(excel_files)[-1]
# #     file_path = os.path.join(output_dir, latest_file)

# #     try:
# #         xl = pd.ExcelFile(file_path)
# #         sheets = {}
# #         for sheet_name in xl.sheet_names:
# #             df = pd.read_excel(xl, sheet_name=sheet_name)
# #             sheets[sheet_name] = df
# #         return sheets
# #     except Exception as e:
# #         st.error(f"Error loading data: {e}")
# #         return None


# # # --------------------------------------------------------------------------
# # # Session state
# # # --------------------------------------------------------------------------
# # defaults = {"data": None, "dark_mode": False, "running": False}
# # for key, value in defaults.items():
# #     if key not in st.session_state:
# #         st.session_state[key] = value

# # colors = DARK_COLORS if st.session_state.dark_mode else LIGHT_COLORS
# # load_css(colors)

# # # --------------------------------------------------------------------------
# # # Sidebar
# # # --------------------------------------------------------------------------
# # with st.sidebar:
# #     st.markdown(
# #         f'<p style="font-weight:700; font-size:1.3rem; color:{colors["primary"]}; '
# #         f'margin-bottom:0.1rem;">NIFTY IT</p>',
# #         unsafe_allow_html=True,
# #     )
# #     st.markdown(
# #         f'<p style="font-weight:300; font-size:0.8rem; color:{colors["text_muted"]}; '
# #         f'margin-bottom:1.3rem;">Analytics Dashboard</p>',
# #         unsafe_allow_html=True,
# #     )

# #     dark_mode = st.toggle("Dark mode", value=st.session_state.dark_mode)
# #     if dark_mode != st.session_state.dark_mode:
# #         st.session_state.dark_mode = dark_mode
# #         st.rerun()

# #     st.markdown(f'<hr style="margin:1.3rem 0; border-color:{colors["border"]};">', unsafe_allow_html=True)
# #     st.markdown('<p class="sidebar-section">Controls</p>', unsafe_allow_html=True)

# #     if st.button("Refresh data", use_container_width=True):
# #         st.session_state.running = True
# #         st.rerun()

# #     st.markdown('<p class="sidebar-section">Filters</p>', unsafe_allow_html=True)

# #     selected_companies = None
# #     rev_range = None
# #     deal_range = None

# #     if st.session_state.data is not None:
# #         df_full = st.session_state.data.get("Summary")
# #         if df_full is not None:
# #             companies = df_full["Company Name"].unique().tolist()
# #             selected_companies = st.multiselect(
# #                 "Companies", companies, default=companies, key="company_filter"
# #             )

# #             if "Current Revenue (Cr)" in df_full.columns:
# #                 revenue_col = to_numeric_safe(df_full["Current Revenue (Cr)"])
# #                 if revenue_col.notna().any():
# #                     min_rev = float(revenue_col.min())
# #                     max_rev = float(revenue_col.max())
# #                     rev_range = st.slider(
# #                         "Revenue range (Cr)",
# #                         min_value=min_rev,
# #                         max_value=max_rev,
# #                         value=(min_rev, max_rev),
# #                         step=100.0,
# #                         key="rev_range",
# #                     )

# #             if "Deal Wins" in df_full.columns:
# #                 deals_col = to_numeric_safe(df_full["Deal Wins"])
# #                 if deals_col.notna().any():
# #                     min_deals = int(deals_col.min())
# #                     max_deals = int(deals_col.max())
# #                     deal_range = st.slider(
# #                         "Deal wins",
# #                         min_value=min_deals,
# #                         max_value=max_deals,
# #                         value=(min_deals, max_deals),
# #                         key="deal_range",
# #                     )

# #     st.markdown(f'<hr style="margin:1.3rem 0; border-color:{colors["border"]};">', unsafe_allow_html=True)
# #     st.markdown('<p class="sidebar-section">Export</p>', unsafe_allow_html=True)

# #     if st.session_state.data is not None:
# #         def export_all_sheets():
# #             output = BytesIO()
# #             with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
# #                 for sheet_name, df in st.session_state.data.items():
# #                     df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
# #             return output.getvalue()

# #         col1, col2 = st.columns(2)
# #         with col1:
# #             st.download_button(
# #                 "XLSX",
# #                 data=export_all_sheets(),
# #                 file_name=f"nifty_it_export_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
# #                 mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
# #                 use_container_width=True,
# #             )
# #         with col2:
# #             summary_df = st.session_state.data.get("Summary", pd.DataFrame())
# #             st.download_button(
# #                 "CSV",
# #                 data=summary_df.to_csv(index=False).encode("utf-8"),
# #                 file_name=f"nifty_it_export_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
# #                 mime="text/csv",
# #                 use_container_width=True,
# #             )

# # # --------------------------------------------------------------------------
# # # Main content
# # # --------------------------------------------------------------------------
# # st.markdown('<p class="main-header">NIFTY IT Index</p>', unsafe_allow_html=True)
# # st.markdown(
# #     '<p class="sub-header">Real-time analytics and performance metrics of '
# #     "India's top IT companies</p>",
# #     unsafe_allow_html=True,
# # )

# # if st.session_state.running:
# #     with st.spinner("Running data pipeline... this may take a few minutes."):
# #         try:
# #             result = subprocess.run(
# #                 [sys.executable, "main.py"], capture_output=True, text=True
# #             )
# #             if result.returncode == 0:
# #                 st.session_state.data = load_excel_data()
# #                 st.success("Data refreshed successfully!")
# #             else:
# #                 st.error(f"Pipeline failed: {result.stderr[:200]}")
# #         except Exception as e:
# #             st.error(f"Error: {e}")
# #     st.session_state.running = False
# #     st.rerun()

# # if st.session_state.data is None:
# #     st.session_state.data = load_excel_data()

# # if st.session_state.data is not None:
# #     summary_df = st.session_state.data.get("Summary")
    
# #     if summary_df is not None:
# #         df = summary_df.copy()
        
# #         # Apply filters
# #         if selected_companies:
# #             df = df[df["Company Name"].isin(selected_companies)]
# #         if rev_range and "Current Revenue (Cr)" in df.columns:
# #             rc = to_numeric_safe(df["Current Revenue (Cr)"])
# #             df = df[(rc >= rev_range[0]) & (rc <= rev_range[1])]
# #         if deal_range and "Deal Wins" in df.columns:
# #             dc = to_numeric_safe(df["Deal Wins"])
# #             df = df[(dc >= deal_range[0]) & (dc <= deal_range[1])]

# #         if df.empty:
# #             st.warning("No companies match the current filters. Try widening your filter ranges.")
# #         else:
# #             # Metrics row
# #             c1, c2, c3, c4, c5 = st.columns(5)
# #             with c1:
# #                 st.markdown(
# #                     f"""
# #                     <div class="metric-card">
# #                         <div class="metric-label">Total Revenue</div>
# #                         <div class="metric-value">₹{safe_sum(df, 'Current Revenue (Cr)'):,.0f} Cr</div>
# #                     </div>
# #                     """,
# #                     unsafe_allow_html=True,
# #                 )
# #             with c2:
# #                 st.markdown(
# #                     f"""
# #                     <div class="metric-card">
# #                         <div class="metric-label">Average Revenue</div>
# #                         <div class="metric-value">₹{safe_mean(df, 'Current Revenue (Cr)'):,.0f} Cr</div>
# #                     </div>
# #                     """,
# #                     unsafe_allow_html=True,
# #                 )
# #             with c3:
# #                 st.markdown(
# #                     f"""
# #                     <div class="metric-card">
# #                         <div class="metric-label">Total Deals</div>
# #                         <div class="metric-value">{safe_sum(df, 'Deal Wins'):,.0f}</div>
# #                     </div>
# #                     """,
# #                     unsafe_allow_html=True,
# #                 )
# #             with c4:
# #                 st.markdown(
# #                     f"""
# #                     <div class="metric-card">
# #                         <div class="metric-label">Average Margin</div>
# #                         <div class="metric-value">{safe_mean(df, 'Profit Margin %'):.1f}%</div>
# #                     </div>
# #                     """,
# #                     unsafe_allow_html=True,
# #                 )
# #             with c5:
# #                 st.markdown(
# #                     f"""
# #                     <div class="metric-card">
# #                         <div class="metric-label">Total Clients</div>
# #                         <div class="metric-value">{safe_sum(df, 'Total Clients'):,.0f}</div>
# #                     </div>
# #                     """,
# #                     unsafe_allow_html=True,
# #                 )

# #             # Tabs matching Excel sheets
# #             tab1, tab2, tab3, tab4, tab5 = st.tabs([
# #                 "Summary", "Deal Wins", "Service Details", "Quarterly Details", "Comparison"
# #             ])

# #             # ------------------------------------------------------------------------
# #             # TAB 1: SUMMARY
# #             # ------------------------------------------------------------------------
# #             with tab1:
# #                 st.markdown('<p class="section-title">Performance Overview</p>', unsafe_allow_html=True)
                
# #                 col1, col2 = st.columns(2)
# #                 with col1:
# #                     chart_df = df.dropna(subset=["Current Revenue (Cr)"])
# #                     if not chart_df.empty:
# #                         fig = px.bar(
# #                             chart_df, x="Company Name", y="Current Revenue (Cr)",
# #                             title="Revenue by Company", color="Current Revenue (Cr)",
# #                             color_continuous_scale=colors["chart_seq"],
# #                             text="Current Revenue (Cr)",
# #                         )
# #                         fig.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
# #                         st.plotly_chart(style_chart(fig, colors), use_container_width=True)

# #                 with col2:
# #                     if "Profit Margin %" in df.columns:
# #                         margin_df = df.dropna(subset=["Profit Margin %"])
# #                         if not margin_df.empty:
# #                             fig = px.bar(
# #                                 margin_df, x="Company Name", y="Profit Margin %",
# #                                 title="Profit Margin by Company", color="Profit Margin %",
# #                                 color_continuous_scale="RdYlGn",
# #                                 text="Profit Margin %",
# #                             )
# #                             fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
# #                             st.plotly_chart(style_chart(fig, colors), use_container_width=True)

# #                 # Summary Table - safe formatting
# #                 st.markdown('<p class="section-title">Summary Data</p>', unsafe_allow_html=True)
# #                 display_df = df.copy()
                
# #                 # Format each column safely
# #                 if "Current Revenue (Cr)" in display_df.columns:
# #                     display_df["Current Revenue (Cr)"] = display_df["Current Revenue (Cr)"].apply(format_currency)
# #                 if "Annual Revenue (Cr)" in display_df.columns:
# #                     display_df["Annual Revenue (Cr)"] = display_df["Annual Revenue (Cr)"].apply(format_currency)
# #                 if "Profit Margin %" in display_df.columns:
# #                     display_df["Profit Margin %"] = display_df["Profit Margin %"].apply(format_percent)
# #                 if "Total TCV" in display_df.columns:
# #                     display_df["Total TCV"] = display_df["Total TCV"].apply(format_number)
# #                 if "Deal Wins" in display_df.columns:
# #                     display_df["Deal Wins"] = display_df["Deal Wins"].apply(format_number)
# #                 if "Total Clients" in display_df.columns:
# #                     display_df["Total Clients"] = display_df["Total Clients"].apply(format_number)
                
# #                 st.dataframe(display_df, use_container_width=True, hide_index=True)

# #             # ------------------------------------------------------------------------
# #             # TAB 2: DEAL WINS
# #             # ------------------------------------------------------------------------
# #             with tab2:
# #                 st.markdown('<p class="section-title">Deal Wins Detail</p>', unsafe_allow_html=True)
# #                 deal_df = st.session_state.data.get("Deal Wins")
# #                 if deal_df is not None and not deal_df.empty:
# #                     if selected_companies and "Company" in deal_df.columns:
# #                         deal_df = deal_df[deal_df["Company"].isin(selected_companies)]
                    
# #                     col1, col2 = st.columns(2)
# #                     with col1:
# #                         if "Company" in deal_df.columns:
# #                             deal_counts = deal_df.groupby("Company").size().reset_index(name="Count")
# #                             if not deal_counts.empty:
# #                                 fig = px.bar(
# #                                     deal_counts, x="Company", y="Count",
# #                                     title="Deal Wins by Company",
# #                                     color="Count", color_continuous_scale=colors["chart_seq"],
# #                                     text="Count"
# #                                 )
# #                                 fig.update_traces(texttemplate="%{text}", textposition="outside")
# #                                 st.plotly_chart(style_chart(fig, colors), use_container_width=True)
                    
# #                     with col2:
# #                         if "Deal Value" in deal_df.columns:
# #                             value_counts = deal_df["Deal Value"].value_counts().head(10)
# #                             if not value_counts.empty:
# #                                 fig = px.pie(
# #                                     values=value_counts.values, names=value_counts.index,
# #                                     title="Deal Value Distribution",
# #                                     color_discrete_sequence=colors["chart_seq"]
# #                                 )
# #                                 st.plotly_chart(style_chart(fig, colors, showlegend=True), use_container_width=True)
                    
# #                     st.dataframe(deal_df, use_container_width=True, hide_index=True)
# #                 else:
# #                     st.info("No deal wins data available.")

# #             # ------------------------------------------------------------------------
# #             # TAB 3: SERVICE DETAILS
# #             # ------------------------------------------------------------------------
# #             with tab3:
# #                 st.markdown('<p class="section-title">Service Details</p>', unsafe_allow_html=True)
# #                 service_df = st.session_state.data.get("Services Detail")
# #                 if service_df is not None and not service_df.empty:
# #                     if selected_companies and "Company" in service_df.columns:
# #                         service_df = service_df[service_df["Company"].isin(selected_companies)]
                    
# #                     if "Category" in service_df.columns:
# #                         categories = service_df["Category"].value_counts().head(10)
# #                         if not categories.empty:
# #                             fig = px.bar(
# #                                 x=categories.values, y=categories.index,
# #                                 orientation='h', title="Top Service Categories",
# #                                 color=categories.values, color_continuous_scale=colors["chart_seq"],
# #                                 text=categories.values
# #                             )
# #                             fig.update_traces(texttemplate="%{text}", textposition="outside")
# #                             fig.update_layout(
# #                                 xaxis_title="Count",
# #                                 yaxis_title="Category",
# #                                 height=400
# #                             )
# #                             st.plotly_chart(style_chart(fig, colors), use_container_width=True)
                    
# #                     st.dataframe(service_df, use_container_width=True, hide_index=True)
# #                 else:
# #                     st.info("No service details available.")

# #             # ------------------------------------------------------------------------
# #             # TAB 4: QUARTERLY DETAILS
# #             # ------------------------------------------------------------------------
# #             with tab4:
# #                 st.markdown('<p class="section-title">Quarterly Details</p>', unsafe_allow_html=True)
# #                 quarterly_df = st.session_state.data.get("Quarterly Details")
# #                 if quarterly_df is not None and not quarterly_df.empty:
# #                     if selected_companies and "Company" in quarterly_df.columns:
# #                         quarterly_df = quarterly_df[quarterly_df["Company"].isin(selected_companies)]
                    
# #                     if "Quarter" in quarterly_df.columns and "Revenue (Cr)" in quarterly_df.columns:
# #                         recent_df = quarterly_df.tail(20)
# #                         if not recent_df.empty:
# #                             fig = px.line(
# #                                 recent_df, x="Quarter", y="Revenue (Cr)",
# #                                 color="Company", title="Quarterly Revenue Trend",
# #                                 color_discrete_sequence=colors["chart_seq"]
# #                             )
# #                             st.plotly_chart(style_chart(fig, colors, showlegend=True), use_container_width=True)
                    
# #                     st.dataframe(quarterly_df, use_container_width=True, hide_index=True)
# #                 else:
# #                     st.info("No quarterly data available.")

# #             # ------------------------------------------------------------------------
# #             # TAB 5: COMPARISON
# #             # ------------------------------------------------------------------------
# #             with tab5:
# #                 st.markdown('<p class="section-title">Company Comparison</p>', unsafe_allow_html=True)
                
# #                 col1, col2 = st.columns(2)
# #                 with col1:
# #                     scatter_df = df.dropna(subset=["Current Revenue (Cr)", "Annual Profit (Cr)"])
# #                     if not scatter_df.empty:
# #                         fig = px.scatter(
# #                             scatter_df, x="Current Revenue (Cr)", y="Annual Profit (Cr)",
# #                             size="Current Revenue (Cr)", color="Company Name",
# #                             text="Company Name", title="Revenue vs Profit",
# #                             color_discrete_sequence=colors["chart_seq"],
# #                         )
# #                         fig.update_traces(textposition="top center")
# #                         st.plotly_chart(style_chart(fig, colors), use_container_width=True)
                
# #                 with col2:
# #                     tcv_df = df.dropna(subset=["Total TCV", "Deal Wins"])
# #                     if not tcv_df.empty:
# #                         fig = px.scatter(
# #                             tcv_df, x="Total TCV", y="Deal Wins",
# #                             size="Total TCV", color="Company Name",
# #                             text="Company Name", title="TCV vs Deal Wins",
# #                             color_discrete_sequence=colors["chart_seq"],
# #                         )
# #                         fig.update_traces(textposition="top center")
# #                         st.plotly_chart(style_chart(fig, colors), use_container_width=True)
                
# #                 comparison_df = st.session_state.data.get("Comparison")
# #                 if comparison_df is not None:
# #                     st.markdown('<p class="section-title">Comparison Data</p>', unsafe_allow_html=True)
# #                     st.dataframe(comparison_df, use_container_width=True, hide_index=True)

# # else:
# #     st.info("No data found. Click 'Refresh Data' in the sidebar to run the pipeline and fetch the latest data.")

# # # Footer
# # st.markdown(
# #     f"""
# #     <hr style="margin:2rem 0 1rem 0; border-color:{colors['border']};">
# #     <p style="font-size:0.75rem; color:{colors['text_muted']}; text-align:center; letter-spacing:0.03em;">
# #         Data sourced from Screener.in and Company Investor Relations | Updated: {datetime.now().strftime('%d %b %Y, %H:%M')}
# #     </p>
# #     """,
# #     unsafe_allow_html=True,
# # )

# # dashboard.py (COMPLETE FIXED VERSION)
# """
# NIFTY IT Analytics Dashboard
# """

# import os
# import sys
# import subprocess
# from datetime import datetime
# from io import BytesIO

# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# import streamlit as st

# # --------------------------------------------------------------------------
# # Page configuration
# # --------------------------------------------------------------------------
# st.set_page_config(
#     page_title="NIFTY IT Analytics Dashboard",
#     page_icon="📊",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# # --------------------------------------------------------------------------
# # Color palettes
# # --------------------------------------------------------------------------
# LIGHT_COLORS = {
#     "bg": "#F5F8F7",
#     "card": "#FFFFFF",
#     "text_primary": "#0B1F1B",
#     "text_secondary": "#3F5D52",
#     "text_muted": "#6B8478",
#     "border": "#DCE7E1",
#     "primary": "#155E4B",
#     "secondary": "#1F7A5E",
#     "accent": "#2FA37B",
#     "chip_bg": "#E4F3EC",
#     "positive": "#0F9D68",
#     "negative": "#D64545",
#     "chart_seq": ["#0B3B2E", "#155E4B", "#2FA37B", "#63C79A", "#9BDCBE", "#CDEEDD"],
# }

# DARK_COLORS = {
#     "bg": "#0B120F",
#     "card": "#121D19",
#     "text_primary": "#EAF3EF",
#     "text_secondary": "#BBD6C9",
#     "text_muted": "#84A597",
#     "border": "#233731",
#     "primary": "#4FD9A6",
#     "secondary": "#39B78C",
#     "accent": "#7FE6BE",
#     "chip_bg": "#17251F",
#     "positive": "#3ADF9B",
#     "negative": "#FF6B6B",
#     "chart_seq": ["#CDEEDD", "#9BDCBE", "#63C79A", "#2FA37B", "#155E4B", "#0B3B2E"],
# }


# # --------------------------------------------------------------------------
# # Helpers
# # --------------------------------------------------------------------------
# def to_numeric_safe(series: pd.Series) -> pd.Series:
#     """Safely convert series to numeric, handling strings with currency symbols."""
#     if pd.api.types.is_numeric_dtype(series):
#         return series
#     # Remove currency symbols and commas, then convert
#     cleaned = series.astype(str).str.replace('₹', '', regex=False).str.replace(',', '', regex=False).str.strip()
#     cleaned = cleaned.replace('', 'NaN').replace('N/A', 'NaN')
#     return pd.to_numeric(cleaned, errors='coerce')


# def clean_dataframe_for_plotting(df: pd.DataFrame, numeric_cols: list) -> pd.DataFrame:
#     """Clean a dataframe for plotting - convert numeric cols and drop NaN."""
#     df_clean = df.copy()
#     for col in numeric_cols:
#         if col in df_clean.columns:
#             df_clean[col] = to_numeric_safe(df_clean[col])
#     return df_clean.dropna(subset=numeric_cols)


# def safe_sum(df: pd.DataFrame, col: str) -> float:
#     if col not in df.columns:
#         return 0.0
#     s = to_numeric_safe(df[col])
#     return float(s.sum()) if s.notna().any() else 0.0


# def safe_mean(df: pd.DataFrame, col: str) -> float:
#     if col not in df.columns:
#         return 0.0
#     s = to_numeric_safe(df[col])
#     return float(s.mean()) if s.notna().any() else 0.0


# def format_currency(value) -> str:
#     if pd.isna(value):
#         return "N/A"
#     try:
#         return f"₹{float(value):,.0f}"
#     except (ValueError, TypeError):
#         return "N/A"


# def format_percent(value) -> str:
#     if pd.isna(value):
#         return "N/A"
#     try:
#         return f"{float(value):.1f}%"
#     except (ValueError, TypeError):
#         return "N/A"


# def format_number(value) -> str:
#     if pd.isna(value):
#         return "N/A"
#     try:
#         return f"{float(value):,.0f}"
#     except (ValueError, TypeError):
#         return "N/A"


# def style_chart(fig, colors: dict, showlegend: bool = False, height: int = 400):
#     fig.update_layout(
#         plot_bgcolor="rgba(0,0,0,0)",
#         paper_bgcolor="rgba(0,0,0,0)",
#         font=dict(family="Inter, sans-serif", size=12, color=colors["text_secondary"]),
#         title_font=dict(color=colors["text_primary"], size=14),
#         height=height,
#         margin=dict(l=40, r=40, t=50, b=40),
#         showlegend=showlegend,
#         legend=dict(font=dict(color=colors["text_secondary"])),
#     )
#     fig.update_xaxes(color=colors["text_secondary"], gridcolor=colors["border"])
#     fig.update_yaxes(color=colors["text_secondary"], gridcolor=colors["border"])
#     return fig


# # --------------------------------------------------------------------------
# # CSS
# # --------------------------------------------------------------------------
# def load_css(colors: dict):
#     st.markdown(
#         f"""
#     <style>
#         @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

#         html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
#             background-color: {colors['bg']};
#         }}

#         [data-testid="stAppViewContainer"],
#         [data-testid="stAppViewContainer"] p,
#         [data-testid="stAppViewContainer"] span,
#         [data-testid="stAppViewContainer"] label,
#         [data-testid="stMarkdownContainer"] {{
#             font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
#             color: {colors['text_primary']};
#         }}

#         [data-testid="stHeader"] {{
#             background-color: transparent;
#         }}

#         [data-testid="stSidebar"] {{
#             background-color: {colors['card']};
#             border-right: 1px solid {colors['border']};
#         }}
#         [data-testid="stSidebar"] * {{
#             color: {colors['text_primary']};
#         }}
#         [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {{
#             color: {colors['text_secondary']};
#             font-weight: 500;
#         }}

#         .main-header {{
#             font-weight: 700;
#             font-size: 2.3rem;
#             color: {colors['primary']};
#             margin-bottom: 0.2rem;
#             letter-spacing: -0.02em;
#         }}

#         .sub-header {{
#             font-weight: 400;
#             font-size: 1rem;
#             color: {colors['text_secondary']};
#             margin-bottom: 1.8rem;
#         }}

#         .metric-card {{
#             background: {colors['card']};
#             border-radius: 14px;
#             padding: 1.1rem 1.4rem;
#             border: 1px solid {colors['border']};
#             box-shadow: 0 1px 3px rgba(0,0,0,0.08);
#             transition: transform 0.15s ease, box-shadow 0.15s ease;
#             position: relative;
#             overflow: hidden;
#         }}
#         .metric-card::before {{
#             content: '';
#             position: absolute;
#             top: 0; left: 0; right: 0;
#             height: 3px;
#             background: linear-gradient(90deg, {colors['secondary']}, {colors['accent']});
#         }}
#         .metric-card:hover {{
#             transform: translateY(-2px);
#             box-shadow: 0 8px 20px rgba(0,0,0,0.12);
#         }}
#         .metric-label {{
#             font-weight: 500;
#             font-size: 0.75rem;
#             color: {colors['text_muted']};
#             text-transform: uppercase;
#             letter-spacing: 0.06em;
#         }}
#         .metric-value {{
#             font-weight: 700;
#             font-size: 1.7rem;
#             color: {colors['text_primary']};
#             margin-top: 0.25rem;
#         }}

#         .section-title {{
#             font-weight: 600;
#             font-size: 1.15rem;
#             color: {colors['text_primary']};
#             margin: 1.4rem 0 0.9rem 0;
#             letter-spacing: -0.01em;
#         }}

#         .sidebar-section {{
#             font-weight: 600;
#             font-size: 0.75rem;
#             color: {colors['text_muted']};
#             text-transform: uppercase;
#             letter-spacing: 0.06em;
#             margin: 1.4rem 0 0.5rem 0;
#         }}

#         .stTabs [data-baseweb="tab-list"] {{
#             gap: 2px;
#             background-color: {colors['chip_bg']};
#             border-radius: 12px;
#             padding: 4px;
#         }}
#         .stTabs [data-baseweb="tab"] {{
#             font-weight: 500;
#             font-size: 0.85rem;
#             border-radius: 8px;
#             padding: 0.5rem 1.2rem;
#             color: {colors['text_secondary']};
#         }}
#         .stTabs [aria-selected="true"] {{
#             background-color: {colors['secondary']} !important;
#             color: #ffffff !important;
#         }}

#         .stButton > button, .stDownloadButton > button {{
#             font-weight: 500;
#             font-size: 0.85rem;
#             background: {colors['secondary']};
#             color: #ffffff;
#             border: none;
#             border-radius: 8px;
#             padding: 0.5rem 1.2rem;
#             transition: all 0.2s ease;
#         }}
#         .stButton > button:hover, .stDownloadButton > button:hover {{
#             background: {colors['accent']};
#             box-shadow: 0 4px 14px rgba(0,0,0,0.18);
#             color: #ffffff;
#         }}

#         [data-testid="stDataFrame"] {{
#             border: 1px solid {colors['border']};
#             border-radius: 10px;
#         }}

#         #MainMenu {{visibility: hidden;}}
#         footer {{visibility: hidden;}}

#         .positive {{ color: {colors['positive']}; }}
#         .negative {{ color: {colors['negative']}; }}

#         @media (max-width: 768px) {{
#             .main-header {{ font-size: 1.5rem; }}
#             .metric-value {{ font-size: 1.3rem; }}
#         }}
#     </style>
#     """,
#         unsafe_allow_html=True,
#     )


# # --------------------------------------------------------------------------
# # Data loading
# # --------------------------------------------------------------------------
# def load_excel_data():
#     """Load all sheets from the latest Excel file."""
#     output_dir = "output"
#     if not os.path.exists(output_dir):
#         return None

#     excel_files = [
#         f for f in os.listdir(output_dir)
#         if f.endswith(".xlsx") and f.startswith("nifty_it_data_")
#     ]
#     if not excel_files:
#         return None

#     latest_file = sorted(excel_files)[-1]
#     file_path = os.path.join(output_dir, latest_file)

#     try:
#         xl = pd.ExcelFile(file_path)
#         sheets = {}
#         for sheet_name in xl.sheet_names:
#             df = pd.read_excel(xl, sheet_name=sheet_name)
#             sheets[sheet_name] = df
#         return sheets
#     except Exception as e:
#         st.error(f"Error loading data: {e}")
#         return None


# # --------------------------------------------------------------------------
# # Session state
# # --------------------------------------------------------------------------
# defaults = {"data": None, "dark_mode": False, "running": False}
# for key, value in defaults.items():
#     if key not in st.session_state:
#         st.session_state[key] = value

# colors = DARK_COLORS if st.session_state.dark_mode else LIGHT_COLORS
# load_css(colors)

# # --------------------------------------------------------------------------
# # Sidebar
# # --------------------------------------------------------------------------
# with st.sidebar:
#     st.markdown(
#         f'<p style="font-weight:700; font-size:1.3rem; color:{colors["primary"]}; '
#         f'margin-bottom:0.1rem;">NIFTY IT</p>',
#         unsafe_allow_html=True,
#     )
#     st.markdown(
#         f'<p style="font-weight:300; font-size:0.8rem; color:{colors["text_muted"]}; '
#         f'margin-bottom:1.3rem;">Analytics Dashboard</p>',
#         unsafe_allow_html=True,
#     )

#     dark_mode = st.toggle("Dark mode", value=st.session_state.dark_mode)
#     if dark_mode != st.session_state.dark_mode:
#         st.session_state.dark_mode = dark_mode
#         st.rerun()

#     st.markdown(f'<hr style="margin:1.3rem 0; border-color:{colors["border"]};">', unsafe_allow_html=True)
#     st.markdown('<p class="sidebar-section">Controls</p>', unsafe_allow_html=True)

#     if st.button("Refresh data", use_container_width=True):
#         st.session_state.running = True
#         st.rerun()

#     st.markdown('<p class="sidebar-section">Filters</p>', unsafe_allow_html=True)

#     selected_companies = None
#     rev_range = None
#     deal_range = None

#     if st.session_state.data is not None:
#         df_full = st.session_state.data.get("Summary")
#         if df_full is not None:
#             companies = df_full["Company Name"].unique().tolist()
#             selected_companies = st.multiselect(
#                 "Companies", companies, default=companies, key="company_filter"
#             )

#             if "Current Revenue (Cr)" in df_full.columns:
#                 revenue_col = to_numeric_safe(df_full["Current Revenue (Cr)"])
#                 if revenue_col.notna().any():
#                     min_rev = float(revenue_col.min())
#                     max_rev = float(revenue_col.max())
#                     rev_range = st.slider(
#                         "Revenue range (Cr)",
#                         min_value=min_rev,
#                         max_value=max_rev,
#                         value=(min_rev, max_rev),
#                         step=100.0,
#                         key="rev_range",
#                     )

#             if "Deal Wins" in df_full.columns:
#                 deals_col = to_numeric_safe(df_full["Deal Wins"])
#                 if deals_col.notna().any():
#                     min_deals = int(deals_col.min())
#                     max_deals = int(deals_col.max())
#                     deal_range = st.slider(
#                         "Deal wins",
#                         min_value=min_deals,
#                         max_value=max_deals,
#                         value=(min_deals, max_deals),
#                         key="deal_range",
#                     )

#     st.markdown(f'<hr style="margin:1.3rem 0; border-color:{colors["border"]};">', unsafe_allow_html=True)
#     st.markdown('<p class="sidebar-section">Export</p>', unsafe_allow_html=True)

#     if st.session_state.data is not None:
#         def export_all_sheets():
#             output = BytesIO()
#             with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
#                 for sheet_name, df in st.session_state.data.items():
#                     df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
#             return output.getvalue()

#         col1, col2 = st.columns(2)
#         with col1:
#             st.download_button(
#                 "XLSX",
#                 data=export_all_sheets(),
#                 file_name=f"nifty_it_export_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
#                 mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#                 use_container_width=True,
#             )
#         with col2:
#             summary_df = st.session_state.data.get("Summary", pd.DataFrame())
#             st.download_button(
#                 "CSV",
#                 data=summary_df.to_csv(index=False).encode("utf-8"),
#                 file_name=f"nifty_it_export_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
#                 mime="text/csv",
#                 use_container_width=True,
#             )

# # --------------------------------------------------------------------------
# # Main content
# # --------------------------------------------------------------------------
# st.markdown('<p class="main-header">NIFTY IT Index</p>', unsafe_allow_html=True)
# st.markdown(
#     '<p class="sub-header">Real-time analytics and performance metrics of '
#     "India's top IT companies</p>",
#     unsafe_allow_html=True,
# )

# if st.session_state.running:
#     with st.spinner("Running data pipeline... this may take a few minutes."):
#         try:
#             result = subprocess.run(
#                 [sys.executable, "main.py"], capture_output=True, text=True
#             )
#             if result.returncode == 0:
#                 st.session_state.data = load_excel_data()
#                 st.success("Data refreshed successfully!")
#             else:
#                 st.error(f"Pipeline failed: {result.stderr[:200]}")
#         except Exception as e:
#             st.error(f"Error: {e}")
#     st.session_state.running = False
#     st.rerun()

# if st.session_state.data is None:
#     st.session_state.data = load_excel_data()

# if st.session_state.data is not None:
#     summary_df = st.session_state.data.get("Summary")
    
#     if summary_df is not None:
#         df = summary_df.copy()
        
#         # Clean numeric columns for the entire dataframe
#         numeric_cols = ["Current Revenue (Cr)", "Annual Revenue (Cr)", "Annual Profit (Cr)", 
#                        "Total TCV", "Deal Wins", "Total Clients", "Profit Margin %"]
#         for col in numeric_cols:
#             if col in df.columns:
#                 df[col] = to_numeric_safe(df[col])
        
#         # Apply filters
#         if selected_companies:
#             df = df[df["Company Name"].isin(selected_companies)]
#         if rev_range and "Current Revenue (Cr)" in df.columns:
#             rc = df["Current Revenue (Cr)"]
#             df = df[(rc >= rev_range[0]) & (rc <= rev_range[1])]
#         if deal_range and "Deal Wins" in df.columns:
#             dc = df["Deal Wins"]
#             df = df[(dc >= deal_range[0]) & (dc <= deal_range[1])]

#         if df.empty:
#             st.warning("No companies match the current filters. Try widening your filter ranges.")
#         else:
#             # Metrics row
#             c1, c2, c3, c4, c5 = st.columns(5)
#             with c1:
#                 st.markdown(
#                     f"""
#                     <div class="metric-card">
#                         <div class="metric-label">Total Revenue</div>
#                         <div class="metric-value">₹{df['Current Revenue (Cr)'].sum():,.0f} Cr</div>
#                     </div>
#                     """,
#                     unsafe_allow_html=True,
#                 )
#             with c2:
#                 st.markdown(
#                     f"""
#                     <div class="metric-card">
#                         <div class="metric-label">Average Revenue</div>
#                         <div class="metric-value">₹{df['Current Revenue (Cr)'].mean():,.0f} Cr</div>
#                     </div>
#                     """,
#                     unsafe_allow_html=True,
#                 )
#             with c3:
#                 st.markdown(
#                     f"""
#                     <div class="metric-card">
#                         <div class="metric-label">Total Deals</div>
#                         <div class="metric-value">{df['Deal Wins'].sum():,.0f}</div>
#                     </div>
#                     """,
#                     unsafe_allow_html=True,
#                 )
#             with c4:
#                 st.markdown(
#                     f"""
#                     <div class="metric-card">
#                         <div class="metric-label">Average Margin</div>
#                         <div class="metric-value">{df['Profit Margin %'].mean():.1f}%</div>
#                     </div>
#                     """,
#                     unsafe_allow_html=True,
#                 )
#             with c5:
#                 st.markdown(
#                     f"""
#                     <div class="metric-card">
#                         <div class="metric-label">Total Clients</div>
#                         <div class="metric-value">{df['Total Clients'].sum():,.0f}</div>
#                     </div>
#                     """,
#                     unsafe_allow_html=True,
#                 )

#             # Tabs matching Excel sheets
#             tab1, tab2, tab3, tab4, tab5 = st.tabs([
#                 "Summary", "Deal Wins", "Service Details", "Quarterly Details", "Comparison"
#             ])

#             # ------------------------------------------------------------------------
#             # TAB 1: SUMMARY
#             # ------------------------------------------------------------------------
#             with tab1:
#                 st.markdown('<p class="section-title">Performance Overview</p>', unsafe_allow_html=True)
                
#                 col1, col2 = st.columns(2)
#                 with col1:
#                     chart_df = df.dropna(subset=["Current Revenue (Cr)"])
#                     if not chart_df.empty:
#                         fig = px.bar(
#                             chart_df, x="Company Name", y="Current Revenue (Cr)",
#                             title="Revenue by Company", color="Current Revenue (Cr)",
#                             color_continuous_scale=colors["chart_seq"],
#                             text="Current Revenue (Cr)",
#                         )
#                         fig.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
#                         st.plotly_chart(style_chart(fig, colors), use_container_width=True)

#                 with col2:
#                     margin_df = df.dropna(subset=["Profit Margin %"])
#                     if not margin_df.empty:
#                         fig = px.bar(
#                             margin_df, x="Company Name", y="Profit Margin %",
#                             title="Profit Margin by Company", color="Profit Margin %",
#                             color_continuous_scale="RdYlGn",
#                             text="Profit Margin %",
#                         )
#                         fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
#                         st.plotly_chart(style_chart(fig, colors), use_container_width=True)

#                 # Summary Table
#                 st.markdown('<p class="section-title">Summary Data</p>', unsafe_allow_html=True)
#                 display_df = df.copy()
                
#                 # Format each column safely
#                 if "Current Revenue (Cr)" in display_df.columns:
#                     display_df["Current Revenue (Cr)"] = display_df["Current Revenue (Cr)"].apply(format_currency)
#                 if "Annual Revenue (Cr)" in display_df.columns:
#                     display_df["Annual Revenue (Cr)"] = display_df["Annual Revenue (Cr)"].apply(format_currency)
#                 if "Profit Margin %" in display_df.columns:
#                     display_df["Profit Margin %"] = display_df["Profit Margin %"].apply(format_percent)
#                 if "Total TCV" in display_df.columns:
#                     display_df["Total TCV"] = display_df["Total TCV"].apply(format_number)
#                 if "Deal Wins" in display_df.columns:
#                     display_df["Deal Wins"] = display_df["Deal Wins"].apply(format_number)
#                 if "Total Clients" in display_df.columns:
#                     display_df["Total Clients"] = display_df["Total Clients"].apply(format_number)
                
#                 st.dataframe(display_df, use_container_width=True, hide_index=True)

#             # ------------------------------------------------------------------------
#             # TAB 2: DEAL WINS
#             # ------------------------------------------------------------------------
#             with tab2:
#                 st.markdown('<p class="section-title">Deal Wins Detail</p>', unsafe_allow_html=True)
#                 deal_df = st.session_state.data.get("Deal Wins")
#                 if deal_df is not None and not deal_df.empty:
#                     if selected_companies and "Company" in deal_df.columns:
#                         deal_df = deal_df[deal_df["Company"].isin(selected_companies)]
                    
#                     col1, col2 = st.columns(2)
#                     with col1:
#                         if "Company" in deal_df.columns:
#                             deal_counts = deal_df.groupby("Company").size().reset_index(name="Count")
#                             if not deal_counts.empty:
#                                 fig = px.bar(
#                                     deal_counts, x="Company", y="Count",
#                                     title="Deal Wins by Company",
#                                     color="Count", color_continuous_scale=colors["chart_seq"],
#                                     text="Count"
#                                 )
#                                 fig.update_traces(texttemplate="%{text}", textposition="outside")
#                                 st.plotly_chart(style_chart(fig, colors), use_container_width=True)
                    
#                     with col2:
#                         if "Deal Value" in deal_df.columns:
#                             value_counts = deal_df["Deal Value"].value_counts().head(10)
#                             if not value_counts.empty:
#                                 fig = px.pie(
#                                     values=value_counts.values, names=value_counts.index,
#                                     title="Deal Value Distribution",
#                                     color_discrete_sequence=colors["chart_seq"]
#                                 )
#                                 st.plotly_chart(style_chart(fig, colors, showlegend=True), use_container_width=True)
                    
#                     st.dataframe(deal_df, use_container_width=True, hide_index=True)
#                 else:
#                     st.info("No deal wins data available.")

#             # ------------------------------------------------------------------------
#             # TAB 3: SERVICE DETAILS
#             # ------------------------------------------------------------------------
#             with tab3:
#                 st.markdown('<p class="section-title">Service Details</p>', unsafe_allow_html=True)
#                 service_df = st.session_state.data.get("Services Detail")
#                 if service_df is not None and not service_df.empty:
#                     if selected_companies and "Company" in service_df.columns:
#                         service_df = service_df[service_df["Company"].isin(selected_companies)]
                    
#                     if "Category" in service_df.columns:
#                         categories = service_df["Category"].value_counts().head(10)
#                         if not categories.empty:
#                             fig = px.bar(
#                                 x=categories.values, y=categories.index,
#                                 orientation='h', title="Top Service Categories",
#                                 color=categories.values, color_continuous_scale=colors["chart_seq"],
#                                 text=categories.values
#                             )
#                             fig.update_traces(texttemplate="%{text}", textposition="outside")
#                             fig.update_layout(
#                                 xaxis_title="Count",
#                                 yaxis_title="Category",
#                                 height=400
#                             )
#                             st.plotly_chart(style_chart(fig, colors), use_container_width=True)
                    
#                     st.dataframe(service_df, use_container_width=True, hide_index=True)
#                 else:
#                     st.info("No service details available.")

#             # ------------------------------------------------------------------------
#             # TAB 4: QUARTERLY DETAILS
#             # ------------------------------------------------------------------------
#             with tab4:
#                 st.markdown('<p class="section-title">Quarterly Details</p>', unsafe_allow_html=True)
#                 quarterly_df = st.session_state.data.get("Quarterly Details")
#                 if quarterly_df is not None and not quarterly_df.empty:
#                     if selected_companies and "Company" in quarterly_df.columns:
#                         quarterly_df = quarterly_df[quarterly_df["Company"].isin(selected_companies)]
                    
#                     # Clean numeric columns for quarterly data
#                     if "Revenue (Cr)" in quarterly_df.columns:
#                         quarterly_df["Revenue (Cr)"] = to_numeric_safe(quarterly_df["Revenue (Cr)"])
                    
#                     if "Quarter" in quarterly_df.columns and "Revenue (Cr)" in quarterly_df.columns:
#                         recent_df = quarterly_df.tail(20).dropna(subset=["Revenue (Cr)"])
#                         if not recent_df.empty:
#                             fig = px.line(
#                                 recent_df, x="Quarter", y="Revenue (Cr)",
#                                 color="Company", title="Quarterly Revenue Trend",
#                                 color_discrete_sequence=colors["chart_seq"]
#                             )
#                             st.plotly_chart(style_chart(fig, colors, showlegend=True), use_container_width=True)
                    
#                     st.dataframe(quarterly_df, use_container_width=True, hide_index=True)
#                 else:
#                     st.info("No quarterly data available.")

#             # ------------------------------------------------------------------------
#             # TAB 5: COMPARISON
#             # ------------------------------------------------------------------------
#             with tab5:
#                 st.markdown('<p class="section-title">Company Comparison</p>', unsafe_allow_html=True)
                
#                 col1, col2 = st.columns(2)
#                 with col1:
#                     scatter_df = df.dropna(subset=["Current Revenue (Cr)", "Annual Profit (Cr)"])
#                     if not scatter_df.empty:
#                         fig = px.scatter(
#                             scatter_df, x="Current Revenue (Cr)", y="Annual Profit (Cr)",
#                             size="Current Revenue (Cr)", color="Company Name",
#                             text="Company Name", title="Revenue vs Profit",
#                             color_discrete_sequence=colors["chart_seq"],
#                         )
#                         fig.update_traces(textposition="top center")
#                         st.plotly_chart(style_chart(fig, colors), use_container_width=True)
#                     else:
#                         st.info("No data available for Revenue vs Profit scatter plot.")
                
#                 with col2:
#                     tcv_df = df.dropna(subset=["Total TCV", "Deal Wins"])
#                     if not tcv_df.empty:
#                         fig = px.scatter(
#                             tcv_df, x="Total TCV", y="Deal Wins",
#                             size="Total TCV", color="Company Name",
#                             text="Company Name", title="TCV vs Deal Wins",
#                             color_discrete_sequence=colors["chart_seq"],
#                         )
#                         fig.update_traces(textposition="top center")
#                         st.plotly_chart(style_chart(fig, colors), use_container_width=True)
#                     else:
#                         st.info("No data available for TCV vs Deal Wins scatter plot.")
                
#                 comparison_df = st.session_state.data.get("Comparison")
#                 if comparison_df is not None:
#                     st.markdown('<p class="section-title">Comparison Data</p>', unsafe_allow_html=True)
#                     st.dataframe(comparison_df, use_container_width=True, hide_index=True)

# else:
#     st.info("No data found. Click 'Refresh Data' in the sidebar to run the pipeline and fetch the latest data.")

# # Footer
# st.markdown(
#     f"""
#     <hr style="margin:2rem 0 1rem 0; border-color:{colors['border']};">
#     <p style="font-size:0.75rem; color:{colors['text_muted']}; text-align:center; letter-spacing:0.03em;">
#         Data sourced from Screener.in and Company Investor Relations | Updated: {datetime.now().strftime('%d %b %Y, %H:%M')}
#     </p>
#     """,
#     unsafe_allow_html=True,
# )

# # dashboard.py
# """
# NIFTY IT Analytics Dashboard
# """

# import os
# import sys
# import subprocess
# from datetime import datetime
# from io import BytesIO

# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# import streamlit as st

# # --------------------------------------------------------------------------
# # Page configuration
# # --------------------------------------------------------------------------
# st.set_page_config(
#     page_title="NIFTY IT Analytics Dashboard",
#     page_icon="📊",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# # --------------------------------------------------------------------------
# # Color palettes
# # --------------------------------------------------------------------------
# LIGHT_COLORS = {
#     "bg": "#F5F8F7",
#     "card": "#FFFFFF",
#     "text_primary": "#0B1F1B",
#     "text_secondary": "#3F5D52",
#     "text_muted": "#6B8478",
#     "border": "#DCE7E1",
#     "primary": "#155E4B",
#     "secondary": "#1F7A5E",
#     "accent": "#2FA37B",
#     "chip_bg": "#E4F3EC",
#     "positive": "#0F9D68",
#     "negative": "#D64545",
#     "chart_seq": ["#0B3B2E", "#155E4B", "#2FA37B", "#63C79A", "#9BDCBE", "#CDEEDD"],
# }

# DARK_COLORS = {
#     "bg": "#0B120F",
#     "card": "#121D19",
#     "text_primary": "#EAF3EF",
#     "text_secondary": "#BBD6C9",
#     "text_muted": "#84A597",
#     "border": "#233731",
#     "primary": "#4FD9A6",
#     "secondary": "#39B78C",
#     "accent": "#7FE6BE",
#     "chip_bg": "#17251F",
#     "positive": "#3ADF9B",
#     "negative": "#FF6B6B",
#     "chart_seq": ["#CDEEDD", "#9BDCBE", "#63C79A", "#2FA37B", "#155E4B", "#0B3B2E"],
# }


# # --------------------------------------------------------------------------
# # Helpers
# # --------------------------------------------------------------------------
# def to_numeric_safe(series: pd.Series) -> pd.Series:
#     """Safely convert series to numeric, handling strings with currency symbols."""
#     if pd.api.types.is_numeric_dtype(series):
#         return series
#     cleaned = series.astype(str).str.replace('₹', '', regex=False).str.replace(',', '', regex=False).str.strip()
#     cleaned = cleaned.replace('', 'NaN').replace('N/A', 'NaN')
#     return pd.to_numeric(cleaned, errors='coerce')


# def format_currency(value) -> str:
#     if pd.isna(value):
#         return "N/A"
#     try:
#         return f"₹{float(value):,.0f}"
#     except (ValueError, TypeError):
#         return "N/A"


# def format_percent(value) -> str:
#     if pd.isna(value):
#         return "N/A"
#     try:
#         return f"{float(value):.1f}%"
#     except (ValueError, TypeError):
#         return "N/A"


# def format_number(value) -> str:
#     if pd.isna(value):
#         return "N/A"
#     try:
#         return f"{float(value):,.0f}"
#     except (ValueError, TypeError):
#         return "N/A"


# def style_chart(fig, colors: dict, showlegend: bool = False, height: int = 400):
#     fig.update_layout(
#         plot_bgcolor="rgba(0,0,0,0)",
#         paper_bgcolor="rgba(0,0,0,0)",
#         font=dict(family="Inter, sans-serif", size=12, color=colors["text_secondary"]),
#         title_font=dict(color=colors["text_primary"], size=14),
#         height=height,
#         margin=dict(l=40, r=40, t=50, b=40),
#         showlegend=showlegend,
#         legend=dict(font=dict(color=colors["text_secondary"])),
#     )
#     fig.update_xaxes(color=colors["text_secondary"], gridcolor=colors["border"])
#     fig.update_yaxes(color=colors["text_secondary"], gridcolor=colors["border"])
#     return fig


# # --------------------------------------------------------------------------
# # CSS
# # --------------------------------------------------------------------------
# def load_css(colors: dict):
#     st.markdown(
#         f"""
#     <style>
#         @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

#         html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
#             background-color: {colors['bg']};
#         }}

#         [data-testid="stAppViewContainer"],
#         [data-testid="stAppViewContainer"] p,
#         [data-testid="stAppViewContainer"] span,
#         [data-testid="stAppViewContainer"] label,
#         [data-testid="stMarkdownContainer"] {{
#             font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
#             color: {colors['text_primary']};
#         }}

#         [data-testid="stHeader"] {{
#             background-color: transparent;
#         }}

#         [data-testid="stSidebar"] {{
#             background-color: {colors['card']};
#             border-right: 1px solid {colors['border']};
#         }}
#         [data-testid="stSidebar"] * {{
#             color: {colors['text_primary']};
#         }}
#         [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {{
#             color: {colors['text_secondary']};
#             font-weight: 500;
#         }}

#         .main-header {{
#             font-weight: 700;
#             font-size: 2.3rem;
#             color: {colors['primary']};
#             margin-bottom: 0.2rem;
#             letter-spacing: -0.02em;
#         }}

#         .sub-header {{
#             font-weight: 400;
#             font-size: 1rem;
#             color: {colors['text_secondary']};
#             margin-bottom: 1.8rem;
#         }}

#         .metric-card {{
#             background: {colors['card']};
#             border-radius: 14px;
#             padding: 1.1rem 1.4rem;
#             border: 1px solid {colors['border']};
#             box-shadow: 0 1px 3px rgba(0,0,0,0.08);
#             transition: transform 0.15s ease, box-shadow 0.15s ease;
#             position: relative;
#             overflow: hidden;
#         }}
#         .metric-card::before {{
#             content: '';
#             position: absolute;
#             top: 0; left: 0; right: 0;
#             height: 3px;
#             background: linear-gradient(90deg, {colors['secondary']}, {colors['accent']});
#         }}
#         .metric-card:hover {{
#             transform: translateY(-2px);
#             box-shadow: 0 8px 20px rgba(0,0,0,0.12);
#         }}
#         .metric-label {{
#             font-weight: 500;
#             font-size: 0.75rem;
#             color: {colors['text_muted']};
#             text-transform: uppercase;
#             letter-spacing: 0.06em;
#         }}
#         .metric-value {{
#             font-weight: 700;
#             font-size: 1.7rem;
#             color: {colors['text_primary']};
#             margin-top: 0.25rem;
#         }}

#         .section-title {{
#             font-weight: 600;
#             font-size: 1.15rem;
#             color: {colors['text_primary']};
#             margin: 1.4rem 0 0.9rem 0;
#             letter-spacing: -0.01em;
#         }}

#         .sidebar-section {{
#             font-weight: 600;
#             font-size: 0.75rem;
#             color: {colors['text_muted']};
#             text-transform: uppercase;
#             letter-spacing: 0.06em;
#             margin: 1.4rem 0 0.5rem 0;
#         }}

#         .stTabs [data-baseweb="tab-list"] {{
#             gap: 2px;
#             background-color: {colors['chip_bg']};
#             border-radius: 12px;
#             padding: 4px;
#         }}
#         .stTabs [data-baseweb="tab"] {{
#             font-weight: 500;
#             font-size: 0.85rem;
#             border-radius: 8px;
#             padding: 0.5rem 1.2rem;
#             color: {colors['text_secondary']};
#         }}
#         .stTabs [aria-selected="true"] {{
#             background-color: {colors['secondary']} !important;
#             color: #ffffff !important;
#         }}

#         .stButton > button, .stDownloadButton > button {{
#             font-weight: 500;
#             font-size: 0.85rem;
#             background: {colors['secondary']};
#             color: #ffffff;
#             border: none;
#             border-radius: 8px;
#             padding: 0.5rem 1.2rem;
#             transition: all 0.2s ease;
#         }}
#         .stButton > button:hover, .stDownloadButton > button:hover {{
#             background: {colors['accent']};
#             box-shadow: 0 4px 14px rgba(0,0,0,0.18);
#             color: #ffffff;
#         }}

#         [data-testid="stDataFrame"] {{
#             border: 1px solid {colors['border']};
#             border-radius: 10px;
#         }}

#         #MainMenu {{visibility: hidden;}}
#         footer {{visibility: hidden;}}

#         .positive {{ color: {colors['positive']}; }}
#         .negative {{ color: {colors['negative']}; }}

#         @media (max-width: 768px) {{
#             .main-header {{ font-size: 1.5rem; }}
#             .metric-value {{ font-size: 1.3rem; }}
#         }}
#     </style>
#     """,
#         unsafe_allow_html=True,
#     )


# # --------------------------------------------------------------------------
# # Data loading
# # --------------------------------------------------------------------------
# def load_excel_data():
#     """Load all sheets from the latest Excel file."""
#     output_dir = "output"
#     if not os.path.exists(output_dir):
#         return None

#     excel_files = [
#         f for f in os.listdir(output_dir)
#         if f.endswith(".xlsx") and f.startswith("nifty_it_data_")
#     ]
#     if not excel_files:
#         return None

#     latest_file = sorted(excel_files)[-1]
#     file_path = os.path.join(output_dir, latest_file)

#     try:
#         xl = pd.ExcelFile(file_path)
#         sheets = {}
#         for sheet_name in xl.sheet_names:
#             df = pd.read_excel(xl, sheet_name=sheet_name)
#             sheets[sheet_name] = df
#         return sheets
#     except Exception as e:
#         st.error(f"Error loading data: {e}")
#         return None


# # --------------------------------------------------------------------------
# # Session state
# # --------------------------------------------------------------------------
# defaults = {"data": None, "dark_mode": False, "running": False}
# for key, value in defaults.items():
#     if key not in st.session_state:
#         st.session_state[key] = value

# colors = DARK_COLORS if st.session_state.dark_mode else LIGHT_COLORS
# load_css(colors)

# # --------------------------------------------------------------------------
# # Sidebar
# # --------------------------------------------------------------------------
# with st.sidebar:
#     st.markdown(
#         f'<p style="font-weight:700; font-size:1.3rem; color:{colors["primary"]}; '
#         f'margin-bottom:0.1rem;">NIFTY IT</p>',
#         unsafe_allow_html=True,
#     )
#     st.markdown(
#         f'<p style="font-weight:300; font-size:0.8rem; color:{colors["text_muted"]}; '
#         f'margin-bottom:1.3rem;">Analytics Dashboard</p>',
#         unsafe_allow_html=True,
#     )

#     dark_mode = st.toggle("Dark mode", value=st.session_state.dark_mode)
#     if dark_mode != st.session_state.dark_mode:
#         st.session_state.dark_mode = dark_mode
#         st.rerun()

#     st.markdown(f'<hr style="margin:1.3rem 0; border-color:{colors["border"]};">', unsafe_allow_html=True)
#     st.markdown('<p class="sidebar-section">Controls</p>', unsafe_allow_html=True)

#     if st.button("Refresh data", use_container_width=True):
#         st.session_state.running = True
#         st.rerun()

#     st.markdown('<p class="sidebar-section">Filters</p>', unsafe_allow_html=True)

#     selected_companies = None
#     rev_range = None
#     deal_range = None

#     if st.session_state.data is not None:
#         df_full = st.session_state.data.get("Summary")
#         if df_full is not None:
#             companies = df_full["Company Name"].unique().tolist()
#             selected_companies = st.multiselect(
#                 "Companies", companies, default=companies, key="company_filter"
#             )

#             if "Current Revenue (Cr)" in df_full.columns:
#                 revenue_col = to_numeric_safe(df_full["Current Revenue (Cr)"])
#                 if revenue_col.notna().any():
#                     min_rev = float(revenue_col.min())
#                     max_rev = float(revenue_col.max())
#                     rev_range = st.slider(
#                         "Revenue range (Cr)",
#                         min_value=min_rev,
#                         max_value=max_rev,
#                         value=(min_rev, max_rev),
#                         step=100.0,
#                         key="rev_range",
#                     )

#             if "Deal Wins" in df_full.columns:
#                 deals_col = to_numeric_safe(df_full["Deal Wins"])
#                 if deals_col.notna().any():
#                     min_deals = int(deals_col.min())
#                     max_deals = int(deals_col.max())
#                     deal_range = st.slider(
#                         "Deal wins",
#                         min_value=min_deals,
#                         max_value=max_deals,
#                         value=(min_deals, max_deals),
#                         key="deal_range",
#                     )

#     st.markdown(f'<hr style="margin:1.3rem 0; border-color:{colors["border"]};">', unsafe_allow_html=True)
#     st.markdown('<p class="sidebar-section">Export</p>', unsafe_allow_html=True)

#     if st.session_state.data is not None:
#         def export_all_sheets():
#             output = BytesIO()
#             with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
#                 for sheet_name, df in st.session_state.data.items():
#                     df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
#             return output.getvalue()

#         col1, col2 = st.columns(2)
#         with col1:
#             st.download_button(
#                 "XLSX",
#                 data=export_all_sheets(),
#                 file_name=f"nifty_it_export_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
#                 mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#                 use_container_width=True,
#             )
#         with col2:
#             summary_df = st.session_state.data.get("Summary", pd.DataFrame())
#             st.download_button(
#                 "CSV",
#                 data=summary_df.to_csv(index=False).encode("utf-8"),
#                 file_name=f"nifty_it_export_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
#                 mime="text/csv",
#                 use_container_width=True,
#             )

# # --------------------------------------------------------------------------
# # Main content
# # --------------------------------------------------------------------------
# st.markdown('<p class="main-header">NIFTY IT Index</p>', unsafe_allow_html=True)
# st.markdown(
#     '<p class="sub-header">Real-time analytics and performance metrics of '
#     "India's top IT companies</p>",
#     unsafe_allow_html=True,
# )

# if st.session_state.running:
#     with st.spinner("Running data pipeline... this may take a few minutes."):
#         try:
#             result = subprocess.run(
#                 [sys.executable, "main.py"], capture_output=True, text=True
#             )
#             if result.returncode == 0:
#                 st.session_state.data = load_excel_data()
#                 st.success("Data refreshed successfully!")
#             else:
#                 st.error(f"Pipeline failed: {result.stderr[:200]}")
#         except Exception as e:
#             st.error(f"Error: {e}")
#     st.session_state.running = False
#     st.rerun()

# if st.session_state.data is None:
#     st.session_state.data = load_excel_data()

# if st.session_state.data is not None:
#     summary_df = st.session_state.data.get("Summary")
    
#     if summary_df is not None:
#         df = summary_df.copy()
        
#         # Clean numeric columns
#         numeric_cols = ["Current Revenue (Cr)", "Annual Revenue (Cr)", "Annual Profit (Cr)", 
#                        "Total TCV", "Deal Wins", "Total Clients", "Profit Margin %"]
#         for col in numeric_cols:
#             if col in df.columns:
#                 df[col] = to_numeric_safe(df[col])
        
#         # Apply filters
#         if selected_companies:
#             df = df[df["Company Name"].isin(selected_companies)]
#         if rev_range and "Current Revenue (Cr)" in df.columns:
#             rc = df["Current Revenue (Cr)"]
#             df = df[(rc >= rev_range[0]) & (rc <= rev_range[1])]
#         if deal_range and "Deal Wins" in df.columns:
#             dc = df["Deal Wins"]
#             df = df[(dc >= deal_range[0]) & (dc <= deal_range[1])]

#         if df.empty:
#             st.warning("No companies match the current filters.")
#         else:
#             # Metrics row
#             c1, c2, c3, c4, c5 = st.columns(5)
#             with c1:
#                 st.markdown(
#                     f"""
#                     <div class="metric-card">
#                         <div class="metric-label">Total Revenue</div>
#                         <div class="metric-value">₹{df['Current Revenue (Cr)'].sum():,.0f} Cr</div>
#                     </div>
#                     """,
#                     unsafe_allow_html=True,
#                 )
#             with c2:
#                 st.markdown(
#                     f"""
#                     <div class="metric-card">
#                         <div class="metric-label">Average Revenue</div>
#                         <div class="metric-value">₹{df['Current Revenue (Cr)'].mean():,.0f} Cr</div>
#                     </div>
#                     """,
#                     unsafe_allow_html=True,
#                 )
#             with c3:
#                 st.markdown(
#                     f"""
#                     <div class="metric-card">
#                         <div class="metric-label">Total Deals</div>
#                         <div class="metric-value">{df['Deal Wins'].sum():,.0f}</div>
#                     </div>
#                     """,
#                     unsafe_allow_html=True,
#                 )
#             with c4:
#                 st.markdown(
#                     f"""
#                     <div class="metric-card">
#                         <div class="metric-label">Average Margin</div>
#                         <div class="metric-value">{df['Profit Margin %'].mean():.1f}%</div>
#                     </div>
#                     """,
#                     unsafe_allow_html=True,
#                 )
#             with c5:
#                 st.markdown(
#                     f"""
#                     <div class="metric-card">
#                         <div class="metric-label">Total Clients</div>
#                         <div class="metric-value">{df['Total Clients'].sum():,.0f}</div>
#                     </div>
#                     """,
#                     unsafe_allow_html=True,
#                 )

#             # Tabs
#             tab1, tab2, tab3, tab4, tab5 = st.tabs([
#                 "Summary", "Deal Wins", "Service Details", "Quarterly Details", "Comparison"
#             ])

#             # TAB 1: SUMMARY
#             with tab1:
#                 st.markdown('<p class="section-title">Performance Overview</p>', unsafe_allow_html=True)
                
#                 col1, col2 = st.columns(2)
#                 with col1:
#                     chart_df = df.dropna(subset=["Current Revenue (Cr)"])
#                     if not chart_df.empty:
#                         fig = px.bar(
#                             chart_df, x="Company Name", y="Current Revenue (Cr)",
#                             title="Revenue by Company", color="Current Revenue (Cr)",
#                             color_continuous_scale=colors["chart_seq"],
#                             text="Current Revenue (Cr)",
#                         )
#                         fig.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
#                         st.plotly_chart(style_chart(fig, colors), use_container_width=True)

#                 with col2:
#                     margin_df = df.dropna(subset=["Profit Margin %"])
#                     if not margin_df.empty:
#                         fig = px.bar(
#                             margin_df, x="Company Name", y="Profit Margin %",
#                             title="Profit Margin by Company", color="Profit Margin %",
#                             color_continuous_scale="RdYlGn",
#                             text="Profit Margin %",
#                         )
#                         fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
#                         st.plotly_chart(style_chart(fig, colors), use_container_width=True)

#                 # Summary Table
#                 st.markdown('<p class="section-title">Summary Data</p>', unsafe_allow_html=True)
#                 display_df = df.copy()
#                 if "Current Revenue (Cr)" in display_df.columns:
#                     display_df["Current Revenue (Cr)"] = display_df["Current Revenue (Cr)"].apply(format_currency)
#                 if "Annual Revenue (Cr)" in display_df.columns:
#                     display_df["Annual Revenue (Cr)"] = display_df["Annual Revenue (Cr)"].apply(format_currency)
#                 if "Profit Margin %" in display_df.columns:
#                     display_df["Profit Margin %"] = display_df["Profit Margin %"].apply(format_percent)
#                 if "Total TCV" in display_df.columns:
#                     display_df["Total TCV"] = display_df["Total TCV"].apply(format_number)
#                 if "Deal Wins" in display_df.columns:
#                     display_df["Deal Wins"] = display_df["Deal Wins"].apply(format_number)
#                 if "Total Clients" in display_df.columns:
#                     display_df["Total Clients"] = display_df["Total Clients"].apply(format_number)
                
#                 st.dataframe(display_df, use_container_width=True, hide_index=True)

#             # TAB 2: DEAL WINS
#             with tab2:
#                 st.markdown('<p class="section-title">Deal Wins Detail</p>', unsafe_allow_html=True)
#                 deal_df = st.session_state.data.get("Deal Wins")
#                 if deal_df is not None and not deal_df.empty:
#                     if selected_companies and "Company" in deal_df.columns:
#                         deal_df = deal_df[deal_df["Company"].isin(selected_companies)]
                    
#                     col1, col2 = st.columns(2)
#                     with col1:
#                         if "Company" in deal_df.columns:
#                             deal_counts = deal_df.groupby("Company").size().reset_index(name="Count")
#                             if not deal_counts.empty:
#                                 fig = px.bar(
#                                     deal_counts, x="Company", y="Count",
#                                     title="Deal Wins by Company",
#                                     color="Count", color_continuous_scale=colors["chart_seq"],
#                                     text="Count"
#                                 )
#                                 fig.update_traces(texttemplate="%{text}", textposition="outside")
#                                 st.plotly_chart(style_chart(fig, colors), use_container_width=True)
                    
#                     with col2:
#                         if "Deal Value" in deal_df.columns:
#                             value_counts = deal_df["Deal Value"].value_counts().head(10)
#                             if not value_counts.empty:
#                                 fig = px.pie(
#                                     values=value_counts.values, names=value_counts.index,
#                                     title="Deal Value Distribution",
#                                     color_discrete_sequence=colors["chart_seq"]
#                                 )
#                                 st.plotly_chart(style_chart(fig, colors, showlegend=True), use_container_width=True)
                    
#                     st.dataframe(deal_df, use_container_width=True, hide_index=True)
#                 else:
#                     st.info("No deal wins data available.")

#             # TAB 3: SERVICE DETAILS
#             with tab3:
#                 st.markdown('<p class="section-title">Service Details</p>', unsafe_allow_html=True)
#                 service_df = st.session_state.data.get("Services Detail")
#                 if service_df is not None and not service_df.empty:
#                     if selected_companies and "Company" in service_df.columns:
#                         service_df = service_df[service_df["Company"].isin(selected_companies)]
                    
#                     if "Category" in service_df.columns:
#                         categories = service_df["Category"].value_counts().head(10)
#                         if not categories.empty:
#                             fig = px.bar(
#                                 x=categories.values, y=categories.index,
#                                 orientation='h', title="Top Service Categories",
#                                 color=categories.values, color_continuous_scale=colors["chart_seq"],
#                                 text=categories.values
#                             )
#                             fig.update_traces(texttemplate="%{text}", textposition="outside")
#                             fig.update_layout(
#                                 xaxis_title="Count",
#                                 yaxis_title="Category",
#                                 height=400
#                             )
#                             st.plotly_chart(style_chart(fig, colors), use_container_width=True)
                    
#                     st.dataframe(service_df, use_container_width=True, hide_index=True)
#                 else:
#                     st.info("No service details available.")

#             # TAB 4: QUARTERLY DETAILS
#             with tab4:
#                 st.markdown('<p class="section-title">Quarterly Details</p>', unsafe_allow_html=True)
#                 quarterly_df = st.session_state.data.get("Quarterly Details")
#                 if quarterly_df is not None and not quarterly_df.empty:
#                     if selected_companies and "Company" in quarterly_df.columns:
#                         quarterly_df = quarterly_df[quarterly_df["Company"].isin(selected_companies)]
                    
#                     if "Revenue (Cr)" in quarterly_df.columns:
#                         quarterly_df["Revenue (Cr)"] = to_numeric_safe(quarterly_df["Revenue (Cr)"])
                    
#                     if "Quarter" in quarterly_df.columns and "Revenue (Cr)" in quarterly_df.columns:
#                         recent_df = quarterly_df.tail(20).dropna(subset=["Revenue (Cr)"])
#                         if not recent_df.empty:
#                             fig = px.line(
#                                 recent_df, x="Quarter", y="Revenue (Cr)",
#                                 color="Company", title="Quarterly Revenue Trend",
#                                 color_discrete_sequence=colors["chart_seq"]
#                             )
#                             st.plotly_chart(style_chart(fig, colors, showlegend=True), use_container_width=True)
                    
#                     st.dataframe(quarterly_df, use_container_width=True, hide_index=True)
#                 else:
#                     st.info("No quarterly data available.")

#             # TAB 5: COMPARISON
#             with tab5:
#                 st.markdown('<p class="section-title">Company Comparison</p>', unsafe_allow_html=True)
                
#                 col1, col2 = st.columns(2)
#                 with col1:
#                     scatter_df = df.dropna(subset=["Current Revenue (Cr)", "Annual Profit (Cr)"])
#                     if not scatter_df.empty:
#                         fig = px.scatter(
#                             scatter_df, x="Current Revenue (Cr)", y="Annual Profit (Cr)",
#                             size="Current Revenue (Cr)", color="Company Name",
#                             text="Company Name", title="Revenue vs Profit",
#                             color_discrete_sequence=colors["chart_seq"],
#                         )
#                         fig.update_traces(textposition="top center")
#                         st.plotly_chart(style_chart(fig, colors), use_container_width=True)
                
#                 with col2:
#                     tcv_df = df.dropna(subset=["Total TCV", "Deal Wins"])
#                     if not tcv_df.empty:
#                         fig = px.scatter(
#                             tcv_df, x="Total TCV", y="Deal Wins",
#                             size="Total TCV", color="Company Name",
#                             text="Company Name", title="TCV vs Deal Wins",
#                             color_discrete_sequence=colors["chart_seq"],
#                         )
#                         fig.update_traces(textposition="top center")
#                         st.plotly_chart(style_chart(fig, colors), use_container_width=True)
                
#                 comparison_df = st.session_state.data.get("Comparison")
#                 if comparison_df is not None:
#                     st.markdown('<p class="section-title">Comparison Data</p>', unsafe_allow_html=True)
#                     st.dataframe(comparison_df, use_container_width=True, hide_index=True)

# else:
#     st.info("No data found. Click 'Refresh Data' in the sidebar to run the pipeline and fetch the latest data.")

# # Footer
# st.markdown(
#     f"""
#     <hr style="margin:2rem 0 1rem 0; border-color:{colors['border']};">
#     <p style="font-size:0.75rem; color:{colors['text_muted']}; text-align:center; letter-spacing:0.03em;">
#         Data sourced from Screener.in and Company Investor Relations | Updated: {datetime.now().strftime('%d %b %Y, %H:%M')}
#     </p>
#     """,
#     unsafe_allow_html=True,
# )