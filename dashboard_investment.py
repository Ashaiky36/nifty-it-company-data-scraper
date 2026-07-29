# # dashboard_investment.py
# """
# NIFTY IT Investment Decision Dashboard
# """

# import os
# import sys
# import subprocess
# from datetime import datetime
# from io import BytesIO

# import pandas as pd
# import numpy as np
# import plotly.express as px
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# import streamlit as st

# # Import the investment indicators
# from investment_indicators import InvestmentIndicators

# # ... (previous color palettes, helpers, CSS - keep same as before) ...

# # --------------------------------------------------------------------------
# # Investment Dashboard Specific Functions
# # --------------------------------------------------------------------------
# def create_investment_chart(df: pd.DataFrame, colors: dict):
#     """Create investment decision chart"""
#     fig = make_subplots(
#         rows=2, cols=2,
#         subplot_titles=(
#             'Revenue Growth vs Margin',
#             'Deal Momentum',
#             'Investment Score by Company',
#             'Risk vs Return'
#         ),
#         specs=[[{"secondary_y": True}, {}],
#                [{"colspan": 2}, None]]
#     )
    
#     # 1. Revenue Growth vs Margin
#     fig.add_trace(
#         go.Bar(
#             x=df['Company Name'],
#             y=df['Revenue_Growth'],
#             name='Revenue Growth %',
#             marker_color=colors['chart_seq'][0],
#             text=df['Revenue_Growth'].round(1),
#             textposition='outside'
#         ),
#         row=1, col=1, secondary_y=False
#     )
    
#     fig.add_trace(
#         go.Scatter(
#             x=df['Company Name'],
#             y=df['Net_Margin'],
#             name='Net Margin %',
#             mode='lines+markers',
#             marker=dict(color=colors['accent'], size=12),
#             line=dict(color=colors['accent'], width=3),
#             text=df['Net_Margin'].round(1),
#             textposition='top center'
#         ),
#         row=1, col=1, secondary_y=True
#     )
    
#     # 2. Deal Momentum
#     fig.add_trace(
#         go.Bar(
#             x=df['Company Name'],
#             y=df['Deal_to_Revenue_Ratio'],
#             name='Deal to Revenue Ratio',
#             marker_color=colors['chart_seq'][1],
#             text=df['Deal_to_Revenue_Ratio'].round(1),
#             textposition='outside'
#         ),
#         row=1, col=2
#     )
    
#     # 3. Investment Score
#     colors_scale = ['#ff6b6b', '#ffa94d', '#ffd93d', '#6bcb77', '#4d96ff']
#     fig.add_trace(
#         go.Bar(
#             x=df['Company Name'],
#             y=df['Investment_Score'],
#             name='Investment Score',
#             marker_color=[colors_scale[int(score-1) % len(colors_scale)] for score in df['Investment_Score']],
#             text=df['Investment_Score'].round(2),
#             textposition='outside'
#         ),
#         row=2, col=1
#     )
    
#     fig.update_layout(
#         height=800,
#         showlegend=True,
#         font=dict(family="Inter, sans-serif"),
#         template='plotly_white'
#     )
    
#     fig.update_xaxes(title_text="Company", row=1, col=1)
#     fig.update_xaxes(title_text="Company", row=1, col=2)
#     fig.update_xaxes(title_text="Company", row=2, col=1)
    
#     fig.update_yaxes(title_text="Growth %", row=1, col=1, secondary_y=False)
#     fig.update_yaxes(title_text="Margin %", row=1, col=1, secondary_y=True)
    
#     return fig

# def create_risk_matrix(df: pd.DataFrame, colors: dict):
#     """Create risk-reward matrix"""
#     fig = go.Figure()
    
#     # Define risk levels and colors
#     risk_colors = {
#         'Low': '#6bcb77',
#         'Medium': '#ffd93d',
#         'High': '#ffa94d',
#         'Very High': '#ff6b6b'
#     }
    
#     fig.add_trace(go.Scatter(
#         x=df['Risk_Score'],
#         y=df['Investment_Score'],
#         mode='markers+text',
#         marker=dict(
#             size=[score * 10 for score in df['Investment_Score']],
#             color=[risk_colors[risk] for risk in df['Risk_Level']],
#             line=dict(width=2, color='white')
#         ),
#         text=df['Company Name'],
#         textposition='top center',
#         name='Companies'
#     ))
    
#     # Add quadrant lines
#     fig.add_hline(y=df['Investment_Score'].mean(), line_dash="dash", line_color="gray")
#     fig.add_vline(x=df['Risk_Score'].mean(), line_dash="dash", line_color="gray")
    
#     # Add quadrant labels
#     fig.add_annotation(
#         x=df['Risk_Score'].max() * 0.85,
#         y=df['Investment_Score'].max() * 0.85,
#         text="Champions",
#         showarrow=False,
#         font=dict(size=14, color=colors['positive']),
#         opacity=0.5
#     )
#     fig.add_annotation(
#         x=df['Risk_Score'].min() * 1.15,
#         y=df['Investment_Score'].max() * 0.85,
#         text="High Growth - Low Risk",
#         showarrow=False,
#         font=dict(size=14, color=colors['positive']),
#         opacity=0.5
#     )
#     fig.add_annotation(
#         x=df['Risk_Score'].max() * 0.85,
#         y=df['Investment_Score'].min() * 1.15,
#         text="High Risk - Low Return",
#         showarrow=False,
#         font=dict(size=14, color=colors['negative']),
#         opacity=0.5
#     )
#     fig.add_annotation(
#         x=df['Risk_Score'].min() * 1.15,
#         y=df['Investment_Score'].min() * 1.15,
#         text="Value Traps",
#         showarrow=False,
#         font=dict(size=14, color=colors['text_muted']),
#         opacity=0.5
#     )
    
#     fig.update_layout(
#         title="Risk-Reward Matrix",
#         xaxis_title="Risk Score",
#         yaxis_title="Investment Score",
#         height=500,
#         font=dict(family="Inter, sans-serif"),
#         plot_bgcolor="rgba(0,0,0,0)",
#         paper_bgcolor="rgba(0,0,0,0)",
#     )
    
#     return fig

# defaults = {"data": None, "dark_mode": False, "running": False}
# for key, value in defaults.items():
#     if key not in st.session_state:
#         st.session_state[key] = value

# # --------------------------------------------------------------------------
# # Main Dashboard
# # --------------------------------------------------------------------------
# def main():
#       # Initialize session state FIRST
#     if "data" not in st.session_state:
#         st.session_state.data = None
#     if "dark_mode" not in st.session_state:
#         st.session_state.dark_mode = False
#     if "running" not in st.session_state:
#         st.session_state.running = False
    
#     # Then load data
#     if st.session_state.data is None:
#         st.session_state.data = load_excel_data()
#     # ... (previous sidebar and data loading code) ...
    
#     if st.session_state.data is not None:
#         summary_df = st.session_state.data.get("Summary")
        
#         if summary_df is not None:
#             # Calculate investment indicators
#             df = InvestmentIndicators.calculate_indicators(summary_df)
            
#             # Investment Summary Section
#             st.markdown('<p class="section-title">Investment Decision Summary</p>', unsafe_allow_html=True)
            
#             # Investment Score Cards
#             c1, c2, c3, c4 = st.columns(4)
            
#             with c1:
#                 top_pick = df.loc[df['Investment_Score'].idxmax(), 'Company Name']
#                 st.markdown(f"""
#                 <div class="metric-card">
#                     <div class="metric-label">Top Pick</div>
#                     <div class="metric-value" style="font-size:1.2rem;">{top_pick}</div>
#                     <div style="font-size:0.8rem; color:{colors['text_secondary']};">
#                         Score: {df['Investment_Score'].max():.2f}
#                     </div>
#                 </div>
#                 """, unsafe_allow_html=True)
            
#             with c2:
#                 best_growth = df.loc[df['Revenue_Growth'].idxmax(), 'Company Name']
#                 st.markdown(f"""
#                 <div class="metric-card">
#                     <div class="metric-label">Highest Growth</div>
#                     <div class="metric-value" style="font-size:1.2rem;">{best_growth}</div>
#                     <div style="font-size:0.8rem; color:{colors['text_secondary']};">
#                         {df['Revenue_Growth'].max():.1f}% YoY
#                     </div>
#                 </div>
#                 """, unsafe_allow_html=True)
            
#             with c3:
#                 best_margin = df.loc[df['Net_Margin'].idxmax(), 'Company Name']
#                 st.markdown(f"""
#                 <div class="metric-card">
#                     <div class="metric-label">Best Margin</div>
#                     <div class="metric-value" style="font-size:1.2rem;">{best_margin}</div>
#                     <div style="font-size:0.8rem; color:{colors['text_secondary']};">
#                         {df['Net_Margin'].max():.1f}%
#                     </div>
#                 </div>
#                 """, unsafe_allow_html=True)
            
#             with c4:
#                 best_deal = df.loc[df['Deal_to_Revenue_Ratio'].idxmax(), 'Company Name']
#                 st.markdown(f"""
#                 <div class="metric-card">
#                     <div class="metric-label">Best Deal Momentum</div>
#                     <div class="metric-value" style="font-size:1.2rem;">{best_deal}</div>
#                     <div style="font-size:0.8rem; color:{colors['text_secondary']};">
#                         {df['Deal_to_Revenue_Ratio'].max():.1f}%
#                     </div>
#                 </div>
#                 """, unsafe_allow_html=True)
            
#             # Investment Recommendations Table
#             st.markdown('<p class="section-title">Investment Recommendations</p>', unsafe_allow_html=True)
            
#             rec_df = df[['Company Name', 'Investment_Score', 'Recommendation', 'Risk_Level', 
#                         'Revenue_Growth', 'Net_Margin', 'Deal_to_Revenue_Ratio']].copy()
            
#             # Format for display
#             rec_df['Investment_Score'] = rec_df['Investment_Score'].round(2)
#             rec_df['Revenue_Growth'] = rec_df['Revenue_Growth'].round(1).map(lambda x: f"{x:.1f}%")
#             rec_df['Net_Margin'] = rec_df['Net_Margin'].round(1).map(lambda x: f"{x:.1f}%")
#             rec_df['Deal_to_Revenue_Ratio'] = rec_df['Deal_to_Revenue_Ratio'].round(1).map(lambda x: f"{x:.1f}%")
            
#             # Color code recommendations
#             def color_recommendation(val):
#                 colors_map = {
#                     'Strong Buy': '#6bcb77',
#                     'Buy': '#ffd93d',
#                     'Hold': '#ffa94d',
#                     'Sell': '#ff6b6b',
#                     'Strong Sell': '#cc0000'
#                 }
#                 return f'<span style="color:{colors_map.get(val, "#666")}; font-weight:bold;">{val}</span>'
            
#             rec_df['Recommendation'] = rec_df['Recommendation'].apply(color_recommendation)
            
#             st.markdown(rec_df.to_html(escape=False, index=False), unsafe_allow_html=True)
            
#             # Investment Charts
#             st.markdown('<p class="section-title">Investment Analytics</p>', unsafe_allow_html=True)
            
#             tab1, tab2 = st.tabs(["Investment Dashboard", "Risk-Reward Matrix"])
            
#             with tab1:
#                 fig = create_investment_chart(df, colors)
#                 st.plotly_chart(fig, use_container_width=True)
            
#             with tab2:
#                 # Calculate risk scores
#                 df['Risk_Score'] = df['Risk_Level'].map({
#                     'Low': 1, 'Medium': 2, 'High': 3, 'Very High': 4
#                 })
#                 fig = create_risk_matrix(df, colors)
#                 st.plotly_chart(fig, use_container_width=True)
            
#             # Investment Insights
#             st.markdown('<p class="section-title">Investment Insights</p>', unsafe_allow_html=True)
            
#             insights = []
            
#             # Top performer insight
#             top = df.loc[df['Investment_Score'].idxmax()]
#             insights.append(f"🏆 **Top Pick: {top['Company Name']}** - Score {top['Investment_Score']:.2f}/5.0")
            
#             # Growth insight
#             fastest = df.loc[df['Revenue_Growth'].idxmax()]
#             insights.append(f"📈 **Fastest Growing: {fastest['Company Name']}** - {fastest['Revenue_Growth']:.1f}% YoY growth")
            
#             # Margin insight
#             most_profitable = df.loc[df['Net_Margin'].idxmax()]
#             insights.append(f"💰 **Most Profitable: {most_profitable['Company Name']}** - {most_profitable['Net_Margin']:.1f}% net margin")
            
#             # Risk insight
#             lowest_risk = df.loc[df['Risk_Score'].idxmin()]
#             insights.append(f"🛡️ **Lowest Risk: {lowest_risk['Company Name']}** - {lowest_risk['Risk_Level']} risk")
            
#             # Deal momentum insight
#             best_deal = df.loc[df['Deal_to_Revenue_Ratio'].idxmax()]
#             insights.append(f"💼 **Best Deal Momentum: {best_deal['Company Name']}** - Deal/Revenue ratio: {best_deal['Deal_to_Revenue_Ratio']:.1f}%")
            
#             # Market sentiment
#             buys = len(df[df['Recommendation'].str.contains('Buy')])
#             holds = len(df[df['Recommendation'] == 'Hold'])
#             sells = len(df[df['Recommendation'].str.contains('Sell')])
#             insights.append(f"📊 **Market Sentiment**: {buys} Buys, {holds} Holds, {sells} Sells")
            
#             for insight in insights:
#                 st.markdown(f"<p style='margin:0.3rem 0; color:{colors['text_secondary']};'>{insight}</p>", unsafe_allow_html=True)

# if __name__ == "__main__":
#     main()

# dashboard_investment.py
"""
NIFTY IT Investment Decision Dashboard
"""

import os
import sys
import subprocess
from datetime import datetime
from io import BytesIO

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# --------------------------------------------------------------------------
# Color palettes
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


# --------------------------------------------------------------------------
# Data Helpers
# --------------------------------------------------------------------------
def to_numeric_safe(series: pd.Series) -> pd.Series:
    """Safely convert series to numeric, handling strings with currency symbols."""
    if pd.api.types.is_numeric_dtype(series):
        return series
    cleaned = series.astype(str).str.replace('₹', '', regex=False).str.replace(',', '', regex=False).str.strip()
    cleaned = cleaned.replace('', 'NaN').replace('N/A', 'NaN')
    return pd.to_numeric(cleaned, errors='coerce')


def load_excel_data():
    """Load all sheets from the latest Excel file."""
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
        xl = pd.ExcelFile(file_path)
        sheets = {}
        for sheet_name in xl.sheet_names:
            df = pd.read_excel(xl, sheet_name=sheet_name)
            # Clean numeric columns for Summary sheet
            if sheet_name == "Summary":
                numeric_cols = ["Current Revenue (Cr)", "Annual Revenue (Cr)", "Annual Profit (Cr)", 
                               "Total TCV", "Deal Wins", "Total Clients", "Profit Margin %"]
                for col in numeric_cols:
                    if col in df.columns:
                        df[col] = to_numeric_safe(df[col])
            sheets[sheet_name] = df
        return sheets
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None


def format_currency(value) -> str:
    if pd.isna(value):
        return "N/A"
    try:
        return f"₹{float(value):,.0f}"
    except (ValueError, TypeError):
        return "N/A"


def format_percent(value) -> str:
    if pd.isna(value):
        return "N/A"
    try:
        return f"{float(value):.1f}%"
    except (ValueError, TypeError):
        return "N/A"


def format_number(value) -> str:
    if pd.isna(value):
        return "N/A"
    try:
        return f"{float(value):,.0f}"
    except (ValueError, TypeError):
        return "N/A"


def style_chart(fig, colors: dict, showlegend: bool = False, height: int = 400):
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
# Investment Indicators
# --------------------------------------------------------------------------
def calculate_investment_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate all investment indicators"""
    df = df.copy()
    
    # 1. Growth Indicators
    df['Revenue_Growth'] = df['Annual Revenue (Cr)'].pct_change() * 100
    
    # 2. Profitability Indicators
    df['Net_Margin'] = (df['Annual Profit (Cr)'] / df['Annual Revenue (Cr)']) * 100
    
    # 3. Scale Indicators
    df['Revenue_per_Client'] = df['Annual Revenue (Cr)'] / df['Total Clients'].replace(0, np.nan)
    
    # 4. Deal Momentum
    df['Deal_to_Revenue_Ratio'] = (df['Deal Wins'] / (df['Annual Revenue (Cr)'] / 100)) * 100
    
    # 5. Composite Score (Weighted)
    df['Growth_Score'] = pd.qcut(df['Revenue_Growth'].rank(pct=True), 5, labels=False) + 1
    df['Profit_Score'] = pd.qcut(df['Net_Margin'].rank(pct=True), 5, labels=False) + 1
    df['Scale_Score'] = pd.qcut(df['Annual Revenue (Cr)'].rank(pct=True), 5, labels=False) + 1
    df['Deal_Score'] = pd.qcut(df['Deal_to_Revenue_Ratio'].rank(pct=True), 5, labels=False) + 1
    
    df['Investment_Score'] = (
        df['Growth_Score'] * 0.30 +
        df['Profit_Score'] * 0.25 +
        df['Scale_Score'] * 0.25 +
        df['Deal_Score'] * 0.20
    )
    
    # 6. Recommendation
    def get_recommendation(score):
        if score >= 4.5:
            return 'Strong Buy'
        elif score >= 3.5:
            return 'Buy'
        elif score >= 2.5:
            return 'Hold'
        elif score >= 1.5:
            return 'Sell'
        else:
            return 'Strong Sell'
    
    df['Recommendation'] = df['Investment_Score'].apply(get_recommendation)
    
    # 7. Risk Level
    def get_risk(row):
        risk = 0
        if row.get('Revenue_Growth', 0) < 5:
            risk += 1
        if row.get('Net_Margin', 0) < 15:
            risk += 1
        if row.get('Deal_to_Revenue_Ratio', 0) < 50:
            risk += 1
        if row.get('Total Clients', 0) < 50:
            risk += 1
        
        if risk <= 1:
            return 'Low'
        elif risk <= 2:
            return 'Medium'
        elif risk <= 3:
            return 'High'
        else:
            return 'Very High'
    
    df['Risk_Level'] = df.apply(get_risk, axis=1)
    df['Risk_Score'] = df['Risk_Level'].map({'Low': 1, 'Medium': 2, 'High': 3, 'Very High': 4})
    
    return df


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

        [data-testid="stDataFrame"] {{
            border: 1px solid {colors['border']};
            border-radius: 10px;
        }}

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
# Investment Chart Functions
# --------------------------------------------------------------------------
def create_investment_chart(df: pd.DataFrame, colors: dict):
    """Create investment decision chart"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Revenue Growth vs Margin',
            'Deal Momentum',
            'Investment Score by Company',
            'Risk vs Return'
        ),
        specs=[[{"secondary_y": True}, {}],
               [{"colspan": 2}, None]]
    )
    
    # 1. Revenue Growth vs Margin
    fig.add_trace(
        go.Bar(
            x=df['Company Name'],
            y=df['Revenue_Growth'],
            name='Revenue Growth %',
            marker_color=colors['chart_seq'][0],
            text=df['Revenue_Growth'].round(1) if df['Revenue_Growth'].notna().any() else None,
            textposition='outside'
        ),
        row=1, col=1, secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(
            x=df['Company Name'],
            y=df['Net_Margin'],
            name='Net Margin %',
            mode='lines+markers',
            marker=dict(color=colors['accent'], size=12),
            line=dict(color=colors['accent'], width=3),
        ),
        row=1, col=1, secondary_y=True
    )
    
    # 2. Deal Momentum
    fig.add_trace(
        go.Bar(
            x=df['Company Name'],
            y=df['Deal_to_Revenue_Ratio'],
            name='Deal to Revenue Ratio',
            marker_color=colors['chart_seq'][1],
        ),
        row=1, col=2
    )
    
    # 3. Investment Score
    colors_scale = ['#ff6b6b', '#ffa94d', '#ffd93d', '#6bcb77', '#4d96ff']
    fig.add_trace(
        go.Bar(
            x=df['Company Name'],
            y=df['Investment_Score'],
            name='Investment Score',
            marker_color=[colors_scale[min(int(score-1), 4)] for score in df['Investment_Score'].fillna(3)],
        ),
        row=2, col=1
    )
    
    fig.update_layout(
        height=800,
        showlegend=True,
        font=dict(family="Inter, sans-serif"),
    )
    
    fig.update_xaxes(title_text="Company", row=1, col=1)
    fig.update_xaxes(title_text="Company", row=1, col=2)
    fig.update_xaxes(title_text="Company", row=2, col=1)
    
    fig.update_yaxes(title_text="Growth %", row=1, col=1, secondary_y=False)
    fig.update_yaxes(title_text="Margin %", row=1, col=1, secondary_y=True)
    
    return fig


def create_risk_matrix(df: pd.DataFrame, colors: dict):
    """Create risk-reward matrix"""
    fig = go.Figure()
    
    risk_colors = {
        'Low': '#6bcb77',
        'Medium': '#ffd93d',
        'High': '#ffa94d',
        'Very High': '#ff6b6b'
    }
    
    # Get valid data
    valid_df = df.dropna(subset=['Risk_Score', 'Investment_Score'])
    
    if not valid_df.empty:
        fig.add_trace(go.Scatter(
            x=valid_df['Risk_Score'],
            y=valid_df['Investment_Score'],
            mode='markers+text',
            marker=dict(
                size=[min(max(score * 10, 20), 80) for score in valid_df['Investment_Score'].fillna(3)],
                color=[risk_colors.get(risk, '#888') for risk in valid_df['Risk_Level']],
                line=dict(width=2, color='white')
            ),
            text=valid_df['Company Name'],
            textposition='top center',
            name='Companies'
        ))
    
    # Add quadrant lines
    fig.add_hline(y=df['Investment_Score'].mean(), line_dash="dash", line_color="gray")
    fig.add_vline(x=df['Risk_Score'].mean(), line_dash="dash", line_color="gray")
    
    fig.update_layout(
        title="Risk-Reward Matrix",
        xaxis_title="Risk Score",
        yaxis_title="Investment Score",
        height=500,
        font=dict(family="Inter, sans-serif"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    
    return fig


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
def main():
    # Initialize session state
    if "data" not in st.session_state:
        st.session_state.data = None
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False
    if "running" not in st.session_state:
        st.session_state.running = False
    
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
            f'margin-bottom:1.3rem;">Investment Dashboard</p>',
            unsafe_allow_html=True,
        )

        dark_mode = st.toggle("Dark mode", value=st.session_state.dark_mode)
        if dark_mode != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_mode
            st.rerun()

        st.markdown(f'<hr style="margin:1.3rem 0; border-color:{colors["border"]};">', unsafe_allow_html=True)
        st.markdown('<p class="sidebar-section">Controls</p>', unsafe_allow_html=True)

        if st.button("Refresh data", use_container_width=True):
            st.session_state.running = True
            st.rerun()

        st.markdown('<p class="sidebar-section">Filters</p>', unsafe_allow_html=True)

        selected_companies = None
        rev_range = None
        deal_range = None

        if st.session_state.data is not None:
            df_full = st.session_state.data.get("Summary")
            if df_full is not None:
                companies = df_full["Company Name"].unique().tolist()
                selected_companies = st.multiselect(
                    "Companies", companies, default=companies, key="company_filter"
                )

        st.markdown(f'<hr style="margin:1.3rem 0; border-color:{colors["border"]};">', unsafe_allow_html=True)
        st.markdown('<p class="sidebar-section">Export</p>', unsafe_allow_html=True)

        if st.session_state.data is not None:
            def export_all_sheets():
                output = BytesIO()
                with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                    for sheet_name, df in st.session_state.data.items():
                        df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
                return output.getvalue()

            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    "XLSX",
                    data=export_all_sheets(),
                    file_name=f"nifty_it_export_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                )
            with col2:
                summary_df = st.session_state.data.get("Summary", pd.DataFrame())
                st.download_button(
                    "CSV",
                    data=summary_df.to_csv(index=False).encode("utf-8"),
                    file_name=f"nifty_it_export_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

    # --------------------------------------------------------------------------
    # Main content
    # --------------------------------------------------------------------------
    st.markdown('<p class="main-header">NIFTY IT Index</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Investment Decision Dashboard - Real-time analytics for India\'s top IT companies</p>',
        unsafe_allow_html=True,
    )

    if st.session_state.running:
        with st.spinner("Running data pipeline... this may take a few minutes."):
            try:
                result = subprocess.run(
                    [sys.executable, "main.py"], capture_output=True, text=True
                )
                if result.returncode == 0:
                    st.session_state.data = load_excel_data()
                    st.success("Data refreshed successfully!")
                else:
                    st.error(f"Pipeline failed: {result.stderr[:200]}")
            except Exception as e:
                st.error(f"Error: {e}")
        st.session_state.running = False
        st.rerun()

    # Load data if not loaded
    if st.session_state.data is None:
        st.session_state.data = load_excel_data()

    if st.session_state.data is not None:
        summary_df = st.session_state.data.get("Summary")
        
        if summary_df is not None:
            df = summary_df.copy()
            
            # Apply company filter
            if selected_companies:
                df = df[df["Company Name"].isin(selected_companies)]

            if df.empty:
                st.warning("No companies match the current filters.")
            else:
                # Calculate investment indicators
                df_invest = calculate_investment_indicators(df)
                
                # Investment Summary Section
                st.markdown('<p class="section-title">Investment Decision Summary</p>', unsafe_allow_html=True)
                
                # Investment Score Cards
                c1, c2, c3, c4 = st.columns(4)
                
                with c1:
                    top_pick = df_invest.loc[df_invest['Investment_Score'].idxmax(), 'Company Name']
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Top Pick</div>
                        <div class="metric-value" style="font-size:1.2rem;">{top_pick}</div>
                        <div style="font-size:0.8rem; color:{colors['text_secondary']};">
                            Score: {df_invest['Investment_Score'].max():.2f}/5.0
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with c2:
                    if df_invest['Revenue_Growth'].notna().any():
                        best_growth = df_invest.loc[df_invest['Revenue_Growth'].idxmax(), 'Company Name']
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Highest Growth</div>
                            <div class="metric-value" style="font-size:1.2rem;">{best_growth}</div>
                            <div style="font-size:0.8rem; color:{colors['text_secondary']};">
                                {df_invest['Revenue_Growth'].max():.1f}% YoY
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                with c3:
                    if df_invest['Net_Margin'].notna().any():
                        best_margin = df_invest.loc[df_invest['Net_Margin'].idxmax(), 'Company Name']
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Best Margin</div>
                            <div class="metric-value" style="font-size:1.2rem;">{best_margin}</div>
                            <div style="font-size:0.8rem; color:{colors['text_secondary']};">
                                {df_invest['Net_Margin'].max():.1f}%
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                with c4:
                    if df_invest['Deal_to_Revenue_Ratio'].notna().any():
                        best_deal = df_invest.loc[df_invest['Deal_to_Revenue_Ratio'].idxmax(), 'Company Name']
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Best Deal Momentum</div>
                            <div class="metric-value" style="font-size:1.2rem;">{best_deal}</div>
                            <div style="font-size:0.8rem; color:{colors['text_secondary']};">
                                {df_invest['Deal_to_Revenue_Ratio'].max():.1f}%
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Investment Recommendations Table
                st.markdown('<p class="section-title">Investment Recommendations</p>', unsafe_allow_html=True)
                
                rec_df = df_invest[['Company Name', 'Investment_Score', 'Recommendation', 'Risk_Level', 
                                    'Revenue_Growth', 'Net_Margin', 'Deal_to_Revenue_Ratio']].copy()
                
                rec_df['Investment_Score'] = rec_df['Investment_Score'].round(2)
                rec_df['Revenue_Growth'] = rec_df['Revenue_Growth'].round(1).map(lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A")
                rec_df['Net_Margin'] = rec_df['Net_Margin'].round(1).map(lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A")
                rec_df['Deal_to_Revenue_Ratio'] = rec_df['Deal_to_Revenue_Ratio'].round(1).map(lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A")
                
                # Color code recommendations
                def color_recommendation(val):
                    colors_map = {
                        'Strong Buy': '#6bcb77',
                        'Buy': '#ffd93d',
                        'Hold': '#ffa94d',
                        'Sell': '#ff6b6b',
                        'Strong Sell': '#cc0000'
                    }
                    return f'<span style="color:{colors_map.get(val, "#666")}; font-weight:bold;">{val}</span>'
                
                rec_df['Recommendation'] = rec_df['Recommendation'].apply(color_recommendation)
                
                st.markdown(rec_df.to_html(escape=False, index=False), unsafe_allow_html=True)
                
                # Investment Charts
                st.markdown('<p class="section-title">Investment Analytics</p>', unsafe_allow_html=True)
                
                tab1, tab2 = st.tabs(["Investment Dashboard", "Risk-Reward Matrix"])
                
                with tab1:
                    fig = create_investment_chart(df_invest, colors)
                    st.plotly_chart(fig, use_container_width=True)
                
                with tab2:
                    fig = create_risk_matrix(df_invest, colors)
                    st.plotly_chart(fig, use_container_width=True)
                
                # Investment Insights
                st.markdown('<p class="section-title">Investment Insights</p>', unsafe_allow_html=True)
                
                insights = []
                
                if not df_invest.empty:
                    # Top performer insight
                    top = df_invest.loc[df_invest['Investment_Score'].idxmax()]
                    insights.append(f"Top Pick: {top['Company Name']} - Score {top['Investment_Score']:.2f}/5.0")
                    
                    # Growth insight
                    if df_invest['Revenue_Growth'].notna().any():
                        fastest = df_invest.loc[df_invest['Revenue_Growth'].idxmax()]
                        insights.append(f"Fastest Growing: {fastest['Company Name']} - {fastest['Revenue_Growth']:.1f}% YoY growth")
                    
                    # Margin insight
                    if df_invest['Net_Margin'].notna().any():
                        most_profitable = df_invest.loc[df_invest['Net_Margin'].idxmax()]
                        insights.append(f"Most Profitable: {most_profitable['Company Name']} - {most_profitable['Net_Margin']:.1f}% net margin")
                    
                    # Risk insight
                    lowest_risk = df_invest.loc[df_invest['Risk_Score'].idxmin()]
                    insights.append(f"Lowest Risk: {lowest_risk['Company Name']} - {lowest_risk['Risk_Level']} risk")
                    
                    # Deal momentum insight
                    if df_invest['Deal_to_Revenue_Ratio'].notna().any():
                        best_deal_insight = df_invest.loc[df_invest['Deal_to_Revenue_Ratio'].idxmax()]
                        insights.append(f"Best Deal Momentum: {best_deal_insight['Company Name']} - Deal/Revenue ratio: {best_deal_insight['Deal_to_Revenue_Ratio']:.1f}%")
                    
                    # Market sentiment
                    buys = len(df_invest[df_invest['Recommendation'].str.contains('Buy')])
                    holds = len(df_invest[df_invest['Recommendation'] == 'Hold'])
                    sells = len(df_invest[df_invest['Recommendation'].str.contains('Sell')])
                    insights.append(f"Market Sentiment: {buys} Buys, {holds} Holds, {sells} Sells")
                
                for insight in insights:
                    st.markdown(f"<p style='margin:0.3rem 0; color:{colors['text_secondary']};'>• {insight}</p>", unsafe_allow_html=True)
        else:
            st.info("No Summary sheet found in the data.")
    else:
        st.info("No data found. Click 'Refresh Data' in the sidebar to run the pipeline and fetch the latest data.")

    # Footer
    st.markdown(
        f"""
        <hr style="margin:2rem 0 1rem 0; border-color:{colors['border']};">
        <p style="font-size:0.75rem; color:{colors['text_muted']}; text-align:center; letter-spacing:0.03em;">
            Data sourced from Screener.in and Company Investor Relations | Updated: {datetime.now().strftime('%d %b %Y, %H:%M')}
        </p>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()