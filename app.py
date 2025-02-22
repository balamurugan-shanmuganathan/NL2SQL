import streamlit as st
import pandas as pd

from user_codes.chatbot import get_tablenames,sql_code_generator,run_sql_query #,load_dataset


def main():
    st.set_page_config(page_title="NL2SQL", page_icon=":bar_chart:")
    st.markdown("""
        <h1 style="text-align: center; color: #4CAF50;">NL2SQL</h1>
        <p style="text-align: center; font-size: 20px; color: #777;">Natural Language to SQL converter.</p>     
    """, unsafe_allow_html=True)

    github_repo_url="https://github.com/balamurugan-shanmuganathan/NL2SQL"
    kaggle_url = "https://www.kaggle.com/datasets/andrexibiza/grocery-sales-dataset"

    st.markdown(f"""
        <style>
            .github-icon {{
                position: absolute;
                top: 10px;
                right: 20px;
            }}
        </style>

        <a href="{github_repo_url}" class="github-icon" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png"  alt="GitHub Logo" width="30"/>
            View on GitHub
        </a>
        <a href="{kaggle_url}" class="top-right" target="_blank">Dataset:
        <img src="https://nlposs.github.io/2018/img/kaggle.png" alt="Kaggle Logo" width="80"/>
        </a><br><br>
    """, unsafe_allow_html=True)



    with st.expander("DataBase Details"):
        st.image("database_details.png", caption="Sample Image", use_container_width =True)

    # Load dataset from Kaggle and store into store.db
    # load_dataset()

    tables_names = get_tablenames()

    if prompt := st.chat_input("Enter your query to filter the population"):
        with st.chat_message("user"):
            st.markdown(f"**You asked:** {prompt}")

        with st.chat_message("assistant"):
            sql_code = sql_code_generator(prompt,tables_names)
            st.code(sql_code, language="sql")
            result=run_sql_query(sql_code)
            st.dataframe(result)  # Display dataframe

if __name__ == "__main__":
    main()
