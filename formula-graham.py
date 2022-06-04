import requests
import bs4
import pandas
import re
import numpy

print("Extraindo dados de empresas através do site http://www.fundamentus.com.br")

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"}
page = requests.get("http://www.fundamentus.com.br/resultado.php", headers=headers)

html = bs4.BeautifulSoup(page.content, "html.parser")
table = html.find("table", attrs={"id": "resultado"})

columns = table.find("thead").find_all("th")
column_names = [ column.string for column in columns ]

rows = table.find("tbody").find_all("tr")
table_rows = []
for tr in rows:
    tds = tr.find_all("td")
    row = [ str(cell.get_text()).strip() for cell in tds ]
    table_rows.append(row)

dataframe = pandas.DataFrame(table_rows, columns=column_names)

dataframe = dataframe.reindex(
    columns=[
        "Papel",
        "Cotação",
        "P/L",
        "P/VP",
        "Mrg. Líq.",
        "ROE",
        "ROIC",
        "Div.Yield",
        "Dív.Brut/ Patrim.",
        "Liq. Corr.",
        "Liq.2meses",
        "Patrim. Líq",
    ]
)

dataframe["Cotação"] = dataframe["Cotação"].apply(
    lambda n: float(n.replace(".","").replace(",", ".") if n else 0)
)
dataframe["P/L"] = dataframe["P/L"].apply(
    lambda n: float(n.replace(".","").replace(",", ".") if n else 0)
)
dataframe["P/VP"] = dataframe["P/VP"].apply(
    lambda n: float(n.replace(".","").replace(",", ".") if n else 0)
)
dataframe["Mrg. Líq."] = dataframe["Mrg. Líq."].apply(
    lambda n: float(n.replace("%","").replace(".","").replace(",", ".") if n else 0)
)
dataframe["ROE"] = dataframe["ROE"].apply(
    lambda n: float(n.replace("%","").replace(".","").replace(",", ".") if n else 0)
)
dataframe["ROIC"] = dataframe["ROIC"].apply(
    lambda n: float(n.replace("%","").replace(".","").replace(",", ".") if n else 0)
)
dataframe["Div.Yield"] = dataframe["Div.Yield"].apply(
    lambda n: float(n.replace("%","").replace(".","").replace(",", ".") if n else 0)
)
dataframe["Dív.Brut/ Patrim."] = dataframe["Dív.Brut/ Patrim."].apply(
    lambda n: float(n.replace(".","").replace(",", ".") if n else 0)
)
dataframe["Liq. Corr."] = dataframe["Liq. Corr."].apply(
    lambda n: float(n.replace(".","").replace(",", ".") if n else 0)
)
dataframe["Liq.2meses"] = dataframe["Liq.2meses"].apply(
    lambda n: float(n.replace(".","").replace(",", ".") if n else 0)
)
dataframe["Patrim. Líq"] = dataframe["Patrim. Líq"].apply(
    lambda n: float(n.replace(".","").replace(",", ".") if n else 0)
)

print(f"Total de registros: {dataframe['Papel'].count()}")

print("Filtrando apenas empresas com patrimônio líquido positivo")
dataframe = dataframe.loc[
    (dataframe["Patrim. Líq"] > 0)
]
print(f"Total de registros: {dataframe['Papel'].count()}")

print("Filtrando apenas empresas com liquidez maior que R$ 200.000,00")
dataframe = dataframe.loc[
    (dataframe["Liq.2meses"] >= 200000)
]
print(f"Total de registros: {dataframe['Papel'].count()}")

print("Filtrando apenas empresas com P/L entre 0 e 15")
dataframe = dataframe.loc[
    (dataframe["P/L"] >= 0)
    &
    (dataframe["P/L"] <= 15)
]
print(f"Total de registros: {dataframe['Papel'].count()}")

print("Filtrando apenas empresas com P/VP entre 0 e 1.5")
dataframe = dataframe.loc[
    (dataframe["P/VP"] >= 0)
    &
    (dataframe["P/VP"] <= 1.5)
]
print(f"Total de registros: {dataframe['Papel'].count()}")

print("Buscando os lucros dos últimos 5 anos")
dataframe["Lucro Ano -1"] = ""
dataframe["Lucro Ano -2"] = ""
dataframe["Lucro Ano -3"] = ""
dataframe["Lucro Ano -4"] = ""
dataframe["Lucro Ano -5"] = ""

for index, row in dataframe.iterrows():
    try:
        ticker = row['Papel']
        request = requests.get(f"https://statusinvest.com.br/acao/getdre?code={ticker}", headers=headers)
        if request.status_code == 200:
            content = request.json()
            if (content['success']) == True:
                if len(content['data']['grid']) > 0:
                    for row in content['data']['grid']:
                        if row['isHeader'] == False:
                            if row['gridLineModel']['key'] == "LucroLiquido":
                                values = row['gridLineModel']['values']
                                values.pop(0)
                                print('- {}: {}'.format(ticker, values))
        
        if len(values) >= 1:
            dataframe.at[index, "Lucro Ano -1"] = values[0]
        else:
            dataframe.at[index, "Lucro Ano -1"] = 0

        if len(values) >= 2:
            dataframe.at[index, "Lucro Ano -2"] = values[1]
        else:
            dataframe.at[index, "Lucro Ano -2"] = 0
        
        if len(values) >= 3:
            dataframe.at[index, "Lucro Ano -3"] = values[2]
        else:
            dataframe.at[index, "Lucro Ano -3"] = 0
        
        if len(values) >= 4:
            dataframe.at[index, "Lucro Ano -4"] = values[3]
        else:
            dataframe.at[index, "Lucro Ano -4"] = 0
        
        if len(values) >= 5:
            dataframe.at[index, "Lucro Ano -5"] = values[4]
        else:
            dataframe.at[index, "Lucro Ano -5"] = 0
    except Exception as error:
        print(f"O sistema não conseguiu buscar o lucro dos últimos 5 anos da empresa {row['Papel']}")

        dataframe.at[index, "Lucro Ano -1"] = 0
        dataframe.at[index, "Lucro Ano -2"] = 0
        dataframe.at[index, "Lucro Ano -3"] = 0
        dataframe.at[index, "Lucro Ano -4"] = 0
        dataframe.at[index, "Lucro Ano -5"] = 0

print("Filtrando apenas empresas com que não tiveram prejuízo nos últimos 5 anos")
dataframe = dataframe.loc[
    (dataframe["Lucro Ano -1"] >= 0)
    &
    (dataframe["Lucro Ano -2"] >= 0)
    &
    (dataframe["Lucro Ano -3"] >= 0)
    &
    (dataframe["Lucro Ano -4"] >= 0)
    &
    (dataframe["Lucro Ano -5"] >= 0)
]
print(f"Total de registros: {dataframe['Papel'].count()}")

print("Buscando os valores de LPA e VPA")
dataframe["LPA"] = ""
dataframe["VPA"] = ""

for index, row in dataframe.iterrows():
    page = requests.get(f"http://www.fundamentus.com.br/detalhes.php?papel={row['Papel']}", headers=headers)
    html = bs4.BeautifulSoup(page.content, "html.parser")
    
    spans = html.find_all("span", attrs={"class": "txt"})
    for span in spans:
        lpa_label = span.find(string=re.compile("LPA"))
        vpa_label = span.find(string=re.compile("VPA"))

        if lpa_label:
            lpa_value = lpa_label.parent.parent.findNext('td').find('span').string
            dataframe.at[index, "LPA"] = lpa_value
        
        if vpa_label:
            vpa_value = vpa_label.parent.parent.findNext('td').find('span').string
            dataframe.at[index, "VPA"] = vpa_value

dataframe["LPA"] = dataframe["LPA"].apply(
    lambda n: float(n.replace("%","").replace(".","").replace(",", ".") if n else 0)
)
dataframe["VPA"] = dataframe["VPA"].apply(
    lambda n: float(n.replace("%","").replace(".","").replace(",", ".") if n else 0)
)

print("Calculando o Valor Intrínseco usando a Fórmula de Graham")
dataframe["Valor Intrínseco"] = round(numpy.sqrt(22.5 * dataframe["LPA"] * dataframe["VPA"]),2)

print("Calculando a Margem de Segurança")
dataframe["Margem de Segurança"] = round(1 - (dataframe["Cotação"] / dataframe["Valor Intrínseco"]),2)
    
dataframe = dataframe.sort_values("Margem de Segurança", ascending=False)

dataframe = dataframe.reindex(
    columns=[
        "Papel",
        "P/L",
        "P/VP",
        "Cotação",
        "Valor Intrínseco",
        "Margem de Segurança",
        "Div.Yield",
        "Mrg. Líq.",
        "ROE",
        "ROIC",
        "Dív.Brut/ Patrim.",
        "Liq. Corr.",
        "Patrim. Líq",
        "Liq.2meses",
        "LPA",
        "VPA",
        "Lucro Ano -1",
        "Lucro Ano -2",
        "Lucro Ano -3",
        "Lucro Ano -4",
        "Lucro Ano -5"
    ]
)

print("Extraindo os resultados para a planilha Excel")
dataframe.to_excel("formula-graham.xlsx", index=False)

print("Processo finalizado com sucesso")
ok = input("Pressione ENTER para fechar essa janela")