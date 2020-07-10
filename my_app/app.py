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

# Model Interpretting
import lime
import lime.lime_tabular

from managed_db import *

# password
def generate_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def verify_hashes(password,hashed_text):
    if generate_hashes(password) == hashed_text:
        return hashed_text
    return False

feature_names_best = ["age","sex","steroid","antivirals","fatigue","spiders","ascites",
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


html_temp = """
		<div style="background-color:{};padding:10px;border-radius:10px">
		<h1 style="color:white;text-align:center;">Disease Mortality Prediction </h1>
		<h5 style="color:white;text-align:center;">Hepatitis B </h5>
		</div>
		"""

# Avatar Image using a url
avatar1 ="https://www.w3schools.com/howto/img_avatar1.png"
avatar2 ="https://www.w3schools.com/howto/img_avatar2.png"

result_temp ="""
	<div style="background-color:#464e5f;padding:10px;border-radius:10px;margin:10px;">
	<h4 style="color:white;text-align:center;">Algorithm:: {}</h4>
	<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;" >
	<br/>
	<br/>
	<p style="text-align:justify;color:white">{} % probalibilty that Patient {}s</p>
	</div>
	"""

result_temp2 ="""
	<div style="background-color:#464e5f;padding:10px;border-radius:10px;margin:10px;">
	<h4 style="color:white;text-align:center;">Algorithm:: {}</h4>
	<img src="https://www.w3schools.com/howto/{}" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;" >
	<br/>
	<br/>
	<p style="text-align:justify;color:white">{} % probalibilty that Patient {}s</p>
	</div>
	"""

prescriptive_message_temp ="""
	<div style="background-color:silver;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
		<h3 style="text-align:justify;color:black;padding:10px">Recommended Life style modification</h3>
		<ul>
		<li style="text-align:justify;color:black;padding:10px">Exercise Daily</li>
		<li style="text-align:justify;color:black;padding:10px">Get Plenty of Rest</li>
		<li style="text-align:justify;color:black;padding:10px">Exercise Daily</li>
		<li style="text-align:justify;color:black;padding:10px">Avoid Alchol</li>
		<li style="text-align:justify;color:black;padding:10px">Proper diet</li>
		<ul>
		<h3 style="text-align:justify;color:black;padding:10px">Medical Mgmt</h3>
		<ul>
		<li style="text-align:justify;color:black;padding:10px">Consult your doctor</li>
		<li style="text-align:justify;color:black;padding:10px">Take your interferons</li>
		<li style="text-align:justify;color:black;padding:10px">Go for checkups</li>
		<ul>
	</div>
	"""


descriptive_message_temp ="""
	<div style="background-color:silver;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
		<h3 style="text-align:justify;color:black;padding:10px">Definition</h3>
		<p>Hepatitis B is a viral infection that attacks the liver and can cause both acute and chronic disease.</p>
	</div>
	"""

@st.cache
def load_image(img):
	im =Image.open(os.path.join(img))
	return im


def change_avatar(sex):
	if sex == "male":
		avatar_img = 'img_avatar.png'
	else:
		avatar_img = 'img_avatar2.png'
	return avatar_img



def main():
    """Mortality Prediction App"""
    st.title("Hepatitis Disease Mortality Prediction App")
    # st.markdown(html_temp.format("royalblue"),unsafe_allow_html=True)


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
                    steroid = st.radio("Do You Take Steroids?",tuple(feature_dict.keys()))
                    antivirals = st.radio("Do You Take Antivirals?",tuple(feature_dict.keys()))
                    fatique = st.radio("Do You Have Fatique?",tuple(feature_dict.keys()))
                    spiders = st.radio("Presence of Spider Naeve",tuple(feature_dict.keys()))
                    ascites = st.selectbox("Ascites",tuple(feature_dict.keys()))
                    varices = st.selectbox("Presence of Varices",tuple(feature_dict.keys()))
                    bilirubin = st.number_input("bilirubin Content",0.0,8.0)
                    alk_phosphate = st.number_input("Alkaline Phosphate Content",0.0,296.0)
                    sgot = st.number_input("Sgot",0.0,648.0)
                    albumin = st.number_input("Albumin",0.0,6.4)
                    protime = st.number_input("Prothrombin Time",0.0,100.0)
                    histology = st.radio("Histology",tuple(feature_dict.keys()))
                    feature_list = [age,get_value(sex,gender_dict),get_fvalue(steroid),get_fvalue(antivirals),get_fvalue(fatique),get_fvalue(spiders)
                           ,get_fvalue(ascites),get_fvalue(varices),bilirubin,alk_phosphate,sgot,albumin,int(protime),get_fvalue(histology)]
                    st.write(len(feature_list))
                    st.write(feature_list)
                    pretty_result = {"age":age,"sex":sex,"steroid":steroid,"antivirals":antivirals,"fatique":fatique,"spiders":spiders,
                                  "ascites":ascites , "varices":varices ,"bilirubin":bilirubin,"alk_phosphate":alk_phosphate,"sgot":sgot,
                                  "albumin":albumin,"protime":protime,"histology":histology}
                    st.json(pretty_result)
                    single_sample = np.array(feature_list).reshape(1,-1)

                    # # Machine Learning models
                    model_choice = st.selectbox("Select Model",["LR","KNN","DecisionTree"])

                    if st.button("Predict"):
                        if model_choice == "KNN":
                            loaded_model = load_model("models/KNN_HepatitisB_model.pkl")
                            prediction=loaded_model.predict(single_sample)
                            pred_prob=loaded_model.predict_proba(single_sample)
                        elif model_choice == "DecisionTree":
                            loaded_model=load_model("models/decision_tree_clf_HepatitisB_model.pkl")
                            prediction=loaded_model.predict(single_sample)
                            pred_prob=loaded_model.predict_proba(single_sample)
                        else:
                            loaded_model = load_model("models/LogisticReg_HepatitisB_model.pkl")
                            prediction=loaded_model.predict(single_sample)
                            pred_prob=loaded_model.predict_proba(single_sample)

                        # st.write(prediction)
                        # 	# prediction_label = {"Die":1,"Live":2}
    					# 	# final_result = get_key(prediction,prediction_label)
                        if prediction == 1:
                            st.warning("Patient Dies")
                            pred_probability_score = {"Die":pred_prob[0][0]*100 , "Live":pred_prob[0][1]*100}
                            st.subheader("Prediction Probability Score using {}".format(model_choice))
                            st.json(pred_probability_score)
    						st.subheader("Prescriptive Analytics")
                            st.markdonw(prescriptive_message_temp,unsafe_allow_html=True)

                        else:
                            st.success("Patient Lives")
                            pred_probability_score = {"Die":pred_prob[0][0]*100,"Live":pred_prob[0][1]*100}
                            st.subheader("Prediction Probability Score using {}".format(model_choice))
                            st.json(pred_probability_score)

                if st.checkbox("Interpret"):
                    if model_choice == "KNN":
                        loaded_model = load_model("models/KNN_HepatitisB_model.pkl")

                    elif model_choice == "DecisionTree":
                        loaded_model = load_model("models/decision_tree_clf_HepatitisB_model.pkl")

                    else:
                        loaded_model = load_model("models/LogisticReg_HepatitisB_model.pkl")


                        # loaded_model = load_model("models/logistic_regression_model.pkl")
                        # 1 Die and 2 Live
                        df = pd.read_csv("data/cleaned_data.csv")
                        x = df[['age', 'sex', 'steroid', 'antivirals','fatigue','spiders', 'ascites','varices', 'bilirubin', 'alk_phosphate', 'sgot', 'albumin', 'protime','histology']]
                        feature_names = ['age', 'sex', 'steroid', 'antivirals','fatigue','spiders', 'ascites','varices', 'bilirubin', 'alk_phosphate', 'sgot', 'albumin', 'protime','histology']
                        class_names = ['Die(1)','Live(2)']
                        explainer = lime.lime_tabular.LimeTabularExplainer(x.values,feature_names=feature_names, class_names=class_names,discretize_continuous=True)
                        # The Explainer Instance
                        exp = explainer.explain_instance(np.array(feature_list), loaded_model.predict_proba,num_features=13, top_labels=1)
                        exp.show_in_notebook(show_table=True, show_all=False)
                        # exp.save_to_file('lime_oi.html')
                        st.write(exp.as_list())
                        new_exp = exp.as_list()
                        label_limits = [i[0] for i in new_exp]
                        # st.write(label_limits)
                        label_scores = [i[1] for i in new_exp]
                        plt.barh(label_limits,label_scores)
                        st.pyplot()
                        plt.figure(figsize=(20,10))
                        fig = exp.as_pyplot_figure()
                        st.pyplot()




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
