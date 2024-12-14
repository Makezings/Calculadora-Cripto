import streamlit as st

# Calculadora original: Càlcul de guanys/pèrdues
def calcular_guany_unitari(preu_compra, preu_venda):
    # Comissió fixa de Binance en BNB (0.075% = 0.00075)
    comissio = 0.00075

    # Cost unitari de compra amb comissió
    cost_unitari_compra = preu_compra * (1 + comissio)

    # Ingrés unitari de venda amb comissió
    ingress_unitari_venda = preu_venda * (1 - comissio)

    # Guany/pèrdua unitari
    guany_unitari = ingress_unitari_venda - cost_unitari_compra
    return guany_unitari

def calcular_guany_total(guany_unitari, unitats):
    return guany_unitari * unitats

# Interfície Streamlit
st.title("Calculadora per criptomonedes")

# **Primera funcionalitat: Calculadora de guanys/pèrdues**
st.header("Calculadora de guanys/pèrdues")

# Inputs de la calculadora original
preu_compra = st.number_input("Preu de compra unitari (USD)", value=0.0, key="calc_preu_compra")
preu_venda = st.number_input("Preu de venda unitari (USD)", value=0.0, key="calc_preu_venda")
unitats = st.number_input("Unitats (comprades o venudes)", value=0.0, key="calc_unitats")

# Botó per calcular
if st.button("Calcular guanys/pèrdues"):
    guany_unitari = calcular_guany_unitari(preu_compra, preu_venda)
    guany_total = calcular_guany_total(guany_unitari, unitats)

    st.write(f"**Guany o pèrdua per unitat:** {guany_unitari:.4f} USD")
    st.write(f"**Guany o pèrdua total:** {guany_total:.2f} USD")

# Separador
st.markdown("---")

# **Segona funcionalitat: Simulador de venda i recompra**
st.header("Simulador de venda i recompra de tokens")

# Checkbox per copiar dades
utilitzar_dades_calculadora = st.checkbox("Utilitzar les dades de la calculadora anterior")

# Inputs del simulador
if utilitzar_dades_calculadora:
    venda_tokens = st.number_input("Quants tokens vols vendre?", value=int(unitats), min_value=1, step=1, key="sim_venda_tokens")
    preu_venda_sim = st.number_input("Preu de venda per token (USD)", value=preu_venda, min_value=0.0, step=0.01, key="sim_preu_venda")
    preu_recompra = st.number_input("Preu de recompra per token (USD)", value=preu_compra, min_value=0.0, step=0.01, key="sim_preu_recompra")
else:
    venda_tokens = st.number_input("Quants tokens vols vendre?", min_value=1, step=1, key="sim_venda_tokens_manual")
    preu_venda_sim = st.number_input("Preu de venda per token (USD)", min_value=0.0, step=0.01, key="sim_preu_venda_manual")
    preu_recompra = st.number_input("Preu de recompra per token (USD)", min_value=0.0, step=0.01, key="sim_preu_recompra_manual")

comissio_percent = 0.075  # Comissió fixa per Binance pagant en BNB

# Botó per calcular al simulador
if st.button("Calcular venda i recompra"):
    if venda_tokens > 0 and preu_venda_sim > 0:
        # Calcula el total després de la venda
        comissio = (venda_tokens * preu_venda_sim) * (comissio_percent / 100)
        diners_despres_venda = (venda_tokens * preu_venda_sim) - comissio
        st.write(f"💵 Total obtingut després de la venda (USD): {diners_despres_venda:.2f}")
        st.write(f"🧾 Comissió deduïda (USD): {comissio:.4f}")
        
        # Calcula quants tokens pots recomprar
        if preu_recompra > 0:
            tokens_recomprats = diners_despres_venda / preu_recompra
            st.write(f"🔄 Tokens que podries comprar al preu actual: {tokens_recomprats:.4f}")
            
            # Compara si guanyes o perds tokens
            diferència_tokens = tokens_recomprats - venda_tokens
            if diferència_tokens > 0:
                st.success(f"🎉 Amb aquesta operació acumularies {diferència_tokens:.4f} tokens més!")
            elif diferència_tokens < 0:
                st.error(f"⚠️ Perdries {-diferència_tokens:.4f} tokens amb aquesta operació.")
            else:
                st.info("🔄 El nombre de tokens es mantindria igual.")
