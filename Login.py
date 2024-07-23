import streamlit as st
import sqlite3
import mysql
import pandas as pd

# Database connection
def get_connection():
    con = sqlite3.connect('user_database.db')
    cur = con.cursor()
    return con,cur

# create the table
def init_db():
    con,cur = get_connection()
    cur.execute("""CREATE TABLE IF NOT EXISTS Users(
                id INTEGER,
                name TEXT, 
                dob TEXT,
                age INTEGER,
                contact TEXT,
                email TEXT,
                password TEXT
                )
                """)
    con.commit()


# REGISTRATION FUNCTION
def register_user(name,dob,age,contact,email,password):
    con,cur = get_connection()
    cur.execute("INSERT INTO Users(name,dob,age,contact,email,password) VALUES(?,?,?,?,?,?)", (name,dob,age,contact,email,password))
    con.commit()

# LOGIN FUNCTION
def login_user(email,password):
    con,cur = get_connection()
    cur.execute("SELECT * FROM Users WHERE email =? AND password =?", (email,password))
    user = cur.fetchone()
    return user

# FETCH USER DETAILS
def get_user_details(email):
    con,cur = get_connection()
    cur.execute("SELECT name,dob,age,contact FROM Users WHERE email = ?", (email))
    user = cur.fetchone()
    return user

# UPDATE USER DETAILS
def update_user_details(name,dob,age,contact,email):
    con,cur = get_connection()
    cur.execute("UPDATE Users SET name = ?,dob = ?,age = ?, contact = ? WHERE email =?",(name,dob,age,contact,email))
    con.commit()

# Main app
def main():
    st.title("User Authentication System")

# NAVIGATION
menu = ["Register","Login","Profile"]
choice = st.sidebar.selectbox("Menu",menu)

# Initialize the database
init_db()

# REGISTRATION PAGE   
if choice == "Register":
    st.subheader("REGISTRATION PAGE")
    with st.form("register_form"):
            name = st.text_input("Name")
            dob = st.text_input("Date of Birth")
            age = st.number_input("Age", min_value=1, max_value=120)
            contact = st.text_input("Contact Number")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Register")

            if submitted:
                try:
                    register_user(name, dob, age, contact, email, password)
                    st.success("You have successfully registered")
                except sqlite3.IntegrityError:
                    st.error("User with this email already exists")


# LOGIN PAGE
elif choice == "Login":
        st.subheader("Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = login_user(email, password)
            if user:
                st.success("Login successful")
                st.session_state.logged_in = True
                st.session_state.email = email
            else:
                st.error("Invalid email or password")

# PROFILE PAGE
elif choice == "Profile":
    
    if "logged_in" in st.session_state and st.session_state.logged_in:
        st.subheader("PROFILE PAGE")
        user_details = get_user_details(st.session_state.email)
        with st.form("profile_form"):
            name = st.text_input("Name", value=user_details[0])
            dob = st.text_input("Date of Birth", value=user_details[1])
            age = st.number_input("Age", min_value=1, max_value=120, value=user_details[2])
            contact = st.text_input("Contact Number", value=user_details[3])
            submitted = st.form_submit_button("Update")

            if submitted:
                update_user_details(name, dob, age, contact, st.session_state.email)
                st.success("Profile updated successfully")

    else:
        st.warning("please login first")





if __name__ == "__main__":
    main()    