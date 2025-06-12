import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")
st.title("📊 성병 관련 감염병 월별 발생 추이")

@st.cache_data
def load_data():
    df = pd.read_csv("감염병_발생현황월별_20250602121908.csv", encoding="cp949")
    df.columns = df.columns.str.strip()  # 혹시 공백 제거
    return df

df = load_data()

# 컬럼명과 데이터 샘플 보여주기 (확인용)
st.write("컬럼명 리스트:", df.columns.tolist())
st.write(df.head())

# 성병 관련 키워드 설정
sti_keywords = ['임질', '클라미디아', '성병', '매독', '성기', '에이즈']

# 감염병명 컬럼명 — 정확히 맞춰주세요 (예: '법정감염병군별(1)')
disease_col = '법정감염병군별(1)'

# 성병 관련 행만 필터링 (NaN 방지 위해 na=False)
df_sti = df[df[disease_col].str.contains('|'.join(sti_keywords), na=False)]

# 월별 데이터 컬럼(2019, 2019.1, 2019.2 ...)만 추출
month_cols = df.columns[2:]  # 앞 2개 컬럼은 감염병명, 다른 메타 정보라고 가정

# 데이터 형태 바꾸기: wide → long (melt)
df_melted = df_sti.melt(id_vars=[disease_col], value_vars=month_cols,
                        var_name='월', value_name='발생수')

# 숫자형으로 변환, NaN은 0으로 채우기
df_melted['발생수'] = pd.to_numeric(df_melted['발생수'], errors='coerce').fillna(0)

# 그래프 그리기
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_melted, x='월', y='발생수', hue=disease_col, marker='o')
plt.xticks(rotation=45)
plt.title('성병 관련 감염병 월별 발생 추이')
plt.xlabel('월')
plt.ylabel('발생수')
plt.legend(title=disease_col)
plt.tight_layout()

st.pyplot(plt)
