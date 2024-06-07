
# Streamlit dependencies
import streamlit as st
import joblib

# Data dependencies
import pandas as pd
import numpy as np

# Define a function to clear input values
def clear_input_values():
    st.session_state.text_input = ""
    st.session_state.number_input = None
    st.session_state.selected_option = None


model_file = open("resources/model.pkl","rb")
model = joblib.load(model_file) # loading your data transformer and model from the pkl file

# The main function where we will build the actual app
def main():
	"""Fraudulent Claims Classifier App with Streamlit """

	# Clear input values when the app starts
	clear_input_values()
	# Creates a main title and subheader on your page -
	st.title("Fraud Classifier")
	st.subheader("Classify claims as fraudulent or non-fraudulent")
	
	# Creating sidebar with selection box -
	# you can create multiple pages this way
	options = ["Classify", "Information"]
	selection = st.sidebar.selectbox("Choose Option", options)

	# Building out the "Information" page
	if selection == "Information":
		st.info("General Information")
		# You can read a markdown file from supporting resources folder
		st.markdown("Please note that this app was built exclusively for the Explore Data Science Course and should not be used commercially.")
		
	# Building out the predication page
	if selection == "Classify":
		st.session_state.clear()
		st.info("Classify this claim as potentially fraudulent")
		# Creating a text box for user input
		csl = st.selectbox("Combined Single Limit (CSL)",['','100/300','250/500','500/1000'])
		incident_severity = st.selectbox("Incident Severity",['', 'Major Damage', 'Minor Damage', 'Trivial Damage','Total Loss'])
		incident_state = st.selectbox("Incident State",['','SC', 'VA', 'NY', 'OH', 'WV', 'NC', 'PA'])
		authorities_contacted = st.selectbox("Which authorities were contacted",['','Police', 'Fire', 'Other', 'Ambulance', 'None'])
		property_damage = st.selectbox("Was there any property damage?",['','YES', 'NO'])
		police_report_available = st.selectbox("Is a police report available?",['','YES', 'NO'])
			
		policy_csl_5001000 = 0
		if csl == '500/1000':
			policy_csl_5001000 = 1
		incident_severity_MinorDamage = 0
		incident_severity_TotalLoss = 0
		incident_severity_TrivialDamage = 0
		if incident_severity == 'Minor Damage':
			incident_severity_MinorDamage = 1
		elif incident_severity == 'Total Loss':
			incident_severity_TotalLoss = 1
		elif incident_severity == 'Trivial Damage':
			incident_severity_TrivialDamage = 1
		authorities_contacted_None = 0
		authorities_contacted_Police = 0
		if authorities_contacted == 'None':
			authorities_contacted_None = 1
		if authorities_contacted == 'Police':
			authorities_contacted_Police = 1
		incident_state_NY = 0
		incident_state_WV = 0
		if incident_state == 'NY':
			incident_state_NY = 1
		elif incident_state == 'WV':
			incident_state_WV = 1
		property_damage_NO = 0
		if property_damage == 'NO':
			property_damage_NO = 1
		police_report_available_YES = 0
		if police_report_available == 'YES':
			police_report_available_YES = 1

		X_unseen = np.array([policy_csl_5001000,incident_severity_MinorDamage,
                    incident_severity_TotalLoss, incident_severity_TrivialDamage,
                    authorities_contacted_None, authorities_contacted_Police,
                    incident_state_NY, incident_state_WV,property_damage_NO,
                    police_report_available_YES]).reshape(1, -1)
		
		if st.button("Classify"):
			if '' in [csl, incident_severity, incident_state, authorities_contacted, property_damage, police_report_available]:
				st.error("Please fill in all fields.", icon=":material/rule:")
				return
			else:
				prediction = model.predict(X_unseen)
				if prediction == 'Y':
					message = 'There is a high probability that this claim is fraudulent.  Please pay special attention to this during your claim assessment process.'
					st.error(message, icon="🚨")
				else:
					message = 'This claim is likely not fraudulent.'
					st.success(message, icon=":material/verified:")
					st.balloons()

# Required to let Streamlit instantiate our web app.  
if __name__ == '__main__':
	main()
