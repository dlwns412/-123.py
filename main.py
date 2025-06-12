import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import streamlit as st

# 한글 폰트 설정
font = "NanumGothic.ttf"
font = fm.FontProperties(fname=font_path, size=12)
plt.rcParams['font.family'] = fontprop.get_name()

# 데이터 로딩
df = pd.read_csv("감염병_발생현황월별_20250602121908.csv", encoding="cp949")
df.columns = df.columns.str.strip()  # 혹시 모를 공백 제거

# 실제 컬럼명 확인
st.write("컬럼명 확인:", df.columns)

# 성병 관련 키워드 필터링
sti_keywords = ['임질', '클라미디아', '성병', '매독', '성기', '에이즈']
sti_mask = df[df.columns[0]].str.contains('|'.join(sti_keywords), na=False)
df_sti = df[sti_mask]

# 시각화
plt.figure(figsize=(10, 6))
for name in df_sti[df.columns[0]].unique():
    subset = df_sti[df_sti[df.columns[0]] == name]
    plt.plot(subset[df.columns[1]], subset[df.columns[2]], label=name)

plt.title("성병 감염병 월별 추이")
plt.xlabel(df.columns[1])
plt.ylabel(df.columns[2])
plt.legend()
st.pyplot(plt)
