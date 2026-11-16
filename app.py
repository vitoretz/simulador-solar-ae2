import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Simulador Educacional de Energia Solar",
    page_icon="☀️",
    layout="wide",
)

# Casos reais fornecidos para a atividade acadêmica.
# Os nomes dos clientes foram removidos da aplicação para preservar privacidade.
CASOS = {
    "Caso Rural A - Sistema 96,39 kWp": {
        "consumo_mensal": 13340.0,
        "valor_conta": 9905.49,
        "potencia_kwp": 96.39,
        "geracao_anual_prevista": 126463.68,
        "investimento": 300000.00,
        "geracao_2026": 96820.0,
        "desempenho_periodo": 94.14,
        "data_conta": "SET/2022",
        "data_instalacao": "18/09/2024",
        "fonte_geracao": "monitoramento da usina",
        "observacao": "Sistema com 189 módulos de 510 W e inversor de 75 kW.",
    },
    "Caso Rural B - Sistema 44,00 kWp": {
        "consumo_mensal": 7134.0,
        "valor_conta": 5534.13,
        "potencia_kwp": 44.0,
        "geracao_anual_prevista": 57728.0,
        "investimento": 129483.00,
        "geracao_2026": 48430.0,
        "desempenho_periodo": 101.84,
        "data_conta": "NOV/2024",
        "data_instalacao": "14/04/2025",
        "fonte_geracao": "monitoramento da usina",
        "observacao": "Sistema com 80 módulos de 550 W e dois inversores de 25 kW.",
    },
    "Caso Rural C - Sistema 6,10 kWp": {
        "consumo_mensal": 321.0,
        "valor_conta": 314.00,
        "potencia_kwp": 6.10,
        "geracao_anual_prevista": 7284.83,
        "investimento": 22955.00,
        "geracao_2026": 7340.0,
        "desempenho_periodo": 125.77,
        "data_conta": "JUL/2025",
        "data_instalacao": "17/09/2025",
        "fonte_geracao": "monitoramento da usina",
        "observacao": (
            "O orçamento informa geração média de 657 kWh/mês, enquanto o cadastro de "
            "monitoramento informa 7.284,83 kWh/ano (aprox. 607,07 kWh/mês). "
            "Nesta simulação é usado o valor anual do monitoramento, sem ocultar a divergência."
        ),
    },
}


def br_money(v: float) -> str:
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def br_number(v: float, decimals: int = 0) -> str:
    txt = f"{v:,.{decimals}f}"
    return txt.replace(",", "X").replace(".", ",").replace("X", ".")


def calcular(consumo_mensal, tarifa, potencia, geracao_anual, investimento):
    consumo_anual = consumo_mensal * 12
    geracao_aproveitada = min(consumo_anual, geracao_anual)
    economia_anual = geracao_aproveitada * tarifa
    cobertura = (geracao_anual / consumo_anual * 100) if consumo_anual > 0 else 0
    payback = investimento / economia_anual if economia_anual > 0 and investimento > 0 else None
    produtividade_anual = geracao_anual / potencia if potencia > 0 else 0
    produtividade_mensal = produtividade_anual / 12 if produtividade_anual > 0 else 0
    return {
        "consumo_anual": consumo_anual,
        "geracao_aproveitada": geracao_aproveitada,
        "economia_anual": economia_anual,
        "cobertura": cobertura,
        "payback": payback,
        "produtividade_anual": produtividade_anual,
        "produtividade_mensal": produtividade_mensal,
    }


st.title("Simulador Educacional de Energia Solar Fotovoltaica")
st.caption(
    "Atividade Extensionista II - Ciência de Dados | ferramenta educativa para análise inicial de sistemas fotovoltaicos rurais."
)

aba_casos, aba_livre, aba_comparacao = st.tabs([
    "Casos rurais reais",
    "Simulação livre",
    "Comparação dos casos",
])

with aba_casos:
    caso_nome = st.selectbox("Selecione um caso real anonimizado", list(CASOS.keys()))
    caso = CASOS[caso_nome]

    tarifa_efetiva = caso["valor_conta"] / caso["consumo_mensal"] if caso["consumo_mensal"] else 0
    calc = calcular(
        caso["consumo_mensal"],
        tarifa_efetiva,
        caso["potencia_kwp"],
        caso["geracao_anual_prevista"],
        caso["investimento"],
    )

    st.subheader("Dados de entrada do caso")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Consumo da fatura", f"{br_number(caso['consumo_mensal'])} kWh/mês")
    c2.metric("Valor da fatura", br_money(caso["valor_conta"]))
    c3.metric("Tarifa efetiva", f"{br_money(tarifa_efetiva)}/kWh")
    c4.metric("Potência instalada", f"{br_number(caso['potencia_kwp'], 2)} kWp")

    c5, c6, c7, c8 = st.columns(4)
    c5.metric("Geração anual prevista", f"{br_number(caso['geracao_anual_prevista'])} kWh")
    c6.metric("Investimento", br_money(caso["investimento"]))
    c7.metric("Geração registrada em 2026", f"{br_number(caso['geracao_2026'])} kWh")
    c8.metric("Desempenho do período", f"{caso['desempenho_periodo']:.2f}%")

    st.caption(
        f"Fatura de referência: {caso['data_conta']} | instalação: {caso['data_instalacao']} | geração real: {caso['fonte_geracao']}."
    )

    st.subheader("Resultados educacionais")
    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Consumo anual estimado", f"{br_number(calc['consumo_anual'])} kWh")
    r2.metric("Cobertura teórica", f"{calc['cobertura']:.1f}%")
    r3.metric("Economia anual simplificada", br_money(calc["economia_anual"]))
    r4.metric("Payback simples", f"{calc['payback']:.1f} anos" if calc["payback"] else "-")

    df = pd.DataFrame(
        {
            "Indicador": ["Consumo anual estimado", "Geração anual prevista"],
            "Energia (kWh)": [calc["consumo_anual"], caso["geracao_anual_prevista"]],
        }
    ).set_index("Indicador")
    st.bar_chart(df)

    st.info(
        "A economia é uma estimativa simplificada calculada com a tarifa efetiva da fatura e limitada ao consumo anual. "
        "Não considera regras completas de compensação, impostos futuros, custo de disponibilidade, degradação, manutenção ou reajustes tarifários."
    )
    st.write("**Observação técnica do caso:**", caso["observacao"])

with aba_livre:
    st.subheader("Teste uma nova situação")
    left, right = st.columns(2)
    with left:
        consumo = st.number_input("Consumo médio mensal (kWh)", min_value=0.0, value=1000.0, step=50.0)
        tarifa = st.number_input("Tarifa média efetiva (R$/kWh)", min_value=0.0, value=0.85, step=0.01, format="%.3f")
        potencia = st.number_input("Potência do sistema (kWp)", min_value=0.0, value=10.0, step=0.5)
    with right:
        geracao = st.number_input("Geração anual estimada (kWh)", min_value=0.0, value=13000.0, step=100.0)
        investimento = st.number_input("Investimento total (R$)", min_value=0.0, value=35000.0, step=500.0)

    livre = calcular(consumo, tarifa, potencia, geracao, investimento)
    a, b, c, d = st.columns(4)
    a.metric("Consumo anual", f"{br_number(livre['consumo_anual'])} kWh")
    b.metric("Cobertura teórica", f"{livre['cobertura']:.1f}%")
    c.metric("Economia anual simplificada", br_money(livre["economia_anual"]))
    d.metric("Payback simples", f"{livre['payback']:.1f} anos" if livre["payback"] else "-")

    st.write(
        f"Produtividade implícita do sistema: **{livre['produtividade_anual']:.0f} kWh/kWp/ano** "
        f"({livre['produtividade_mensal']:.1f} kWh/kWp/mês)."
    )

with aba_comparacao:
    st.subheader("Resumo dos três casos selecionados")
    linhas = []
    for nome, c in CASOS.items():
        tarifa = c["valor_conta"] / c["consumo_mensal"] if c["consumo_mensal"] else 0
        res = calcular(c["consumo_mensal"], tarifa, c["potencia_kwp"], c["geracao_anual_prevista"], c["investimento"])
        linhas.append(
            {
                "Caso": nome.split(" - ")[0],
                "Potência (kWp)": c["potencia_kwp"],
                "Consumo fatura (kWh)": c["consumo_mensal"],
                "Geração anual prevista (kWh)": c["geracao_anual_prevista"],
                "Investimento (R$)": c["investimento"],
                "Cobertura teórica (%)": round(res["cobertura"], 1),
                "Payback simples (anos)": round(res["payback"], 2) if res["payback"] else None,
                "Desempenho do período (%)": c["desempenho_periodo"],
            }
        )
    comp = pd.DataFrame(linhas).set_index("Caso")
    st.dataframe(comp, use_container_width=True)
    st.bar_chart(comp[["Potência (kWp)"]])
    st.bar_chart(comp[["Desempenho do período (%)"]])

st.divider()
st.subheader("Como interpretar a ferramenta")
st.markdown(
    """
- **Cobertura teórica** compara a geração anual prevista com o consumo anual estimado a partir da fatura de referência.
- **Tarifa efetiva** é calculada dividindo o valor total da fatura pelo consumo faturado do mês; serve somente como aproximação educacional.
- **Economia anual simplificada** considera a energia aproveitável limitada ao consumo anual e a tarifa efetiva informada.
- **Payback simples** divide o investimento pela economia anual simplificada, sem fluxo de caixa descontado.
- **Desempenho do período** é o indicador exibido pela plataforma de monitoramento da usina e não deve ser confundido com a razão entre geração parcial de 2026 e geração anual prevista.

> Esta aplicação possui finalidade educacional e de triagem inicial. Não substitui projeto elétrico, análise tarifária, estudo de irradiação, homologação, orçamento comercial ou dimensionamento executado por profissional habilitado.
"""
)
