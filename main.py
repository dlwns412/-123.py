import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans

st.title("배송 위치 군집 시각화")

uploaded_file = st.file_uploader("CSV 파일 업로드", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("원본 데이터")
    st.dataframe(df.head())

    num_clusters = st.slider("군집 수 선택", min_value=2, max_value=10, value=3)

    # 군집 분석 수행
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    df["cluster"] = kmeans.fit_predict(df[["Latitude", "Longitude"]])

    st.subheader("군집 결과 시각화")
    fig = px.scatter_mapbox(
        df,
        lat="Latitude",
        lon="Longitude",
        color="cluster",
        zoom=10,
        mapbox_style="open-street-map",
        hover_data=["Num"]
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("CSV 파일을 업로드해 주세요.")

