import streamlit as st
import duckdb
import pandas as pd

from user_codes.chatbot import get_tablenames,sql_code_generator,run_sql_query #,load_dataset


def main():
    st.set_page_config(page_title="NL2SQL", page_icon=":bar_chart:", layout="wide")
    st.markdown("""
        <h1 style="text-align: center; color: #4CAF50;">NL2SQL</h1>
        <p style="text-align: center; font-size: 20px; color: #777;">
             Natural Language to SQL converter.
        </p>       
    """, unsafe_allow_html=True)

    # Load dataset from Kaggle and store into store.db
    # load_dataset()

    tables_names = get_tablenames()

    table_list = list(tables_names.keys())
    tname = st.sidebar.selectbox("Tables", table_list)
    tdf= pd.DataFrame({tname: tables_names[tname]})
    st.sidebar.markdown("Table Names", unsafe_allow_html=True)
    st.sidebar.dataframe(tdf)


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
