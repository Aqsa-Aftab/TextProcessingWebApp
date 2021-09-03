# -*- coding: utf-8 -*-
import spacy

from aitextgen import aitextgen #for ai text gen

import streamlit as st

from textblob import TextBlob

from gingerit.gingerit import GingerIt



nlp = spacy.load('en_core_web_sm')

#Sumy packages 
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer


#Web Scrapping Packages
from bs4 import BeautifulSoup
from urllib.request import urlopen



#Function for Web Scraping 
@st.cache
def get_text(raw_url):
    page = urlopen(raw_url)
    soup = BeautifulSoup(page, features="lxml")
    fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
    return fetched_text


#Fuctionforsumy
def sumy_summarizer(docx):
    parser = PlaintextParser.from_string(docx, Tokenizer("english"))
    lex_summarizer = LexRankSummarizer()
    summary = lex_summarizer(parser.document, 3)
    summary_list = [str(sentence) for sentence in summary]
    result = ' '.join(summary_list)
    return result




def main():
    
    st.title("Text Editor Web App")
    
    activities = ["Summarize Via Text", "Summarize via URL", "Translate text","Automatic text generation" ,"Grammar Check", "Spell correction"]
    choice = st.sidebar.selectbox("Select Activity", activities)
    
    if choice == 'Summarize Via Text':
        st.subheader("Summary using NLP")
        raw_text = st.text_area("Enter Text Here","Type here")
        
        if st.button("Summarize Via Text"):
           
             summary_result = sumy_summarizer(raw_text)
                
             st.write(summary_result)
            
            
    if choice == 'Summarize via URL':
        st.subheader("Summarize Your URL")
        raw_url = st.text_input("Enter URL","Type Here")
        if st.button("Summarize"):
            result = get_text(raw_url)
            #st.write(result)
            st.subheader("Summarized Text")
            docx = sumy_summarizer(result)
            
            
            
            html = docx.replace("\n\n" , "\n")
            st.markdown(html,unsafe_allow_html=True)
            
            
    if choice == 'Spell correction':
        st.subheader(" Check your text")
        raw_text = st.text_area("Enter Text Here","Type here")
        if st.button("Check Spelling"):
            a = TextBlob(raw_text)
            #st.write(result)
            st.subheader("Summarized Text")
            st.write(a.correct())
            
            
    if choice == 'Translate text':
        st.subheader("Translate your text")
        raw_text = st.text_area("Enter Text Here","Type here")
        translation_text = TextBlob(raw_text)
        list1 = ["en","ta","pa","gu","hi","ur","kn","bn","te"]
        a= st.selectbox("select",list1)
        if st.button("Translate"):
            
            st.subheader("Translated text")
            st.write(translation_text.translate(to=a))        
              
        
         
                  
        
    if choice == 'Grammar Check':
        st.subheader("Check your text")
        raw_text = st.text_area("Enter Text Here","Type here")
        parser = GingerIt()
        
        if st.button("Check"):
            
            st.subheader("Corrected text")
            result_dict = parser.parse(raw_text)
            st.markdown( str(result_dict["result"]))    
        
    if choice == 'Automatic text generation':
        st.subheader("Aumtomatic Text Generation")
        ai = aitextgen()
        prompt_text = st.text_input(label = "Enter your Prompt text...",
            value = "Computer is beautiful")

        with st.spinner("AI is at Work........"):
            # text generation
            gpt_text = ai.generate_one(prompt=prompt_text,
            max_length = 100 )
        
        st.success("AI Successfully generated the below text ")
        st.write(gpt_text)
        
    
        
            
                 
    
    
if __name__ == '__main__':
    main()