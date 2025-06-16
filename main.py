import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

# 🎨 한글 폰트 설정
font_path = "NanumGothic.ttf"
fontprop = fm.FontProperties(fname=font_path).get_name()
plt.rc('font', family=fontprop)
sns.set(style="whitegrid")

# 📊 페이지 설정
st.set_page_config(layout="wide")
st.title("📈 성병 관련 감염병 발생 현황 시각화")

# 🔄 데이터 로딩
@st.cache_data
def load_data():
    data_by_army = pd.read_csv("감염병_군별_발생현황_20250602122005.csv", encoding='cp949')
    data_by_age = pd.read_csv("감염병_발생현황연령별_20250602121946.csv", encoding='cp949')
    data_by_month = pd.read_csv("감염병_발생현황월별_20250602121908.csv", encoding='cp949')
    data_by_year_gender_age = pd.read_csv("감염병_연도별_및_연령별__성별_발생수_20250602121929.csv", encoding='cp949')
    return data_by_army, data_by_age, data_by_month, data_by_year_gender_age

# 📁 데이터 불러오기
army, age, month, year_gender_age = load_data()

# 🎯 성병 키워드 정의
sti_keywords = ['클라미디아', '매독', '임질', '성병']

def filter_sti_data(df, column_name):
    if column_name in df.columns:
        mask = df[column_name].astype(str).str.contains('|'.join(sti_keywords), na=False)
        return df[mask]
    return df

# 데이터 필터링
army_sti = filter_sti_data(army, '감염병명') if '감염병명' in army.columns else army
age_sti = filter_sti_data(age, '감염병명') if '감염병명' in age.columns else age
month_sti = filter_sti_data(month, '감염병명') if '감염병명' in month.columns else month
year_gender_age_sti = filter_sti_data(year_gender_age, '감염병명') if '감염병명' in year_gender_age.columns else year_gender_age

# 📌 시각화 선택
section = st.sidebar.selectbox(
    "성병 관련 시각화 항목 선택",
    ["군별 발생 현황", "연령별 발생 현황", "월별 발생 추이", "연도/성별/연령별"]
)

# ——————————— 시각화 ———————————

if section == "군별 발생 현황":
    st.header("🪖 성병 관련 군별 감염병 발생")
    if not army_sti.empty:
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=army_sti, x=army_sti.columns[0], y=army_sti.columns[1], palette='Set2', ax=ax)
        ax.set_title("군별 성병 감염병 발생", fontsize=14)
        ax.set_xlabel("군 구분")
        ax.set_ylabel("발생 건수")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.warning("성병 관련 데이터가 없습니다.")

elif section == "연령별 발생 현황":
    st.header("🧒 연령별 성병 발생")
    if not age_sti.empty:
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=age_sti, x=age_sti.columns[0], y=age_sti.columns[1], hue=age_sti.columns[2], ax=ax, palette='pastel')
        ax.set_title("연령대별 성병 감염병", fontsize=14)
        ax.set_xlabel("연령대")
        ax.set_ylabel("발생 건수")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.warning("성병 관련 데이터가 없습니다.")

elif section == "월별 발생 추이":
    st.header("📆 성병 월별 발생 추이")
    if not month_sti.empty:
        fig, ax = plt.subplots(figsize=(12, 5))
        sns.lineplot(data=month_sti, x=month_sti.columns[0], y=month_sti.columns[1], marker='o', hue=month_sti[month_sti.columns[2]], ax=ax)
        ax.set_title("월별 성병 발생 추이", fontsize=14)
        ax.set_xlabel("월")
        ax.set_ylabel("발생 건수")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.warning("성병 관련 데이터가 없습니다.")

elif section == "연도/성별/연령별":
    st.header("📊 연도별 성병 발생 (연령 & 성별)")
    if not year_gender_age_sti.empty:
        years = year_gender_age_sti['연도'].unique()
        selected_year = st.selectbox("연도 선택", sorted(years))
        filtered = year_gender_age_sti[year_gender_age_sti['연도'] == selected_year]
        fig, ax = plt.subplots(figsize=(12, 5))
        sns.barplot(data=filtered, x='연령', y='발생수', hue='성별', palette='Set1', ax=ax)
        ax.set_title(f"{selected_year}년 성병 감염병 발생 (성별/연령별)", fontsize=14)
        ax.set_xlabel("연령")
        ax.set_ylabel("발생 건수")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.warning("성병 관련 데이터가 없습니다.")
