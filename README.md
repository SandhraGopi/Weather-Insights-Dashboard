# Weather-Insights-Dashboard
Weather Insights Dashboard using Python and Power BI

#  Weather Insights Dashboard

An end-to-end weather analytics project with **Power BI visualization** and **Streamlit web deployment**.

## Project Overview
This project analyzes daily weather and air quality data from Cairo, Egypt (Jan–Mar 2025) to provide actionable insights through interactive dashboards.
- **Python** for data cleaning and transformation
- **Power BI** for interactive visual dashboard
- **Streamlit** for web deployment and real-time access

##  Tools & Technologies
- **Python** (Pandas, NumPy, Streamlit) – Data processing & web app
- **Power BI** – Dashboard visualization
- **Streamlit Cloud** – Web deployment
- **VS Code** – Development environment
- **GitHub** – Version control

##  Project Structure

project/
│
├── dashboard/
│ └── weather_insights_dashboard.pbix
│
├── Daily_Weather_Insights.csv
├── cleaned_weather_data.csv
├── weather_insights.ipynb
├── README.md
│
├── screenshots/
│ ├── Cleaned_Data.png
│ ├── Dashboard.png
│ ├── Dashboard_Interaction1.png
│ ├── Dashboard_Interaction2.png
│ ├── Data_Flow_Diagram.png
│ └── Data_Loading.png
│ └── Data_Transformation.png
├── screenshots_streamlit
│ ├── dash(1).png
│ ├── dash(2).png
│ ├── dash(3).png
│ ├── password.png
├── cleaned_weather_data.csv
├── dashboard.py
├── requirements.txt
├── weather_insights.ipynb

---


##  Data Flow
1. **Raw Data** → `Daily_Weather_Insights.csv` (Kaggle)
2. **Python Cleaning** → Data transformation & feature engineering
3. **Cleaned Data** → `cleaned_weather_data.csv`
4. **Power BI** → Interactive visual dashboard (local)
5. **Streamlit** → Web dashboard (deployed online)

##  Dashboard Features
### Power BI Dashboard
- Line chart showing temperature trends over time
- Bar charts for average temperature by month/condition
- KPI cards (Avg Temp, Max Temp, Avg AQI, Total Rainfall)
- Scatter plot (Rainfall vs Visibility)
- Interactive slicers (Month, Weather Condition, Temperature/AQI Categories)

### Streamlit Web Dashboard
- Real-time filtering via dropdowns and sliders
- Responsive design for desktop & mobile
- Live metrics and interactive charts
- Secure password-protected access

##  Deployment
**Live Dashboard:** [https://weather-insights-dashboard-msqijgvhidtsrbd7lpte8s.streamlit.app](https://weather-insights-dashboard-msqijgvhidtsrbd7lpte8s.streamlit.app)  
**Access Password:** `weather2025`

##  Screenshots
The `screenshots/` folder includes:
- Data flow diagram
- Cleaned data preview
- Power BI dashboard views
- Streamlit web interface
- Interactive filtering examples

##  Data Cleaning Steps (Python)
1. Checked dataset structure and statistics
2. Verified no missing values
3. Removed duplicate records
4. Converted Date column to datetime format
5. Created derived columns (Year, Month, Month Name, Temperature Category, AQI Category)
6. Exported cleaned data for Power BI & Streamlit usage

##  How to Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/SandhraGopi/Weather-Insights-Dashboard.git
   cd Weather-Insights-Dashboard

2. Install dependencies:
  pip install -r requirements.txt

3. Run Streamlit app:
   streamlit run dashboard.py

4. Open Power BI file (dashboard/weather_insights_dashboard.pbix) for local visualization

Dataset Source
Daily Weather Insights 2025 - Kaggle

 ## Key Insights
January showed the lowest average temperatures, increasing through March

Highest rainfall occurred in January, decreasing significantly by March

AQI remained mostly "Moderate" with occasional "Good" days

Higher rainfall days correlated with reduced visibility

## License
This project is for educational and portfolio purposes.

## Author
Sandhra Gopi
Aspiring Data Analyst
