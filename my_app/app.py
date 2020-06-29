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


from managed_db import *

# password
def generate_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def verify_hashes(password,hashed_text):
    if generate_hashes(password) == hashed_text:
        return hashed_text
    return False



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
            create_usertable()
            hashed_pswd = generate_hashes(password)
            result = login_user(username,verify_hashes(password,hashed_pswd))
            # if password == "12345":
            if result:
                st.success("Welcome {}".format(username))

                activity = st.selectbox("Activity",submenu)
                if activity == "Plot":
                    st.subheader("Data Visualization Plot")
                    df = pd.read_csv("data/cleaned_data.csv")
                    st.dataframe(df)

                    # freq distribution plot
                    freq_df = pd.read_csv("data/Age_frq_Dist.csv")
                    st.bar_chart(freq_df["count"])
                    st.dataframe(freq_df)

                    df['class'].value_counts().plot(kind="bar")
                    st.pyplot()

                    if st.checkbox("Area Chart"):
                        all_columns = df.columns.to_list()
                        feat_choices = st.multiselect("Choose a feature" , all_columns)
                        new_df = df[feat_choices]
                        st.area_chart(new_df)

                    if st.checkbox("Bar Plot"):
                        all_columns = df.columns.to_list()
                        feat_choices = st.multiselect("Choose a feature" , all_columns)
                        new_df = df[feat_choices]
                        st.area_chart(new_df)


                elif activity == "Prediction":
                    st.subheader("Predictive Analytics")

            else:
                st.warning("Incorrect Username/Password")


    elif choice == "SignUp":
        new_username = st.text_input("User name")
        new_password = st.text_input("Password",type="password")

        confirm_password = st.text_input("Confirm Password",type="password")
        if new_password  == confirm_password:
            st.success("Password Confirmed")
        else:
            st.warning("Passwords not the same")

        if st.button("Submit"):
            create_usertable()
            hashed_new_password = generate_hashes(new_password)
            add_userdata(new_username , hashed_new_password)
            st.success("Successfully created new account")
            st.info("Login To Get Started")



if __name__ == '__main__':
    main()
