import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

# 한글 폰트 설정 (NanumGothic.ttf 경로 맞게 설정)
font_path = "NanumGothic.ttf"
fontprop = fm.FontProperties(fname=font_path).get_name()
sns.set(font=fontprop)

st.set_page_config(layout="wide")
st.title("📊 성병 관련 감염병 발생 현황 시각화")

@st.cache_data
def load_data():
    data_by_army = pd.read_csv("감염병_군별_발생현황_20250602122005.csv", encoding='cp949')
    data_by_age = pd.read_csv("감염병_발생현황연령별_20250602121946.csv", encoding='cp949')
    data_by_month = pd.read_csv("감염병_발생현황월별_20250602121908.csv", encoding='cp949')
    data_by_year_gender_age = pd.read_csv("감염병_연도별_및_연령별__성별_발생수_20250602121929.csv", encoding='cp949')
    return data_by_army, data_by_age, data_by_month, data_by_year_gender_age

army, age, month, year_gender_age = load_data()

section = st.sidebar.selectbox(
    "시각화 항목 선택",
    ["군별 발생 현황", "연령별 발생 현황", "월별 발생 현황", "연도/성별/연령별 발생"]
)

if section == "군별 발생 현황":
    st.header("🪖 군별 감염병 발생 현황")
    if army.empty:
        st.warning("군별 발생 데이터가 없습니다.")
    else:
        st.dataframe(army)
        army_x, army_y = army.columns[0], army.columns[1]
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=army, x=army_x, y=army_y, ax=ax)
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

elif section == "연령별 발생 현황":
    st.header("👶👩‍🦳 연령별 감염병 발생 현황")
    if age.empty:
        st.warning("연령별 발생 데이터가 없습니다.")
    else:
        st.dataframe(age)
        age_x, age_y = age.columns[0], age.columns[1]
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=age, x=age_x, y=age_y, ax=ax)
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

elif section == "월별 발생 현황":
    st.header("🗓 월별 감염병 발생 추이")
    if month.empty:
        st.warning("월별 발생 데이터가 없습니다.")
    else:
        st.dataframe(month)
        month_x, month_y = month.columns[0], month.columns[1]
        month[month_x] = pd.to_datetime(month[month_x], errors='coerce')
        month_sorted = month.sort_values(by=month_x)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=month_sorted, x=month_x, y=month_y, marker='o', ax=ax)
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

elif section == "연도/성별/연령별 발생":
    st.header("📅 연도별 및 성별/연령별 감염병 발생 수")
    if year_gender_age.empty:
        st.warning("연도별/성별/연령별 발생 데이터가 없습니다.")
    else:
        st.dataframe(year_gender_age)
        years = year_gender_age['연도'].unique()
        selected_year = st.selectbox("연도 선택", sorted(years))
        filtered = year_gender_age[year_gender_age['연도'] == selected_year]
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=filtered, x='연령', y='발생수', hue='성별', ax=ax)
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)
