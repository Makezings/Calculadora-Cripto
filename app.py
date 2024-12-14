import streamlit as st

# Funció per estilitzar inputs i millorar l'experiència
def estilitzar():
    st.markdown(
        """
        <style>
        /* Inputs numèrics més grans */
        input[type=number] {
            font-size: 1.5rem !important;
            height: 3rem !important;
            text-align: center !important;
        }
        /* Centrat del contingut */
        div[data-testid="stNumberInput"] {
            display: flex;
            justify-content: center;
            margin-bottom: 1rem;
        }
        /* Botons més accessibles */
        button {
            font-size: 1.2rem !important;
            padding: 0.5rem 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Aplica els estils personalitzats
estilitzar()

# **Inicialitza valors a Session State si no existeixen**
for key, value in {
    "calc_preu_compra": 0.0,
    "calc_preu_venda": 0.0,
    "calc_unitats": 0.0,
    "sim_tokens_actuals": 1.0,
    "sim_preu_venda": 0.0,
    "sim_preu_recompra": 0.0,
    "focus_cleared_calc_preu_compra": False,
    "focus_cleared_calc_preu_venda": False,
    "focus_cleared_calc_unitats": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Funció per esborrar el contingut en tocar el camp
def clear_on_focus(key):
    if not st.session_state[f"focus_cleared_{key}"]:
        st.session_state[key] = ""
        st.session_state[f"focus_cleared_{key}"] = True

# **Primera calculadora: Guanys/pèrdues**
st.title("Calculadora per criptomonedes")

st.header("Calculadora de guanys/pèrdues")
st.number_input(
    "Preu de compra unitari (USD)",
    step=0.0001,
    format="%.8f",
    key="calc_preu_compra",
    on_change=clear_on_focus,
    args=("calc_preu_compra",),
)
st.number_input(
    "Preu de venda unitari (USD)",
    step=0.0001,
    format="%.8f",
    key="calc_preu_venda",
    on_change=clear_on_focus,
    args=("calc_preu_venda",),
)
st.number_input(
    "Unitats (comprades o venudes)",
    step=0.0001,
    format="%.8f",
    key="calc_unitats",
    on_change=clear_on_focus,
    args=("calc_unitats",),
)

# Botó per calcular
if st.button("Calcular guanys/pèrdues"):
    comissio = 0.00075
    guany_unitari = (
        st.session_state.calc_preu_venda * (1 - comissio)
        - st.session_state.calc_preu_compra * (1 + comissio)
    )
    guany_total = guany_unitari * st.session_state.calc_unitats

    st.write(f"**Guany o pèrdua per unitat:** {guany_unitari:.8f} USD")
    st.write(f"**Guany o pèrdua total:** {guany_total:.8f} USD")

st.markdown("---")

# **Segona calculadora: Simulador de tokens**
st.header("Simulador per incrementar tokens")

# Checkbox per copiar dades
st.checkbox("Copiar dades de la primera calculadora", key="copiar_dades")

# Inputs per a la segona calculadora
st.number_input(
    "Quants tokens tens actualment?",
    min_value=0.0,
    step=0.0001,
    format="%.8f",
    key="sim_tokens_actuals",
)
st.number_input(
    "A quin preu vens els tokens?",
    min_value=0.0,
    step=0.0001,
    format="%.8f",
    key="sim_preu_venda",
)
st.number_input(
    "A quin preu vols recomprar els tokens?",
    min_value=0.0,
    step=0.0001,
    format="%.8f",
    key="sim_preu_recompra",
)

# Botó per calcular al simulador
if st.button("Calcular increment de tokens"):
    comissio_percent = 0.075
    comissio = (
        st.session_state.sim_tokens_actuals * st.session_state.sim_preu_venda
    ) * (comissio_percent / 100)
    diners_despres_venda = (
        st.session_state.sim_tokens_actuals * st.session_state.sim_preu_venda
    ) - comissio
    tokens_recomprats = (
        diners_despres_venda / st.session_state.sim_preu_recompra
        if st.session_state.sim_preu_recompra > 0
        else 0
    )
    diferència_tokens = tokens_recomprats - st.session_state.sim_tokens_actuals

    st.write(f"💵 Total obtingut després de la venda (USD): {diners_despres_venda:.8f}")
    st.write(f"🔄 Tokens que podries comprar: {tokens_recomprats:.8f}")
    if diferència_tokens > 0:
        st.success(f"🎉 Acumularies {diferència_tokens:.8f} tokens més!")
    elif diferència_tokens < 0:
        st.error(f"⚠️ Perdries {-diferència_tokens:.8f} tokens.")
    else:
        st.info("🔄 No canviaria el nombre de tokens.")
