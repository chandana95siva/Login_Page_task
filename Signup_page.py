import streamlit as st
import pandas as pd
import sqlite3
import mysql


with st.form("my_form"):
    
   NAME = st.text_input(" Enter your Name:", value ="",)
   DOB = st.text_input("Enter your DOB:", value ="")
   AGE = st.text_input("Enter your Age", value ="")
   CONTACT =st.text_input(" Enter your Contact.no", value ="")
   st.form_submit_button("submit")
con = sqlite3.connect("signup_page.db")
cur = con.cursor
cur = con.execute("CREATE TABLE IF NOT EXISTS Registration_Form(Name TEXT, DOB TEXT, Age INT, Contact INT)")
    
#data = {'Name': 'NAME', 'DOB': 'DOB', 'Age': 'AGE','Contact': 'CONTACT'}
# for k in p:
#         s.execute(
#             'INSERT INTO pet_owners (person, pet) VALUES (:owner, :pet);',
#             params=dict(owner=k, pet=pet_owners[k])
#         )
#     s.commit()