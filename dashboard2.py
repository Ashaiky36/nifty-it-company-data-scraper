# # dashboard.py
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# import os
# from datetime import datetime
# import subprocess
# import sys
# import json
# import base64
# from io import BytesIO

# # Page configuration
# st.set_page_config(
#     page_title="NIFTY IT Analytics Dashboard",
#     page_icon="📊",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS for premium minimalist design
# def load_css():
#     st.markdown(f"""
#     <style>
#         /* Import premium fonts */
#         @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
#         /* Dark mode variables */
#         :root {{
#             --bg-primary: #ffffff;
#             --bg-secondary: #f8f9fa;
#             --bg-card: #ffffff;
#             --text-primary: #1a1a2e;
#             --text-secondary: #4a4a6a;
#             --text-muted: #8a8aaa;
#             --border-color: #e8e8f0;
#             --accent: #6366f1;
#             --accent-hover: #4f46e5;
#             --shadow: 0 1px 3px rgba(0,0,0,0.06);
#         }}
        
#         /* Dark mode */
#         [data-theme="dark"] {{
#             --bg-primary: #0f0f1a;
#             --bg-secondary: #1a1a2e;
#             --bg-card: #1e1e32;
#             --text-primary: #e8e8f0;
#             --text-secondary: #b0b0d0;
#             --text-muted: #6a6a8a;
#             --border-color: #2a2a4a;
#             --shadow: 0 1px 3px rgba(0,0,0,0.3);
#         }}
        
#         /* Global styles */
#         .stApp {{
#             background-color: var(--bg-primary);
#             font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
#         }}
        
#         .main-header {{
#             font-family: 'Inter', sans-serif;
#             font-weight: 600;
#             font-size: 2.2rem;
#             color: var(--text-primary);
#             margin-bottom: 0.2rem;
#             letter-spacing: -0.02em;
#         }}
        
#         .sub-header {{
#             font-family: 'Inter', sans-serif;
#             font-weight: 400;
#             font-size: 0.95rem;
#             color: var(--text-secondary);
#             margin-bottom: 2rem;
#         }}
        
#         .metric-card {{
#             background: var(--bg-card);
#             border-radius: 12px;
#             padding: 1.2rem 1.5rem;
#             border: 1px solid var(--border-color);
#             box-shadow: var(--shadow);
#             transition: all 0.2s ease;
#         }}
        
#         .metric-card:hover {{
#             transform: translateY(-2px);
#             box-shadow: 0 4px 12px rgba(99, 102, 241, 0.1);
#         }}
        
#         .metric-label {{
#             font-family: 'Inter', sans-serif;
#             font-weight: 400;
#             font-size: 0.8rem;
#             color: var(--text-muted);
#             text-transform: uppercase;
#             letter-spacing: 0.05em;
#         }}
        
#         .metric-value {{
#             font-family: 'Inter', sans-serif;
#             font-weight: 600;
#             font-size: 1.8rem;
#             color: var(--text-primary);
#             margin-top: 0.2rem;
#         }}
        
#         .metric-change {{
#             font-family: 'Inter', sans-serif;
#             font-size: 0.8rem;
#             font-weight: 500;
#             margin-top: 0.2rem;
#         }}
        
#         .positive { color: #10b981; }
#         .negative { color: #ef4444; }
        
#         .section-title {{
#             font-family: 'Inter', sans-serif;
#             font-weight: 600;
#             font-size: 1.1rem;
#             color: var(--text-primary);
#             margin: 1.5rem 0 0.8rem 0;
#             letter-spacing: -0.01em;
#         }}
        
#         /* Table styling */
#         .dataframe {{
#             font-family: 'Inter', sans-serif;
#             font-size: 0.85rem;
#             border-collapse: separate;
#             border-spacing: 0;
#             width: 100%;
#         }}
        
#         .dataframe th {{
#             background: var(--bg-secondary);
#             color: var(--text-secondary);
#             font-weight: 500;
#             padding: 0.6rem 0.8rem;
#             border-bottom: 2px solid var(--border-color);
#             text-align: left;
#         }}
        
#         .dataframe td {{
#             padding: 0.5rem 0.8rem;
#             border-bottom: 1px solid var(--border-color);
#             color: var(--text-primary);
#         }}
        
#         /* Custom button */
#         .stButton > button {{
#             font-family: 'Inter', sans-serif;
#             font-weight: 500;
#             font-size: 0.85rem;
#             background: var(--accent);
#             color: white;
#             border: none;
#             border-radius: 8px;
#             padding: 0.5rem 1.2rem;
#             transition: all 0.2s ease;
#         }}
        
#         .stButton > button:hover {{
#             background: var(--accent-hover);
#             box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
#         }}
        
#         /* Sidebar */
#         .sidebar-section {{
#             font-family: 'Inter', sans-serif;
#             font-weight: 500;
#             font-size: 0.75rem;
#             color: var(--text-muted);
#             text-transform: uppercase;
#             letter-spacing: 0.05em;
#             margin: 1.5rem 0 0.5rem 0;
#         }}
        
#         /* Hide Streamlit branding */
#         #MainMenu {{visibility: hidden;}}
#         footer {{visibility: hidden;}}
#         header {{visibility: hidden;}}
        
#         /* Responsive */
#         @media (max-width: 768px) {{
#             .main-header {{ font-size: 1.5rem; }}
#             .metric-value {{ font-size: 1.3rem; }}
#         }}
#     </style>
#     """, unsafe_allow_html=True)

# # Initialize session state
# if 'data' not in st.session_state:
#     st.session_state.data = None
# if 'dark_mode' not in st.session_state:
#     st.session_state.dark_mode = False
# if 'running' not in st.session_state:
#     st.session_state.running = False

# # Load CSS
# load_css()

# # Apply dark mode
# if st.session_state.dark_mode:
#     st.markdown('<script>document.documentElement.setAttribute("data-theme", "dark");</script>', unsafe_allow_html=True)
# else:
#     st.markdown('<script>document.documentElement.setAttribute("data-theme", "light");</script>', unsafe_allow_html=True)

# # Sidebar
# with st.sidebar:
#     st.markdown('<p style="font-family: Inter; font-weight: 600; font-size: 1.2rem; color: var(--text-primary); margin-bottom: 0.5rem;">NIFTY IT</p>', unsafe_allow_html=True)
#     st.markdown('<p style="font-family: Inter; font-weight: 300; font-size: 0.8rem; color: var(--text-muted); margin-bottom: 1.5rem;">Analytics Dashboard</p>', unsafe_allow_html=True)
    
#     # Dark mode toggle
#     dark_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
#     if dark_mode != st.session_state.dark_mode:
#         st.session_state.dark_mode = dark_mode
#         st.rerun()
    
#     st.markdown('<hr style="border-color: var(--border-color); margin: 1.5rem 0;">', unsafe_allow_html=True)
    
#     # Controls
#     st.markdown('<p class="sidebar-section">Controls</p>', unsafe_allow_html=True)
    
#     if st.button("🔄 Refresh Data", use_container_width=True):
#         st.session_state.running = True
#         st.rerun()
    
#     # Filters
#     st.markdown('<p class="sidebar-section">Filters</p>', unsafe_allow_html=True)
    
#     if st.session_state.data is not None:
#         df = st.session_state.data
        
#         # Company filter
#         companies = df['Company Name'].unique().tolist()
#         selected_companies = st.multiselect(
#             "Companies",
#             companies,
#             default=companies,
#             key="company_filter"
#         )
        
#         # Revenue filter
#         min_rev, max_rev = df['Current Revenue (Cr)'].min(), df['Current Revenue (Cr)'].max()
#         rev_range = st.slider(
#             "Revenue Range (Cr)",
#             min_value=float(min_rev) if min_rev else 0.0,
#             max_value=float(max_rev) if max_rev else 10000.0,
#             value=(float(min_rev) if min_rev else 0.0, float(max_rev) if max_rev else 10000.0),
#             step=100.0
#         )
        
#         # Deal wins filter
#         min_deals = df['Deal Wins'].min()
#         max_deals = df['Deal Wins'].max()
#         deal_range = st.slider(
#             "Deal Wins",
#             min_value=int(min_deals) if min_deals else 0,
#             max_value=int(max_deals) if max_deals else 10,
#             value=(int(min_deals) if min_deals else 0, int(max_deals) if max_deals else 10)
#         )
    
#     # Export
#     st.markdown('<hr style="border-color: var(--border-color); margin: 1.5rem 0;">', unsafe_allow_html=True)
#     st.markdown('<p class="sidebar-section">Export</p>', unsafe_allow_html=True)
    
#     if st.session_state.data is not None:
#         col1, col2 = st.columns(2)
#         with col1:
#             if st.button("📊 XLSX", use_container_width=True):
#                 st.session_state.export_format = 'xlsx'
#         with col2:
#             if st.button("📄 PDF", use_container_width=True):
#                 st.session_state.export_format = 'pdf'

# # Main content
# st.markdown('<p class="main-header">NIFTY IT Index</p>', unsafe_allow_html=True)
# st.markdown('<p class="sub-header">Real-time analytics & performance metrics of India\'s top IT companies</p>', unsafe_allow_html=True)

# # Data loading function
# def load_data():
#     """Load the latest Excel file from output directory"""
#     output_dir = "output"
#     if not os.path.exists(output_dir):
#         return None
    
#     excel_files = [f for f in os.listdir(output_dir) if f.endswith('.xlsx') and f.startswith('nifty_it_data_')]
#     if not excel_files:
#         return None
    
#     latest_file = sorted(excel_files)[-1]
#     file_path = os.path.join(output_dir, latest_file)
    
#     try:
#         df = pd.read_excel(file_path, sheet_name='Summary')
#         return df
#     except:
#         return None
    
# # Add this to dashboard.py after the data loading section

# def export_data(format_type):
#     """Export data to XLSX or PDF"""
#     if st.session_state.data is None:
#         return
    
#     df = st.session_state.data
    
#     if format_type == 'xlsx':
#         output = BytesIO()
#         with pd.ExcelWriter(output, engine='openpyxl') as writer:
#             df.to_excel(writer, sheet_name='Summary', index=False)
#         output.seek(0)
        
#         st.download_button(
#             label="📥 Download XLSX",
#             data=output,
#             file_name=f"nifty_it_data_{datetime.now().strftime('%Y%m%d')}.xlsx",
#             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#         )
    
#     elif format_type == 'pdf':
#         # Simplified PDF export using plotly
#         fig = go.Figure(data=[go.Table(
#             header=dict(values=list(df.columns),
#                        fill_color='#6366f1',
#                        align='left',
#                        font=dict(color='white', size=12)),
#             cells=dict(values=[df[col] for col in df.columns],
#                       fill_color='rgba(99, 102, 241, 0.05)',
#                       align='left',
#                       font=dict(size=11))
#         )])
        
#         fig.update_layout(
#             title=f"NIFTY IT Data - {datetime.now().strftime('%d %b %Y')}",
#             width=1200,
#             height=800,
#             font=dict(family='Inter')
#         )
        
#         st.plotly_chart(fig, use_container_width=True)    

# # Handle refresh
# if st.session_state.running:
#     with st.spinner("Running data pipeline... This may take a few minutes."):
#         try:
#             # Run the main.py script
#             result = subprocess.run([sys.executable, "main.py"], capture_output=True, text=True)
#             if result.returncode == 0:
#                 st.session_state.data = load_data()
#                 st.success("✅ Data refreshed successfully!")
#             else:
#                 st.error(f"❌ Pipeline failed: {result.stderr[:200]}")
#         except Exception as e:
#             st.error(f"❌ Error: {str(e)}")
#     st.session_state.running = False
#     st.rerun()

# # Load data if not loaded
# if st.session_state.data is None:
#     st.session_state.data = load_data()

# # Display data
# if st.session_state.data is not None:
#     df = st.session_state.data
    
#     # Apply filters
#     if 'selected_companies' in st.session_state:
#         df = df[df['Company Name'].isin(st.session_state.company_filter)]
    
#     if 'rev_range' in st.session_state:
#         df = df[(df['Current Revenue (Cr)'] >= st.session_state.rev_range[0]) & 
#                 (df['Current Revenue (Cr)'] <= st.session_state.rev_range[1])]
    
#     if 'deal_range' in st.session_state:
#         df = df[(df['Deal Wins'] >= st.session_state.deal_range[0]) & 
#                 (df['Deal Wins'] <= st.session_state.deal_range[1])]
    
#     # Metrics Row
#     col1, col2, col3, col4, col5 = st.columns(5)
    
#     with col1:
#         total_revenue = df['Current Revenue (Cr)'].sum()
#         st.markdown(f"""
#         <div class="metric-card">
#             <div class="metric-label">Total Revenue</div>
#             <div class="metric-value">₹{total_revenue:,.0f} Cr</div>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col2:
#         avg_revenue = df['Current Revenue (Cr)'].mean()
#         st.markdown(f"""
#         <div class="metric-card">
#             <div class="metric-label">Average Revenue</div>
#             <div class="metric-value">₹{avg_revenue:,.0f} Cr</div>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col3:
#         total_deals = df['Deal Wins'].sum() if 'Deal Wins' in df.columns else 0
#         st.markdown(f"""
#         <div class="metric-card">
#             <div class="metric-label">Total Deals</div>
#             <div class="metric-value">{total_deals:,.0f}</div>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col4:
#         avg_margin = df['Profit Margin %'].mean() if 'Profit Margin %' in df.columns else 0
#         st.markdown(f"""
#         <div class="metric-card">
#             <div class="metric-label">Avg Margin</div>
#             <div class="metric-value">{avg_margin:.1f}%</div>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col5:
#         total_clients = df['Total Clients'].sum() if 'Total Clients' in df.columns else 0
#         st.markdown(f"""
#         <div class="metric-card">
#             <div class="metric-label">Total Clients</div>
#             <div class="metric-value">{total_clients:,.0f}</div>
#         </div>
#         """, unsafe_allow_html=True)
    
#     # Charts
#     st.markdown('<p class="section-title">Performance Overview</p>', unsafe_allow_html=True)
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         # Revenue bar chart
#         fig_revenue = px.bar(
#             df,
#             x='Company Name',
#             y='Current Revenue (Cr)',
#             title='Revenue by Company',
#             color='Current Revenue (Cr)',
#             color_continuous_scale='Blues',
#             text='Current Revenue (Cr)'
#         )
#         fig_revenue.update_layout(
#             plot_bgcolor='rgba(0,0,0,0)',
#             paper_bgcolor='rgba(0,0,0,0)',
#             font=dict(family='Inter', size=12),
#             height=400,
#             margin=dict(l=40, r=40, t=40, b=40),
#             showlegend=False
#         )
#         fig_revenue.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
#         st.plotly_chart(fig_revenue, use_container_width=True)
    
#     with col2:
#         # Revenue vs Deal Wins scatter
#         fig_scatter = px.scatter(
#             df,
#             x='Current Revenue (Cr)',
#             y='Deal Wins',
#             size='Current Revenue (Cr)',
#             color='Company Name',
#             text='Company Name',
#             title='Revenue vs Deal Wins'
#         )
#         fig_scatter.update_layout(
#             plot_bgcolor='rgba(0,0,0,0)',
#             paper_bgcolor='rgba(0,0,0,0)',
#             font=dict(family='Inter', size=12),
#             height=400,
#             margin=dict(l=40, r=40, t=40, b=40),
#             showlegend=False
#         )
#         fig_scatter.update_traces(textposition='top center')
#         st.plotly_chart(fig_scatter, use_container_width=True)
    
#     # Data table
#     st.markdown('<p class="section-title">Company Data</p>', unsafe_allow_html=True)
    
#     display_cols = ['Company Name', 'Current Revenue (Cr)', 'Annual Revenue (Cr)', 
#                    'Profit Margin %', 'Total TCV', 'Deal Wins', 'Total Clients']
#     display_df = df[display_cols].copy()
#     display_df['Current Revenue (Cr)'] = display_df['Current Revenue (Cr)'].map(lambda x: f"₹{x:,.0f}" if pd.notna(x) else "N/A")
#     display_df['Annual Revenue (Cr)'] = display_df['Annual Revenue (Cr)'].map(lambda x: f"₹{x:,.0f}" if pd.notna(x) else "N/A")
#     display_df['Profit Margin %'] = display_df['Profit Margin %'].map(lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A")
    
#     st.dataframe(
#         display_df,
#         use_container_width=True,
#         hide_index=True,
#         column_config={
#             "Company Name": st.column_config.TextColumn("Company", width="medium"),
#             "Current Revenue (Cr)": st.column_config.TextColumn("Current Revenue", width="small"),
#             "Annual Revenue (Cr)": st.column_config.TextColumn("Annual Revenue", width="small"),
#             "Profit Margin %": st.column_config.TextColumn("Margin", width="small"),
#             "Total TCV": st.column_config.TextColumn("Total TCV", width="small"),
#             "Deal Wins": st.column_config.TextColumn("Deals", width="small"),
#             "Total Clients": st.column_config.TextColumn("Clients", width="small")
#         }
#     )

# else:
#     st.info("📂 No data found. Click 'Refresh Data' in the sidebar to run the pipeline and fetch the latest data.")

# # Footer
# st.markdown("""
# <hr style="border-color: var(--border-color); margin: 2rem 0 1rem 0;">
# <p style="font-family: Inter; font-size: 0.75rem; color: var(--text-muted); text-align: center; letter-spacing: 0.03em;">
#     Data sourced from Screener.in & Company Investor Relations | Updated: {}
# </p>
# """.format(datetime.now().strftime("%d %b %Y, %H:%M")), unsafe_allow_html=True)

# # # # # dashboard.py (FIXED)
# # # # import streamlit as st
# # # # import pandas as pd
# # # # import plotly.express as px
# # # # import plotly.graph_objects as go
# # # # from plotly.subplots import make_subplots
# # # # import os
# # # # from datetime import datetime
# # # # import subprocess
# # # # import sys
# # # # import json
# # # # import base64
# # # # from io import BytesIO

# # # # # Page configuration
# # # # st.set_page_config(
# # # #     page_title="NIFTY IT Analytics Dashboard",
# # # #     page_icon="📊",
# # # #     layout="wide",
# # # #     initial_sidebar_state="expanded"
# # # # )

# # # # # Custom CSS for premium minimalist design
# # # # def load_css():
# # # #     st.markdown("""
# # # #     <style>
# # # #         /* Import premium fonts */
# # # #         @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
# # # #         /* Global styles */
# # # #         .stApp {
# # # #             background-color: #ffffff;
# # # #             font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
# # # #         }
        
# # # #         /* Dark mode overrides */
# # # #         .dark-mode .stApp {
# # # #             background-color: #0f0f1a;
# # # #         }
        
# # # #         .dark-mode .stApp * {
# # # #             color: #e8e8f0;
# # # #         }
        
# # # #         .main-header {
# # # #             font-family: 'Inter', sans-serif;
# # # #             font-weight: 600;
# # # #             font-size: 2.2rem;
# # # #             color: #1a1a2e;
# # # #             margin-bottom: 0.2rem;
# # # #             letter-spacing: -0.02em;
# # # #         }
        
# # # #         .dark-mode .main-header {
# # # #             color: #e8e8f0;
# # # #         }
        
# # # #         .sub-header {
# # # #             font-family: 'Inter', sans-serif;
# # # #             font-weight: 400;
# # # #             font-size: 0.95rem;
# # # #             color: #4a4a6a;
# # # #             margin-bottom: 2rem;
# # # #         }
        
# # # #         .dark-mode .sub-header {
# # # #             color: #b0b0d0;
# # # #         }
        
# # # #         .metric-card {
# # # #             background: #ffffff;
# # # #             border-radius: 12px;
# # # #             padding: 1.2rem 1.5rem;
# # # #             border: 1px solid #e8e8f0;
# # # #             box-shadow: 0 1px 3px rgba(0,0,0,0.06);
# # # #             transition: all 0.2s ease;
# # # #         }
        
# # # #         .dark-mode .metric-card {
# # # #             background: #1e1e32;
# # # #             border-color: #2a2a4a;
# # # #             box-shadow: 0 1px 3px rgba(0,0,0,0.3);
# # # #         }
        
# # # #         .metric-card:hover {
# # # #             transform: translateY(-2px);
# # # #             box-shadow: 0 4px 12px rgba(99, 102, 241, 0.1);
# # # #         }
        
# # # #         .metric-label {
# # # #             font-family: 'Inter', sans-serif;
# # # #             font-weight: 400;
# # # #             font-size: 0.8rem;
# # # #             color: #8a8aaa;
# # # #             text-transform: uppercase;
# # # #             letter-spacing: 0.05em;
# # # #         }
        
# # # #         .metric-value {
# # # #             font-family: 'Inter', sans-serif;
# # # #             font-weight: 600;
# # # #             font-size: 1.8rem;
# # # #             color: #1a1a2e;
# # # #             margin-top: 0.2rem;
# # # #         }
        
# # # #         .dark-mode .metric-value {
# # # #             color: #e8e8f0;
# # # #         }
        
# # # #         .positive {
# # # #             color: #10b981;
# # # #         }
        
# # # #         .negative {
# # # #             color: #ef4444;
# # # #         }
        
# # # #         .section-title {
# # # #             font-family: 'Inter', sans-serif;
# # # #             font-weight: 600;
# # # #             font-size: 1.1rem;
# # # #             color: #1a1a2e;
# # # #             margin: 1.5rem 0 0.8rem 0;
# # # #             letter-spacing: -0.01em;
# # # #         }
        
# # # #         .dark-mode .section-title {
# # # #             color: #e8e8f0;
# # # #         }
        
# # # #         /* Table styling */
# # # #         .dataframe {
# # # #             font-family: 'Inter', sans-serif;
# # # #             font-size: 0.85rem;
# # # #             border-collapse: separate;
# # # #             border-spacing: 0;
# # # #             width: 100%;
# # # #         }
        
# # # #         .dataframe th {
# # # #             background: #f8f9fa;
# # # #             color: #4a4a6a;
# # # #             font-weight: 500;
# # # #             padding: 0.6rem 0.8rem;
# # # #             border-bottom: 2px solid #e8e8f0;
# # # #             text-align: left;
# # # #         }
        
# # # #         .dark-mode .dataframe th {
# # # #             background: #1a1a2e;
# # # #             color: #b0b0d0;
# # # #             border-color: #2a2a4a;
# # # #         }
        
# # # #         .dataframe td {
# # # #             padding: 0.5rem 0.8rem;
# # # #             border-bottom: 1px solid #e8e8f0;
# # # #             color: #1a1a2e;
# # # #         }
        
# # # #         .dark-mode .dataframe td {
# # # #             color: #e8e8f0;
# # # #             border-color: #2a2a4a;
# # # #         }
        
# # # #         /* Custom button */
# # # #         .stButton > button {
# # # #             font-family: 'Inter', sans-serif;
# # # #             font-weight: 500;
# # # #             font-size: 0.85rem;
# # # #             background: #6366f1;
# # # #             color: white;
# # # #             border: none;
# # # #             border-radius: 8px;
# # # #             padding: 0.5rem 1.2rem;
# # # #             transition: all 0.2s ease;
# # # #         }
        
# # # #         .stButton > button:hover {
# # # #             background: #4f46e5;
# # # #             box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
# # # #         }
        
# # # #         /* Sidebar */
# # # #         .sidebar-section {
# # # #             font-family: 'Inter', sans-serif;
# # # #             font-weight: 500;
# # # #             font-size: 0.75rem;
# # # #             color: #8a8aaa;
# # # #             text-transform: uppercase;
# # # #             letter-spacing: 0.05em;
# # # #             margin: 1.5rem 0 0.5rem 0;
# # # #         }
        
# # # #         .dark-mode .sidebar-section {
# # # #             color: #6a6a8a;
# # # #         }
        
# # # #         /* Hide Streamlit branding */
# # # #         #MainMenu {visibility: hidden;}
# # # #         footer {visibility: hidden;}
# # # #         header {visibility: hidden;}
        
# # # #         /* Responsive */
# # # #         @media (max-width: 768px) {
# # # #             .main-header { font-size: 1.5rem; }
# # # #             .metric-value { font-size: 1.3rem; }
# # # #         }
# # # #     </style>
# # # #     """, unsafe_allow_html=True)

# # # # # Initialize session state
# # # # if 'data' not in st.session_state:
# # # #     st.session_state.data = None
# # # # if 'dark_mode' not in st.session_state:
# # # #     st.session_state.dark_mode = False
# # # # if 'running' not in st.session_state:
# # # #     st.session_state.running = False
# # # # if 'export_format' not in st.session_state:
# # # #     st.session_state.export_format = None

# # # # # Load CSS
# # # # load_css()

# # # # # Apply dark mode class
# # # # if st.session_state.dark_mode:
# # # #     st.markdown('<div class="dark-mode">', unsafe_allow_html=True)

# # # # # Sidebar
# # # # with st.sidebar:
# # # #     st.markdown('<p style="font-family: Inter; font-weight: 600; font-size: 1.2rem; color: #1a1a2e; margin-bottom: 0.5rem;">NIFTY IT</p>', unsafe_allow_html=True)
# # # #     if st.session_state.dark_mode:
# # # #         st.markdown('<p style="font-family: Inter; font-weight: 300; font-size: 0.8rem; color: #6a6a8a; margin-bottom: 1.5rem;">Analytics Dashboard</p>', unsafe_allow_html=True)
# # # #     else:
# # # #         st.markdown('<p style="font-family: Inter; font-weight: 300; font-size: 0.8rem; color: #8a8aaa; margin-bottom: 1.5rem;">Analytics Dashboard</p>', unsafe_allow_html=True)
    
# # # #     # Dark mode toggle
# # # #     dark_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
# # # #     if dark_mode != st.session_state.dark_mode:
# # # #         st.session_state.dark_mode = dark_mode
# # # #         st.rerun()
    
# # # #     st.markdown('<hr style="margin: 1.5rem 0;">', unsafe_allow_html=True)
    
# # # #     # Controls
# # # #     st.markdown('<p class="sidebar-section">Controls</p>', unsafe_allow_html=True)
    
# # # #     if st.button("🔄 Refresh Data", use_container_width=True):
# # # #         st.session_state.running = True
# # # #         st.rerun()
    
# # # #     # Filters
# # # #     st.markdown('<p class="sidebar-section">Filters</p>', unsafe_allow_html=True)
    
# # # #     if st.session_state.data is not None:
# # # #         df = st.session_state.data
        
# # # #         # Company filter
# # # #         companies = df['Company Name'].unique().tolist()
# # # #         selected_companies = st.multiselect(
# # # #             "Companies",
# # # #             companies,
# # # #             default=companies,
# # # #             key="company_filter"
# # # #         )
        
# # # #         # Revenue filter
# # # #         # Revenue filter - ensure numeric
# # # #         if 'Current Revenue (Cr)' in df.columns:
# # # #             revenue_col = df['Current Revenue (Cr)']
# # # #             if revenue_col.dtype == 'object':
# # # #                 revenue_col = pd.to_numeric(revenue_col, errors='coerce')
            
# # # #             min_rev = revenue_col.min() if revenue_col.notna().any() else 0
# # # #             max_rev = revenue_col.max() if revenue_col.notna().any() else 10000
            
# # # #             rev_range = st.slider(
# # # #                 "Revenue Range (Cr)",
# # # #                 min_value=float(min_rev),
# # # #                 max_value=float(max_rev),
# # # #                 value=(float(min_rev), float(max_rev)),
# # # #                 step=100.0
# # # #             )

# # # #         # Deal wins filter - ensure numeric
# # # #         if 'Deal Wins' in df.columns:
# # # #             deals_col = df['Deal Wins']
# # # #             if deals_col.dtype == 'object':
# # # #                 deals_col = pd.to_numeric(deals_col, errors='coerce')
            
# # # #             min_deals = deals_col.min() if deals_col.notna().any() else 0
# # # #             max_deals = deals_col.max() if deals_col.notna().any() else 10
            
# # # #             deal_range = st.slider(
# # # #                 "Deal Wins",
# # # #                 min_value=int(min_deals),
# # # #                 max_value=int(max_deals),
# # # #                 value=(int(min_deals), int(max_deals))
# # # #             )
        
# # # #         # min_rev = df['Current Revenue (Cr)'].min() if df['Current Revenue (Cr)'].notna().any() else 0
# # # #         # max_rev = df['Current Revenue (Cr)'].max() if df['Current Revenue (Cr)'].notna().any() else 10000
        
# # # #         # rev_range = st.slider(
# # # #         #     "Revenue Range (Cr)",
# # # #         #     min_value=float(min_rev),
# # # #         #     max_value=float(max_rev),
# # # #         #     value=(float(min_rev), float(max_rev)),
# # # #         #     step=100.0
# # # #         # )
        
# # # #         # # Deal wins filter
# # # #         # if 'Deal Wins' in df.columns:
# # # #         #     min_deals = df['Deal Wins'].min() if df['Deal Wins'].notna().any() else 0
# # # #         #     max_deals = df['Deal Wins'].max() if df['Deal Wins'].notna().any() else 10
            
# # # #         #     deal_range = st.slider(
# # # #         #         "Deal Wins",
# # # #         #         min_value=int(min_deals),
# # # #         #         max_value=int(max_deals),
# # # #         #         value=(int(min_deals), int(max_deals))
# # # #         #     )
    
# # # #     # Export
# # # #     st.markdown('<hr style="margin: 1.5rem 0;">', unsafe_allow_html=True)
# # # #     st.markdown('<p class="sidebar-section">Export</p>', unsafe_allow_html=True)
    
# # # #     if st.session_state.data is not None:
# # # #         col1, col2 = st.columns(2)
# # # #         with col1:
# # # #             if st.button("📊 XLSX", use_container_width=True):
# # # #                 st.session_state.export_format = 'xlsx'
# # # #         with col2:
# # # #             if st.button("📄 PDF", use_container_width=True):
# # # #                 st.session_state.export_format = 'pdf'

# # # # # Main content
# # # # st.markdown('<p class="main-header">NIFTY IT Index</p>', unsafe_allow_html=True)
# # # # st.markdown('<p class="sub-header">Real-time analytics & performance metrics of India\'s top IT companies</p>', unsafe_allow_html=True)

# # # # # Data loading function
# # # # def load_data():
# # # #     """Load the latest Excel file from output directory"""
# # # #     output_dir = "output"
# # # #     if not os.path.exists(output_dir):
# # # #         return None
    
# # # #     excel_files = [f for f in os.listdir(output_dir) if f.endswith('.xlsx') and f.startswith('nifty_it_data_')]
# # # #     if not excel_files:
# # # #         return None
    
# # # #     latest_file = sorted(excel_files)[-1]
# # # #     file_path = os.path.join(output_dir, latest_file)
    
# # # #     try:
# # # #         df = pd.read_excel(file_path, sheet_name='Summary')
        
# # # #         # Clean numeric columns - remove currency symbols and commas
# # # #         numeric_cols = ['Current Revenue (Cr)', 'Annual Revenue (Cr)', 'Annual Profit (Cr)']
# # # #         for col in numeric_cols:
# # # #             if col in df.columns:
# # # #                 # Convert to string, remove ₹, commas, and convert to numeric
# # # #                 df[col] = df[col].astype(str).str.replace('₹', '').str.replace(',', '').str.strip()
# # # #                 df[col] = pd.to_numeric(df[col], errors='coerce')
        
# # # #         # Clean 'Total TCV' - extract numeric value
# # # #         if 'Total TCV' in df.columns:
# # # #             df['Total TCV'] = df['Total TCV'].astype(str).str.extract(r'([\d.]+)')[0]
# # # #             df['Total TCV'] = pd.to_numeric(df['Total TCV'], errors='coerce')
        
# # # #         return df
# # # #     except Exception as e:
# # # #         st.error(f"Error loading data: {e}")
# # # #         return None
# # # # # def load_data():
# # # # #     """Load the latest Excel file from output directory"""
# # # # #     output_dir = "output"
# # # # #     if not os.path.exists(output_dir):
# # # # #         return None
    
# # # # #     excel_files = [f for f in os.listdir(output_dir) if f.endswith('.xlsx') and f.startswith('nifty_it_data_')]
# # # # #     if not excel_files:
# # # # #         return None
    
# # # # #     latest_file = sorted(excel_files)[-1]
# # # # #     file_path = os.path.join(output_dir, latest_file)
    
# # # # #     try:
# # # # #         df = pd.read_excel(file_path, sheet_name='Summary')
# # # # #         return df
# # # # #     except:
# # # # #         return None

# # # # # Export function
# # # # def export_data(format_type):
# # # #     """Export data to XLSX or PDF"""
# # # #     if st.session_state.data is None:
# # # #         return
    
# # # #     df = st.session_state.data
    
# # # #     if format_type == 'xlsx':
# # # #         output = BytesIO()
# # # #         with pd.ExcelWriter(output, engine='openpyxl') as writer:
# # # #             df.to_excel(writer, sheet_name='Summary', index=False)
# # # #         output.seek(0)
        
# # # #         st.download_button(
# # # #             label="📥 Download XLSX",
# # # #             data=output,
# # # #             file_name=f"nifty_it_data_{datetime.now().strftime('%Y%m%d')}.xlsx",
# # # #             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
# # # #         )
    
# # # #     elif format_type == 'pdf':
# # # #         # Simplified PDF export using plotly
# # # #         fig = go.Figure(data=[go.Table(
# # # #             header=dict(values=list(df.columns),
# # # #                        fill_color='#6366f1',
# # # #                        align='left',
# # # #                        font=dict(color='white', size=12)),
# # # #             cells=dict(values=[df[col] for col in df.columns],
# # # #                       fill_color='rgba(99, 102, 241, 0.05)',
# # # #                       align='left',
# # # #                       font=dict(size=11))
# # # #         )])
        
# # # #         fig.update_layout(
# # # #             title=f"NIFTY IT Data - {datetime.now().strftime('%d %b %Y')}",
# # # #             width=1200,
# # # #             height=800,
# # # #             font=dict(family='Inter')
# # # #         )
        
# # # #         st.plotly_chart(fig, use_container_width=True)

# # # # # Handle refresh
# # # # if st.session_state.running:
# # # #     with st.spinner("Running data pipeline... This may take a few minutes."):
# # # #         try:
# # # #             # Run the main.py script
# # # #             result = subprocess.run([sys.executable, "main.py"], capture_output=True, text=True)
# # # #             if result.returncode == 0:
# # # #                 st.session_state.data = load_data()
# # # #                 st.success("✅ Data refreshed successfully!")
# # # #             else:
# # # #                 st.error(f"❌ Pipeline failed: {result.stderr[:200]}")
# # # #         except Exception as e:
# # # #             st.error(f"❌ Error: {str(e)}")
# # # #     st.session_state.running = False
# # # #     st.rerun()

# # # # # Load data if not loaded
# # # # if st.session_state.data is None:
# # # #     st.session_state.data = load_data()

# # # # # Display data
# # # # if st.session_state.data is not None:
# # # #     df = st.session_state.data
    
# # # #     # Apply filters
# # # #     if 'company_filter' in st.session_state and st.session_state.company_filter:
# # # #         df = df[df['Company Name'].isin(st.session_state.company_filter)]
    
# # # #     if 'rev_range' in st.session_state:
# # # #         df = df[(df['Current Revenue (Cr)'] >= st.session_state.rev_range[0]) & 
# # # #                 (df['Current Revenue (Cr)'] <= st.session_state.rev_range[1])]
    
# # # #     if 'deal_range' in st.session_state:
# # # #         df = df[(df['Deal Wins'] >= st.session_state.deal_range[0]) & 
# # # #                 (df['Deal Wins'] <= st.session_state.deal_range[1])]
    
# # # #     # Metrics Row
# # # #     # Metrics Row
# # # #     col1, col2, col3, col4, col5 = st.columns(5)

# # # #     with col1:
# # # #         # Ensure numeric before sum
# # # #         revenue_col = df['Current Revenue (Cr)']
# # # #         if revenue_col.dtype == 'object':
# # # #             revenue_col = pd.to_numeric(revenue_col, errors='coerce')
# # # #         total_revenue = revenue_col.sum() if revenue_col.notna().any() else 0
# # # #         st.markdown(f"""
# # # #         <div class="metric-card">
# # # #             <div class="metric-label">Total Revenue</div>
# # # #             <div class="metric-value">₹{total_revenue:,.0f} Cr</div>
# # # #         </div>
# # # #         """, unsafe_allow_html=True)

# # # #     with col2:
# # # #         revenue_col = df['Current Revenue (Cr)']
# # # #         if revenue_col.dtype == 'object':
# # # #             revenue_col = pd.to_numeric(revenue_col, errors='coerce')
# # # #         avg_revenue = revenue_col.mean() if revenue_col.notna().any() else 0
# # # #         st.markdown(f"""
# # # #         <div class="metric-card">
# # # #             <div class="metric-label">Average Revenue</div>
# # # #             <div class="metric-value">₹{avg_revenue:,.0f} Cr</div>
# # # #         </div>
# # # #         """, unsafe_allow_html=True)

# # # #     with col3:
# # # #         if 'Deal Wins' in df.columns:
# # # #             deals_col = df['Deal Wins']
# # # #             if deals_col.dtype == 'object':
# # # #                 deals_col = pd.to_numeric(deals_col, errors='coerce')
# # # #             total_deals = deals_col.sum() if deals_col.notna().any() else 0
# # # #         else:
# # # #             total_deals = 0
# # # #         st.markdown(f"""
# # # #         <div class="metric-card">
# # # #             <div class="metric-label">Total Deals</div>
# # # #             <div class="metric-value">{total_deals:,.0f}</div>
# # # #         </div>
# # # #         """, unsafe_allow_html=True)

# # # #     with col4:
# # # #         if 'Profit Margin %' in df.columns:
# # # #             margin_col = df['Profit Margin %']
# # # #             if margin_col.dtype == 'object':
# # # #                 margin_col = pd.to_numeric(margin_col, errors='coerce')
# # # #             avg_margin = margin_col.mean() if margin_col.notna().any() else 0
# # # #         else:
# # # #             avg_margin = 0
# # # #         st.markdown(f"""
# # # #         <div class="metric-card">
# # # #             <div class="metric-label">Avg Margin</div>
# # # #             <div class="metric-value">{avg_margin:.1f}%</div>
# # # #         </div>
# # # #         """, unsafe_allow_html=True)

# # # #     with col5:
# # # #         if 'Total Clients' in df.columns:
# # # #             clients_col = df['Total Clients']
# # # #             if clients_col.dtype == 'object':
# # # #                 clients_col = pd.to_numeric(clients_col, errors='coerce')
# # # #             total_clients = clients_col.sum() if clients_col.notna().any() else 0
# # # #         else:
# # # #             total_clients = 0
# # # #         st.markdown(f"""
# # # #         <div class="metric-card">
# # # #             <div class="metric-label">Total Clients</div>
# # # #             <div class="metric-value">{total_clients:,.0f}</div>
# # # #         </div>
# # # #         """, unsafe_allow_html=True)
# # # #     # col1, col2, col3, col4, col5 = st.columns(5)
    
# # # #     # with col1:
# # # #     #     total_revenue = df['Current Revenue (Cr)'].sum() if df['Current Revenue (Cr)'].notna().any() else 0
# # # #     #     st.markdown(f"""
# # # #     #     <div class="metric-card">
# # # #     #         <div class="metric-label">Total Revenue</div>
# # # #     #         <div class="metric-value">₹{total_revenue:,.0f} Cr</div>
# # # #     #     </div>
# # # #     #     """, unsafe_allow_html=True)
    
# # # #     # with col2:
# # # #     #     avg_revenue = df['Current Revenue (Cr)'].mean() if df['Current Revenue (Cr)'].notna().any() else 0
# # # #     #     st.markdown(f"""
# # # #     #     <div class="metric-card">
# # # #     #         <div class="metric-label">Average Revenue</div>
# # # #     #         <div class="metric-value">₹{avg_revenue:,.0f} Cr</div>
# # # #     #     </div>
# # # #     #     """, unsafe_allow_html=True)
    
# # # #     # with col3:
# # # #     #     total_deals = df['Deal Wins'].sum() if 'Deal Wins' in df.columns and df['Deal Wins'].notna().any() else 0
# # # #     #     st.markdown(f"""
# # # #     #     <div class="metric-card">
# # # #     #         <div class="metric-label">Total Deals</div>
# # # #     #         <div class="metric-value">{total_deals:,.0f}</div>
# # # #     #     </div>
# # # #     #     """, unsafe_allow_html=True)
    
# # # #     # with col4:
# # # #     #     avg_margin = df['Profit Margin %'].mean() if 'Profit Margin %' in df.columns and df['Profit Margin %'].notna().any() else 0
# # # #     #     st.markdown(f"""
# # # #     #     <div class="metric-card">
# # # #     #         <div class="metric-label">Avg Margin</div>
# # # #     #         <div class="metric-value">{avg_margin:.1f}%</div>
# # # #     #     </div>
# # # #     #     """, unsafe_allow_html=True)
    
# # # #     # with col5:
# # # #     #     total_clients = df['Total Clients'].sum() if 'Total Clients' in df.columns and df['Total Clients'].notna().any() else 0
# # # #     #     st.markdown(f"""
# # # #     #     <div class="metric-card">
# # # #     #         <div class="metric-label">Total Clients</div>
# # # #     #         <div class="metric-value">{total_clients:,.0f}</div>
# # # #     #     </div>
# # # #     #     """, unsafe_allow_html=True)
    
# # # #     # Charts
# # # #     st.markdown('<p class="section-title">Performance Overview</p>', unsafe_allow_html=True)
    
# # # #     col1, col2 = st.columns(2)
    
# # # #     with col1:
# # # #         # Revenue bar chart
# # # #         fig_revenue = px.bar(
# # # #             df,
# # # #             x='Company Name',
# # # #             y='Current Revenue (Cr)',
# # # #             title='Revenue by Company',
# # # #             color='Current Revenue (Cr)',
# # # #             color_continuous_scale='Blues',
# # # #             text='Current Revenue (Cr)'
# # # #         )
# # # #         fig_revenue.update_layout(
# # # #             plot_bgcolor='rgba(0,0,0,0)',
# # # #             paper_bgcolor='rgba(0,0,0,0)',
# # # #             font=dict(family='Inter', size=12),
# # # #             height=400,
# # # #             margin=dict(l=40, r=40, t=40, b=40),
# # # #             showlegend=False
# # # #         )
# # # #         fig_revenue.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
# # # #         st.plotly_chart(fig_revenue, use_container_width=True)
    
# # # #     with col2:
# # # #         # Revenue vs Deal Wins scatter
# # # #         if 'Deal Wins' in df.columns and df['Deal Wins'].notna().any():
# # # #             fig_scatter = px.scatter(
# # # #                 df,
# # # #                 x='Current Revenue (Cr)',
# # # #                 y='Deal Wins',
# # # #                 size='Current Revenue (Cr)',
# # # #                 color='Company Name',
# # # #                 text='Company Name',
# # # #                 title='Revenue vs Deal Wins'
# # # #             )
# # # #             fig_scatter.update_layout(
# # # #                 plot_bgcolor='rgba(0,0,0,0)',
# # # #                 paper_bgcolor='rgba(0,0,0,0)',
# # # #                 font=dict(family='Inter', size=12),
# # # #                 height=400,
# # # #                 margin=dict(l=40, r=40, t=40, b=40),
# # # #                 showlegend=False
# # # #             )
# # # #             fig_scatter.update_traces(textposition='top center')
# # # #             st.plotly_chart(fig_scatter, use_container_width=True)
    
# # # #     # Data table
# # # #     st.markdown('<p class="section-title">Company Data</p>', unsafe_allow_html=True)
    
# # # #     display_cols = ['Company Name', 'Current Revenue (Cr)', 'Annual Revenue (Cr)', 
# # # #                    'Profit Margin %', 'Total TCV', 'Deal Wins', 'Total Clients']
    
# # # #     # Only include columns that exist
# # # #     available_cols = [col for col in display_cols if col in df.columns]
# # # #     display_df = df[available_cols].copy()
    
# # # #     # Format columns
# # # #     for col in ['Current Revenue (Cr)', 'Annual Revenue (Cr)']:
# # # #         if col in display_df.columns:
# # # #             display_df[col] = display_df[col].map(lambda x: f"₹{x:,.0f}" if pd.notna(x) else "N/A")
    
# # # #     if 'Profit Margin %' in display_df.columns:
# # # #         display_df['Profit Margin %'] = display_df['Profit Margin %'].map(lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A")
    
# # # #     if 'Total TCV' in display_df.columns:
# # # #         display_df['Total TCV'] = display_df['Total TCV'].map(lambda x: x if pd.notna(x) else "N/A")
    
# # # #     if 'Deal Wins' in display_df.columns:
# # # #         display_df['Deal Wins'] = display_df['Deal Wins'].map(lambda x: f"{x:,.0f}" if pd.notna(x) else "0")
    
# # # #     if 'Total Clients' in display_df.columns:
# # # #         display_df['Total Clients'] = display_df['Total Clients'].map(lambda x: f"{x:,.0f}" if pd.notna(x) else "N/A")
    
# # # #     # Rename columns for display
# # # #     column_rename = {
# # # #         'Company Name': 'Company',
# # # #         'Current Revenue (Cr)': 'Current Revenue',
# # # #         'Annual Revenue (Cr)': 'Annual Revenue',
# # # #         'Profit Margin %': 'Margin',
# # # #         'Total TCV': 'TCV',
# # # #         'Deal Wins': 'Deals',
# # # #         'Total Clients': 'Clients'
# # # #     }
# # # #     display_df = display_df.rename(columns=column_rename)
    
# # # #     st.dataframe(
# # # #         display_df,
# # # #         use_container_width=True,
# # # #         hide_index=True,
# # # #         column_config={
# # # #             "Company": st.column_config.TextColumn("Company", width="medium"),
# # # #             "Current Revenue": st.column_config.TextColumn("Revenue", width="small"),
# # # #             "Annual Revenue": st.column_config.TextColumn("Annual", width="small"),
# # # #             "Margin": st.column_config.TextColumn("Margin", width="small"),
# # # #             "TCV": st.column_config.TextColumn("TCV", width="small"),
# # # #             "Deals": st.column_config.TextColumn("Deals", width="small"),
# # # #             "Clients": st.column_config.TextColumn("Clients", width="small")
# # # #         }
# # # #     )

# # # # else:
# # # #     st.info("📂 No data found. Click 'Refresh Data' in the sidebar to run the pipeline and fetch the latest data.")

# # # # # Footer
# # # # st.markdown("""
# # # # <hr style="margin: 2rem 0 1rem 0;">
# # # # <p style="font-family: Inter; font-size: 0.75rem; color: #8a8aaa; text-align: center; letter-spacing: 0.03em;">
# # # #     Data sourced from Screener.in & Company Investor Relations | Updated: {}
# # # # </p>
# # # # """.format(datetime.now().strftime("%d %b %Y, %H:%M")), unsafe_allow_html=True)

# # # # # Close dark mode div
# # # # if st.session_state.dark_mode:
# # # #     st.markdown('</div>', unsafe_allow_html=True)

# # # # dashboard.py (COMPLETE FIXED VERSION)
# # # import streamlit as st
# # # import pandas as pd
# # # import plotly.express as px
# # # import plotly.graph_objects as go
# # # from plotly.subplots import make_subplots
# # # import os
# # # from datetime import datetime
# # # import subprocess
# # # import sys
# # # import json
# # # import base64
# # # from io import BytesIO
# # # import numpy as np

# # # # Page configuration
# # # st.set_page_config(
# # #     page_title="NIFTY IT Analytics Dashboard",
# # #     page_icon="📊",
# # #     layout="wide",
# # #     initial_sidebar_state="expanded"
# # # )

# # # # Custom CSS for premium minimalist design
# # # def load_css():
# # #     st.markdown("""
# # #     <style>
# # #         /* Import premium fonts */
# # #         @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
# # #         /* Global styles */
# # #         .stApp {
# # #             background-color: #ffffff;
# # #             font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
# # #         }
        
# # #         /* Dark mode overrides */
# # #         .dark-mode .stApp {
# # #             background-color: #0f0f1a;
# # #         }
        
# # #         .dark-mode .stApp * {
# # #             color: #e8e8f0;
# # #         }
        
# # #         .main-header {
# # #             font-family: 'Inter', sans-serif;
# # #             font-weight: 600;
# # #             font-size: 2.2rem;
# # #             color: #1a1a2e;
# # #             margin-bottom: 0.2rem;
# # #             letter-spacing: -0.02em;
# # #         }
        
# # #         .dark-mode .main-header {
# # #             color: #e8e8f0;
# # #         }
        
# # #         .sub-header {
# # #             font-family: 'Inter', sans-serif;
# # #             font-weight: 400;
# # #             font-size: 0.95rem;
# # #             color: #4a4a6a;
# # #             margin-bottom: 2rem;
# # #         }
        
# # #         .dark-mode .sub-header {
# # #             color: #b0b0d0;
# # #         }
        
# # #         .metric-card {
# # #             background: #ffffff;
# # #             border-radius: 12px;
# # #             padding: 1.2rem 1.5rem;
# # #             border: 1px solid #e8e8f0;
# # #             box-shadow: 0 1px 3px rgba(0,0,0,0.06);
# # #             transition: all 0.2s ease;
# # #         }
        
# # #         .dark-mode .metric-card {
# # #             background: #1e1e32;
# # #             border-color: #2a2a4a;
# # #             box-shadow: 0 1px 3px rgba(0,0,0,0.3);
# # #         }
        
# # #         .metric-card:hover {
# # #             transform: translateY(-2px);
# # #             box-shadow: 0 4px 12px rgba(99, 102, 241, 0.1);
# # #         }
        
# # #         .metric-label {
# # #             font-family: 'Inter', sans-serif;
# # #             font-weight: 400;
# # #             font-size: 0.8rem;
# # #             color: #8a8aaa;
# # #             text-transform: uppercase;
# # #             letter-spacing: 0.05em;
# # #         }
        
# # #         .metric-value {
# # #             font-family: 'Inter', sans-serif;
# # #             font-weight: 600;
# # #             font-size: 1.8rem;
# # #             color: #1a1a2e;
# # #             margin-top: 0.2rem;
# # #         }
        
# # #         .dark-mode .metric-value {
# # #             color: #e8e8f0;
# # #         }
        
# # #         .positive {
# # #             color: #10b981;
# # #         }
        
# # #         .negative {
# # #             color: #ef4444;
# # #         }
        
# # #         .section-title {
# # #             font-family: 'Inter', sans-serif;
# # #             font-weight: 600;
# # #             font-size: 1.1rem;
# # #             color: #1a1a2e;
# # #             margin: 1.5rem 0 0.8rem 0;
# # #             letter-spacing: -0.01em;
# # #         }
        
# # #         .dark-mode .section-title {
# # #             color: #e8e8f0;
# # #         }
        
# # #         /* Custom button */
# # #         .stButton > button {
# # #             font-family: 'Inter', sans-serif;
# # #             font-weight: 500;
# # #             font-size: 0.85rem;
# # #             background: #6366f1;
# # #             color: white;
# # #             border: none;
# # #             border-radius: 8px;
# # #             padding: 0.5rem 1.2rem;
# # #             transition: all 0.2s ease;
# # #         }
        
# # #         .stButton > button:hover {
# # #             background: #4f46e5;
# # #             box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
# # #         }
        
# # #         /* Sidebar */
# # #         .sidebar-section {
# # #             font-family: 'Inter', sans-serif;
# # #             font-weight: 500;
# # #             font-size: 0.75rem;
# # #             color: #8a8aaa;
# # #             text-transform: uppercase;
# # #             letter-spacing: 0.05em;
# # #             margin: 1.5rem 0 0.5rem 0;
# # #         }
        
# # #         .dark-mode .sidebar-section {
# # #             color: #6a6a8a;
# # #         }
        
# # #         /* Hide Streamlit branding */
# # #         #MainMenu {visibility: hidden;}
# # #         footer {visibility: hidden;}
# # #         header {visibility: hidden;}
        
# # #         /* Responsive */
# # #         @media (max-width: 768px) {
# # #             .main-header { font-size: 1.5rem; }
# # #             .metric-value { font-size: 1.3rem; }
# # #         }
# # #     </style>
# # #     """, unsafe_allow_html=True)

# # # # Initialize session state
# # # if 'data' not in st.session_state:
# # #     st.session_state.data = None
# # # if 'dark_mode' not in st.session_state:
# # #     st.session_state.dark_mode = False
# # # if 'running' not in st.session_state:
# # #     st.session_state.running = False
# # # if 'export_format' not in st.session_state:
# # #     st.session_state.export_format = None

# # # # Load CSS
# # # load_css()

# # # # Apply dark mode class
# # # if st.session_state.dark_mode:
# # #     st.markdown('<div class="dark-mode">', unsafe_allow_html=True)

# # # # Sidebar
# # # with st.sidebar:
# # #     st.markdown('<p style="font-family: Inter; font-weight: 600; font-size: 1.2rem; color: #1a1a2e; margin-bottom: 0.5rem;">NIFTY IT</p>', unsafe_allow_html=True)
# # #     if st.session_state.dark_mode:
# # #         st.markdown('<p style="font-family: Inter; font-weight: 300; font-size: 0.8rem; color: #6a6a8a; margin-bottom: 1.5rem;">Analytics Dashboard</p>', unsafe_allow_html=True)
# # #     else:
# # #         st.markdown('<p style="font-family: Inter; font-weight: 300; font-size: 0.8rem; color: #8a8aaa; margin-bottom: 1.5rem;">Analytics Dashboard</p>', unsafe_allow_html=True)
    
# # #     # Dark mode toggle
# # #     dark_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
# # #     if dark_mode != st.session_state.dark_mode:
# # #         st.session_state.dark_mode = dark_mode
# # #         st.rerun()
    
# # #     st.markdown('<hr style="margin: 1.5rem 0;">', unsafe_allow_html=True)
    
# # #     # Controls
# # #     st.markdown('<p class="sidebar-section">Controls</p>', unsafe_allow_html=True)
    
# # #     if st.button("🔄 Refresh Data", use_container_width=True):
# # #         st.session_state.running = True
# # #         st.rerun()
    
# # #     # Filters
# # #     st.markdown('<p class="sidebar-section">Filters</p>', unsafe_allow_html=True)
    
# # #     if st.session_state.data is not None:
# # #         df = st.session_state.data
        
# # #         # Company filter
# # #         companies = df['Company Name'].unique().tolist()
# # #         selected_companies = st.multiselect(
# # #             "Companies",
# # #             companies,
# # #             default=companies,
# # #             key="company_filter"
# # #         )
        
# # #         # Revenue filter - ensure numeric
# # #         if 'Current Revenue (Cr)' in df.columns:
# # #             revenue_col = df['Current Revenue (Cr)']
# # #             if revenue_col.dtype == 'object':
# # #                 revenue_col = pd.to_numeric(revenue_col, errors='coerce')
            
# # #             min_rev = revenue_col.min() if revenue_col.notna().any() else 0
# # #             max_rev = revenue_col.max() if revenue_col.notna().any() else 10000
            
# # #             rev_range = st.slider(
# # #                 "Revenue Range (Cr)",
# # #                 min_value=float(min_rev) if not pd.isna(min_rev) else 0.0,
# # #                 max_value=float(max_rev) if not pd.isna(max_rev) else 10000.0,
# # #                 value=(float(min_rev) if not pd.isna(min_rev) else 0.0, 
# # #                        float(max_rev) if not pd.isna(max_rev) else 10000.0),
# # #                 step=100.0
# # #             )

# # #         # Deal wins filter - ensure numeric
# # #         if 'Deal Wins' in df.columns:
# # #             deals_col = df['Deal Wins']
# # #             if deals_col.dtype == 'object':
# # #                 deals_col = pd.to_numeric(deals_col, errors='coerce')
            
# # #             min_deals = deals_col.min() if deals_col.notna().any() else 0
# # #             max_deals = deals_col.max() if deals_col.notna().any() else 10
            
# # #             deal_range = st.slider(
# # #                 "Deal Wins",
# # #                 min_value=int(min_deals) if not pd.isna(min_deals) else 0,
# # #                 max_value=int(max_deals) if not pd.isna(max_deals) else 10,
# # #                 value=(int(min_deals) if not pd.isna(min_deals) else 0, 
# # #                        int(max_deals) if not pd.isna(max_deals) else 10)
# # #             )
    
# # #     # Export
# # #     st.markdown('<hr style="margin: 1.5rem 0;">', unsafe_allow_html=True)
# # #     st.markdown('<p class="sidebar-section">Export</p>', unsafe_allow_html=True)
    
# # #     if st.session_state.data is not None:
# # #         col1, col2 = st.columns(2)
# # #         with col1:
# # #             if st.button("📊 XLSX", use_container_width=True):
# # #                 st.session_state.export_format = 'xlsx'
# # #         with col2:
# # #             if st.button("📄 PDF", use_container_width=True):
# # #                 st.session_state.export_format = 'pdf'

# # # # Main content
# # # st.markdown('<p class="main-header">NIFTY IT Index</p>', unsafe_allow_html=True)
# # # st.markdown('<p class="sub-header">Real-time analytics & performance metrics of India\'s top IT companies</p>', unsafe_allow_html=True)

# # # # Data loading function
# # # def load_data():
# # #     """Load the latest Excel file from output directory"""
# # #     output_dir = "output"
# # #     if not os.path.exists(output_dir):
# # #         return None
    
# # #     excel_files = [f for f in os.listdir(output_dir) if f.endswith('.xlsx') and f.startswith('nifty_it_data_')]
# # #     if not excel_files:
# # #         return None
    
# # #     latest_file = sorted(excel_files)[-1]
# # #     file_path = os.path.join(output_dir, latest_file)
    
# # #     try:
# # #         df = pd.read_excel(file_path, sheet_name='Summary')
        
# # #         # Clean numeric columns - remove currency symbols and commas
# # #         numeric_cols = ['Current Revenue (Cr)', 'Annual Revenue (Cr)', 'Annual Profit (Cr)']
# # #         for col in numeric_cols:
# # #             if col in df.columns:
# # #                 # Convert to string, remove ₹, commas, and convert to numeric
# # #                 df[col] = df[col].astype(str).str.replace('₹', '').str.replace(',', '').str.strip()
# # #                 df[col] = pd.to_numeric(df[col], errors='coerce')
        
# # #         # Clean 'Total TCV' - extract numeric value
# # #         if 'Total TCV' in df.columns:
# # #             df['Total TCV'] = df['Total TCV'].astype(str).str.extract(r'([\d.]+)')[0]
# # #             df['Total TCV'] = pd.to_numeric(df['Total TCV'], errors='coerce')
        
# # #         # Clean 'Deal Wins'
# # #         if 'Deal Wins' in df.columns:
# # #             df['Deal Wins'] = pd.to_numeric(df['Deal Wins'], errors='coerce')
        
# # #         # Clean 'Total Clients'
# # #         if 'Total Clients' in df.columns:
# # #             df['Total Clients'] = pd.to_numeric(df['Total Clients'], errors='coerce')
        
# # #         # Clean 'Profit Margin %'
# # #         if 'Profit Margin %' in df.columns:
# # #             df['Profit Margin %'] = pd.to_numeric(df['Profit Margin %'], errors='coerce')
        
# # #         return df
# # #     except Exception as e:
# # #         st.error(f"Error loading data: {e}")
# # #         return None

# # # # Export function
# # # def export_data(format_type):
# # #     """Export data to XLSX or PDF"""
# # #     if st.session_state.data is None:
# # #         return
    
# # #     df = st.session_state.data
    
# # #     if format_type == 'xlsx':
# # #         output = BytesIO()
# # #         with pd.ExcelWriter(output, engine='openpyxl') as writer:
# # #             df.to_excel(writer, sheet_name='Summary', index=False)
# # #         output.seek(0)
        
# # #         st.download_button(
# # #             label="📥 Download XLSX",
# # #             data=output,
# # #             file_name=f"nifty_it_data_{datetime.now().strftime('%Y%m%d')}.xlsx",
# # #             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
# # #         )
    
# # #     elif format_type == 'pdf':
# # #         # Simplified PDF export using plotly
# # #         fig = go.Figure(data=[go.Table(
# # #             header=dict(values=list(df.columns),
# # #                        fill_color='#6366f1',
# # #                        align='left',
# # #                        font=dict(color='white', size=12)),
# # #             cells=dict(values=[df[col] for col in df.columns],
# # #                       fill_color='rgba(99, 102, 241, 0.05)',
# # #                       align='left',
# # #                       font=dict(size=11))
# # #         )])
        
# # #         fig.update_layout(
# # #             title=f"NIFTY IT Data - {datetime.now().strftime('%d %b %Y')}",
# # #             width=1200,
# # #             height=800,
# # #             font=dict(family='Inter')
# # #         )
        
# # #         st.plotly_chart(fig, use_container_width=True)

# # # # Handle refresh
# # # if st.session_state.running:
# # #     with st.spinner("Running data pipeline... This may take a few minutes."):
# # #         try:
# # #             # Run the main.py script
# # #             result = subprocess.run([sys.executable, "main.py"], capture_output=True, text=True)
# # #             if result.returncode == 0:
# # #                 st.session_state.data = load_data()
# # #                 st.success("✅ Data refreshed successfully!")
# # #             else:
# # #                 st.error(f"❌ Pipeline failed: {result.stderr[:200]}")
# # #         except Exception as e:
# # #             st.error(f"❌ Error: {str(e)}")
# # #     st.session_state.running = False
# # #     st.rerun()

# # # # Load data if not loaded
# # # if st.session_state.data is None:
# # #     st.session_state.data = load_data()

# # # # Display data
# # # if st.session_state.data is not None:
# # #     df = st.session_state.data
    
# # #     # Apply filters
# # #     if 'company_filter' in st.session_state and st.session_state.company_filter:
# # #         df = df[df['Company Name'].isin(st.session_state.company_filter)]
    
# # #     if 'rev_range' in st.session_state:
# # #         df = df[(df['Current Revenue (Cr)'] >= st.session_state.rev_range[0]) & 
# # #                 (df['Current Revenue (Cr)'] <= st.session_state.rev_range[1])]
    
# # #     if 'deal_range' in st.session_state:
# # #         df = df[(df['Deal Wins'] >= st.session_state.deal_range[0]) & 
# # #                 (df['Deal Wins'] <= st.session_state.deal_range[1])]
    
# # #     # Metrics Row
# # #     col1, col2, col3, col4, col5 = st.columns(5)

# # #     with col1:
# # #         revenue_col = df['Current Revenue (Cr)']
# # #         if revenue_col.dtype == 'object':
# # #             revenue_col = pd.to_numeric(revenue_col, errors='coerce')
# # #         total_revenue = revenue_col.sum() if revenue_col.notna().any() else 0
# # #         st.markdown(f"""
# # #         <div class="metric-card">
# # #             <div class="metric-label">Total Revenue</div>
# # #             <div class="metric-value">₹{total_revenue:,.0f} Cr</div>
# # #         </div>
# # #         """, unsafe_allow_html=True)

# # #     with col2:
# # #         revenue_col = df['Current Revenue (Cr)']
# # #         if revenue_col.dtype == 'object':
# # #             revenue_col = pd.to_numeric(revenue_col, errors='coerce')
# # #         avg_revenue = revenue_col.mean() if revenue_col.notna().any() else 0
# # #         st.markdown(f"""
# # #         <div class="metric-card">
# # #             <div class="metric-label">Average Revenue</div>
# # #             <div class="metric-value">₹{avg_revenue:,.0f} Cr</div>
# # #         </div>
# # #         """, unsafe_allow_html=True)

# # #     with col3:
# # #         if 'Deal Wins' in df.columns:
# # #             deals_col = df['Deal Wins']
# # #             if deals_col.dtype == 'object':
# # #                 deals_col = pd.to_numeric(deals_col, errors='coerce')
# # #             total_deals = deals_col.sum() if deals_col.notna().any() else 0
# # #         else:
# # #             total_deals = 0
# # #         st.markdown(f"""
# # #         <div class="metric-card">
# # #             <div class="metric-label">Total Deals</div>
# # #             <div class="metric-value">{total_deals:,.0f}</div>
# # #         </div>
# # #         """, unsafe_allow_html=True)

# # #     with col4:
# # #         if 'Profit Margin %' in df.columns:
# # #             margin_col = df['Profit Margin %']
# # #             if margin_col.dtype == 'object':
# # #                 margin_col = pd.to_numeric(margin_col, errors='coerce')
# # #             avg_margin = margin_col.mean() if margin_col.notna().any() else 0
# # #         else:
# # #             avg_margin = 0
# # #         st.markdown(f"""
# # #         <div class="metric-card">
# # #             <div class="metric-label">Avg Margin</div>
# # #             <div class="metric-value">{avg_margin:.1f}%</div>
# # #         </div>
# # #         """, unsafe_allow_html=True)

# # #     with col5:
# # #         if 'Total Clients' in df.columns:
# # #             clients_col = df['Total Clients']
# # #             if clients_col.dtype == 'object':
# # #                 clients_col = pd.to_numeric(clients_col, errors='coerce')
# # #             total_clients = clients_col.sum() if clients_col.notna().any() else 0
# # #         else:
# # #             total_clients = 0
# # #         st.markdown(f"""
# # #         <div class="metric-card">
# # #             <div class="metric-label">Total Clients</div>
# # #             <div class="metric-value">{total_clients:,.0f}</div>
# # #         </div>
# # #         """, unsafe_allow_html=True)
    
# # #     # Charts
# # #     st.markdown('<p class="section-title">Performance Overview</p>', unsafe_allow_html=True)
    
# # #     col1, col2 = st.columns(2)
    
# # #     with col1:
# # #         # Revenue bar chart - handle NaN values
# # #         chart_df = df.dropna(subset=['Current Revenue (Cr)'])
# # #         if not chart_df.empty:
# # #             fig_revenue = px.bar(
# # #                 chart_df,
# # #                 x='Company Name',
# # #                 y='Current Revenue (Cr)',
# # #                 title='Revenue by Company',
# # #                 color='Current Revenue (Cr)',
# # #                 color_continuous_scale='Blues',
# # #                 text='Current Revenue (Cr)'
# # #             )
# # #             fig_revenue.update_layout(
# # #                 plot_bgcolor='rgba(0,0,0,0)',
# # #                 paper_bgcolor='rgba(0,0,0,0)',
# # #                 font=dict(family='Inter', size=12),
# # #                 height=400,
# # #                 margin=dict(l=40, r=40, t=40, b=40),
# # #                 showlegend=False
# # #             )
# # #             fig_revenue.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
# # #             st.plotly_chart(fig_revenue, use_container_width=True)
    
# # #     with col2:
# # #         # Revenue vs Deal Wins scatter - handle NaN values
# # #         if 'Deal Wins' in df.columns:
# # #             scatter_df = df.dropna(subset=['Current Revenue (Cr)', 'Deal Wins'])
# # #             if not scatter_df.empty and scatter_df['Deal Wins'].notna().any():
# # #                 fig_scatter = px.scatter(
# # #                     scatter_df,
# # #                     x='Current Revenue (Cr)',
# # #                     y='Deal Wins',
# # #                     size='Current Revenue (Cr)',
# # #                     color='Company Name',
# # #                     text='Company Name',
# # #                     title='Revenue vs Deal Wins'
# # #                 )
# # #                 fig_scatter.update_layout(
# # #                     plot_bgcolor='rgba(0,0,0,0)',
# # #                     paper_bgcolor='rgba(0,0,0,0)',
# # #                     font=dict(family='Inter', size=12),
# # #                     height=400,
# # #                     margin=dict(l=40, r=40, t=40, b=40),
# # #                     showlegend=False
# # #                 )
# # #                 fig_scatter.update_traces(textposition='top center')
# # #                 st.plotly_chart(fig_scatter, use_container_width=True)
# # #             else:
# # #                 st.info("No deal wins data available for scatter plot")
    
# # #     # Data table
# # #     st.markdown('<p class="section-title">Company Data</p>', unsafe_allow_html=True)
    
# # #     display_cols = ['Company Name', 'Current Revenue (Cr)', 'Annual Revenue (Cr)', 
# # #                    'Profit Margin %', 'Total TCV', 'Deal Wins', 'Total Clients']
    
# # #     # Only include columns that exist
# # #     available_cols = [col for col in display_cols if col in df.columns]
# # #     display_df = df[available_cols].copy()
    
# # #     # Format columns - handle NaN values
# # #     for col in ['Current Revenue (Cr)', 'Annual Revenue (Cr)']:
# # #         if col in display_df.columns:
# # #             display_df[col] = display_df[col].map(lambda x: f"₹{x:,.0f}" if pd.notna(x) else "N/A")
    
# # #     if 'Profit Margin %' in display_df.columns:
# # #         display_df['Profit Margin %'] = display_df['Profit Margin %'].map(lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A")
    
# # #     if 'Total TCV' in display_df.columns:
# # #         display_df['Total TCV'] = display_df['Total TCV'].map(lambda x: f"{x:,.0f}" if pd.notna(x) else "N/A")
    
# # #     if 'Deal Wins' in display_df.columns:
# # #         display_df['Deal Wins'] = display_df['Deal Wins'].map(lambda x: f"{x:,.0f}" if pd.notna(x) else "0")
    
# # #     if 'Total Clients' in display_df.columns:
# # #         display_df['Total Clients'] = display_df['Total Clients'].map(lambda x: f"{x:,.0f}" if pd.notna(x) else "N/A")
    
# # #     # Rename columns for display
# # #     column_rename = {
# # #         'Company Name': 'Company',
# # #         'Current Revenue (Cr)': 'Current Revenue',
# # #         'Annual Revenue (Cr)': 'Annual Revenue',
# # #         'Profit Margin %': 'Margin',
# # #         'Total TCV': 'TCV',
# # #         'Deal Wins': 'Deals',
# # #         'Total Clients': 'Clients'
# # #     }
# # #     display_df = display_df.rename(columns=column_rename)
    
# # #     st.dataframe(
# # #         display_df,
# # #         use_container_width=True,
# # #         hide_index=True,
# # #         column_config={
# # #             "Company": st.column_config.TextColumn("Company", width="medium"),
# # #             "Current Revenue": st.column_config.TextColumn("Revenue", width="small"),
# # #             "Annual Revenue": st.column_config.TextColumn("Annual", width="small"),
# # #             "Margin": st.column_config.TextColumn("Margin", width="small"),
# # #             "TCV": st.column_config.TextColumn("TCV", width="small"),
# # #             "Deals": st.column_config.TextColumn("Deals", width="small"),
# # #             "Clients": st.column_config.TextColumn("Clients", width="small")
# # #         }
# # #     )

# # # else:
# # #     st.info("📂 No data found. Click 'Refresh Data' in the sidebar to run the pipeline and fetch the latest data.")

# # # # Footer
# # # st.markdown("""
# # # <hr style="margin: 2rem 0 1rem 0;">
# # # <p style="font-family: Inter; font-size: 0.75rem; color: #8a8aaa; text-align: center; letter-spacing: 0.03em;">
# # #     Data sourced from Screener.in & Company Investor Relations | Updated: {}
# # # </p>
# # # """.format(datetime.now().strftime("%d %b %Y, %H:%M")), unsafe_allow_html=True)

# # # # Close dark mode div
# # # if st.session_state.dark_mode:
# # #     st.markdown('</div>', unsafe_allow_html=True)

# # # dashboard.py (ENHANCED WITH YOUR COLOR PALETTE)
# # import streamlit as st
# # import pandas as pd
# # import plotly.express as px
# # import plotly.graph_objects as go
# # from plotly.subplots import make_subplots
# # import os
# # from datetime import datetime
# # import subprocess
# # import sys
# # import json
# # import base64
# # from io import BytesIO
# # import numpy as np

# # # Page configuration
# # st.set_page_config(
# #     page_title="NIFTY IT Analytics Dashboard",
# #     page_icon="📊",
# #     layout="wide",
# #     initial_sidebar_state="expanded"
# # )

# # # Color palette
# # COLORS = {
# #     'primary': '#091413',
# #     'secondary': '#285A48',
# #     'accent': '#408A71',
# #     'light': '#B0E4CC',
# #     'background': '#F5F8F7',
# #     'card_bg': '#FFFFFF',
# #     'text_primary': '#091413',
# #     'text_secondary': '#4A6A5A',
# #     'text_muted': '#8AAA9A',
# #     'border': '#E0EAE5'
# # }

# # # Custom CSS for premium minimalist design with your color palette
# # def load_css():
# #     st.markdown(f"""
# #     <style>
# #         /* Import premium fonts */
# #         @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
# #         /* Global styles */
# #         .stApp {{
# #             background-color: {COLORS['background']};
# #             font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
# #         }}
        
# #         /* Dark mode overrides */
# #         .dark-mode .stApp {{
# #             background-color: #0a0f0e;
# #         }}
        
# #         .dark-mode .stApp * {{
# #             color: #e8f0ed;
# #         }}
        
# #         .main-header {{
# #             font-family: 'Inter', sans-serif;
# #             font-weight: 700;
# #             font-size: 2.4rem;
# #             color: {COLORS['primary']};
# #             margin-bottom: 0.2rem;
# #             letter-spacing: -0.03em;
# #         }}
        
# #         .dark-mode .main-header {{
# #             color: {COLORS['light']};
# #         }}
        
# #         .sub-header {{
# #             font-family: 'Inter', sans-serif;
# #             font-weight: 400;
# #             font-size: 1rem;
# #             color: {COLORS['text_secondary']};
# #             margin-bottom: 2rem;
# #         }}
        
# #         .dark-mode .sub-header {{
# #             color: #b0d0c0;
# #         }}
        
# #         .metric-card {{
# #             background: {COLORS['card_bg']};
# #             border-radius: 16px;
# #             padding: 1.2rem 1.5rem;
# #             border: 1px solid {COLORS['border']};
# #             box-shadow: 0 1px 3px rgba(9, 20, 19, 0.06);
# #             transition: all 0.3s ease;
# #             position: relative;
# #             overflow: hidden;
# #         }}
        
# #         .metric-card::before {{
# #             content: '';
# #             position: absolute;
# #             top: 0;
# #             left: 0;
# #             right: 0;
# #             height: 3px;
# #             background: linear-gradient(90deg, {COLORS['secondary']}, {COLORS['accent']}, {COLORS['light']});
# #         }}
        
# #         .dark-mode .metric-card {{
# #             background: #141c19;
# #             border-color: #1a2a24;
# #             box-shadow: 0 1px 3px rgba(0,0,0,0.3);
# #         }}
        
# #         .metric-card:hover {{
# #             transform: translateY(-3px);
# #             box-shadow: 0 8px 24px rgba(40, 90, 72, 0.12);
# #         }}
        
# #         .metric-label {{
# #             font-family: 'Inter', sans-serif;
# #             font-weight: 500;
# #             font-size: 0.75rem;
# #             color: {COLORS['text_muted']};
# #             text-transform: uppercase;
# #             letter-spacing: 0.06em;
# #         }}
        
# #         .metric-value {{
# #             font-family: 'Inter', sans-serif;
# #             font-weight: 700;
# #             font-size: 1.8rem;
# #             color: {COLORS['primary']};
# #             margin-top: 0.2rem;
# #         }}
        
# #         .dark-mode .metric-value {{
# #             color: {COLORS['light']};
# #         }}
        
# #         .metric-change {{
# #             font-family: 'Inter', sans-serif;
# #             font-size: 0.8rem;
# #             font-weight: 500;
# #             margin-top: 0.2rem;
# #         }}
        
# #         .positive {{ color: #10b981; }}
# #         .negative {{ color: #ef4444; }}
        
# #         .section-title {{
# #             font-family: 'Inter', sans-serif;
# #             font-weight: 600;
# #             font-size: 1.2rem;
# #             color: {COLORS['primary']};
# #             margin: 1.5rem 0 1rem 0;
# #             letter-spacing: -0.01em;
# #         }}
        
# #         .dark-mode .section-title {{
# #             color: {COLORS['light']};
# #         }}
        
# #         /* Tabs styling */
# #         .stTabs [data-baseweb="tab-list"] {{
# #             gap: 2px;
# #             background-color: {COLORS['background']};
# #             border-radius: 12px;
# #             padding: 4px;
# #         }}
        
# #         .dark-mode .stTabs [data-baseweb="tab-list"] {{
# #             background-color: #0a0f0e;
# #         }}
        
# #         .stTabs [data-baseweb="tab"] {{
# #             font-family: 'Inter', sans-serif;
# #             font-weight: 500;
# #             font-size: 0.85rem;
# #             border-radius: 8px;
# #             padding: 0.5rem 1.2rem;
# #             transition: all 0.2s ease;
# #         }}
        
# #         .stTabs [data-baseweb="tab"]:hover {{
# #             background-color: {COLORS['light']};
# #             opacity: 0.7;
# #         }}
        
# #         .stTabs [aria-selected="true"] {{
# #             background-color: {COLORS['accent']};
# #             color: white !important;
# #         }}
        
# #         .dark-mode .stTabs [aria-selected="true"] {{
# #             background-color: {COLORS['secondary']};
# #         }}
        
# #         /* Custom button */
# #         .stButton > button {{
# #             font-family: 'Inter', sans-serif;
# #             font-weight: 500;
# #             font-size: 0.85rem;
# #             background: {COLORS['secondary']};
# #             color: white;
# #             border: none;
# #             border-radius: 8px;
# #             padding: 0.5rem 1.2rem;
# #             transition: all 0.3s ease;
# #         }}
        
# #         .stButton > button:hover {{
# #             background: {COLORS['accent']};
# #             box-shadow: 0 4px 16px rgba(40, 90, 72, 0.3);
# #             transform: translateY(-1px);
# #         }}
        
# #         /* Sidebar */
# #         .sidebar-section {{
# #             font-family: 'Inter', sans-serif;
# #             font-weight: 500;
# #             font-size: 0.75rem;
# #             color: {COLORS['text_muted']};
# #             text-transform: uppercase;
# #             letter-spacing: 0.06em;
# #             margin: 1.5rem 0 0.5rem 0;
# #         }}
        
# #         .dark-mode .sidebar-section {{
# #             color: #6a8a7a;
# #         }}
        
# #         /* Hide Streamlit branding */
# #         #MainMenu {{visibility: hidden;}}
# #         footer {{visibility: hidden;}}
# #         header {{visibility: hidden;}}
        
# #         /* Company detail card */
# #         .company-detail-card {{
# #             background: {COLORS['card_bg']};
# #             border-radius: 12px;
# #             padding: 1.5rem;
# #             border: 1px solid {COLORS['border']};
# #             margin-bottom: 1rem;
# #         }}
        
# #         .dark-mode .company-detail-card {{
# #             background: #141c19;
# #             border-color: #1a2a24;
# #         }}
        
# #         .company-name-title {{
# #             font-family: 'Inter', sans-serif;
# #             font-weight: 700;
# #             font-size: 1.8rem;
# #             color: {COLORS['primary']};
# #         }}
        
# #         .dark-mode .company-name-title {{
# #             color: {COLORS['light']};
# #         }}
        
# #         .detail-label {{
# #             font-family: 'Inter', sans-serif;
# #             font-weight: 500;
# #             font-size: 0.8rem;
# #             color: {COLORS['text_muted']};
# #             text-transform: uppercase;
# #             letter-spacing: 0.04em;
# #         }}
        
# #         .detail-value {{
# #             font-family: 'Inter', sans-serif;
# #             font-weight: 600;
# #             font-size: 1.1rem;
# #             color: {COLORS['primary']};
# #         }}
        
# #         .dark-mode .detail-value {{
# #             color: #e8f0ed;
# #         }}
        
# #         /* Responsive */
# #         @media (max-width: 768px) {{
# #             .main-header {{ font-size: 1.5rem; }}
# #             .metric-value {{ font-size: 1.3rem; }}
# #         }}
# #     </style>
# #     """, unsafe_allow_html=True)

# # # Initialize session state
# # if 'data' not in st.session_state:
# #     st.session_state.data = None
# # if 'dark_mode' not in st.session_state:
# #     st.session_state.dark_mode = False
# # if 'running' not in st.session_state:
# #     st.session_state.running = False
# # if 'export_format' not in st.session_state:
# #     st.session_state.export_format = None

# # # Load CSS
# # load_css()

# # # Apply dark mode class
# # if st.session_state.dark_mode:
# #     st.markdown('<div class="dark-mode">', unsafe_allow_html=True)

# # # Sidebar
# # with st.sidebar:
# #     st.markdown(f'<p style="font-family: Inter; font-weight: 700; font-size: 1.3rem; color: {COLORS["primary"]}; margin-bottom: 0.2rem;">NIFTY IT</p>', unsafe_allow_html=True)
# #     if st.session_state.dark_mode:
# #         st.markdown(f'<p style="font-family: Inter; font-weight: 300; font-size: 0.8rem; color: #6a8a7a; margin-bottom: 1.5rem;">Analytics Dashboard</p>', unsafe_allow_html=True)
# #     else:
# #         st.markdown(f'<p style="font-family: Inter; font-weight: 300; font-size: 0.8rem; color: {COLORS["text_muted"]}; margin-bottom: 1.5rem;">Analytics Dashboard</p>', unsafe_allow_html=True)
    
# #     # Dark mode toggle
# #     dark_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
# #     if dark_mode != st.session_state.dark_mode:
# #         st.session_state.dark_mode = dark_mode
# #         st.rerun()
    
# #     st.markdown(f'<hr style="margin: 1.5rem 0; border-color: {COLORS["border"]};">', unsafe_allow_html=True)
    
# #     # Controls
# #     st.markdown('<p class="sidebar-section">Controls</p>', unsafe_allow_html=True)
    
# #     if st.button("🔄 Refresh Data", use_container_width=True):
# #         st.session_state.running = True
# #         st.rerun()
    
# #     # Filters
# #     st.markdown('<p class="sidebar-section">Filters</p>', unsafe_allow_html=True)
    
# #     if st.session_state.data is not None:
# #         df = st.session_state.data
        
# #         # Company filter
# #         companies = df['Company Name'].unique().tolist()
# #         selected_companies = st.multiselect(
# #             "Companies",
# #             companies,
# #             default=companies,
# #             key="company_filter"
# #         )
        
# #         # Revenue filter
# #         if 'Current Revenue (Cr)' in df.columns:
# #             revenue_col = df['Current Revenue (Cr)']
# #             if revenue_col.dtype == 'object':
# #                 revenue_col = pd.to_numeric(revenue_col, errors='coerce')
            
# #             min_rev = revenue_col.min() if revenue_col.notna().any() else 0
# #             max_rev = revenue_col.max() if revenue_col.notna().any() else 10000
            
# #             rev_range = st.slider(
# #                 "Revenue Range (Cr)",
# #                 min_value=float(min_rev) if not pd.isna(min_rev) else 0.0,
# #                 max_value=float(max_rev) if not pd.isna(max_rev) else 10000.0,
# #                 value=(float(min_rev) if not pd.isna(min_rev) else 0.0, 
# #                        float(max_rev) if not pd.isna(max_rev) else 10000.0),
# #                 step=100.0
# #             )

# #         # Deal wins filter
# #         if 'Deal Wins' in df.columns:
# #             deals_col = df['Deal Wins']
# #             if deals_col.dtype == 'object':
# #                 deals_col = pd.to_numeric(deals_col, errors='coerce')
            
# #             min_deals = deals_col.min() if deals_col.notna().any() else 0
# #             max_deals = deals_col.max() if deals_col.notna().any() else 10
            
# #             deal_range = st.slider(
# #                 "Deal Wins",
# #                 min_value=int(min_deals) if not pd.isna(min_deals) else 0,
# #                 max_value=int(max_deals) if not pd.isna(max_deals) else 10,
# #                 value=(int(min_deals) if not pd.isna(min_deals) else 0, 
# #                        int(max_deals) if not pd.isna(max_deals) else 10)
# #             )
    
# #     # Export
# #     st.markdown(f'<hr style="margin: 1.5rem 0; border-color: {COLORS["border"]};">', unsafe_allow_html=True)
# #     st.markdown('<p class="sidebar-section">Export</p>', unsafe_allow_html=True)
    
# #     if st.session_state.data is not None:
# #         col1, col2 = st.columns(2)
# #         with col1:
# #             if st.button("📊 XLSX", use_container_width=True):
# #                 st.session_state.export_format = 'xlsx'
# #         with col2:
# #             if st.button("📄 PDF", use_container_width=True):
# #                 st.session_state.export_format = 'pdf'

# # # Main content
# # st.markdown('<p class="main-header">NIFTY IT Index</p>', unsafe_allow_html=True)
# # st.markdown('<p class="sub-header">Real-time analytics & performance metrics of India\'s top IT companies</p>', unsafe_allow_html=True)

# # # Data loading function
# # def load_data():
# #     """Load the latest Excel file from output directory"""
# #     output_dir = "output"
# #     if not os.path.exists(output_dir):
# #         return None
    
# #     excel_files = [f for f in os.listdir(output_dir) if f.endswith('.xlsx') and f.startswith('nifty_it_data_')]
# #     if not excel_files:
# #         return None
    
# #     latest_file = sorted(excel_files)[-1]
# #     file_path = os.path.join(output_dir, latest_file)
    
# #     try:
# #         df = pd.read_excel(file_path, sheet_name='Summary')
        
# #         # Clean numeric columns
# #         numeric_cols = ['Current Revenue (Cr)', 'Annual Revenue (Cr)', 'Annual Profit (Cr)']
# #         for col in numeric_cols:
# #             if col in df.columns:
# #                 df[col] = df[col].astype(str).str.replace('₹', '').str.replace(',', '').str.strip()
# #                 df[col] = pd.to_numeric(df[col], errors='coerce')
        
# #         if 'Total TCV' in df.columns:
# #             df['Total TCV'] = df['Total TCV'].astype(str).str.extract(r'([\d.]+)')[0]
# #             df['Total TCV'] = pd.to_numeric(df['Total TCV'], errors='coerce')
        
# #         if 'Deal Wins' in df.columns:
# #             df['Deal Wins'] = pd.to_numeric(df['Deal Wins'], errors='coerce')
        
# #         if 'Total Clients' in df.columns:
# #             df['Total Clients'] = pd.to_numeric(df['Total Clients'], errors='coerce')
        
# #         if 'Profit Margin %' in df.columns:
# #             df['Profit Margin %'] = pd.to_numeric(df['Profit Margin %'], errors='coerce')
        
# #         return df
# #     except Exception as e:
# #         st.error(f"Error loading data: {e}")
# #         return None

# # # Handle refresh
# # if st.session_state.running:
# #     with st.spinner("Running data pipeline... This may take a few minutes."):
# #         try:
# #             result = subprocess.run([sys.executable, "main.py"], capture_output=True, text=True)
# #             if result.returncode == 0:
# #                 st.session_state.data = load_data()
# #                 st.success("✅ Data refreshed successfully!")
# #             else:
# #                 st.error(f"❌ Pipeline failed: {result.stderr[:200]}")
# #         except Exception as e:
# #             st.error(f"❌ Error: {str(e)}")
# #     st.session_state.running = False
# #     st.rerun()

# # # Load data if not loaded
# # if st.session_state.data is None:
# #     st.session_state.data = load_data()

# # # Display data
# # if st.session_state.data is not None:
# #     df = st.session_state.data
    
# #     # Apply filters
# #     if 'company_filter' in st.session_state and st.session_state.company_filter:
# #         df = df[df['Company Name'].isin(st.session_state.company_filter)]
    
# #     if 'rev_range' in st.session_state:
# #         df = df[(df['Current Revenue (Cr)'] >= st.session_state.rev_range[0]) & 
# #                 (df['Current Revenue (Cr)'] <= st.session_state.rev_range[1])]
    
# #     if 'deal_range' in st.session_state:
# #         df = df[(df['Deal Wins'] >= st.session_state.deal_range[0]) & 
# #                 (df['Deal Wins'] <= st.session_state.deal_range[1])]
    
# #     # Create tabs
# #     tab1, tab2, tab3 = st.tabs(["📊 Overview", "🏢 Company Details", "📈 Analytics"])
    
# #     # TAB 1: OVERVIEW
# #     with tab1:
# #         # Metrics Row
# #         col1, col2, col3, col4, col5 = st.columns(5)

# #         with col1:
# #             revenue_col = df['Current Revenue (Cr)']
# #             if revenue_col.dtype == 'object':
# #                 revenue_col = pd.to_numeric(revenue_col, errors='coerce')
# #             total_revenue = revenue_col.sum() if revenue_col.notna().any() else 0
# #             st.markdown(f"""
# #             <div class="metric-card">
# #                 <div class="metric-label">Total Revenue</div>
# #                 <div class="metric-value">₹{total_revenue:,.0f} Cr</div>
# #             </div>
# #             """, unsafe_allow_html=True)

# #         with col2:
# #             revenue_col = df['Current Revenue (Cr)']
# #             if revenue_col.dtype == 'object':
# #                 revenue_col = pd.to_numeric(revenue_col, errors='coerce')
# #             avg_revenue = revenue_col.mean() if revenue_col.notna().any() else 0
# #             st.markdown(f"""
# #             <div class="metric-card">
# #                 <div class="metric-label">Average Revenue</div>
# #                 <div class="metric-value">₹{avg_revenue:,.0f} Cr</div>
# #             </div>
# #             """, unsafe_allow_html=True)

# #         with col3:
# #             if 'Deal Wins' in df.columns:
# #                 deals_col = df['Deal Wins']
# #                 if deals_col.dtype == 'object':
# #                     deals_col = pd.to_numeric(deals_col, errors='coerce')
# #                 total_deals = deals_col.sum() if deals_col.notna().any() else 0
# #             else:
# #                 total_deals = 0
# #             st.markdown(f"""
# #             <div class="metric-card">
# #                 <div class="metric-label">Total Deals</div>
# #                 <div class="metric-value">{total_deals:,.0f}</div>
# #             </div>
# #             """, unsafe_allow_html=True)

# #         with col4:
# #             if 'Profit Margin %' in df.columns:
# #                 margin_col = df['Profit Margin %']
# #                 if margin_col.dtype == 'object':
# #                     margin_col = pd.to_numeric(margin_col, errors='coerce')
# #                 avg_margin = margin_col.mean() if margin_col.notna().any() else 0
# #             else:
# #                 avg_margin = 0
# #             st.markdown(f"""
# #             <div class="metric-card">
# #                 <div class="metric-label">Avg Margin</div>
# #                 <div class="metric-value">{avg_margin:.1f}%</div>
# #             </div>
# #             """, unsafe_allow_html=True)

# #         with col5:
# #             if 'Total Clients' in df.columns:
# #                 clients_col = df['Total Clients']
# #                 if clients_col.dtype == 'object':
# #                     clients_col = pd.to_numeric(clients_col, errors='coerce')
# #                 total_clients = clients_col.sum() if clients_col.notna().any() else 0
# #             else:
# #                 total_clients = 0
# #             st.markdown(f"""
# #             <div class="metric-card">
# #                 <div class="metric-label">Total Clients</div>
# #                 <div class="metric-value">{total_clients:,.0f}</div>
# #             </div>
# #             """, unsafe_allow_html=True)
        
# #         # Charts
# #         st.markdown('<p class="section-title">Performance Overview</p>', unsafe_allow_html=True)
        
# #         col1, col2 = st.columns(2)
        
# #         with col1:
# #             chart_df = df.dropna(subset=['Current Revenue (Cr)'])
# #             if not chart_df.empty:
# #                 fig_revenue = px.bar(
# #                     chart_df,
# #                     x='Company Name',
# #                     y='Current Revenue (Cr)',
# #                     title='Revenue by Company',
# #                     color='Current Revenue (Cr)',
# #                     color_continuous_scale=['#B0E4CC', '#408A71', '#285A48', '#091413'],
# #                     text='Current Revenue (Cr)'
# #                 )
# #                 fig_revenue.update_layout(
# #                     plot_bgcolor='rgba(0,0,0,0)',
# #                     paper_bgcolor='rgba(0,0,0,0)',
# #                     font=dict(family='Inter', size=12, color=COLORS['text_secondary']),
# #                     height=400,
# #                     margin=dict(l=40, r=40, t=40, b=40),
# #                     showlegend=False
# #                 )
# #                 fig_revenue.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
# #                 st.plotly_chart(fig_revenue, use_container_width=True)
        
# #         with col2:
# #             if 'Deal Wins' in df.columns:
# #                 scatter_df = df.dropna(subset=['Current Revenue (Cr)', 'Deal Wins'])
# #                 if not scatter_df.empty and scatter_df['Deal Wins'].notna().any():
# #                     fig_scatter = px.scatter(
# #                         scatter_df,
# #                         x='Current Revenue (Cr)',
# #                         y='Deal Wins',
# #                         size='Current Revenue (Cr)',
# #                         color='Company Name',
# #                         text='Company Name',
# #                         title='Revenue vs Deal Wins',
# #                         color_discrete_sequence=['#091413', '#285A48', '#408A71', '#B0E4CC']
# #                     )
# #                     fig_scatter.update_layout(
# #                         plot_bgcolor='rgba(0,0,0,0)',
# #                         paper_bgcolor='rgba(0,0,0,0)',
# #                         font=dict(family='Inter', size=12, color=COLORS['text_secondary']),
# #                         height=400,
# #                         margin=dict(l=40, r=40, t=40, b=40),
# #                         showlegend=False
# #                     )
# #                     fig_scatter.update_traces(textposition='top center')
# #                     st.plotly_chart(fig_scatter, use_container_width=True)
# #                 else:
# #                     st.info("No deal wins data available for scatter plot")
    
# #     # TAB 2: COMPANY DETAILS
# #     with tab2:
# #         st.markdown('<p class="section-title">Individual Company Analysis</p>', unsafe_allow_html=True)
        
# #         # Company selector
# #         companies = df['Company Name'].unique().tolist()
# #         selected_company = st.selectbox("Select Company", companies)
        
# #         if selected_company:
# #             company_data = df[df['Company Name'] == selected_company].iloc[0]
            
# #             # Company metrics
# #             col1, col2, col3, col4 = st.columns(4)
            
# #             with col1:
# #                 st.markdown(f"""
# #                 <div class="company-detail-card">
# #                     <div class="detail-label">Current Revenue</div>
# #                     <div class="detail-value">₹{company_data['Current Revenue (Cr)']:,.0f} Cr</div>
# #                 </div>
# #                 """, unsafe_allow_html=True)
            
# #             with col2:
# #                 st.markdown(f"""
# #                 <div class="company-detail-card">
# #                     <div class="detail-label">Annual Revenue</div>
# #                     <div class="detail-value">₹{company_data['Annual Revenue (Cr)']:,.0f} Cr</div>
# #                 </div>
# #                 """, unsafe_allow_html=True)
            
# #             with col3:
# #                 margin = company_data.get('Profit Margin %', 0)
# #                 st.markdown(f"""
# #                 <div class="company-detail-card">
# #                     <div class="detail-label">Profit Margin</div>
# #                     <div class="detail-value">{margin:.1f}%</div>
# #                 </div>
# #                 """, unsafe_allow_html=True)
            
# #             with col4:
# #                 deals = company_data.get('Deal Wins', 0)
# #                 st.markdown(f"""
# #                 <div class="company-detail-card">
# #                     <div class="detail-label">Deal Wins</div>
# #                     <div class="detail-value">{deals:,.0f}</div>
# #                 </div>
# #                 """, unsafe_allow_html=True)
            
# #             # Additional details
# #             col1, col2 = st.columns(2)
            
# #             with col1:
# #                 st.markdown(f"""
# #                 <div class="company-detail-card">
# #                     <div class="detail-label">Financial Year</div>
# #                     <div class="detail-value">{company_data.get('Financial Year', 'N/A')}</div>
# #                 </div>
# #                 <div class="company-detail-card">
# #                     <div class="detail-label">Total TCV</div>
# #                     <div class="detail-value">{company_data.get('Total TCV', 'N/A')}</div>
# #                 </div>
# #                 """, unsafe_allow_html=True)
            
# #             with col2:
# #                 clients = company_data.get('Total Clients', 'N/A')
# #                 st.markdown(f"""
# #                 <div class="company-detail-card">
# #                     <div class="detail-label">Total Clients</div>
# #                     <div class="detail-value">{clients:,.0f}</div>
# #                 </div>
# #                 <div class="company-detail-card">
# #                     <div class="detail-label">Service Categories</div>
# #                     <div class="detail-value">{company_data.get('Service Categories', 'N/A')}</div>
# #                 </div>
# #                 """, unsafe_allow_html=True)
            
# #             # Services/Products
# #             st.markdown('<p class="section-title">Services & Products</p>', unsafe_allow_html=True)
# #             services = company_data.get('Services/Products', 'No data available')
# #             st.markdown(f"""
# #             <div class="company-detail-card">
# #                 <div style="font-family: Inter; font-size: 0.9rem; color: {COLORS['text_secondary']}; white-space: pre-wrap;">
# #                     {services[:1000]}{'...' if len(str(services)) > 1000 else ''}
# #                 </div>
# #             </div>
# #             """, unsafe_allow_html=True)
    
# #     # TAB 3: ANALYTICS
# #     with tab3:
# #         st.markdown('<p class="section-title">Advanced Analytics</p>', unsafe_allow_html=True)
        
# #         col1, col2 = st.columns(2)
        
# #         with col1:
# #             # Revenue distribution
# #             fig_pie = px.pie(
# #                 df,
# #                 values='Current Revenue (Cr)',
# #                 names='Company Name',
# #                 title='Revenue Distribution',
# #                 color_discrete_sequence=['#091413', '#285A48', '#408A71', '#B0E4CC', '#6AB89A', '#8ECDB2']
# #             )
# #             fig_pie.update_layout(
# #                 plot_bgcolor='rgba(0,0,0,0)',
# #                 paper_bgcolor='rgba(0,0,0,0)',
# #                 font=dict(family='Inter', size=12, color=COLORS['text_secondary']),
# #                 height=400
# #             )
# #             st.plotly_chart(fig_pie, use_container_width=True)
        
# #         with col2:
# #             # Margin vs Revenue
# #             if 'Profit Margin %' in df.columns:
# #                 fig_margin = px.scatter(
# #                     df,
# #                     x='Current Revenue (Cr)',
# #                     y='Profit Margin %',
# #                     size='Current Revenue (Cr)',
# #                     color='Company Name',
# #                     text='Company Name',
# #                     title='Margin vs Revenue',
# #                     color_discrete_sequence=['#091413', '#285A48', '#408A71', '#B0E4CC']
# #                 )
# #                 fig_margin.update_layout(
# #                     plot_bgcolor='rgba(0,0,0,0)',
# #                     paper_bgcolor='rgba(0,0,0,0)',
# #                     font=dict(family='Inter', size=12, color=COLORS['text_secondary']),
# #                     height=400,
# #                     showlegend=False
# #                 )
# #                 fig_margin.update_traces(textposition='top center')
# #                 st.plotly_chart(fig_margin, use_container_width=True)
        
# #         # Data table
# #         st.markdown('<p class="section-title">Complete Data</p>', unsafe_allow_html=True)
        
# #         display_cols = ['Company Name', 'Current Revenue (Cr)', 'Annual Revenue (Cr)', 
# #                        'Profit Margin %', 'Total TCV', 'Deal Wins', 'Total Clients', 'Service Categories']
        
# #         available_cols = [col for col in display_cols if col in df.columns]
# #         display_df = df[available_cols].copy()
        
# #         # Format columns
# #         for col in ['Current Revenue (Cr)', 'Annual Revenue (Cr)']:
# #             if col in display_df.columns:
# #                 display_df[col] = display_df[col].map(lambda x: f"₹{x:,.0f}" if pd.notna(x) else "N/A")
        
# #         if 'Profit Margin %' in display_df.columns:
# #             display_df['Profit Margin %'] = display_df['Profit Margin %'].map(lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A")
        
# #         if 'Total TCV' in display_df.columns:
# #             display_df['Total TCV'] = display_df['Total TCV'].map(lambda x: f"{x:,.0f}" if pd.notna(x) else "N/A")
        
# #         if 'Deal Wins' in display_df.columns:
# #             display_df['Deal Wins'] = display_df['Deal Wins'].map(lambda x: f"{x:,.0f}" if pd.notna(x) else "0")
        
# #         if 'Total Clients' in display_df.columns:
# #             display_df['Total Clients'] = display_df['Total Clients'].map(lambda x: f"{x:,.0f}" if pd.notna(x) else "N/A")
        
# #         display_df = display_df.rename(columns={
# #             'Company Name': 'Company',
# #             'Current Revenue (Cr)': 'Revenue',
# #             'Annual Revenue (Cr)': 'Annual',
# #             'Profit Margin %': 'Margin',
# #             'Total TCV': 'TCV',
# #             'Deal Wins': 'Deals',
# #             'Total Clients': 'Clients'
# #         })
        
# #         st.dataframe(
# #             display_df,
# #             use_container_width=True,
# #             hide_index=True,
# #             column_config={
# #                 "Company": st.column_config.TextColumn("Company", width="medium"),
# #                 "Revenue": st.column_config.TextColumn("Revenue", width="small"),
# #                 "Annual": st.column_config.TextColumn("Annual", width="small"),
# #                 "Margin": st.column_config.TextColumn("Margin", width="small"),
# #                 "TCV": st.column_config.TextColumn("TCV", width="small"),
# #                 "Deals": st.column_config.TextColumn("Deals", width="small"),
# #                 "Clients": st.column_config.TextColumn("Clients", width="small")
# #             }
# #         )

# # else:
# #     st.info("📂 No data found. Click 'Refresh Data' in the sidebar to run the pipeline and fetch the latest data.")

# # # Footer
# # st.markdown(f"""
# # <hr style="margin: 2rem 0 1rem 0; border-color: {COLORS['border']};">
# # <p style="font-family: Inter; font-size: 0.75rem; color: {COLORS['text_muted']}; text-align: center; letter-spacing: 0.03em;">
# #     Data sourced from Screener.in & Company Investor Relations | Updated: {datetime.now().strftime("%d %b %Y, %H:%M")}
# # </p>
# # """, unsafe_allow_html=True)

# # # Close dark mode div
# # if st.session_state.dark_mode:
# #     st.markdown('</div>', unsafe_allow_html=True)