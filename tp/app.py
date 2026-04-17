import streamlit as st
import math
import pandas as pd

st.session_state.setdefault("history", [])

diff_x = st.number_input("Scostamento in x", format="%.3f")
diff_y = st.number_input("Scostamento in y", format="%.3f")

if st.button("Calcola"):
    result = round((2 * math.sqrt(((diff_x ** 2) + (diff_y ** 2)))), 3)
    st.success(result)
    st.session_state.history.append({
        "Scostamento in x": diff_x,
        "Scostamento in y": diff_y,
        "True Position": result
    })

df = pd.DataFrame(st.session_state.history)
st.dataframe(df)

csv = df.to_csv(index=False)

st.download_button(
    label="Esporta in CSV",
    data=csv,
    file_name="dati.csv",
    mime="text/csv"
)
