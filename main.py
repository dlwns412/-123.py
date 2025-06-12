import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# ✅ 한글 폰트 설정
font_path = './fonts/NanumGothic.ttf'
if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    plt.rc('font', family='NanumGothic')
else:
    st.warning("❗ './fonts/NanumGothic.ttf' 폰트를 넣어주세요.")
plt.rcParams['axes.unicode_minus'] = False

# ✅ 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("감염병_발생현황월별_20250602121908.csv", encoding='cp949')
    return df

st.title("📊 성병 관련 감염병 월별 발생 현황 시각화")

df = load_data()

if df.empty:
    st.error("데이터를 불러오지 못했습니다.")
    st.stop()

# ✅ 감염병명에 해당하는 컬럼 자동 탐색
disease_col = next((col for col in df.columns if '감염병' in col), None)
month_col = next((col for col in df.columns if '월' in col or '시점' in col), None)
value_col = next((col for col in df.columns if '발생' in col or '건수' in col or '수' in col), None)

if not disease_col or not month_col or not value_col:
    st.error(f"❌ 필요한 컬럼이 없습니다.\n감염병: {disease_col}, 월: {month_col}, 값: {value_col}")
    st.dataframe(df.head())  # 디버깅용
    st.stop()

# ✅ 성병 키워드로 필터링
sti_keywords = ['성병', '클라미디아', '임질', '매독', '헤르페스', '에이즈', 'HIV']
df_sti = df[df[disease_col].astype(str).str.contains('|'.join(sti_keywords), na=False)]

if df_sti.empty:
    st.warning("성병 관련 데이터가 없습니다.")
    st.dataframe(df.head())  # 참고용 원본 데이터 출력
    st.stop()

# ✅ 감염병 선택
selected_disease = st.selectbox("🔽 감염병 선택", df_sti[disease_col].unique())
filtered = df_sti[df_sti[disease_col] == selected_disease].sort_values(by=month_col)

# ✅ 그래프 그리기
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(filtered[month_col], filtered[value_col], marker='o', color='tomato')
ax.set_title(f"{selected_disease} 월별 발생 추이")
ax.set_xlabel("월")
ax.set_ylabel("발생 수")
ax.grid(True)
st.pyplot(fig)
