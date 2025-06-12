import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

st.set_page_config(layout="wide")
st.title("📊 성병 관련 감염병 월별 발생 추이")

@st.cache_data
def load_data():
    df = pd.read_csv("감염병_발생현황월별_20250602121908.csv", encoding="cp949")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

st.write("컬럼명 리스트:", df.columns.tolist())
st.write(df.head())

sti_keywords = ['임질', '클라미디아', '성병', '매독', '성기', '에이즈']
target_col = '법정감염병군별(1)'

df_sti = df[df[target_col].str.contains('|'.join(sti_keywords), na=False)]
month_cols = df_sti.columns[2:]
df_melted = df_sti.melt(id_vars=[target_col], value_vars=month_cols,
                        var_name='월', value_name='발생수')
df_melted['발생수'] = pd.to_numeric(df_melted['발생수'], errors='coerce').fillna(0)

plt.figure(figsize=(12, 6))
sns.lineplot(data=df_melted, x='월', y='발생수', hue=target_col, marker='o')
plt.xticks(rotation=45)
plt.title('성병 관련 감염병 월별 발생 추이')
plt.xlabel('월')
plt.ylabel('발생수')
plt.legend(title=target_col)
plt.tight_layout()

st.pyplot(plt)
