import os
from dotenv import load_dotenv
import json
import pandas as pd
import traceback
from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain_community.callbacks.manager import get_openai_callback
import PyPDF2
from datetime import datetime
from src.mcqgenerator.logger import logging
import streamlit as st
import sys
print("Before sys.path.append")
sys.path.append('/Users/shreyagajbhiye/Desktop/openai/project/src')
print("After sys.path.append")
sys.path.append('/Users/shreyagajbhiye/Desktop/openai/project/src')
from src.mcqgenerator.mcqgenerator import generate_evaluate_chain
from src.mcqgenerator.utils import get_table_data



with open('/Users/shreyagajbhiye/Desktop/openai/project/Response.json','r') as file:
    RESPONSE_JSON = json.load(file)
#title of the application
st.title("Music Recommendation Playlist Based on Mood")
##creating a form using st.from
with st.form("user_inputs"):
    #input fields
    song_count=st.number_input("No. of songs",min_value = 3, max_value = 10)

    mood=st.text_input("Your current mood",max_chars=20,placeholder="Happy")

    button=st.form_submit_button("Generate List")

    #check if the button is clicked and all the fields have input

    if button is not None and song_count and mood:
        with st.spinner("Loading...."):
            try:
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain(
                        {
                        "number":song_count,
                        "mood":mood,
                        "response_json":json.dumps(RESPONSE_JSON)
                        }
                    )
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")
            else:
                print(f"Total Tokens:{cb.total_tokens}")
                print(f"Prompt Tokens:{cb.prompt_tokens}")
                print(f"Completion Tokens:{cb.completion_tokens}")
                print(f"Total Cost:{cb.total_cost}")
                if isinstance(response,dict):
                    #extract the music data from the response
                    music=response.get("music",None)
                    #st.write(f"Music JSON string: {music}")
                    if music is not None:
                        table_data=get_table_data(music)
                        if table_data is not None:
                            df=pd.DataFrame(table_data)
                            df.index=df.index+1
                            st.table(df)
                            #display the review text as well
                            st.text_area(label="Review",value=response["review"])
                        else:
                            st.error("Error in the table data")
                    else:
                        st.error("Music data not found in the response")
                else:
                    st.write(response)
    





