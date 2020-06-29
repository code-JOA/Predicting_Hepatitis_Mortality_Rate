import streamlit as st

import pandas as pd
import numpy as np

import os
import joblib
import hashlib
# passlib, bcrypt

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")




def main():
    """Mortality Prediction App"""
    st.title("Hepatitis Disease Mortality Prediction App")


    menu = ["Home","Login","SignUp"]
    submenu = ["Plot","Prediction","Metrics"]

    choice = st.sidebar.selectbox("Menu",menu)
    if choice == "Home":
        st.subheader("Home")
        st.text("Welcome")

    elif choice == "Login":
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password",type="password")
        if st.sidebar.checkbox("Login"):
            if password == "12345":
                st.success("Welcome {}".format(username))
                activity = st.selectbox("Activity",submenu)
                if activity == "Plot":
                    st.subheader("Data Visualization Plot")

                elif activity == "Prediction":
                    st.subheader("Predictive Analytics")
            # create_usertable()

        else:st.warning("Incorrect Username/Password")
