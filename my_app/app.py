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

feature_names_best = ["age","sex","steriod","antivirals","fatigue","spiders","ascites",
                      "varices","bilirubin","alk_phosphate","sgot","albumin","protime","histology"]

gender_dict = {"male":1,"female":2}
feature_dict = {"No":1 , "Yes":2}


def get_value(val,my_dict):
    for key,value in my_dict.items():
        if val == key:
            return value


def get_key(val,my_dict):
    for key, value in my_dict.items():
        if val == key:
            return key


def get_fvalue(val):
    feature_dict = {"No":1,"Yes":2}
    for key,value in feature_dict.items():
        if val == key:
            return value


# loading ML models
def load_model(model_file):
    loaded_model = joblib.load(open(os.path.join(model_file) , "rb"))
    return loaded_model


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


                # prediction
                elif activity == "Prediction":
                    st.subheader("Predictive Analytics")

                    age = st.number_input("Age",7,80)
                    sex = st.radio("Sex",tuple(gender_dict.keys()))
                    steriod = st.radio("Do You Take Steriods?",tuple(feature_dict.keys()))
                    antivirals = st.radio("Do You Take Antivirals?",tuple(feature_dict.keys()))
                    fatique = st.radio("Do You Have Fatique",tuple(feature_dict.keys()))
                    spiders = st.radio("Presence of Spider Naeve",tuple(feature_dict.keys()))
                    ascites = st.selectbox("Ascites",tuple(feature_dict.keys()))
                    varices = st.selectbox("Presence of Varices",tuple(feature_dict.keys()))
                    bilirubin = st.number_input("bilirubin Content",0.0,8.0)
                    alk_phosphate = st.number_input("Alkaline Phosphate Content",0.0,296.0)
                    sgot = st.number_input("Sgot",0.0,648.0)
                    albumin = st.number_input("Albumin",0.0,6.4)
                    protime = st.number_input("Prothrombin Time",0.0,100.0)
                    histology = st.radio("Histology",tuple(feature_dict.keys()))






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
