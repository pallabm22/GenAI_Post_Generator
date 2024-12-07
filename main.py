from fewshots import FewShots
import streamlit as st
from post_generator import Generate_Response_from_LLM
def main():
    fs=FewShots()
    st.title("Post Generator")
    col1,col2,col3=st.columns(3)

    with col1:
        selected_tag=st.selectbox("Title",options=fs.get_tag())

    with col2:
        length_type=["Short","Medium","Long"]
        selected_length=st.selectbox("Length",options=length_type)

    with col3:
        selected_language=st.selectbox("Language", options=set(fs.df["language"]))

    post=Generate_Response_from_LLM(selected_tag,selected_length,selected_language)
    if st.button("Generate"):
        st.write(post.content)

if __name__=="__main__":
    main()