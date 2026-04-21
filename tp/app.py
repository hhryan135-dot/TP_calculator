import streamlit as st
import math
import pandas as pd
from PIL import Image, ImageDraw
import io

def genera_icona(diff_x, diff_y, tp_tol, result):
    size = 100
    center = size // 2

    img = Image.new("RGB", (size, size), "white")
    draw = ImageDraw.Draw(img)

    # cerchio tolleranza
    r = int((tp_tol / tp_tol) * (size * 0.4))  # normalizzato
    draw.ellipse(
        (center - r, center - r, center + r, center + r),
        outline="black",
        width=2
    )

    # assi
    draw.line((0, center, size, center), fill="black")
    draw.line((center, 0, center, size), fill="black")

    # punto (scalato)
    scale = size * 0.4 / tp_tol if tp_tol != 0 else 1
    px = center + diff_x * scale
    py = center - diff_y * scale

    # colore dinamico
    ratio = min(result / tp_tol, 1.5) if tp_tol != 0 else 0
    if ratio <= 1:
        color = (int(255 * ratio), 255, 0)
    else:
        color = (255, int(255 * (2 - ratio)), 0)

    draw.ellipse((px-4, py-4, px+4, py+4), fill=color)

    # converti in bytes
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

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

df = pd.DataFrame(st.session_state.history)

if not df.empty:
    df["Grafico"] = df.apply(
        lambda row: genera_icona(
            row["Scostamento in x"],
            row["Scostamento in y"],
            row["Tolleranza di posizione"],
            row["Esatta Posizione"]
        ),
        axis=1
    )

st.dataframe(
    df,
    column_config={
        "Grafico": st.column_config.ImageColumn("Grafico")
    }
)

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
