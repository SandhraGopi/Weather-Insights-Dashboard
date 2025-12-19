# dashboard.py - EXACT Power BI Replica Dashboard
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Weather Insights Dashboard - Cairo",
    page_icon="🌤️",
    layout="wide"
)

# --- PASSWORD PROTECTION ---
def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False
    
    if "password_correct" not in st.session_state:
        st.text_input("Enter Dashboard Password", type="password", 
                     on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Enter Dashboard Password", type="password", 
                     on_change=password_entered, key="password")
        st.error("😕 Password incorrect")
        return False
    else:
        return True

# --- LOAD YOUR CLEANED DATA ---
@st.cache_data
def load_data():
    # Load YOUR cleaned CSV file
    df = pd.read_csv('cleaned_weather_data.csv')
    
    # Convert date column if needed
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
    
    # Create display names for categories to match Power BI
    df['Temp_Category_Display'] = df['Temp_Category'].replace({
        'Cold': 'Cold (<15°C)',
        'Mild': 'Mild (15-25°C)', 
        'Warm': 'Warm (25-30°C)',
        'Hot': 'Hot (>30°C)'
    })
    
    df['AQI_Category_Display'] = df['AQI_Category'].replace({
        'Good': 'Good (0-50)',
        'Moderate': 'Moderate (51-100)',
        'Poor': 'Poor (101-150)',
        'Unhealthy': 'Unhealthy (151-200)',
        'Very Unhealthy': 'Very Unhealthy (>200)'
    })
    
    return df

# --- MAIN APP ---
if not check_password():
    st.stop()

# Load data
df = load_data()

# --- DASHBOARD HEADER (Matches Power BI) ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("<h1 style='text-align: center;'>WEATHER INSIGHTS DASHBOARD</h1>", 
                unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: gray;'>Cairo, Egypt (Jan-Mar 2025)</h3>", 
                unsafe_allow_html=True)

st.markdown("---")

# --- SIDEBAR FILTERS (Matches Power BI Filters) ---
st.sidebar.header("🔍 Filters")

# Month filter
available_months = df['Month_Name'].unique()
months = st.sidebar.multiselect(
    "Select Month(s):",
    options=available_months,
    default=available_months
)

# Temperature Category filter
temp_categories = st.sidebar.multiselect(
    "Temperature Category:",
    options=df['Temp_Category'].unique(),
    default=df['Temp_Category'].unique()
)

# Weather Condition filter
conditions = st.sidebar.multiselect(
    "Weather Condition:",
    options=df['Weather_Condition'].unique(),
    default=df['Weather_Condition'].unique()
)

# AQI Category filter
aqi_categories = st.sidebar.multiselect(
    "AQI Category:",
    options=df['AQI_Category'].unique(),
    default=df['AQI_Category'].unique()
)

# Apply all filters
filtered_df = df[
    (df['Month_Name'].isin(months)) &
    (df['Temp_Category'].isin(temp_categories)) &
    (df['Weather_Condition'].isin(conditions)) &
    (df['AQI_Category'].isin(aqi_categories))
]

# --- KEY METRICS ROW (Top Metrics from Power BI) ---
st.markdown("### 📊 Key Weather Metrics")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="Avg Temperature (°C)",
        value=f"{filtered_df['Temp_High_C'].mean():.2f}",
        delta=f"Range: {filtered_df['Temp_High_C'].min():.1f}-{filtered_df['Temp_High_C'].max():.1f}°C"
    )

with col2:
    st.metric(
        label="Avg Humidity (%)",
        value=f"{filtered_df['Humidity_Perc'].mean():.1f}",
        delta=f"Range: {filtered_df['Humidity_Perc'].min():.0f}-{filtered_df['Humidity_Perc'].max():.0f}%"
    )

with col3:
    st.metric(
        label="Avg Air Quality Index",
        value=f"{filtered_df['Air_Quality_Index'].mean():.1f}",
        delta=f"Range: {filtered_df['Air_Quality_Index'].min():.0f}-{filtered_df['Air_Quality_Index'].max():.0f}"
    )

with col4:
    st.metric(
        label="Max Temperature (°C)",
        value=f"{filtered_df['Temp_High_C'].max():.1f}",
        delta=f"Min: {filtered_df['Temp_High_C'].min():.1f}°C"
    )

with col5:
    st.metric(
        label="Total Rainfall (mm)",
        value=f"{filtered_df['Precipitation_mm'].sum():.1f}",
        delta=f"Avg: {filtered_df['Precipitation_mm'].mean():.1f} mm/day"
    )

st.markdown("---")

# --- VISUALIZATION ROW 1 (Matches Power BI Layout) ---
st.markdown("### 📈 Temperature Analysis")

col1, col2 = st.columns(2)

# Chart 1: Daily High Temperature Trend (Line Chart)
with col1:
    st.markdown("**Daily High Temperature Trend**")
    fig_temp_trend = px.line(
        filtered_df, 
        x='Date', 
        y='Temp_High_C',
        title='',
        labels={'Temp_High_C': 'Temperature (°C)', 'Date': 'Date'}
    )
    fig_temp_trend.update_layout(
        height=400,
        xaxis_title="Date",
        yaxis_title="High Temperature (°C)",
        showlegend=False
    )
    st.plotly_chart(fig_temp_trend, use_container_width=True)

# Chart 2: Average High Temperature by Month (Bar Chart)
with col2:
    st.markdown("**Average High Temperature by Month**")
    monthly_avg = filtered_df.groupby('Month_Name').agg({'Temp_High_C': 'mean'}).reset_index()
    # Order months correctly
    month_order = ['January', 'February', 'March']
    monthly_avg['Month_Name'] = pd.Categorical(monthly_avg['Month_Name'], categories=month_order, ordered=True)
    monthly_avg = monthly_avg.sort_values('Month_Name')
    
    fig_monthly_temp = px.bar(
        monthly_avg,
        x='Month_Name',
        y='Temp_High_C',
        title='',
        labels={'Temp_High_C': 'Avg Temperature (°C)', 'Month_Name': 'Month'},
        color='Temp_High_C',
        color_continuous_scale='RdYlBu_r'
    )
    fig_monthly_temp.update_layout(
        height=400,
        xaxis_title="Month",
        yaxis_title="Average High Temperature (°C)",
        showlegend=False
    )
    st.plotly_chart(fig_monthly_temp, use_container_width=True)

# --- VISUALIZATION ROW 2 ---
col1, col2 = st.columns(2)

# Chart 3: Average High Temperature by Weather Condition
with col1:
    st.markdown("**Average High Temperature by Weather Condition**")
    weather_avg = filtered_df.groupby('Weather_Condition').agg({'Temp_High_C': 'mean'}).reset_index()
    
    fig_weather_temp = px.bar(
        weather_avg,
        x='Weather_Condition',
        y='Temp_High_C',
        title='',
        labels={'Temp_High_C': 'Avg Temperature (°C)', 'Weather_Condition': 'Weather Condition'},
        color='Temp_High_C',
        color_continuous_scale='Viridis'
    )
    fig_weather_temp.update_layout(
        height=400,
        xaxis_title="Weather Condition",
        yaxis_title="Average High Temperature (°C)",
        showlegend=False
    )
    st.plotly_chart(fig_weather_temp, use_container_width=True)

# Chart 4: Rainfall vs Visibility Relationship
with col2:
    st.markdown("**Rainfall vs Visibility Relationship in Cairo**")
    fig_rain_vis = px.scatter(
        filtered_df,
        x='Precipitation_mm',
        y='Visibility_km',
        title='',
        labels={'Precipitation_mm': 'Rainfall (mm)', 'Visibility_km': 'Visibility (km)'},
        color='Weather_Condition',
        size='Temp_High_C',
        hover_data=['Date', 'Temp_High_C']
    )
    fig_rain_vis.update_layout(
        height=400,
        xaxis_title="Rainfall (mm)",
        yaxis_title="Visibility (km)"
    )
    st.plotly_chart(fig_rain_vis, use_container_width=True)

# --- VISUALIZATION ROW 3 ---
st.markdown("### 🌫️ Air Quality Analysis")
col1, col2 = st.columns(2)

# Chart 5: Air Quality Distribution
with col1:
    st.markdown("**Air Quality Distribution in Cairo**")
    aqi_dist = filtered_df['AQI_Category'].value_counts().reset_index()
    aqi_dist.columns = ['AQI_Category', 'Count']
    
    fig_aqi_dist = px.pie(
        aqi_dist,
        values='Count',
        names='AQI_Category',
        title='',
        hole=0.4,
        color='AQI_Category',
        color_discrete_map={
            'Good': '#00FF00',
            'Moderate': '#FFFF00',
            'Poor': '#FFA500',
            'Unhealthy': '#FF0000',
            'Very Unhealthy': '#8B0000'
        }
    )
    fig_aqi_dist.update_layout(
        height=400,
        showlegend=True
    )
    fig_aqi_dist.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_aqi_dist, use_container_width=True)

# Chart 6: Weather Condition Distribution
with col2:
    st.markdown("**Weather Condition Distribution in Cairo**")
    weather_dist = filtered_df['Weather_Condition'].value_counts().reset_index()
    weather_dist.columns = ['Weather_Condition', 'Count']
    
    fig_weather_dist = px.bar(
        weather_dist,
        x='Weather_Condition',
        y='Count',
        title='',
        labels={'Count': 'Number of Days', 'Weather_Condition': 'Weather Condition'},
        color='Weather_Condition',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_weather_dist.update_layout(
        height=400,
        xaxis_title="Weather Condition",
        yaxis_title="Number of Days",
        showlegend=False
    )
    st.plotly_chart(fig_weather_dist, use_container_width=True)

# --- DATA TABLE SECTION ---
st.markdown("---")
with st.expander("📋 View Filtered Data Table", expanded=False):
    # Select only the main columns for display
    display_cols = ['Date', 'Temp_High_C', 'Temp_Low_C', 'Humidity_Perc', 
                   'Weather_Condition', 'Air_Quality_Index', 'Precipitation_mm', 
                   'Visibility_km', 'Temp_Category', 'AQI_Category']
    
    display_df = filtered_df[display_cols].copy()
    display_df.columns = ['Date', 'High Temp (°C)', 'Low Temp (°C)', 'Humidity (%)',
                         'Weather Condition', 'AQI', 'Precipitation (mm)', 
                         'Visibility (km)', 'Temp Category', 'AQI Category']
    
    st.dataframe(display_df, use_container_width=True)
    
    # Show data summary
    st.markdown(f"**Showing {len(filtered_df)} of {len(df)} total records**")

# --- DOWNLOAD SECTION (Using YOUR cleaned file) ---
st.sidebar.markdown("---")
st.sidebar.header("📥 Data Export")

# Option 1: Download filtered data
st.sidebar.subheader("Download Filtered Data")
csv = filtered_df.to_csv(index=False)
b64 = base64.b64encode(csv.encode()).decode()
href = f'<a href="data:file/csv;base64,{b64}" download="filtered_weather_data.csv">Download Filtered CSV</a>'
st.sidebar.markdown(href, unsafe_allow_html=True)

# Option 2: Download original cleaned data (YOUR file)
st.sidebar.subheader("Download Full Dataset")
with open('cleaned_weather_data.csv', 'r') as file:
    full_csv = file.read()
full_b64 = base64.b64encode(full_csv.encode()).decode()
href_full = f'<a href="data:file/csv;base64,{full_b64}" download="cleaned_weather_data_full.csv">Download Full Cleaned CSV</a>'
st.sidebar.markdown(href_full, unsafe_allow_html=True)

# --- DEPLOYMENT INFO ---
st.sidebar.markdown("---")
st.sidebar.info("**Dashboard Details**\n"
               "- Data: Cairo Weather (Jan-Mar 2025)\n"
               "- Source: Open Weather Data\n"
               "- Charts: Replicates Power BI Design\n"
               "- Access: Password Protected\n"
               "- Filters: Interactive Multi-Select")

# --- FOOTER ---
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    <p>Weather Insights Dashboard | Cairo, Egypt 2025 | Interactive Power BI Replica</p>
    <p>Data Source: Open Weather Data | Dashboard built with Streamlit & Plotly</p>
    </div>
    """,
    unsafe_allow_html=True
)