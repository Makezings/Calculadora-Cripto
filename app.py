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

# **Primera calculadora: Guanys/pèrdues**
st.title("Calculadora per criptomonedes")

st.header("Calculadora de guanys/pèrdues")
preu_compra = st.number_input("Preu de compra unitari (USD)", value=0.0, step=0.01, key="calc_preu_compra")
preu_venda = st.number_input("Preu de venda unitari (USD)", value=0.0, step=0.01, key="calc_preu_venda")
unitats = st.number_input("Unitats (comprades o venudes)", value=0.0, step=1.0, key="calc_unitats")

# Botó per calcular
if st.button("Calcular guanys/pèrdues"):
    comissio = 0.00075
    guany_unitari = preu_venda * (1 - comissio) - preu_compra * (1 + comissio)
    guany_total = guany_unitari * unitats

    st.write(f"**Guany o pèrdua per unitat:** {guany_unitari:.4f} USD")
    st.write(f"**Guany o pèrdua total:** {guany_total:.2f} USD")

st.markdown("---")

# **Segona calculadora: Simulador de tokens**
st.header("Simulador per incrementar tokens")

# Check per copiar dades
copiar_dades = st.checkbox("Copiar dades de la primera calculadora")

if copiar_dades:
    tokens_actuals = unitats
    preu_venda_sim = preu_venda
    preu_recompra = preu_compra
else:
    tokens_actuals = st.number_input("Quants tokens tens actualment?", min_value=1, step=1, key="sim_tokens_actuals")
    preu_venda_sim = st.number_input("A quin preu vens els tokens?", min_value=0.0, step=0.01, key="sim_preu_venda")
    preu_recompra = st.number_input("A quin preu vols recomprar els tokens?", min_value=0.0, step=0.01, key="sim_preu_recompra")

# Botó per calcular al simulador
if st.button("Calcular increment de tokens"):
    comissio_percent = 0.075
    comissio = (tokens_actuals * preu_venda_sim) * (comissio_percent / 100)
    diners_despres_venda = (tokens_actuals * preu_venda_sim) - comissio
    tokens_recomprats = diners_despres_venda / preu_recompra if preu_recompra > 0 else 0
    diferència_tokens = tokens_recomprats - tokens_actuals

    st.write(f"💵 Total obtingut després de la venda (USD): {diners_despres_venda:.2f}")
    st.write(f"🔄 Tokens que podries comprar: {tokens_recomprats:.4f}")
    if diferència_tokens > 0:
        st.success(f"🎉 Acumularies {diferència_tokens:.4f} tokens més!")
    elif diferència_tokens < 0:
        st.error(f"⚠️ Perdries {-diferència_tokens:.4f} tokens.")
    else:
        st.info("🔄 No canviaria el nombre de tokens.")
