from llm import llm
from fewshots import FewShots
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq

fs=FewShots()

def get_length_str(length):
    if length=="Short":
        return "Write in 1-5 lines"
    elif length=="Medium":
        return "Write in 5-15 lines"
    else:
        return "Write in more than 15 lines"
    
def Generate_Response_from_LLM(tags,length,language):
    prompt=Generate_prompt(tags,length,language)
    print(prompt)
    response=llm.invoke(prompt)
    return response

def Generate_prompt(tags,length,language):
    length_str=get_length_str(length)
    prompt=f"""
    Generate a LinkedIn post using the below information. No preamble.

    1) Topic: {tags}
    2) Length: {length_str}
    3) Language: {language}
    If Language is Hinglish then it means it is a mix of Hindi and English. 
    The script for the generated post should always be English.
    """

    examples=fs.get_filtered_posts(length,language,tags)
    if len(examples)>0:
        prompt+='4) Use the writing style as per the following examples.'

    print(len(examples))

    for i,post in enumerate(examples):
        post_text=post["text"]
        prompt+=f'\n\nexample{i+1}: \n{post_text}'
        if i==1:
            break
    return prompt


if __name__=="__main__":
    print(Generate_Response_from_LLM("Job Search","Short","English"))

