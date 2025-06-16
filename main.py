import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

# 📌 한글 폰트 설정 (수정 금지)
font_path = "./font/NanumGothic.ttf"
fm.fontManager.addfont(font_path)
font_name = fm.FontProperties(fname=font_path).get_name()
plt.rcParams['font.family'] = font_name
plt.rcParams['axes.unicode_minus'] = False
sns.set(font=font_name)

# 🔄 데이터 로딩
@st.cache_data
def load_data():
    data_by_army = pd.read_csv("감염병_군별_발생현황_20250602122005.csv", encoding='cp949')
    data_by_age = pd.read_csv("감염병_발생현황연령별_20250602121946.csv", encoding='cp949')
    data_by_month = pd.read_csv("감염병_발생현황월별_20250602121908.csv", encoding='cp949')
    data_by_year_gender_age = pd.read_csv("감염병_연도별_및_연령별__성별_발생수_20250602121929.csv", encoding='cp949')
    return data_by_army, data_by_age, data_by_month, data_by_year_gender_age

# 📊 Streamlit UI 구성
st.set_page_config(layout="wide")
st.title("📊 성병 관련 감염병 발생 현황 시각화")

# 데이터 불러오기
army, age, month, year_gender_age = load_data()

# 🎯 성병 관련 키워드 필터링 함수
sti_keywords = ['성병', '클라미디아', '임질', '매독']

def filter_sti(df, column_name):
    if column_name in df.columns:
        return df[df[column_name].astype(str).str.contains('|'.join(sti_keywords), na=False)]
    return df  # fallback

# 📂 시각화 선택
section = st.sidebar.selectbox(
    "시각화 항목 선택",
    ["군별 발생 현황", "연령별 발생 현황", "월별 발생 현황", "연도/성별/연령별 발생"]
)

# 👇 항목별 그래프 (성병 키워드 필터 적용)
if section == "군별 발생 현황":
    st.header("군별 성병 감염병 발생 현황")
    filtered_army = filter_sti(army, army.columns[0])
    st.dataframe(filtered_army)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=filtered_army, x=filtered_army.columns[0], y=filtered_army.columns[1], ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif section == "연령별 발생 현황":
    st.header("👶👩‍🦳 연령별 성병 감염병 발생 현황")
    filtered_age = filter_sti(age, age.columns[0])
    st.dataframe(filtered_age)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=filtered_age, x=filtered_age.columns[0], y=filtered_age.columns[1], ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif section == "월별 발생 현황":
    st.header("🗓 월별 성병 감염병 발생 추이")
    filtered_month = filter_sti(month, month.columns[0])
    st.dataframe(filtered_month)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=filtered_month, x=filtered_month.columns[0], y=filtered_month.columns[1], marker='o', ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif section == "연도/성별/연령별 발생":
    st.header("📅 연도별 성병 감염병 발생 (성별/연령별)")
    filtered_year = filter_sti(year_gender_age, '감염병명') if '감염병명' in year_gender_age.columns else year_gender_age
    st.dataframe(filtered_year)
    if not filtered_year.empty:
        years = filtered_year['연도'].unique()
        selected_year = st.selectbox("연도 선택", sorted(years))
        year_filtered = filtered_year[filtered_year['연도'] == selected_year]
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=year_filtered, x='연령', y='발생수', hue='성별', ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.warning("성병 관련 데이터가 없습니다.")

