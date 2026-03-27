import streamlit as st
import pandas as pd
import plotly.express as px
import os 

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide", page_icon="🛒")

@st.cache_data
def load_data():

    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, '..', 'data', 'clean_data.csv')
    
    df = pd.read_csv(csv_path, parse_dates=['InvoiceDate'])
    
    if 'YearMonth' not in df.columns:
        df['YearMonth'] = df['InvoiceDate'].dt.to_period('M').astype(str)
    return df

df = load_data()

st.sidebar.title("Filters")

min_date = df['InvoiceDate'].min()
max_date = df['InvoiceDate'].max()
date_range = st.sidebar.date_input("Date Range", [min_date, max_date])

countries = ["All"] + sorted(df['Country'].dropna().unique().tolist())
selected_Country = st.sidebar.selectbox("Country", countries)

if len(date_range) == 2:
    mask = (df['InvoiceDate'].dt.date >= date_range[0]) & (df['InvoiceDate'].dt.date <= date_range[1])
    
    if selected_Country != 'All':
        mask &= df['Country'] == selected_Country
    
    filtered = df[mask]
    
    st.title("🛒 E-Commerce Sales Intelligence Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    total_rev = filtered['Revenue'].sum()
    n_orders = filtered['InvoiceNo'].nunique()
    n_customers = filtered['CustomerID'].nunique()
    
    aov = total_rev / n_orders if n_orders != 0 else 0
    
    col1.metric("Total Revenue", f"${total_rev:,.0f}")
    col2.metric("Avg Order Value", f"${aov:,.2f}")
    col3.metric("Total Orders", f"{n_orders:,}")
    col4.metric("Unique Customers", f"{n_customers:,}")
    
    st.divider()
    
    if filtered.empty:
        st.warning("No data available for the selected filters.")
    else:
        tab1, tab2, tab3, tab4 = st.tabs([
            "📈 Sales Trends",
            "🏆 Top Products",
            "👥 Customer Insights",
            "🔮 Sales Forecast"
        ])
        
        with tab1:
            monthly = filtered.groupby('YearMonth')['Revenue'].sum().reset_index()
            fig = px.line(monthly, x='YearMonth', y='Revenue',
                          title='Monthly Revenue Trend',
                          markers=True)
            st.plotly_chart(fig, use_container_width=True)
            
            monthly['Growth %'] = monthly['Revenue'].pct_change() * 100
            st.dataframe(monthly.round(2), use_container_width=True)
            
        with tab2:
            top = filtered.groupby('Description')['Revenue'].sum().sort_values(ascending=False).head(10).reset_index()
            top = top.sort_values(by="Revenue", ascending=True) 
            fig2 = px.bar(top, x='Revenue', y='Description',
                          orientation='h', title='Top 10 Products by Revenue',
                          color='Revenue', color_continuous_scale='Blues')
            st.plotly_chart(fig2, use_container_width=True)
            
        with tab3:
            cust = filtered.groupby('CustomerID').agg(
                total_orders=('InvoiceNo', 'nunique'),
                total_spent=('Revenue', 'sum')
            ).reset_index()
            
            if cust.shape[0] > 0:
                repeat = (cust[cust['total_orders'] > 1].shape[0] / cust.shape[0]) * 100
            else:
                repeat = 0.0
                
            st.metric("Repeat Customer Rate", f"{repeat:.1f}%")
            
            fig3 = px.histogram(cust, x='total_orders',
                                title='Orders per Customer Distribution',
                                nbins=20)
            st.plotly_chart(fig3, use_container_width=True)
            
            top_cust = cust.sort_values('total_spent', ascending=False).head(10)
            st.subheader("Top 10 Customers by Spend")
            st.dataframe(top_cust.round(2), use_container_width=True)

        with tab4:
            st.subheader("90-Day Revenue Forecast")
            
           
            current_dir = os.path.dirname(os.path.abspath(__file__))
            
           
            plot_path = os.path.abspath(os.path.join(current_dir, '..', 'data', 'forecast_plot.png'))
            components_path = os.path.abspath(os.path.join(current_dir, '..', 'data', 'forecast_components.png'))

           
            try:
                st.image(plot_path, caption='Prophet Sales Forecast')
                
                st.divider()
                st.subheader("Forecast Components (Trends & Seasonality)")
                st.image(components_path, caption='Trend, Weekly, and Yearly Seasonality')
                
            except Exception as e:
                st.warning("Forecast images not found or couldn't be loaded.")
                st.info(f"Ensure your Prophet script ran successfully. Error details: {e}")
else:
    st.info("Please select both a start and end date to view the dashboard.")