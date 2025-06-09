import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")
st.title("성병 관련 감염병 발생 현황 시각화")

# 파일 업로드
@st.cache_data
def load_data():
    data_by_army = pd.read_csv("감염병_군별_발생현황_20250602122005.csv", encoding='utf-8')
    data_by_age = pd.read_csv("감염병_발생현황연령별_20250602121946.csv", encoding='utf-8')
    data_by_month = pd.read_csv("감염병_발생현황월별_20250602121908.csv", encoding='utf-8')
    data_by_year_gender_age = pd.read_csv("감염병_연도별_및_연령별__성별_발생수_20250602121929.csv", encoding='utf-8')
    return data_by_army, data_by_age, data_by_month, data_by_year_gender_age

army, age, month, year_gender_age = load_data()

# 시각화 섹션 선택
section = st.sidebar.selectbox(
    "시각화 선택", 
    ["군별 발생 현황", "연령별 발생 현황", "월별 발생 현황", "연도/성별/연령별 발생"]
)

# 군별 발생 현황
if section == "군별 발생 현황":
    st.header("📌 군별 감염병 발생 현황")
    st.dataframe(army)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=army, x=army.columns[0], y=army.columns[1], ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# 연령별 발생 현황
elif section == "연령별 발생 현황":
    st.header("📌 연령별 감염병 발생 현황")
    st.dataframe(age)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=age, x=age.columns[0], y=age.columns[1], ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# 월별 발생 현황
elif section == "월별 발생 현황":
    st.header("📌 월별 감염병 발생 현황")
    st.dataframe(month)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=month, x=month.columns[0], y=month.columns[1], marker="o", ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# 연도별, 성별, 연령별 발생수
elif section == "연도/성별/연령별 발생":
    st.header("📌 연도별 및 성별/연령별 감염병 발생 수")
    st.dataframe(year_gender_age)
    selected_year = st.selectbox("연도 선택", year_gender_age['연도'].unique())
    filtered = year_gender_age[year_gender_age['연도'] == selected_year]

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=filtered, x='연령', y='발생수', hue='성별', ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)
