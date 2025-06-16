import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

# 한글 폰트 경로
font_path = "./font/NanumGothic.ttf"

# 폰트 등록 및 설정
fm.fontManager.addfont(font_path)
font_name = fm.FontProperties(fname=font_path).get_name()
plt.rcParams['font.family'] = font_name
plt.rcParams['axes.unicode_minus'] = False
sns.set(font=font_name)

# 페이지 설정
st.set_page_config(layout="wide")
st.title("📊 성병 관련 감염병 발생 현황 시각화")

@st.cache_data
def load_data():
    data_by_army = pd.read_csv("감염병_군별_발생현황_20250602122005.csv", encoding='cp949')
    data_by_year_gender_age = pd.read_csv("감염병_연도별_및_연령별__성별_발생수_20250602121929.csv", encoding='cp949')
    return data_by_army, data_by_year_gender_age

army, year_gender_age = load_data()

section = st.sidebar.selectbox(
    "시각화 항목 선택",
    ["군별 발생 현황", "연도/성별/연령별 발생"]
)

# 군별 발생 현황 (변경 없음)
if section == "군별 발생 현황":
    st.header(" 군별 감염병 발생 현황 (성병 관련)")
    sti_keywords = ['클라미디아', '임질', '매독', '성병', '성매개', '에이즈', 'HIV']
    sti_df = army[army['법정감염병군별(2)'].str.contains('|'.join(sti_keywords), case=False, na=False)]

    if sti_df.empty:
        st.warning("성병 관련 데이터가 없습니다.")
    else:
        st.dataframe(sti_df)

        year_columns = [col for col in sti_df.columns if col.startswith("20")]
        melted = sti_df.melt(id_vars=['법정감염병군별(2)'], value_vars=year_columns,
                             var_name='연도', value_name='발생수')

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=melted, x='연도', y='발생수', hue='법정감염병군별(2)', ax=ax)
        ax.set_title("연도별 성병 관련 감염병 발생 현황")
        plt.xticks(rotation=45)
        st.pyplot(fig)

# 연도/성별/연령별 발생 (감염병명 컬럼 없을 경우 병명 합쳐서 필터링)
elif section == "연도/성별/연령별 발생":
    st.header("📅 연도별 및 성별/연령별 감염병 발생 수 (성병 관련)")

    # 컬럼명 확인용 (한번만 보고 지워도 됨)
    # st.write("컬럼명 확인용:", year_gender_age.columns)

    sti_keywords = ['클라미디아', '임질', '매독', '성병', '성매개', '에이즈', 'HIV']

    if '감염병명' in year_gender_age.columns:
        filtered_df = year_gender_age[year_gender_age['감염병명'].str.contains('|'.join(sti_keywords), case=False, na=False)]
    else:
        # '법정감염병군별(1)'과 '법정감염병군별(2)' 합쳐서 텍스트 생성
        year_gender_age['병명합치기'] = year_gender_age['법정감염병군별(1)'].astype(str) + " " + year_gender_age['법정감염병군별(2)'].astype(str)
        filtered_df = year_gender_age[year_gender_age['병명합치기'].str.contains('|'.join(sti_keywords), case=False, na=False)]

    if filtered_df.empty:
        st.warning("성병 관련 데이터가 없습니다.")
    else:
        years = sorted(filtered_df['연도'].unique())
        selected_year = st.selectbox("연도 선택", years)

        year_filtered = filtered_df[filtered_df['연도'] == selected_year]

        age_order = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80 이상']
        year_filtered['연령'] = pd.Categorical(year_filtered['연령'], categories=age_order, ordered=True)

        fig, ax = plt.subplots(figsize=(10, 6))
        hue_col = '성별' if '성별' in year_filtered.columns else None
        sns.barplot(data=year_filtered, x='연령', y='발생수', hue=hue_col, ax=ax)
        ax.set_title(f"{selected_year}년 성별 및 연령별 성병 발생 수")
        plt.xticks(rotation=0)
        ax.set_xlabel("연령대")
        ax.set_ylabel("발생 수")
        st.pyplot(fig)
