import streamlit as st
import pandas as pd

# Set page configuration
#st.set_page_config(page_title="Bike Sharing Analysis in Washington DC", layout="wide", page_icon="🚲")

# Sidebar navigation
# side_bar = st.sidebar
# side_bar.header("Bike Sharing WebApp Navigation")
# side_bar.caption("Please select which section of the dashboard you want to visualize")

# radio = side_bar.radio(
#     'Sections',
#     ['Main Page', 'Data Visualization', 'Feature Engineering', 'Bike Prediction', 'Business Insights'],
#     index=0)

# Define main function for feature engineering
def main_feature_engineering():
    html_temp = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">Model Workflow</h2>
    </div>"""
    
    st.markdown(html_temp, unsafe_allow_html=True)

    st.header("🗂️Original Dataset")
    st.markdown('''
    Below, we can see a snapshot of the orginal dataframe we recieved and the columns it included. The information given can be found below. ''')

    with st.expander('Expand to see all feature details'):
       st.write('''
    - `instant`: record index
    - `dteday` : date
    - `season` : season (1:spring, 2:summer, 3:fall, 4:winter)
    - `yr` : year (0: 2011, 1:2012)
    - `mnth` : month ( 1 to 12)
    - `hr` : hour (0 to 23)
    - `holiday` : weather day is holiday or not (extracted from http://dchr.dc.gov/page/holiday-schedule)
    - `weekday` : day of the week
    - `workingday` : if day is neither weekend nor holiday is 1, otherwise is 0.
    + `weathersit` : 
      - 1: Clear, Few clouds, Partly cloudy, Partly cloudy
      - 2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist
      - 3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds
      - 4: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog
    - `temp` : Normalized temperature in Celsius. The values are divided to 41 (max)
    - `atemp`: Normalized feeling temperature in Celsius. The values are divided to 50 (max)
    - `hum`: Normalized humidity. The values are divided to 100 (max)
    - `windspeed`: Normalized wind speed. The values are divided to 67 (max)
    - `casual`: count of casual users
    - `registered`: count of registered users
    - `cnt`: count of total rental bikes including both casual and registered      
               ''' )
       
    with st.expander('Snapshot of our original DataFrame'):
        og_df = pd.read_csv("hour.csv")
        head = og_df.head()
        st.dataframe(data=head)

    st.header("🗂️Feature engineering")
    st.markdown('''Below a summary of decisions made to clean and prepare our data for modelling. ''')
    
    st.subheader("Dropping Unnecessary Columns")
    st.markdown('''
    - The `instant` column, which is just a unique identifier for each record and doesn’t add predictive value, is removed to streamline the dataset.
    ''')
    
    st.subheader("Correcting season")
    st.markdown('''
    - The `season` column was incongruent with the column `month` and the labels given in the documentation for seasons. So, this column was updated to match the month's season. 
                 ''')
    
    st.subheader("Creating Ratio Features")
    st.markdown('''
    - The features `ratio_casual` and `ratio_registered` are created to show the proportion of casual and registered users relative to the total bike rentals (`cnt`). These features offer several insights:
      - **User Type Insights**: These ratios reveal the mix of casual versus registered users in each record. Casual users likely represent occasional rentals, such as by tourists, while registered users might indicate regular commuters. This differentiation helps in understanding various user behaviors.
      - **Demand Patterns**: The ratios help analyze how factors like time of day, day of the week, or weather conditions affect each user group differently. For example, casual rentals might increase on weekends or in good weather, while registered users may maintain more consistent usage.
      - **Predictive Power**: Adding these ratios enhances the model by capturing demand composition. Rather than treating casual and registered counts separately, the ratios provide a structured view of their contributions to total demand (`cnt`), potentially boosting model accuracy in predicting total rentals.
    ''')

    st.subheader("Different DataFrames: `data` vs `df`")
    st.markdown('''
    - From our input data we will create two different dataframes. They'll both include the same columns after our cleaning and data modelling; however, `data` will be used purely for visualization purposes. Whereas `df`will be used to train the model. Both dfs are indexed by date and hour. 
    ''')
    
    st.subheader("Date-Time Features")
    st.markdown('''
    - The `dteday` column is converted to datetime format to standardize date representation, enabling easy extraction of additional time-based features like day of the week or month.
    - A new index for our DataFrame `data`is created by combining `dteday` (date) and `hr` (hour) into a single hourly timestamp. This index  reflects each observation’s exact hour and provides a continuous, time-structured feature that enhances temporal analysis, allowing the model to capture patterns based on specific hours, days, or longer cycles. This structure supports chronological ordering, facilitating time-based operations such as resampling or lagging.
      - **Sort Data by Index (`date`)**: Sorting the data by the `date` index ensures records are in chronological order, which is critical for time-series modeling and prevents any misalignment of records when analyzing or visualizing temporal trends.
    ''')
    
    st.subheader("Removing Duplicates")
    st.markdown('''
    - Duplicate entries are identified in the dataset, counted, and then removed to ensure data integrity.
    ''')
    
    st.subheader("Binning Time of Day as a Feature")
    st.markdown('''
    - The `hr` (hour) column is transformed into a new categorical feature, `TOD` (Time of Day), by grouping hours into four bins: Morning, Afternoon, Evening, and Night as it is more user-friendly.
      - **Binning Function**:
        - Morning: 6 AM - 12 PM
        - Afternoon: 12 PM - 5 PM
        - Evening: 5 PM - 9 PM
        - Night: 9 PM - 6 AM
      - By creating `TOD`, we add context to each record regarding daily activity patterns, such as commuting times (Morning, Evening) or leisure periods (Afternoon, Night). This simplifies analysis by capturing time-of-day effects, which can be more meaningful for identifying patterns than the exact hour.
    ''')
    
    st.subheader("Binning Rush Hours as a Feature")
    st.markdown('''
    - The `hr` (hour) column is transformed into a new categorical feature, `Rush`, by grouping hours into two categories: Rush and Not Rush.
      - **Binning Function**:
        - Rush: 7 AM - 9 AM and 5 PM - 7 PM
        - Not Rush: All other hours
      - By creating the `Rush` feature, we add context to each record regarding peak traffic times, such as morning and evening commuting hours. This allows the model to capture demand patterns linked to higher activity periods, as rush hours are likely to have different demand levels compared to non-rush times.
    ''')
    
    st.subheader("Binning Wind Speed as a Feature")
    st.markdown('''
    - The `windspeed` column is transformed into a new categorical feature, `Wind`, by grouping wind speeds into three categories: Low, Medium, and High.
      - **Binning Function**:
        - Low: Wind speed less than 10
        - Medium: Wind speed between 10 and 20
        - High: Wind speed above 20
      - By creating the `Wind` feature, we add context to each record about weather conditions, which can influence user behavior and demand. For example, higher wind speeds might reduce bike rentals, while lower speeds may have a minimal effect. This categorization simplifies the analysis by capturing the impact of different wind conditions on bike usage.
    ''')

    st.subheader("Binning Humidity as a Feature")
    st.markdown('''
    - The `hum` column is transformed into a new categorical feature, `Hum`, by grouping humidity into three categories: Low, Medium, and High.
      - **Binning Function**:
        - Low: humidity level less than .3
        - Medium: humidity level between .31 and .6
        - High: humidity level above .6
      - By creating the `Hum` feature, we add context to each record about weather conditions, which can influence user behavior and demand. Additionally, this makes it easier for our user to identify the humidity level for our predicting app. 
    ''')
    
    st.subheader("Creating Lagged Counts")
    st.markdown('''
    - A new feature, `prev_count`, is created to capture the bike rental count from the previous hour, providing a lagged value for `cnt`.
    - The `shift` function moves each count down by one row, so each row’s `prev_count` shows the rental count from the previous time period.
      - **Dropping Missing Values**: Since the first row in `prev_count` will be `NaN` (no prior hour data for the first entry), rows with missing values are removed.
      - By creating `prev_count`, we allow the model to recognize patterns influenced by the previous hour’s activity, which is often useful in time-series forecasting. For example, a high count in the previous hour may indicate sustained demand, helping the model predict demand continuity or fluctuation more effectively.
    ''')

    with st.expander('Snapshot of our transformed DataFrame'):
      clean_df = pd.read_csv("bikes_clean_data.csv")
      head2 = clean_df.head()
      st.dataframe(data=head2)

    st.header("🗂️PyCaret Insights & Model build Up")
    st.markdown('''Below a walkthrough of Pycaret set up. ''')

    with st.expander('Snapshot of our Pycaret Set Up'):
      st.image("media\\pycaret.png")
    
    st.markdown('''
                Our ML framework was designed to be intuitive and graspable. Our core approach involved using PyCarret to analyze a variety of various regression models, ranging from tree based regressors to classic linear regression. 

To set up our experiment, we chose a variety of variables including things like wind speed, temperature, day of week, hour and month. Practically all variables were categorical (e.g. Day of Week, Rush Hour, Hour, etc.), and the numerical variables surrounding wind speed were binned into categorical variables as well. PyCarret automatically one-hot-encodes these variables, so we tried to use them for non-ordinal variables.

A notable exception is the weathersit variable, which though categorical has a clear ordinality in the various classes. This was kept numerical to preserve the information of order.

As far as notable settings go, our data was a time series, and thus our cross validation approach reflected as much. Furthermore, we added a metric to tune our model we call “Weighted R2”, a metric that punishes under-prediction more than over-correction. This comes from the business logic that having too many bikes is a smaller issue than having too few.
                ''')

    
if __name__ == '__main__':
    main_feature_engineering()
