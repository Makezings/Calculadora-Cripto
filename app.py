import streamlit as st

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
st.title("Calculadora de guanys/perdues per criptomonedes")

# Inputs
preu_compra = st.number_input("Preu de compra unitari (USD)", value=0.0)
preu_venda = st.number_input("Preu de venda unitari (USD)", value=0.0)
unitats = st.number_input("Unitats (comprades o venudes)", value=0.0)

# Botó per calcular
if st.button("Calcular"):
    guany_unitari = calcular_guany_unitari(preu_compra, preu_venda)
    guany_total = calcular_guany_total(guany_unitari, unitats)

    st.write(f"**Guany o pèrdua per unitat:** {guany_unitari:.4f} USD")
    st.write(f"**Guany o pèrdua total:** {guany_total:.2f} USD")
