import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import matplotlib.font_manager as fm

# 한글 폰트 설정
font_path = 'fonts/NanumGothic.ttf'
fontprop = fm.FontProperties(fname=font_path)
plt.rc('font', family=fontprop.get_name())

# 데이터 로딩
df = pd.read_csv("감염병_발생현황월별_20250602121908.csv", encoding="cp949")

# 실제 컬럼명 확인
st.write("✅ 데이터 컬럼명 확인:", df.columns.tolist())

# 감염병 열 이름이 '감염병명'이 아닐 경우 자동 처리
column_name = None
for col in df.columns:
    if '감염병' in col:
        column_name = col
        break

if column_name is None:
    st.error("❌ 감염병 관련 열이 없습니다.")
else:
    sti_keywords = ['성병', '에이즈', '임질', '클라미디아', '매독']
    df_sti = df[df[column_name].astype(str).str.contains('|'.join(sti_keywords), na=False)]

    st.write("📊 성병 관련 데이터:", df_sti)

    fig, ax = plt.subplots()
    df_sti.groupby(column_name)['발생건수'].sum().plot(kind='bar', ax=ax)
    ax.set_title("감염병 종류별 성병 발생건수")
    ax.set_ylabel("건수")
    st.pyplot(fig)
