import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

# 한글 폰트 설정
font_path = "font/NanumGothic.ttf"  # 폰트 폴더와 파일명 확인해서 맞게 수정
fontprop = fm.FontProperties(fname=font_path).get_name()
sns.set(font=fontprop)

# 페이지 설정
st.set_page_config(layout="wide")
st.title("📊 감염병 발생 현황 시각화")

@st.cache_data
def load_data():
    army = pd.read_csv("감염병_군별_발생현황_20250602122005.csv", encoding='cp949')
    age = pd.read_csv("감염병_발생현황연령별_20250602121946.csv", encoding='cp949')
    month = pd.read_csv("감염병_발생현황월별_20250602121908.csv", encoding='cp949')
    year_gender_age = pd.read_csv("감염병_연도별_및_연령별__성별_발생.csv", encoding='cp949')
    return army, age, month, year_gender_age

army, age, month, year_gender_age = load_data()

section = st.sidebar.selectbox(
    "시각화 항목 선택",
    ["군별 발생 현황", "연령별 발생 현황", "월별 발생 현황", "연도/성별/연령별 발생"]
)

if section == "군별 발생 현황":
    st.header("🪖 군별 감염병 발생 현황")
    st.dataframe(army)
    x_col, y_col = army.columns[0], army.columns[1]
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=army, x=x_col, y=y_col, ax=ax)
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

elif section == "연령별 발생 현황":
    st.header("👶👩‍🦳 연령별 감염병 발생 현황")
    st.dataframe(age)
    x_col, y_col = age.columns[0], age.columns[1]
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=age, x=x_col, y=y_col, ax=ax)
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

elif section == "월별 발생 현황":
    st.header("🗓 월별 감염병 발생 추이")
    st.dataframe(month)
    x_col, y_col = month.columns[0], month.columns[1]
    # 날짜 컬럼이 날짜형이 아니면 변환 (에러 방지용)
    month[x_col] = pd.to_datetime(month[x_col], errors='coerce')
    month_sorted = month.sort_values(x_col)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=month_sorted, x=x_col, y=y_col, marker='o', ax=ax)
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

elif section == "연도/성별/연령별 발생":
    st.header("📅 연도별/성별/연령별 감염병 발생 수")
    st.dataframe(year_gender_age)
    years = year_gender_age['연도'].unique()
    selected_year = st.selectbox("연도 선택", sorted(years))
    filtered = year_gender_age[year_gender_age['연도'] == selected_year]
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=filtered, x='연령', y='발생수', hue='성별', ax=ax)
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)
