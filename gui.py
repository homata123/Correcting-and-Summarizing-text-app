import streamlit  as st
import numpy as np
import summarize_module
from nltk.corpus import stopwords
import correct_module
import nltk
import PIL.Image
from PIL import Image
import correct_module

from nltk.tokenize import sent_tokenize


# st.markdown('<style>body{background-color:coral;}</style>',unsafe_allow_html=True)

st.markdown('<center><h1>Text correcting and summarizing app<h1></center>', unsafe_allow_html=True)

ch = st.selectbox(
    "Choice",
    [
        "Guide",
        "Start using app",
    ],
    key="main_select",
)

if ch == "Guide":
    st.markdown('<center><h3>HOME<h3></center>', unsafe_allow_html=True)

    a = '<p style="text-align: justify;font-size:20px;">Text correcting and summarizing APP (TCS) is an web APP'
    a += 'that will help you correct and get summary of your input txt file, you can also choose the number of sentence of summarized text'
    a += ' </p><br>'
    st.markdown(a, unsafe_allow_html=True)

    st.markdown('<center><h3>How to use<h3></center>', unsafe_allow_html=True)
    a = "<p style='text-align: justify;font-size:20px;'><ul><li style='text-align: justify;font-size:20px;'>Step 1: Browse your input file (.docx or .txt) </li>"
    a += "<li style='text-align: justify;font-size:20px;'>Step 2: Enter the number of summary sentences</li>"
    a += "<li style='text-align: justify;font-size:20px;'>Step 3: Click convert button,then the result will be showed on the output section</li><br>"
    st.markdown(a, unsafe_allow_html=True)

    st.markdown('<center><h3>EXAMPLE<h3></center>', unsafe_allow_html=True)
    image = Image.open('2021-10-12.png')
    st.image(image, use_column_width=True)

elif ch == "Start using app":
    st.markdown('<center><h3>TCS app by Manh Thang Ho<h3></center>', unsafe_allow_html=True)
    sentences = []
    uploaded_file = st.file_uploader("Add text file !",type=["txt"])
    true_sentences=""
    if uploaded_file:
        st.write("Original text: \n")
        for line in uploaded_file:
            sentences.append(line)
            st.write(line)
        true_sentences=sentences[0]  
        true_sentences=str(true_sentences)
    original_sentences = []
    
    
    original_sentences.append(sent_tokenize(true_sentences))
    original_sentences = [y for x in original_sentences for y in x]
    
    if uploaded_file:
        
        number_of_sentences = st.number_input('Input number of summary sentences', min_value=1, max_value=len(original_sentences[0]),value=1,step=1)
        st.warning("Wrong words suggested :   " +str(correct_module.correct(true_sentences)[0]))
        st.success("Corrected words suggested :   " +str(correct_module.correct(true_sentences)[1]))
        st.write("Summary")
        st.write(summarize_module.summarize(true_sentences,number_of_sentences))
        
        
        
    
    
    

    