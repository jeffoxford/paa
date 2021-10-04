from typing import Text
import pandas as pd
import streamlit as st
import time 
import numpy as np
import base64
from io import BytesIO


import people_also_ask
import re
question_final= []
def get_question (term,list_obj):
    ll =  people_also_ask.get_related_questions(term, 10)
    for q in ll :
        ql = re.sub('Search\sfor:.*','',q)

        if term_initial in ql and ql not in list_obj :
            question_final.append(ql)
        else:
            pass



question_final1= question_final

keywords = st.text_input('Add the Keyword and press the button')
outnr = st.radio('Select the max output', [25,50,75,100,125])
if outnr is None:
    outnr = 25
else:
    outnr = outnr
if st.button('Start Process The Keyword'):
    my_bar = st.progress(0)
    percent_complete=0
    term_initial = keywords
    get_question(term_initial,question_final)
    for ql1 in question_final:
        lenn =len(question_final1)
        if lenn> outnr:
            lenn = outnr
        else :
            lenn =  lenn
        my_bar.progress(lenn/outnr)

        if len(question_final1)>outnr :
            break
        else:
            get_question(ql1,question_final1)

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(df,name):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{name}.xlsx">Download Excel file</a>' # decode b'abc' => abc

record_list = []
for record in question_final1:
    record_list.append({
        'keyword' : keywords,
        'questions' : record

    })

outputDf = pd.DataFrame(record_list)


st.dataframe(outputDf)
st.markdown(get_table_download_link(outputDf,'Google_PAA'), unsafe_allow_html=True)
