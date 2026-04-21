import streamlit as st
import math
import pandas as pd

st.session_state.setdefault("history", [])

diff_x = st.number_input("Scostamento in x", format="%.3f")
diff_y = st.number_input("Scostamento in y", format="%.3f")
tp_tol = st.number_input("Tolleranza di posizione", format="%.3f")

if st.button("Calcola"):
    if tp_tol == 0:
        st.error("Inserisci una tolleranza di posizione")
    result = round((2 * math.sqrt(((diff_x ** 2) + (diff_y ** 2)))), 3)
    st.success(result)
    st.session_state.history.append({
        "Scostamento in x": diff_x,
        "Scostamento in y": diff_y,
        "Esatta Posizione": result
    })

df = pd.DataFrame(st.session_state.history)
st.dataframe(df)

if st.button("Indietro"):
    if st.session_state.history:
        st.session_state.history.pop()
        st.rerun()
            

csv = df.to_csv(sep=";", index=False)


st.download_button(
    label="Esporta in CSV",
    data=csv,
    file_name="dati.csv",
    mime="text/csv"
)
