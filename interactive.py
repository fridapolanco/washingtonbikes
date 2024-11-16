import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def bike_rental_dashboard(data_path="bikes_data_viz.csv"):
    # Load the data
    @st.cache_data
    def load_data():
        return pd.read_csv(data_path)

    data = load_data()
    
    # Title and description
    html_temp = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">Interactive Bike Rental Dashboard</h2>
    </div>"""

    st.markdown(html_temp, unsafe_allow_html=True)

    st.markdown("Explore bike rental data with interactive visualizations for each column, including total counts, averages, occupancy rates, and more.")
    
    # Data preprocessing
    year_mapping = {0: "2011", 1: "2012"}
    data['yr'] = data['yr'].map(year_mapping)
    data['holiday'] = data['holiday'].replace({0: "No", 1: "Yes"})
    data['workingday'] = data['workingday'].replace({0: "No", 1: "Yes"})
    
    # Year Filter
    year_selection = st.selectbox("Select Year", ["All Years"] + sorted(data['yr'].unique()), index=0)
    if year_selection != "All Years":
        data = data[data['yr'] == year_selection]
    
    # Mapping dictionaries for readable axis labels
    season_names = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
    month_names = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
    
    # Yearly Casual vs Registered
    col1, col2 = st.columns(2)
    with col1:
        yearly_data = data.groupby(['yr']).agg(total_casual=('casual', 'sum'), total_registered=('registered', 'sum')).reset_index()
        fig = go.Figure(data=[
            go.Bar(name='Casual', x=yearly_data['yr'], y=yearly_data['total_casual'], marker_color="darkred"),
            go.Bar(name='Registered', x=yearly_data['yr'], y=yearly_data['total_registered'], marker_color="tomato")
        ])
        fig.update_layout(barmode='stack', title="Yearly Total Count of Bikes Rented (Casual vs Registered)", xaxis_title="Year", yaxis_title="Total Count of Bikes")
        st.plotly_chart(fig)
        st.markdown("**Yearly Total Count of Bikes Rented (Casual vs Registered):** This stacked bar chart shows yearly rentals, separated by casual and registered users, indicating user type trends.")
    with col2:
        seasonal_data = data.groupby(['season']).agg(total_casual=('casual', 'sum'), total_registered=('registered', 'sum')).reset_index()
        seasonal_data['season_name'] = seasonal_data['season'].map(season_names)
        fig = go.Figure(data=[
            go.Bar(name='Casual', x=seasonal_data['season_name'], y=seasonal_data['total_casual'], marker_color="darkred"),
            go.Bar(name='Registered', x=seasonal_data['season_name'], y=seasonal_data['total_registered'], marker_color="tomato")
        ])
        fig.update_layout(barmode='stack', title="Seasonal Total Count of Bikes Rented (Casual vs Registered)", xaxis_title="Season", yaxis_title="Total Count of Bikes")
        st.plotly_chart(fig)
        st.markdown("**Seasonal Total Count of Bikes Rented (Casual vs Registered):** Seasonal rental counts split by casual and registered users, showing seasonal usage patterns.")
    
    # Monthly Casual vs Registered Rentals
    col1, col2 = st.columns(2)
    with col1:
        monthly_data = data.groupby(['yr', 'mnth']).agg(total_casual=('casual', 'sum'), total_registered=('registered', 'sum')).reset_index()
        monthly_data['month_name'] = monthly_data['mnth'].map(month_names)
        fig = go.Figure(data=[
            go.Bar(name='Casual', x=monthly_data['month_name'], y=monthly_data['total_casual'], marker_color="darkred"),
            go.Bar(name='Registered', x=monthly_data['month_name'], y=monthly_data['total_registered'], marker_color="tomato")
        ])
        fig.update_layout(barmode='stack', title="Monthly Total Count of Bikes Rented (Casual vs Registered)", xaxis_title="Month", yaxis_title="Total Count of Bikes")
        st.plotly_chart(fig)
        st.markdown("**Monthly Total Count of Bikes Rented (Casual vs Registered):** Monthly rentals split by casual and registered users, indicating monthly demand trends.")
    with col2:
        daily_data = data.groupby(['weekday']).agg(total_casual=('casual', 'sum'), total_registered=('registered', 'sum')).reset_index()
        fig = go.Figure(data=[
            go.Bar(name='Casual', x=daily_data['weekday'], y=daily_data['total_casual'], marker_color="darkred"),
            go.Bar(name='Registered', x=daily_data['weekday'], y=daily_data['total_registered'], marker_color="tomato")
        ])
        fig.update_layout(barmode='stack', title="Daily Total Count of Bikes Rented (Casual vs Registered)", xaxis_title="Day of Week", yaxis_title="Total Count of Bikes")
        st.plotly_chart(fig)
        st.markdown("**Daily Total Count of Bikes Rented (Casual vs Registered):** Daily rental counts separated by casual and registered users, showing demand across the week.")
    
    # Hourly Rentals by Season
    hour_data = data.groupby(['hr', 'season']).agg(total_bikes=('cnt', 'sum'), avg_bikes=('cnt', 'mean')).reset_index()
    hour_data['season'] = hour_data['season'].map(season_names)
    fig = px.line(hour_data, x='hr', y='total_bikes', color='season', title="Total Bikes Rented per Hour with Season Split",
                  labels={'hr': 'Hour of Day', 'total_bikes': 'Total Bikes'}, color_discrete_sequence=["firebrick", "tomato", "salmon", "darkred"])
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
    st.plotly_chart(fig)
    st.markdown("**Total bikes rented per hour**, with different lines for each season. The x-axis represents the hour of the day.")
    
    # Additional Visualizations 
    col1, col2 = st.columns(2)
    with col1:
        workingday_avg = data.groupby('workingday').agg(avg_bikes=('cnt', 'mean')).reset_index()
        fig = px.bar(workingday_avg, x="workingday", y="avg_bikes", title="Average Bikes Rented on Working Days vs Non-Working Days",
                     labels={'workingday': 'Working Day', 'avg_bikes': 'Average Bikes'})
        fig.update_traces(marker_color="tomato")
        st.plotly_chart(fig)
        st.markdown("**Average Bikes Rented on Working Days vs Non-Working Days:** Average bike rentals on working vs. non-working days.")
    with col2:
        holiday_avg = data.groupby('holiday').agg(avg_bikes=('cnt', 'mean')).reset_index()
        fig = px.bar(holiday_avg, x="holiday", y="avg_bikes", title="Average Bikes Rented on Holidays vs Non-Holidays",
                     labels={'holiday': 'Holiday', 'avg_bikes': 'Average Bikes'})
        fig.update_traces(marker_color="tomato")
        st.plotly_chart(fig)
        st.markdown("**Average Bikes Rented on Holidays vs Non-Holidays:** This chart shows the average rentals on holidays vs. regular days.")

    # Average Counts for Humidity and Weather Situation
    col1, col2 = st.columns(2)
    with col1:
        humidity_avg = data.groupby('Hum').agg(avg_bikes=('cnt', 'mean')).reset_index()
        fig = px.bar(humidity_avg, x="Hum", y="avg_bikes", title="Average Bikes Rented by Humidity Level", labels={'Hum': 'Humidity', 'avg_bikes': 'Average Bikes'})
        fig.update_traces(marker_color="tomato")
        st.plotly_chart(fig)
        st.markdown("*Average Bikes Rented by Humidity Level:* Average bike rentals across humidity levels.")

    with col2:
        weathersit_avg = data.groupby('weathersit').agg(avg_bikes=('cnt', 'mean')).reset_index()
        fig = px.bar(weathersit_avg, x="weathersit", y="avg_bikes", title="Average Bikes Rented by Weather Situation", labels={'weathersit': 'Weather Situation', 'avg_bikes': 'Average Bikes'})
        fig.update_traces(marker_color="tomato")
        st.plotly_chart(fig)
        st.markdown("*Average Bikes Rented by Weather Situation:* Average rentals across different weather situations.")

    data["season"] = data["season"].astype(str)
    # Temperature Scatter Plot
    fig = px.scatter(data, x="temp", y="cnt", color="season", title="Temperature vs Total Bikes Rented by Season",
                     labels={'temp': 'Temperature', 'cnt': 'Total Bikes'}, color_discrete_sequence=["darkred", "tomato", "red", "salmon"])
    fig.update_traces(marker=dict(size=5))
    st.plotly_chart(fig)
    st.markdown("**Temperature vs Total Bikes Rented by Season:** This scatter plot shows the relationship between temperature and bike rentals, split by season, illustrating how warmer weather influences bike demand.")

if __name__ == '__main__':
    bike_rental_dashboard()