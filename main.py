import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

# 한글 폰트 설정
plt.rc('font', family='NanumGothic')
plt.rcParams['axes.unicode_minus'] = False

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

# 성병 관련 키워드 리스트
sti_keywords = ['성병', '임질', '매독', '클라미디아', '콘딜로마', '헤르페스']

def filter_sti_data(df, disease_col):
    mask = df[disease_col].str.contains('|'.join(sti_keywords))
    return df[mask]

section = st.sidebar.selectbox(
    "시각화 항목 선택",
    ["군별 발생 현황", "연령별 발생 현황", "월별 발생 현황", "연도/성별/연령별 발생"]
)

sns.set_style("whitegrid")
palette = sns.color_palette("Set2")

if section == "군별 발생 현황":
    st.header("군별 성병 감염병 발생 현황")
    # '질병명' 컬럼 기준 필터링 (예: army 데이터에 '질병명' 컬럼 있을 때)
    army_sti = filter_sti_data(army, army.columns[0])  # 컬럼명 수정 필요시 바꾸세요
    st.dataframe(army_sti)

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=army_sti, x=army_sti.columns[1], y=army_sti.columns[2], palette=palette, ax=ax)
    ax.set_xlabel(army_sti.columns[1], fontsize=12)
    ax.set_ylabel(army_sti.columns[2], fontsize=12)
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif section == "연령별 발생 현황":
    st.header("👶👩‍🦳 연령별 성병 감염병 발생 현황")
    age_sti = filter_sti_data(age, age.columns[0])
    st.dataframe(age_sti)

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=age_sti, x=age_sti.columns[1], y=age_sti.columns[2], palette=palette, ax=ax)
    ax.set_xlabel(age_sti.columns[1], fontsize=12)
    ax.set_ylabel(age_sti.columns[2], fontsize=12)
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif section == "월별 발생 현황":
    st.header("🗓 월별 성병 감염병 발생 추이")
    month_sti = filter_sti_data(month, month.columns[0])
    st.dataframe(month_sti)

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=month_sti, x=month_sti.columns[1], y=month_sti.columns[2], marker='o', color=palette[0], ax=ax)
    ax.set_xlabel(month_sti.columns[1], fontsize=12)
    ax.set_ylabel(month_sti.columns[2], fontsize=12)
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif section == "연도/성별/연령별 발생":
    st.header("📅 연도별 및 성별/연령별 성병 감염병 발생 수")
    year_gender_age_sti = filter_sti_data(year_gender_age, '질병명')  # '질병명' 컬럼명 실제 데이터에 맞게 수정
    st.dataframe(year_gender_age_sti)

    years = year_gender_age_sti['연도'].unique()
    selected_year = st.selectbox("연도 선택", sorted(years))

    filtered = year_gender_age_sti[year_gender_age_sti['연도'] == selected_year]

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=filtered, x='연령', y='발생수', hue='성별', palette=palette, ax=ax)
    ax.set_xlabel('연령', fontsize=12)
    ax.set_ylabel('발생수', fontsize=12)
    plt.xticks(rotation=45)
    st.pyplot(fig)
