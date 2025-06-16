filtered_df = year_gender_age[year_gender_age['감염병명'].str.contains('|'.join(sti_keywords), case=False, na=False)]
st.write(f"필터링된 행 개수: {len(filtered_df)}")
