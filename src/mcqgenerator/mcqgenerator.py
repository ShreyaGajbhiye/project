import os
from dotenv import load_dotenv
import json
import pandas as pd
import traceback
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.callbacks import get_openai_callback #IMPORTANT
import PyPDF2
from datetime import datetime
from src.mcqgenerator.logger import logging
from src.mcqgenerator.utils import get_table_data

#load environment variables from the .env file
load_dotenv()
#access the environment variable
key = os.getenv("OPENAI_API_KEY")

llm=ChatOpenAI(openai_api_key = key, model_name = "gpt-3.5-turbo",temperature=0.7)


template="""
You are an expert in musical knowledge. Given the above text, it is your job to\
create a list of {number} songs for {mood} mood from bollywood since the year 2000.
Make sure that the songs are not repeated and check all the songs to be conforming the mood.
Make sure to format your response like RESPONSE_JSON below and use it as a guide.
Ensure to add {number} of songs
{response_json}

"""
music_generation_prompt=PromptTemplate(
    input_variables = ["number","mood","response_json"],
    template = template
)

music_chain=LLMChain(llm=llm, prompt=music_generation_prompt,output_key="music",verbose=True)

template2 ="""
You are an expert in musical knowledge. Given the list of songs below and the specified mood,\
evaluate whether each song conforms to the {mood} mood.
Provide a detailed analysis for each song, including whether it fits the mood and why.
####Songs_List:
{music}

check from an expert in music:
"""
music_evaluation_prompt = PromptTemplate(input_variables=["mood","music"],template = template2)

review_chain = LLMChain(llm=llm, prompt=music_evaluation_prompt, output_key="review",verbose = True)
print("mcqgenerator.py is being imported")
generate_evaluate_chain = SequentialChain(chains=[music_chain, review_chain],input_variables=["number","mood","response_json"],
                                       output_variables=["music","review"],verbose=True)

# print("mcqgenerator.py is being imported")
# def generate_evaluate_chain():
#     print("generate_evaluate_chain function is called")
#     return SequentialChain(chains=[music_chain, review_chain], input_variables=["number", "mood", "response_json"],
#                            output_variables=["music", "review"], verbose=True)