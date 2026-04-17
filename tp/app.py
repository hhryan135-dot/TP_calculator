import streamlit as st
import math

diff_x = st.number_input("Scostamento in x", format="%.3f")
diff_y = st.number_input("Scostamento in y", format="%.3f")

if st.button("Calcola"):
    result = round((2 * math.sqrt(((diff_x ** 2) + (diff_y ** 2)))), 3)
    st.success(result)
