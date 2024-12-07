import json
import pandas as pd

class FewShots:
    def __init__(self,data_path='processed_path_file.json'):
        self.df=None
        self.unique_tags=None
        self.load_posts(data_path)

    def load_posts(self,data_path):
        with open(data_path,encoding='utf-8') as file:
            posts=json.load(file)
            self.df=pd.json_normalize(posts)
            print(self.df.head())
            self.df["length_type"]=self.df["line_count"].apply(self.length_type)
            print(self.df.head())
            all_tags=self.df["tags"].apply(lambda x: x).sum()
            self.unique_tags=set(list(all_tags))

    def length_type(self,length):
        if length<5:
            return "Short"
        elif 5<=length<=15:
            return "Medium"
        else:
            return "Long"
    
    def get_filtered_posts(self, length, language, tag):
        df_filtered = self.df[
            (self.df['tags'].apply(lambda tags: tag in tags)) &  
            (self.df['language'] == language) &  
            (self.df['length_type'] == length)  
        ]
        return df_filtered.to_dict(orient='records')
    
    def get_tag(self):
        return self.unique_tags

if __name__=="__main__":
    f=FewShots()
    post=f.get_filtered_posts("Medium","English","Job Search")
    print(len(post))
