import streamlit as st
import pandas as pd
import numpy as np
import os
import joblib
import matplotlib.pyplot as plt
%matplotlib.use("Agg")
import seaborn as sns


def main():
    "Mortality Prediction App"
    st.title("Disease Mortality Predicition App")


    menu = ["Home","Login","SignUp"]
    submenu = ["Plot","Prediction","Metrics"]

    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Home":
        st.subheader("Home")
        st.text("What is Hepatitis")

    elif choice == "Login":
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password" , type="password")
        if st.sidebar.checkbox("Login"):
            if password == "12345":
                st.success("Welcome {}".format(username))

                activity = st.selectbox("Activity" , submenu)
                if activity == "Plot":
                    st.subheader("Data Visualization Plot")

                elif actvitiy == "Predicition":
                    st.subheader("Predictive Analytics")

            else:st.warning("Incorrect Username/Password")            








if __name__ == "__main__":
    main()
