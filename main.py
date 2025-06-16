import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

# 폰트 설정 (여기 건들지 마세요)
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
    df = pd.read_csv("감염병_연도별_및_연령별__성별_발생수_20250602121929.csv", encoding='cp949')
    return df

df = load_data()

# 성병 관련 키워드
sti_keywords = ['클라미디아', '매독', 'HIV', '성병']

# '법정전염병군별(1)'과 '(2)' 합쳐서 텍스트 생성
df['병명합치기'] = df['법정전염병군별(1)'].astype(str) + " " + df['법정전염병군별(2)'].astype(str)

# 키워드 포함된 행 필터링
filtered_df = df[df['병명합치기'].str.contains('|'.join(sti_keywords), case=False, na=False)]

st.write("### 필터링된 데이터 미리보기", filtered_df.head())

# 시간(주차) 컬럼들만 뽑아서 그래프 그리기 준비
time_cols = [col for col in filtered_df.columns if col.replace('.', '', 1).isdigit()]

# 행별로 시간 컬럼들 값 평균을 내는 예시 (원하는 시각화 방식에 맞게 바꿔야 함)
filtered_df['발생수합계'] = filtered_df[time_cols].sum(axis=1)

st.write("### 성병 감염병별 발생수 합계")
st.dataframe(filtered_df[['병명합치기', '발생수합계']])

# 예시로 군별 막대그래프
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=filtered_df, x='병명합치기', y='발생수합계', ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)
