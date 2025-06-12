import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import streamlit as st

# 한글 폰트 설정
font_path = "NanumGothic.ttf"
fontprop = fm.FontProperties(fname=font_path, size=12)
plt.rcParams['font.family'] = fontprop.get_name()

# 데이터 로딩
df = pd.read_csv("감염병_발생현황월별_20250602121908.csv", encoding="cp949")
df.columns = df.columns.str.strip()

st.write("컬럼명 확인:", df.columns)

# 날짜 컬럼을 datetime으로 변환 (필요시)
try:
    df[df.columns[1]] = pd.to_datetime(df[df.columns[1]], errors='coerce')
except Exception as e:
    st.write("날짜 변환 오류:", e)

# 성병 관련 키워드 필터링 (문자열 변환 후)
sti_keywords = ['임질', '클라미디아', '성병', '매독', '성기', '에이즈']
sti_mask = df[df.columns[0]].astype(str).str.contains('|'.join(sti_keywords), na=False)
df_sti = df[sti_mask]

# 시각화
fig, ax = plt.subplots(figsize=(10, 6))
for name in df_sti[df.columns[0]].unique():
    subset = df_sti[df_sti[df.columns[0]] == name]
    subset = subset.sort_values(by=df.columns[1])  # 날짜 순 정렬
    ax.plot(subset[df.columns[1]], subset[df.columns[2]], label=name)

ax.set_title("성병 감염병 월별 추이")
ax.set_xlabel(df.columns[1])
ax.set_ylabel(df.columns[2])
ax.legend()

st.pyplot(fig)

