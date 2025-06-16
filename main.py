import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

font_path = "./font/NanumGothic.ttf"
fm.fontManager.addfont(font_path)
font_name = fm.FontProperties(fname=font_path).get_name()
plt.rcParams['font.family'] = font_name
plt.rcParams['axes.unicode_minus'] = False
sns.set(font=font_name)

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

# 컬럼명 확인용 출력
st.write("연도/성별/연령별 데이터 컬럼명:", year_gender_age.columns.tolist())
st.write(year_gender_age.head())

# 성병 관련 키워드
sti_keywords = ["임질", "매독", "클라미디아", "헤르페스", "HIV", "에이즈", "성병"]

# 성병 관련 감염병만 필터링 (컬럼명 맞게 수정)
filtered_df = year_gender_age[
    year_gender_age['법정전염병군별(1)'].str.contains('|'.join(sti_keywords), case=False, na=False)
]

section = st.sidebar.selectbox(
    "시각화 항목 선택",
    ["군별 발생 현황", "연도/성별/연령별 발생(성병만)"]
)

if section == "군별 발생 현황":
    st.header("🪖 군별 감염병 발생 현황")
    st.dataframe(army)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=army, x=army.columns[0], y=army.columns[1], ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif section == "연도/성별/연령별 발생(성병만)":
    st.header("📅 연도별 및 성별/연령별 성병 발생 수")

    # 연도 선택박스는 필터된 데이터 기준으로
    years = filtered_df['연도'].unique()
    selected_year = st.selectbox("연도 선택", sorted(years))

    filtered_year = filtered_df[filtered_df['연도'] == selected_year]

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=filtered_year, x='법정전염병군별(2)', y='발생수', hue='성별', ax=ax)
    plt.xticks(rotation=45)
    plt.title(f"{selected_year}년 성별/연령별 성병 발생 수")
    plt.tight_layout()
    st.pyplot(fig)
