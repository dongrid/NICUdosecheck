import streamlit as st

st.title("👶 NICU Dose Check")

weight = st.number_input("体重 (kg)", value=1.0, step=0.1)
dose_mg_kg = st.number_input("設定用量 (mg/kg)", value=0.1, step=0.01)

total_dose = weight * dose_mg_kg

st.metric("必要投与量", f"{total_dose:.3f} mg")

# よく使う薬剤のショートカット
if st.button("アドレナリン(0.01mg/kg)で計算"):
    st.write(f"計算結果: {weight * 0.01:.3f} mg")