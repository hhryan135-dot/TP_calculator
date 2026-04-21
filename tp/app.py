import streamlit as st
import math
import pandas as pd
import matplotlib.pyplot as plt

def plot_posizione(diff_x, diff_y, tp_tol, result):
    fig, ax = plt.subplots()

    # Disegno cerchio tolleranza
    circle = plt.Circle((0, 0), tp_tol/2, fill=False)
    ax.add_patch(circle)

    # Normalizzazione per colore (0 = dentro, 1 = fuori tanto)
    ratio = min(result / tp_tol, 1.5)

    # Colore graduale (verde → rosso)
    if ratio <= 1:
        color = (ratio, 1, 0)   # verde → giallo
    else:
        color = (1, max(0, 2 - ratio), 0)  # giallo → rosso

    # Scatter punto
    ax.scatter(diff_x, diff_y, color=color, s=100)

    # Assi
    ax.axhline(0)
    ax.axvline(0)

    # Limiti dinamici
    lim = max(tp_tol, abs(diff_x), abs(diff_y))
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)

    ax.set_aspect('equal')

    return fig

st.title("Calcolatore di esatta posizione")

st.session_state.setdefault("history", [])

diff_x = st.number_input("Scostamento in x", format="%.3f")
diff_y = st.number_input("Scostamento in y", format="%.3f")
tp_tol = st.number_input("Tolleranza di posizione", format="%.3f")

if st.button("Calcola"):
    if tp_tol == 0:
        st.error("Inserisci una tolleranza di posizione")
    else:
        result = round((2 * math.sqrt(((diff_x ** 2) + (diff_y ** 2)))), 3)
        st.success(result)
        out_tol = result - tp_tol if result >= tp_tol else 0
        st.session_state.history.append({
            "Scostamento in x": diff_x,
            "Scostamento in y": diff_y,
            "Esatta Posizione": result,
            "Tolleranza di posizione": tp_tol,
            "Fuori tolleranza": out_tol
        })
        fig = plot_posizione(diff_x, diff_y, tp_tol, result)
        st.pyplot(fig)

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
