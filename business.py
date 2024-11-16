import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def bike_sharing_business(data_path="bikes_data_viz.csv"):
    """
    Streamlit app for an interactive bike sharing optimization dashboard.
    
    Args:
        data_path (str): Path to the CSV file containing the bike sharing data.
    """

    # Load the data
    @st.cache_data
    def load_data(path):
        return pd.read_csv(path)

    data = load_data(data_path)

    # Define month names for display
    month_names = {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December"
    }
  
    # Business Page content
    html_temp = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">Business Strategy for Bike Sharing Optimization</h2>
    </div>"""

    st.markdown(html_temp, unsafe_allow_html=True)
  
    st.header("1. Charging and Redistribution Optimization")
    st.write("""
        - **Nighttime Charging in Warehouses**: Collect bikes at the end of each day and charge them overnight in a central warehouse.
        - **Early Morning Distribution**: Redistribute fully charged bikes across key locations by 7 AM to meet demand from morning commuters.
        - **Midday Redistribution**: Shift bikes to high-demand areas between 11 AM and 3 PM for evening rush hour demand.
        """)

        # Hourly Casual vs Registered bar chart
    hourly_data = data.groupby(['hr']).agg(total_casual=('casual', 'sum'), total_registered=('registered', 'sum')).reset_index()
    fig = go.Figure(data=[
        go.Bar(name='Casual', x=hourly_data['hr'], y=hourly_data['total_casual'], marker_color="darkred"),
        go.Bar(name='Registered', x=hourly_data['hr'], y=hourly_data['total_registered'], marker_color="tomato")
        ])
    fig.update_layout(barmode='stack', title="Hourly Total Count of Bikes Rented (Casual vs Registered)", xaxis_title="Hour", yaxis_title="Total Count of Bikes")
    st.plotly_chart(fig)

    st.header("2. Seasonal Fleet Adjustment")
    st.write("""
        - **Full Fleet (May - October)**: Increase the fleet size and frequency of redistribution during high-demand months.
        - **Average Fleet (November - December)**: Maintain a balanced fleet size during moderate usage months.
        - **Reduced Fleet (January- February)**: Deploy a minimal fleet to reduce costs during low-demand winter months.
        """)

    # Monthly Casual vs Registered Rentals
    monthly_data = data.groupby(['yr', 'mnth']).agg(total_casual=('casual', 'sum'), total_registered=('registered', 'sum')).reset_index()
    monthly_data['month_name'] = monthly_data['mnth'].map(month_names)
    fig = go.Figure(data=[
            go.Bar(name='Casual', x=monthly_data['month_name'], y=monthly_data['total_casual'], marker_color="darkred"),
            go.Bar(name='Registered', x=monthly_data['month_name'], y=monthly_data['total_registered'], marker_color="tomato")
        ])
    fig.update_layout(barmode='stack', title="Monthly Total Count of Bikes Rented (Casual vs Registered)", xaxis_title="Month", yaxis_title="Total Count of Bikes")
    st.plotly_chart(fig)

    st.header("3. Maintenance Scheduling")
    st.write("""
        - **On-the-Spot Maintenance:** Schedule repairs early in the morning or during non-rush hours in the afternoon.
        - **Yearly Maintenance and Repairs:** Perform major maintenance during low-utilization months (January and February).
        """)

    # Mapping the months to their names for the heatmap
    data['month_name'] = data['mnth'].map(month_names)
    data['month_name'] = pd.Categorical(data['month_name'], categories=list(month_names.values()), ordered=True)

    # Create a pivot table for the heatmap
    heatmap_data = data.pivot_table(values='cnt', index='hr', columns='month_name', aggfunc='sum')

    # Prepare data for Plotly interactive heatmap
    heatmap_data = heatmap_data.reset_index().melt(id_vars='hr', var_name='Month', value_name='Bike Demand')

    fig = go.Figure(data=go.Heatmap(
        x=heatmap_data['Month'],
        y=heatmap_data['hr'],
        z=heatmap_data['Bike Demand'],
        colorscale='RdYlGn_r',
        colorbar=dict(title="Bike Demand"),
        zmin=heatmap_data['Bike Demand'].min(),
        zmax=heatmap_data['Bike Demand'].max(),
        hoverongaps=False,
        text=heatmap_data['Bike Demand'],
        texttemplate="%{text}",
        textfont={"size": 10}
        ))

    fig.update_layout(
        title="Bike Demand by Hour and Month",
        xaxis_title="Month",
        yaxis_title="Hour of the Day",
        width=1200,
        height=800,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        )

    st.plotly_chart(fig)

    st.header("4. Demand-Based Pricing and User-Specific Adjustments")
    st.write("""
        - **Peak Hour Pricing**: Implement surge pricing during commuting hours (8-10 AM and 5-7 PM).
        - **Casual vs. Registered Users Pricing**:
            - **High Casual User Demand**: Increase rates during high casual activity periods.
            - **Incentives for Off-Peak Hours**: Offer discounts during low-demand times to boost utilization.
        """)

if __name__ == '__main__':
    bike_sharing_business()