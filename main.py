import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager, rc
import os

# 📁 폰트 경로 설정
font_path = os.path.join("fonts", "NanumGothic.ttf")
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)
plt.rcParams['axes.unicode_minus'] = False

# 🎯 STI 관련 키워드 정의
sti_keywords = ['성병', 'HIV', '임질', '매독', '클라미디아', '성매개']

# 📊 데이터 로드
@st.cache_data
def load_data():
    df = pd.read_csv("감염병_연도별_및_연령별__성별_발생수_20250602121929.csv", encoding='cp949')  # 또는 utf-8-sig 시도
    return df

df = load_data()

# 🔍 STI 감염병만 필터링
sti_df = df[df['감염병명'].str.contains('|'.join(sti_keywords), case=False, na=False)]

# 🖼️ 시각화
st.title("성병(STI) 발생 현황 시각화")

# 📌 연도별 성병 발생 수 합계 그래프
grouped = sti_df.groupby('연도')['발생수'].sum().reset_index()

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=grouped, x='연도', y='발생수', marker='o', ax=ax)
ax.set_title("연도별 성병 발생수 추이", fontsize=16)
ax.set_ylabel("발생 수")
ax.set_xlabel("연도")
st.pyplot(fig)
