import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

# 한글 폰트 설정 (NanumGothic.ttf가 현재 폰트 폴더에 있어야 합니다)
font_path = "NanumGothic.ttf"
fontprop = fm.FontProperties(fname=font_path).get_name()
sns.set(font=fontprop)

st.set_page_config(layout="wide")
st.title("📊 성병 관련 감염병 월별 발생 추이")

# 데이터 로드
@st.cache_data
def load_data():
    df = pd.read_csv("감염병_발생현황월별_20250602121908.csv", encoding="cp949")
    df.columns = df.columns.str.strip()  # 컬럼명 공백 제거
    return df

df = load_data()

# 컬럼명 출력 (확인용)
st.write("컬럼명 리스트:", df.columns.tolist())
st.write(df.head())

# 성병 관련 키워드
sti_keywords = ['임질', '클라미디아', '성병', '매독', '성기', '에이즈']

# 실제 감염병명 관련 컬럼명 (주어진 정보 기반)
target_col = '법정감염병군별(1)'

# 필터링 (NaN 있으면 False 처리)
df_sti = df[df[target_col].str.contains('|'.join(sti_keywords), na=False)]

# 월별 데이터로 변환하기 (컬럼명 예: '2019.1', '2019.2' ... 컬럼들이 월별 발생 수)
month_cols = df_sti.columns[2:]  # '법정감염병군별(1)', '법정감염병군별(2)' 이후가 월별 컬럼으로 가정

# 월별 데이터를 세로형으로 변환(melt)
df_melted = df_sti.melt(id_vars=[target_col], value_vars=month_cols,
                        var_name='월', value_name='발생수')

# 숫자형으로 변환 (필요하면)
df_melted['발생수'] = pd.to_numeric(df_melted['발생수'], errors='coerce').fillna(0)

# 그래프 그리기
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_melted, x='월', y='발생수', hue=target_col, marker='o')
plt.xticks(rotation=45)
plt.title('성병 관련 감염병 월별 발생 추이')
plt.xlabel('월')
plt.ylabel('발생수')
plt.legend(title=target_col)
plt.tight_layout()

st.pyplot(plt)
