import streamlit as st




def main():
    # simple login
    st.title("Simple Login App")

    menu = ["Home","Login","SignUp"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Home":
        st.subheader("Home")

    elif choice == "Login":
        st.subheader("Login Section")

        username = st.sidebar.text_input("User Name")
        username = st.sidebar.text_input("Password" , type='password')
        if st.button("Login"):
            st.success("Logged In as {}".format(username))


    elif choice == "SignUp":
        st.subheader("Create new account")




if __name__ == '__main__':
    main()
