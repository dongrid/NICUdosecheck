import streamlit as st

st.title("👶 小児用量チェック")

weight = st.number_input("体重 (kg)", value=10.0, step=1.0)

# よく使う薬剤のショートカット
st.subheader("よく使う薬剤")

col1, col2 = st.columns(2)

with col1:
    if st.button("アドレナリン筋注(0.01mg/kg)"):
        st.session_state['dose_mg_kg'] = 0.01
        st.session_state['ratio_unit'] = "mg/mL"
        st.session_state['ratio_value'] = 1.0  # 1mg/1mL(1:1000)製剤

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

# 薬用量/製剤量比の入力と単位選択を横並びに
ratio_col1, ratio_col2 = st.columns([2, 3])

with ratio_col1:
    ratio_value = st.number_input("薬用量/製剤量比", value=ratio_value_default, step=0.01, min_value=0.0)

with ratio_col2:
    unit_options = ["mg/g", "mg/mL", "%(g)", "%(mL)", "mg/錠"]
    try:
        default_index = unit_options.index(ratio_unit_value)
    except ValueError:
        default_index = 1  # デフォルトは mg/mL
    ratio_unit = st.radio("単位", unit_options, index=default_index, horizontal=True)

total_dose = weight * dose_mg_kg

st.metric("必要投与量（薬用量）", f"{total_dose:.3f} mg")

if total_dose > 0.0 and ratio_value > 0:
    # 単位に応じて製剤量を計算
    if ratio_unit == "mg/g":
        required_preparation = total_dose / ratio_value
        st.metric("必要製剤量", f"{required_preparation:.3f} g")
    elif ratio_unit == "mg/mL":
        required_preparation = total_dose / ratio_value
        st.metric("必要製剤量", f"{required_preparation:.3f} mL")
    elif ratio_unit == "%(g)":
        # 1% = 10mg/g
        mg_per_g = ratio_value * 10
        required_preparation = total_dose / mg_per_g
        st.metric("必要製剤量", f"{required_preparation:.3f} g")
    elif ratio_unit == "%(mL)":
        # 1% = 10mg/mL
        mg_per_ml = ratio_value * 10
        required_preparation = total_dose / mg_per_ml
        st.metric("必要製剤量", f"{required_preparation:.3f} mL")
    elif ratio_unit == "mg/錠":
        required_preparation = total_dose / ratio_value
        st.metric("必要製剤量", f"{required_preparation:.3f} 錠")