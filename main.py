import streamlit as st
import pandas as pd

df = pd.read_csv("감염병_연도별_및_연령별__성별_발생수_20250602121929.csv", encoding="cp949")

st.write("데이터 컬럼명 리스트:")
st.write(df.columns.tolist())

st.write("데이터 샘플 (상위 5개 행):")
st.write(df.head())
