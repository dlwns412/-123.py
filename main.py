import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# 🔤 한글 폰트 설정 (NanumGothic.ttf가 fonts 폴더에 있어야 함)
font_path = './fonts/NanumGothic.ttf'  # GitHub에 올릴 땐 이 경로 기준
if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    plt.rc('font', family='NanumGothic')
else:
    st.warning("❗ 폰트 파일(NanumGothic.ttf)을 './fonts' 폴더에 넣어주세요.")
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지

# 🧺 데이터 불러오기
@st.cache_data
def load_monthly_data():
    try:
        df = pd.read_csv("감염병_발생현황월별_20250602121908.csv", encoding='cp949')
        return df
    except Exception as e:
        st.error(f"파일 불러오기 오류: {e}")
        return pd.DataFrame()

# 🔍 성병 키워드
sti_keywords = ['성병', '클라미디아', '임질', '매독', '헤르페스', '에이즈', 'HIV']

# 📈 앱 시작
st.title("📊 성병 관련 감염병 월별 발생 현황 시각화")

df = load_monthly_data()

# 📌 컬럼명 확인 (디버깅용)
if df.empty:
    st.stop()

st.subheader("📋 원본 데이터 컬럼명")
st.write(df.columns.tolist())  # 컬럼명을 보여줘서 KeyError 방지

# 💡 '감염병명'이라는 컬럼이 있는지 확인
disease_col = None
for col in df.columns:
    if '감염병' in col:
        disease_col = col
        break

if not disease_col:
    st.error("❌ '감염병명' 관련 컬럼이 없습니다.")
    st.stop()

# 🔍 성병 관련 데이터 필터링
df_sti = df[df[disease_col].astype(str).str.contains('|'.join(sti_keywords), na=False)]

if df_sti.empty:
    st.warning("성병 관련 데이터가 없습니다.")
else:
    st.subheader("📊 성병 월별 발생 건수")
    selected_disease = st.selectbox("🔽 감염병 선택", df_sti[disease_col].unique())

    filtered = df_sti[df_sti[disease_col] == selected_disease]

    # 월별로 정렬 시도 (정확한 컬럼명 자동 감지)
    month_col = None
    for col in df_sti.columns:
        if '월' in col or '시점' in col:
            month_col = col
            break

    value_col = None
    for col in df_sti.columns:
        if '발생' in col or '건수' in col or '수' in col:
            value_col = col
            break

    if month_col and value_col:
        filtered = filtered.sort_values(by=month_col)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(filtered[month_col], filtered[value_col], marker='o', color='tomato')
        ax.set_title(f"{selected_disease} 월별 발생 추이")
        ax.set_xlabel("월")
        ax.set_ylabel("발생 수")
        ax.grid(True)
        st.pyplot(fig)
    else:
        st.error("❌ 월 또는 발생 수 관련 컬럼이 없습니다.")
