import streamlit as st
import math

diff_x = st.number_input("Scostamento in x")
diff_y = st.number_input("Scostamento in y")

if st.button("Calcola"):
    result = (2 * math.sqrt(((diff_x ** 2) + (diff_y ** 2))))
