import streamlit as st
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
import glob
from dotenv import load_dotenv
load_dotenv(override=True)
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', 'your-key-if-not-using-env')
# Function to generate names
def generate_names(religion_type, gender):
    llm = OpenAI(temperature=0.5)  # Make sure OPENAI_API_KEY is in your env
    prompt_temp_name = PromptTemplate(
        input_variables=['religion_type', 'gender'],
        template="I am a {religion_type}. Suggest 10 beautiful {religion_type} names I can name my child who is a {gender}."
    )
    name_chain = LLMChain(llm=llm, prompt=prompt_temp_name)
    response = name_chain({'religion_type': religion_type, 'gender': gender})
    return response['text']

    
st.set_page_config(page_title="Beautiful Baby Names", page_icon="👶")

# Sidebar inputs
st.sidebar.header("Choose Your Preferences")
religion_type = st.sidebar.text_input("Religion or Nationality", value="Muslim")
gender = st.sidebar.selectbox("Select Gender", ["Boy", "Girl", "Neutral"])
color = st.sidebar.selectbox("Favorite Color", ["Blue", "Pink", "Green", "Gold", "White"])

# Main page
st.title("👶 Baby Name Generator")
st.write("Get beautiful names tailored to your culture/religion and preferences.")

if st.sidebar.button("Generate Names"):
    with st.spinner("Thinking..."):
        names_text = generate_names(religion_type, gender)
        names_list = [n.strip() for n in names_text.split("\n") if n.strip()]
        
        st.subheader(f"Here are your {color} {gender} names:")
        for idx, name in enumerate(names_list, start=1):
            st.markdown(f"**{idx}.** {name}")
