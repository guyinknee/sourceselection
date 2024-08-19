

# Import necessary libraries
import streamlit as st
import pandas as pd
# Add logo
st.image('C:\\Users\\gaini\\master\\logo.png', use_column_width=False, width=600, clamp=True, channels='RGB', output_format='auto')

# Streamlit code to create the web interface
st.title('Flexibility in source water selection: multi-criteria decision analysis')


# Subheader for program explanation
st.subheader('Master\'s thesis')
st.write('''
This program solves a multi-criteria decision analysis for the best source water selection. 
It takes user inputs on water availability, treatment's unit cost, environmental impact, 
and weighting factors. The program then uses these inputs to find the optimal solution.
''')
# Subheader for input section
st.subheader('Input Section')
st.write('Please enter the required inputs in the text boxes below.')
# Function to load data from an uploaded Excel file

# User uploads the Excel file
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])
if uploaded_file is not None:
    data = pd.read_excel(uploaded_file)

    # User inputs
    mTAW = st.number_input("Enter mTAW value for canal water (default is 3.75 mTAW):", value=3.75, min_value=0.0, max_value=10.0, step=0.01, format="%.2f")
    mTAW = round(mTAW, 2) 
    w1 = st.slider("Enter Weight 1 (w1) for cost considerations:", min_value=0.0, max_value=1.0, value=0.5)
    w2 = 1 - w1
    w2 = round(w2, 2)

    # Display user inputs
    st.write(f"mTAW: {mTAW}")
    st.write(f"Weight 1 (w1): {w1}")
    st.write(f"Weight 2 (w2): {w2}")

    # Initialize results dictionary
    results = {}
    weighted_scores = {}

    # Process data for each month
    for index, row in data.iterrows():
        month = row['Months']
        
        # Extract relevant data
        cost_canal = row['Canal water cost (Eur/m3)']
        env_impact_canal = row['Canal water endpoint environmental impact (mPt/m3)']
        cost_seawater = row['Seawater cost (Eur/m3)']
        env_impact_seawater = row['Seawater endpoint environmental impact (mPt/m3)']
        canal_water_level = row['Canal water level (mTAW)']
        
        # Calculate weighted scores
        if canal_water_level > mTAW:
            weighted_score_canal = (w1 * cost_canal) + (w2 * env_impact_canal)
        else:
            weighted_score_canal = 1000  # Set to 1000 if canal water is not available
        
        weighted_score_seawater = (w1 * cost_seawater) + (w2 * env_impact_seawater)
        
        # Select optimal water source
        if weighted_score_canal < weighted_score_seawater:
            optimal_water_source = "Canal Water"
        else:
            optimal_water_source = "Seawater"
        
        # Store result
        results[month] = optimal_water_source
        weighted_scores[month] = {
        'Weighted Score Canal': weighted_score_canal,
        'Weighted Score Seawater': weighted_score_seawater
    }


    # Output the optimal water source for each month
    st.subheader("Optimal Water Source for Each Month")
    # Convert the results dictionary to a DataFrame
    results_list = list(results.items())[:12]

    # Create a DataFrame from the sliced list
    results_df = pd.DataFrame(results_list, columns=['Month', 'Optimal Water Source'])


    # Display the results in a table
    st.table(results_df)

    st.subheader("Weighted Scores of Sources for Each Month")
    weighted_scores_df = pd.DataFrame.from_dict(weighted_scores, orient='index').reset_index()
    weighted_scores_df.columns = ['Month', 'Weighted Score Canal', 'Weighted Score Seawater']
    weighted_scores_df = weighted_scores_df.head(12)
    # Display the results in a table
    st.table(weighted_scores_df)

else:
    st.write("Please upload an Excel file to proceed.")