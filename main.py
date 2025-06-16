import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

# 한글 폰트 설정 (NanumGothic.ttf는 프로젝트 폴더 내에 있어야 합니다)
font_path = "NanumGothic.ttf"
fontprop = fm.FontProperties(fname=font_path).get_name()
sns.set(font=fontprop)

# 페이지 설정
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

# ——— 성병 관련 키워드 리스트 ———
sti_keywords = ['클라미디아', '매독', '임질', '성병']

def filter_sti_data(df, col_name):
    if col_name in df.columns:
        mask = df[col_name].astype(str).str.contains('|'.join(sti_keywords))
        return df[mask]
    return df

# 데이터별 성병 관련 필터링 (컬럼명에 맞게 수정하세요)
army = filter_sti_data(army, '감염병명')              # 예: '감염병명' 컬럼이 있으면
age = filter_sti_data(age, '감염병명')
month = filter_sti_data(month, '감염병명')
year_gender_age = filter_sti_data(year_gender_age, '감염병명')

# 이후 기존 시각화 코드는 그대로 사용하세요
section = st.sidebar.selectbox(
    "시각화 항목 선택",
    ["군별 발생 현황", "연령별 발생 현황", "월별 발생 현황", "연도/성별/연령별 발생"]
)

if section == "군별 발생 현황":
    st.header("🪖 군별 감염병 발생 현황")
    st.dataframe(army)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=army, x=army.columns[0], y=army.columns[1], ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif section == "연령별 발생 현황":
    st.header("👶👩‍🦳 연령별 감염병 발생 현황")
    st.dataframe(age)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=age, x=age.columns[0], y=age.columns[1], ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif section == "월별 발생 현황":
    st.header("🗓 월별 감염병 발생 추이")
    st.dataframe(month)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=month, x=month.columns[0], y=month.columns[1], marker='o', ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif section == "연도/성별/연령별 발생":
    st.header("📅 연도별 및 성별/연령별 감염병 발생 수")
    st.dataframe(year_gender_age)
    years = year_gender_age['연도'].unique()
    selected_year = st.selectbox("연도 선택", sorted(years))
    filtered = year_gender_age[year_gender_age['연도'] == selected_year]
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=filtered, x='연령', y='발생수', hue='성별', ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)
