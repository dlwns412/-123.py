import streamlit as st
import pandas as pd

df = pd.read_csv("감염병_발생현황월별_20250602121908.csv", encoding="cp949")
st.write("컬럼명 리스트:", df.columns.tolist())  # 컬럼명 리스트 보여줌
st.write("데이터 미리보기:", df.head())        # 데이터 샘플도 보여줌
