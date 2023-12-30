# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

# credit : Gautam Kedia
# organization : Lyft
# twitter : http://twitter.com/thegautam

import asyncio

import dotagent.compiler as compiler
import streamlit as st

essay_type = st.selectbox("What type of essay is it?", ["Informative", "Argumentative", "Opinion"])
essay = st.text_area("Enter your essay")
submitted = st.button("Grade")

async def setup_compiler():
  compiler.llm = compiler.llms.OpenAI("gpt-4")
  compiler.llm.api_key = st.secrets["OPENAI_API_KEY"]
  print(compiler.llm.api_key)

async def run_grader(essay):
  experts = compiler('''
    {{#system~}}
    You are a middle school English teacher. Give feedback to the essay writer by the following points from 1 to 4.
    Explain clearly why you gave the feedback with examples from the essay. If student doesn't get the highest grade, 
    give actionable feedback on how to get a higher grade.

    Here are the scores:
    1: Needs Improvement
    2: Fair 
    3: Strong
    4: Excellent

    Here are the grading criteria:
    A. Topic
    1. Topic is unclear. 
    2. Introduces the topic but the focus is unclear. 
    3. Introduces the topic. 
    4. Clearly introduces the topic.  

    B. Evidence
    1. Little to no facts, concrete details, quotations, or examples included. 
    2. Attempts to develop the topic with facts, concrete details, and examples but some of the information is not relevant. 
    3. Develops the topic with facts, concrete details, quotations, and examples. 
    4. Thoroughly develops the topic with relevant facts, concrete details, quotations, and examples.  

    C. Explanation & Analysis 
    1. Little to no explanation or analysis of the information presented. 
    2. Explanation and analysis attempt to discuss the information but is unclear or lacks depth. 
    3. Clear explanation and analysis that discusses most of the information presented. 
    4. Clear and concise explanation and analysis that thoroughly discusses the information presented. 

    D. Conclusion
    1. Abrupt ending. No concluding statement. 
    2. Ends with a concluding statement that does not clearly relate to the topic. 
    3. Ends with a concluding statement about the topic. 
    4. Effectively ends with a strong concluding statement. 

    E. Formal Tone and Style
    1. Informal language present throughout.
    2. Writing contains some informal elements (e.g., contractions).
    3. Writing attempts to maintain a formal and objective tone. 
    4. Writing maintains a formal and objective tone throughout. 

    F. Organization & Transitions
    1. Little to no attempt at organization. 
    2. Attempts to organize ideas, but transitional language is needed. 
    3. Organizes ideas in a logical way. Transitional language used. 
    4. Strong organization and transitional language used skillfully  throughout. 

    G. Mechanics (Spelling & Grammar)
    1. Distracting mechanical errors throughout.
    2. Mechanical errors distract at times.
    3. A couple errors present, but they do not distract.
    4. Mechanics reflect careful editing.

    H. Vocabulary
    1. Minimal descriptive vocabulary
    2. Repeated and common words like amazing
    3. Unique & specific words that clearly paint a picture
    4. Highly targeted juicy words that paint a pictur like resplendent

    {{~/system}}

    {{#user~}}
    {{essay}}
    {{~/user}}

    {{#assistant~}}
    {{gen 'grades' temperature=0 max_tokens=600}}
    {{~/assistant}}
    ''')

  return experts(essay=essay)

asyncio.run(setup_compiler())


if submitted:
  output = asyncio.run(run_grader(essay))
  st.write(output['grades'])
