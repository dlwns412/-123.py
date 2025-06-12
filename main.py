mport pandas as pd
import streamlit as st

df = pd.read_csv("감염병_발생현황월별_20250602121908.csv", encoding="cp949")

st.write("데이터 컬럼명:", df.columns.tolist())  # 컬럼명을 리스트 형태로 출력
st.write("데이터 미리보기:", df.head())       # 데이터 상위 5개 행 출력
