import pandas as pd

df = pd.read_csv("감염병_군별_발생현황_20250602122005.csv", encoding='cp949')
print(df.columns)
