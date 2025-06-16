import streamlit as st
import pandas as pd

df = pd.read_csv("감염병_군별_발생현황_20250602122005.csv", encoding="cp949")
st.write("✅ 데이터 샘플:")
st.dataframe(df)
st.write("✅ 컬럼명:")
st.write(df.columns.tolist())
