import requests


def recupera_taxa_selic() -> float:
    """ Função simples para recuperar a taxa selic convertida para decimal. """

    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json"
    try:
        response = requests.get(url).json()
    except Exception as e:
        raise RuntimeError(f"Houve um erro ao obter o valor da taxa selic com a API do banco central: {e}")

    return float(response[0]["valor"])/100
