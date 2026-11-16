# Simulador Educacional de Energia Solar Fotovoltaica

Projeto desenvolvido para a Atividade Extensionista II do CST em Ciência de Dados - UNINTER.

## Finalidade
Apoiar uma ação de educação energética e inclusão digital voltada ao meio rural, demonstrando como dados reais de consumo, potência fotovoltaica, geração, investimento e monitoramento podem ser convertidos em indicadores simples de cobertura do consumo, economia e payback.

## Base de validação
A aplicação contém três casos rurais reais anonimizados. Os dados foram extraídos de documentos fornecidos para a atividade: faturas de energia, projetos/memoriais, orçamentos e telas de monitoramento. Nomes, endereços e identificadores dos clientes não são exibidos no aplicativo.

Também existe um quarto caso rural disponível no material de apoio, mantido fora dos presets principais porque o valor de investimento não foi informado, o que impede o cálculo de payback sem criar uma estimativa não documentada.

## Observação de qualidade dos dados
No Caso Rural C, duas fontes fornecidas divergem: o orçamento informa geração média de 657 kWh/mês, enquanto o cadastro do monitoramento informa 7.284,83 kWh/ano (aprox. 607,07 kWh/mês). O aplicativo usa o valor anual do monitoramento e explicita a divergência ao usuário.

## Como executar
1. Instale Python 3.10 ou superior.
2. Abra um terminal na pasta do projeto.
3. Instale as dependências: `pip install -r requirements.txt`
4. Execute: `streamlit run app.py`

## Funcionalidades
- seleção entre três casos rurais reais anonimizados;
- cálculo de tarifa efetiva a partir da fatura de referência;
- consumo anual estimado;
- cobertura teórica do consumo;
- economia anual simplificada;
- payback simples;
- produtividade do sistema;
- apresentação da geração registrada em 2026 e do desempenho do período;
- comparação entre os casos;
- modo livre para novas simulações.

## Limitações
Os cálculos possuem finalidade didática. A ferramenta não modela integralmente regras de compensação, impostos futuros, custo de disponibilidade, degradação dos módulos, manutenção, inflação energética, taxa mínima de atratividade ou fluxo de caixa descontado.
