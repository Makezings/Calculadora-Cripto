import streamlit as st

# Injectem estils personalitzats amb CSS
st.markdown(
    """
    <style>
    /* Augmentar la mida dels inputs un 50% més */
    input[type=number] {
        font-size: 30px !important; /* Augmenta la mida de la font */
        height: 90px !important;   /* Augmenta l'altura del camp */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Calculadora original: Càlcul de guanys/pèrdues
def calcular_guany_unitari(preu_compra, preu_venda):
    comissio = 0.00075  # Comissió fixa de Binance en BNB
    cost_unitari_compra = preu_compra * (1 + comissio)
    ingress_unitari_venda = preu_venda * (1 - comissio)
    guany_unitari = ingress_unitari_venda - cost_unitari_compra
    return guany_unitari

def calcular_guany_total(guany_unitari, unitats):
    return guany_unitari * unitats

# Títol principal
st.title("Calculadora per criptomonedes")

# **Primera funcionalitat: Calculadora de guanys/pèrdues**
st.header("Calculadora de guanys/pèrdues")

preu_compra = st.number_input("Preu de compra unitari (USD)", value=0.0, key="calc_preu_compra")
preu_venda = st.number_input("Preu de venda unitari (USD)", value=0.0, key="calc_preu_venda")
unitats = st.number_input("Unitats (comprades o venudes)", value=0.0, key="calc_unitats")

if st.button("Calcular guanys/pèrdues"):
    comissio = 0.00075
    cost_total = preu_compra * unitats * (1 + comissio)
    guany_unitari = calcular_guany_unitari(preu_compra, preu_venda)
    guany_total = calcular_guany_total(guany_unitari, unitats)

    if cost_total > 0:
        percentatge_guany = (guany_total / cost_total) * 100
    else:
        percentatge_guany = 0

    st.write(f"💵 **Cost total de l'operació (USD):** {cost_total:.2f}")
    if guany_unitari > 0:
        st.success(f"**Guany per unitat:** {guany_unitari:.4f} USD")
    elif guany_unitari < 0:
        st.error(f"**Pèrdua per unitat:** {abs(guany_unitari):.4f} USD")
    else:
        st.info("🔄 **No hi ha guany ni pèrdua per unitat.**")

    if guany_total > 0:
        st.success(f"💰 **Guany total:** {guany_total:.2f} USD")
        st.success(f"📊 **Percentatge de guany:** {percentatge_guany:.2f}%")
    elif guany_total < 0:
        st.error(f"💸 **Pèrdua total:** {abs(guany_total):.2f} USD")
        st.error(f"📊 **Percentatge de pèrdua:** {abs(percentatge_guany):.2f}%")
    else:
        st.info("🔄 **No hi ha guany ni pèrdua total.**")

st.markdown("---")

# **Segona funcionalitat: Simulador de venda i recompra**
st.header("Simulador per incrementar tokens")

st.markdown(
    """
    **Nota sobre aquesta estratègia:**
    Aquesta operació està pensada per **acumular més tokens** aprofitant les fluctuacions de preu. No genera un guany immediat en dòlars, sinó que busca augmentar el teu volum de tokens per a un possible guany futur.

    ⚠️ Aquesta estratègia només és efectiva si:
    - El preu del mercat puja significativament en el futur.
    - Recomprar els tokens redueix el preu mig de la teva posició.
    
    Si no creus que el preu pugui pujar o prefereixes guanyar en dòlars a curt termini, aquesta estratègia no és recomanable.
    """
)

utilitzar_dades_calculadora = st.checkbox("Utilitzar les dades de la calculadora anterior")

if utilitzar_dades_calculadora:
    tokens_actuals = st.number_input("Quants tokens tens actualment?", value=int(unitats), min_value=1, step=1, key="sim_tokens_actuals")
    preu_venda_sim = st.number_input("A quin preu vens els tokens?", value=preu_venda, min_value=0.0, step=0.01, key="sim_preu_venda")
    preu_recompra = st.number_input("A quin preu vols recomprar els tokens?", value=preu_compra, min_value=0.0, step=0.01, key="sim_preu_recompra")
else:
    tokens_actuals = st.number_input("Quants tokens tens actualment?", min_value=1, step=1, key="sim_tokens_actuals_manual")
    preu_venda_sim = st.number_input("A quin preu vens els tokens?", min_value=0.0, step=0.01, key="sim_preu_venda_manual")
    preu_recompra = st.number_input("A quin preu vols recomprar els tokens?", min_value=0.0, step=0.01, key="sim_preu_recompra_manual")

comissio_percent = 0.075

if st.button("Calcular increment de tokens"):
    if tokens_actuals > 0 and preu_venda_sim > 0:
        comissio = (tokens_actuals * preu_venda_sim) * (comissio_percent / 100)
        diners_despres_venda = (tokens_actuals * preu_venda_sim) - comissio
        st.write(f"💵 **Total obtingut després de la venda (USD):** {diners_despres_venda:.2f}")
        st.write(f"🧾 **Comissió deduïda (USD):** {comissio:.4f}")
        
        if preu_recompra > 0:
            tokens_recomprats = diners_despres_venda / preu_recompra
            st.write(f"🔄 **Tokens que podries comprar al preu actual:** {tokens_recomprats:.4f}")
            
            diferència_tokens = tokens_recomprats - tokens_actuals
            if diferència_tokens > 0:
                st.success(f"🎉 Amb aquesta operació acumularies {diferència_tokens:.4f} tokens més!")
            elif diferència_tokens < 0:
                st.error(f"⚠️ Perdries {-diferència_tokens:.4f} tokens amb aquesta operació.")
            else:
                st.info("🔄 El nombre de tokens es mantindria igual.")
