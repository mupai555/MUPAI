import streamlit as st

# Title of the app
st.title("Genetic Potential Calculator for Muscle Growth")

# Description of the app
st.write("""
This app helps you estimate your genetic potential for muscle growth based on scientific models. 
Enter your data below to get started.
""")

# User inputs
st.header("Enter your data")
height = st.number_input("Height (in cm):", min_value=100, max_value=250, step=1)
weight = st.number_input("Weight (in kg):", min_value=30.0, max_value=200.0, step=0.1)
body_fat = st.number_input("Body fat percentage (%):", min_value=5.0, max_value=50.0, step=0.1)

# Perform calculations
if height > 0 and weight > 0 and body_fat > 0:
    # Convert height to meters
    height_m = height / 100

    # Calculate fat-free mass
    lean_mass = weight * (1 - body_fat / 100)  # kg

    # Fat-Free Mass Index (FFMI)
    ffmi = lean_mass / (height_m ** 2)

    # Estimate genetic potential (basic formula)
    genetic_potential = (height - 100) * 1.1

    # Display results
    st.header("Results")
    st.write(f"**Your FFMI:** {ffmi:.2f}")
    st.write(f"**Your Lean Mass:** {lean_mass:.2f} kg")
    st.write(f"**Estimated Genetic Potential for Muscle Growth:** {genetic_potential:.2f} kg")

    # Provide insights
    if ffmi < 25:
        st.success("You are within the natural range for muscle development.")
    else:
        st.warning("Your FFMI exceeds the natural range, which may indicate the use of performance enhancers.")
else:
    st.write("Please enter all the required data to calculate your results.")