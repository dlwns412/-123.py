import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ✅ 한글 폰트 설정
font_path = "./fonts/NanumGothic.ttf"  # 폰트 위치
fontprop = fm.FontProperties(fname=font_path, size=12)
plt.rc('font', family=fontprop.get_name())
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지

# ✅ 데이터 불러오기 함수
@st.cache_data
def load_data():
    encodings = ['utf-8', 'cp949', 'euc-kr']
    paths = {
        "army": "감염병_군별_발생현황_20250602122005.csv",
        "age": "감염병_발생현황연령별_20250602121946.csv",
        "month": "감염병_발생현황월별_20250602121908.csv",
        "year_gender_age": "감염병_연도별_및_연령별__성별_발생수_20250602121929.csv",
    }

    data = {}
    for key, path in paths.items():
        for enc in encodings:
            try:
                df = pd.read_csv(path, encoding=enc)
                df.columns = df.columns.str.strip()  # 공백 제거
                data[key] = df
                break
            except Exception:
                continue
        else:
            st.error(f"'{path}' 파일을 열 수 없습니다. 인코딩 문제일 수 있습니다.")
            data[key] = pd.DataFrame()
    
    return data["army"], data["age"], data["month"], data["year_gender_age"]

# ✅ 데이터 불러오기
army_df, age_df, month_df, year_gender_age_df = load_data()

# ✅ 제목
st.title("📊 성병 관련 감염병 시각화")

# ✅ 성병 키워드 필터링
sti_keywords = ['성병', '임질', '클라미디아', '매독', '에이즈']

# 월별 데이터 중 성병만 필터링
if not month_df.empty and '감염병명' in month_df.columns:
    sti_df = month_df[month_df['감염병명'].str.contains('|'.join(sti_keywords), na=False)]

    st.subheader("📅 월별 성병 발생 추이")
    fig, ax = plt.subplots(figsize=(10, 5))

    for disease in sti_df['감염병명'].unique():
        subset = sti_df[sti_df['감염병명'] == disease]
        ax.plot(subset['월'], subset['발생건수'], marker='o', label=disease)

    ax.set_xlabel("월")
    ax.set_ylabel("발생건수")
    ax.legend(prop=fontprop)
    st.pyplot(fig)
else:
    st.warning("월별 데이터가 없거나 '감염병명' 컬럼이 존재하지 않습니다.")
