import json
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from llm import llm

def preprocess(raw_path_file,processed_path_file):
    enriched_data=[]
    with open(raw_path_file,encoding='utf-8',errors='replace') as file:
        posts=json.load(file)
        for post in posts:
            metadata=extract_metadata(post['text'])
            print(metadata)
            refined_posts=post|metadata
            enriched_data.append(refined_posts)
            # print(enriched_data)
    tags_mapping=get_unique_tags(enriched_data)

    for post in enriched_data:
        tags=post['tags']
        new_tags={tags_mapping[tag] for tag in tags}
        post['tags']=list(new_tags)

    with open(processed_path_file, 'w', encoding='utf-8') as file:
        json.dump(enriched_data, file, indent=4)


def get_unique_tags(enriched_data):
    tag_set=set()
    for data in enriched_data:
        tag_set.update(data['tags'])
    tag_set_list=','.join(tag_set)

    template = '''
    I will give you a list of tags. You need to unify tags with the following requirements,
    1. Tags are unified and merged to create a shorter list. 
       Example 1: "Jobseekers", "Job Hunting" can be all merged into a single tag "Job Search". 
       Example 2: "Motivation", "Inspiration", "Drive" can be mapped to "Motivation"
       Example 3: "Personal Growth", "Personal Development", "Self Improvement" can be mapped to "Self Improvement"
       Example 4: "Scam Alert", "Job Scam" etc. can be mapped to "Scams"
    2. Each tag should be follow title case convention. example: "Motivation", "Job Search"
    3. Output should be a JSON object, No preamble
    3. Output should have mapping of original tag and the unified tag. 
       For example: {{"Jobseekers": "Job Search",  "Job Hunting": "Job Search", "Motivation": "Motivation}}
    
    Here is the list of tags: 
    {tags}
    '''
    template=PromptTemplate.from_template(template)
    chain=template|llm
    response=chain.invoke(input={'tags':str(tag_set_list)})
    try:
        json_parser=JsonOutputParser()
        res=json_parser.parse(response.content)
    except:
        raise OutputParserException("The content is so much. Please reduce.")
    
    return res
    
def extract_metadata(text):
    template="""
    You are given a LinkedIn post. You need to extract number of lines, language of the post and tags.
    1. Return a valid JSON. No preamble. 
    2. JSON object should have exactly three keys: line_count, language and tags. 
    3. tags is an array of text tags. Extract maximum two tags.
    4. Language should be English or Hinglish (Hinglish means hindi + english)
    
    Here is the actual post on which you need to perform this task:  
    {text}
    """
    prompt_template=PromptTemplate.from_template(template)
    chain=prompt_template|llm
    response=chain.invoke(input={"text": text})
    
    try:
        json_parser=JsonOutputParser()
        res=json_parser.parse(response.content)
    except:
        raise OutputParserException("The content is so much. Please reduce.")
    
    return res


if __name__=="__main__":
    preprocess('raw_posts.json','processed_path_file.json')
