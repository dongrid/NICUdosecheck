import streamlit as st

st.title("👶 NICU Dose Check")

weight = st.number_input("体重 (kg)", value=1.0, step=0.1)

# よく使う薬剤のショートカット
st.subheader("よく使う薬剤")

col1, col2 = st.columns(2)

with col1:
    if st.button("アドレナリン(0.01mg/kg)"):
        st.session_state['dose_mg_kg'] = 0.01

with col2:
    if st.button("カルボシステイン(10mg/kg, 5%シロップ)"):
        st.session_state['dose_mg_kg'] = 10.0
        st.session_state['ratio_unit'] = "mg/mL"
        st.session_state['ratio_value'] = 50.0  # 5%シロップ = 50mg/mL

# セッションステートから値を取得（デフォルト値を使用）
dose_mg_kg_value = st.session_state.get('dose_mg_kg', 0.1)
ratio_unit_value = st.session_state.get('ratio_unit', "mg/g")
ratio_value_default = st.session_state.get('ratio_value', 1.0)

dose_mg_kg = st.number_input("設定用量 (mg/kg)", value=dose_mg_kg_value, step=0.01)

# 薬用量/製剤量比の単位選択
unit_options = ["mg/g", "mg/mL", "%"]
try:
    default_index = unit_options.index(ratio_unit_value)
except ValueError:
    default_index = 0
ratio_unit = st.selectbox("薬用量/製剤量比の単位", unit_options, index=default_index)
ratio_value = st.number_input(f"薬用量/製剤量比 ({ratio_unit})", value=ratio_value_default, step=0.01, min_value=0.0)

total_dose = weight * dose_mg_kg

st.metric("必要投与量（薬用量）", f"{total_dose:.3f} mg")

if total_dose > 0 and ratio_value > 0:
    # 単位に応じて製剤量を計算
    if ratio_unit == "mg/g":
        # mg/gの場合：必要な製剤量(g) = 必要投与量(mg) / 薬用量/製剤量比(mg/g)
        required_preparation = total_dose / ratio_value
        st.metric("必要製剤量", f"{required_preparation:.3f} g")
    elif ratio_unit == "mg/mL":
        # mg/mLの場合：必要な製剤量(mL) = 必要投与量(mg) / 薬用量/製剤量比(mg/mL)
        required_preparation = total_dose / ratio_value
        st.metric("必要製剤量", f"{required_preparation:.3f} mL")
    elif ratio_unit == "%":
        # %の場合：% = g/100mL = mg/100mL, つまり 1% = 10mg/mL
        # 必要な製剤量(mL) = 必要投与量(mg) / (比率(%) * 10)
        mg_per_ml = ratio_value * 10  # %をmg/mLに変換（1% = 10mg/mL）
        required_preparation = total_dose / mg_per_ml
        st.metric("必要製剤量", f"{required_preparation:.3f} mL")