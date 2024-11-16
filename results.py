import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pycaret.classification import *

def main_results(data_path="bikes_clean_data.csv"):
    html_temp = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">Model Results</h2>
    </div>"""

    st.markdown(html_temp, unsafe_allow_html=True)

    st.markdown('''
    As mentioned in our technical annex, we added a metric to tune our model we call “Weighted R2”. This metric punishes under-prediction more than over-correction. This comes from the business logic that having too many bikes is a smaller issue than having too few.
    After fine tuning our model to the previously mentioned metric we have the below results. 
    ''')

    col1, col2 = st.columns([2, 5])

    with col1:
        results_df = pd.DataFrame({
            "Fold": [0, 1, 2, 3, 4, "Mean", "STDV"],
            "MAE": [60.07, 29.88, 43.06, 62.77, 97.3, 58.62, 22.73],
            "MSE": [7540.55, 2565.43, 3993.99, 8120.92, 17779.07, 7999.9, 5318.62],
            "RMSE": [86.84, 50.65, 63.20, 90.12, 133.34, 84.33, 28.36],
            "R2": [0.63, 0.89, 0.79, 0.46, 0.59, 0.67, 0.14],
            "RMSLE": [0.76, 0.45, 0.54, 0.81, 0.73, 0.66, 0.14],
            "MAPE": [1.08, 0.41, 0.49, 0.82, 0.65, 0.69, 0.24]
        })
        st.dataframe(results_df, hide_index=True)

    with col2:
        st.markdown('''
        Some insights found with our metrics are: 
        - Our R^2 value approximates 0.7 (0.6665,0.7259), which indicates that **we capture roughly 70% of the variance of the data via the independent variables**. 
        - Our weighted R^2 approximates 0.2695, but we cannot say that the value is not 0 with a 95% confidence level. Indicating it is possible our model entirely under predicts, and thus the attempt to train the model to incur errors via overpredicting alone was not achieved. 
        - A simple solution would be to simply add a bias (X% of the rolling count, for example) which could shift the predictions upwards. However, this would reduce the overall accuracy of the model and thus was not attempted.                
        - MAE: on average our model predicts +/- 58 bikes
        - RMSE: on average our model predicts +/- 84 bikes
        ''')

#GRAPH1
    st.subheader("Predicted vs Unpredicted values")

    def load_data():
        return pd.read_csv(data_path)

    df = load_data()
    df.index = pd.to_datetime(df.index, unit='h')

    model = load_model(model_name='my_second_bike_model')
    final_model = model

    X = df.drop("cnt", axis=1)
    y = df.cnt

    y.index = pd.to_datetime(y.index, unit='h')


    X_train = X.iloc[:13901, :]  # 80%
    X_test = X.iloc[-3476:, :]  # 20%
    y_train = y.iloc[:13901]  # 80%
    y_test = y.iloc[-3476:]  # 20%

    # Predictions
    y_pred = model.predict(X_test.drop(columns=["hum", "prev_count", "windspeed", "yr", "atemp"]))

    # Sort data by index to ensure continuity in the line
    y_test = y_test.sort_index()
    y_pred = pd.Series(y_pred, index=y_test.index).sort_index()

    # Weekly resampling
    y_test_weekly = y_test.resample('W').sum()
    y_pred_weekly = y_pred.resample('W').sum()

    # Plotting actual vs. predicted values
    plt.figure(figsize=(14, 7))

    # Plot actual values as a solid line
    plt.plot(y_test_weekly.index, y_test_weekly, 'ro', label='Actual', color='red', linewidth=1.5)
    # Plot predicted values as a solid line
    plt.plot(y_test_weekly.index, y_pred_weekly, 'bo', label='Predicted', color='grey', linewidth=1.5)

    # Adding labels and title
    plt.xlabel('Date')
    plt.ylabel('Target')
    plt.title('Time Series: Actual vs Predicted')
    plt.legend()

    # Use Streamlit to display the plot
    st.pyplot(plt)

#GRAPH 2 
    st.subheader("Predicted and actual values, aggregated to daily sums")


    # Ensure that y_test and y_pred are sorted by index for continuity in the line
    y_test = y_test.sort_index()
    y_pred = pd.Series(y_pred, index=y_test.index).sort_index()

    # Resampling to daily frequency for smoother visualization (can change to 'W' for weekly)
    y_test_daily = y_test.resample('D').sum()  # Daily resampling
    y_pred_daily = y_pred.resample('D').sum()

    # Plotting actual vs predicted daily counts
    plt.figure(figsize=(12, 6))

    # Plot actual values
    plt.plot(y_test_daily.index, y_test_daily, label='Actual', color='blue', marker='o', linewidth=2)

    # Plot predicted values
    plt.plot(y_pred_daily.index, y_pred_daily, label='Predicted', color='orange', marker='o', linewidth=2)

    # Adding labels, title, and legend
    plt.title('Daily Bike Rentals: Actual vs Predicted', fontsize=14)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Daily Bike Rentals', fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(alpha=0.3)

    # Highlight overprediction and underprediction
    plt.fill_between(
        y_test_daily.index,
        y_test_daily,
        y_pred_daily,
        where=y_pred_daily > y_test_daily,
        color='gray',
        alpha=0.3,
        label='Overprediction'
    )

    plt.fill_between(
        y_test_daily.index,
        y_test_daily,
        y_pred_daily,
        where=y_pred_daily <= y_test_daily,
        color='red',
        alpha=0.3,
        label='Underprediction'
    )

    # Display the plot in Streamlit
    st.pyplot(plt)

#GRAPH 3
    st.subheader("Predicted and actual values, aggregated to hourly sums")

    hours_range = 50

    plt.figure(figsize=(12, 6))

    # Plot actual values (train data)
    plt.plot(y_train.iloc[-hours_range:].index, y_train.iloc[-hours_range:], label='Actual (Train)', color='blue', marker='o', linewidth=2)

    # Plot predicted values (in-sample)
    plt.plot(y_pred.iloc[:hours_range].index, y_pred.iloc[:hours_range], label='Predicted (In-Sample)', color='orange', marker='o', linewidth=2)

    # Plot forecasted values (test data)
    plt.plot(y_test.iloc[:hours_range].index, y_test.iloc[:hours_range], label='Actual (Test)', color='blue', marker='o', linewidth=2)

    # Overprediction shading
    plt.fill_between(
        y_test.iloc[:hours_range].index,
        y_test.iloc[:hours_range],
        y_pred.iloc[:hours_range],
        where=y_pred.iloc[:hours_range] > y_test.iloc[:hours_range],
        color='gray',
        alpha=0.3,
        label='Overprediction'
        )

        # Underprediction shading
    plt.fill_between(
        y_test.iloc[:hours_range].index,
        y_test.iloc[:hours_range],
        y_pred.iloc[:hours_range],
        where=y_pred.iloc[:hours_range] <= y_test.iloc[:hours_range],
        color='red',
        alpha=0.3,
        label='Underprediction'
        )

        # Adding labels, title, and legend
    plt.title('Actual vs Predicted Bike Rentals: Train vs Test', fontsize=14)
    plt.xlabel('Date/Time', fontsize=12)
    plt.ylabel('Bike Rentals', fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(alpha=0.3)

        # Display the plot in Streamlit
    st.pyplot(plt)


    
if __name__ == '__main__':
    main_results()
