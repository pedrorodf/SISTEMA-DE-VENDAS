# Sistema de Cadastro de Vendas

Aplicação web simples para cadastrar vendas, consultar os registros e acompanhar
indicadores em um dashboard. A interface é feita com Streamlit e os dados são
armazenados no arquivo `vendas.csv`.

## Funcionalidades

- Cadastro de vendas pela barra lateral.
- Campos de data, vendedor, produto, quantidade e valor unitário.
- Validação dos campos antes de salvar: quantidade maior que zero e valor
  unitário igual ou maior que zero.
- Consulta das vendas cadastradas na área principal.
- Dashboard com faturamento total, número de vendas, unidades vendidas e
  gráficos por vendedor e produto.

O faturamento de cada registro é calculado como **quantidade × valor unitário**.

## Requisitos

- Python instalado.
- Dependências listadas em `requirements.txt`.

## Instalação e execução no Windows

Abra o PowerShell na pasta do projeto e execute:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run main.py
```

O Streamlit abrirá a aplicação no navegador. Se necessário, acesse o endereço
local informado no terminal.

## Dados das vendas

O arquivo `vendas.csv` fica na mesma pasta que `main.py`. Se ele não existir,
a aplicação cria um arquivo com as colunas:

| Coluna | Descrição |
| --- | --- |
| `data` | Data da venda, no formato ISO (`AAAA-MM-DD`) |
| `vendedor` | Nome do vendedor |
| `produto` | Produto vendido |
| `quantidade` | Unidades vendidas |
| `valor` | Valor unitário do produto |
      
Os vendedores e produtos disponíveis no formulário são definidos em
`main.py`. Para manter os registros, não apague nem substitua `vendas.csv`.
