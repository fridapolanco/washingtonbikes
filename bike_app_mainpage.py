import streamlit as st
from bikeprediction3 import main_bikeprediction as bikeprediction_app
from bikeprediction3 import prediction
from features import main_feature_engineering as main_feature_engineering_app
from results import main_results as results_app
from interactive import bike_rental_dashboard as dashboard_app
from business import bike_sharing_business as business_app



# Set page config
st.set_page_config(page_title="Bike sharing analysis", layout="wide", page_icon="🚲")

st.logo("media\\bike2.png",icon_image="media\\ie.png")

# side_bar = st.sidebar

########################################
def main():
	html_temp = """
	<div style="background-color:tomato;padding:10px">
	<h2 style="color:white;text-align:center;">Bike sharing analysis in Washington DC</h2>
	</div>"""
	st.markdown(html_temp,unsafe_allow_html=True)

	st.image("media\\bike0.png", width=10000)

	st.header("About the analysis")

	st.markdown('''
	As part of IE consultants INC, we were contacted by Washington's office of public transport to analyze if bike sharing services are effective and find possible areas of opportunity. 
	Additionally, we were requested an interactive application for citizens to predict if bycicles will be available when they need them. 

	Data was provided on an hourly basis for the years of 2011 and 2012. With this input, trends and patterns were analyzed to create a linear regression model.
		''')

	st.header("About the application")

	st.markdown('''
	Our original dataset went through some light data cleaning and transformation to have more insightful and user-friendly features. To automate our machine learning workflow we used Pycaret library. This way, we could speed our experiment process and ensure the most accurate model was used for this problem. After setting our model to our needs, such as  splitting the data into train & test, ignoring certain features, removing mulitcollinearity and using k-folds for cross validation our best scored model was Extreme Gradient Boosting. 
	Additionally, we included a personalized metric that penalizes under-predicting to ensure there's always availability for our customers. Thus, this metric will help the business side on inventory and procurement planning. 
	Lastly, users now have a mobile app where they can see if bikes are available for them. The next step of our project will be to include bike stations in our dataset so the user can compare availability within different stations. 
			 
	For more details on modelling our solution please navigate to our 'Model Workflow' section. 
	''')
	st.header("About the dashboard")

	st.markdown('''
The different sections of this dashboard are:
- Main page
- Data Visualization
- Technical Annex
- Results
- Business Insights
- Bike Prediction
''')


	st.header("About the team")
	st.markdown('''
	The following data analysts participated in this project. 
		''')

	col1,col2,col3,col4,col5 = st.columns(5)

	with col1:
		st.image("media\\nicole.jpg", caption="Frida Polanco")
	with col2:
		st.image("media\\nilesh.png", caption="Nilesh Mukherji")
	with col3:
		st.image("media\\alejandro.png", caption="Alejandro Born")
	with col4:
		st.image("media\\charles.png", caption="Charles Miroslaw")
	with col5:
		st.image("media\\nic.png", caption="Niclas Tariq")

########################

side_bar = st.sidebar

#Page navigation instead of radio buttons
pages = {
    "Bike Sharing WebApp Navigation": [
        st.Page(main, title="🏠Main Page"),
		st.Page(dashboard_app, title="📊Data Visualization"),
        st.Page(main_feature_engineering_app, title="🗃️Technical Annex"),
		st.Page(results_app, title="🧪Results"),
		st.Page(business_app, title="📈Business Insights"),
		st.Page(bikeprediction_app, title="🚲Bike Prediction")
	]}
				
pg = st.navigation(pages)
pg.run()
