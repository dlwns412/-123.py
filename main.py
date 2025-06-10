import matplotlib.pyplot as plt
from matplotlib import font_manager
import os

# 폰트 경로 설정
font_path = os.path.join("fonts", "NanumGothic.ttf")  # 파일명이 정확해야 해
font_prop = font_manager.FontProperties(fname=font_path)

# 한글 폰트 적용
plt.rcParams['font.family'] = font_prop.get_name()
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager
import os

# ✅ 폰트 설정
font_path = os.path.join("fonts", "NanumGothic.ttf")
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

# ✅ 데이터 로드
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("감염병_연도별_및_연령별__성별_발생수_20250602121929.csv", encoding='utf-8')
    except:
        df = pd.read_csv("감염병_연도별_및_연령별__성별_발생수_20250602121929.csv", encoding='cp949')
    return df

df = load_data()

# ✅ 성병 데이터 필터링
sti_keywords = ['성병', 'HIV', '임질', '매독', '클라미디아', '성매개']
df_sti = df[df['감염병명'].str.contains('|'.join(sti_keywords), na=False)]

grouped = df_sti.groupby('연도')['발생수'].sum().reset_index()

# ✅ 그래프
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=grouped, x='연도', y='발생수', marker='o', ax=ax)
ax.set_title("성병 발생 추이", fontproperties=font_prop)
ax.set_xlabel("연도", fontproperties=font_prop)
ax.set_ylabel("발생 수", fontproperties=font_prop)
st.pyplot(fig)
