import json

input_path='raw_posts.json'
output_path='processed_raw_posts.json'

def processed_text_to_utf(post):
    return post.encode('utf-8',errors='replace').decode('utf-8')

with open(input_path,'r',encoding='utf-8') as file:
    data=json.load(file)

for post in data:
    post['text']=processed_text_to_utf(post['text'])

with open(output_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print(f"Processed json file is saved to {output_path}")