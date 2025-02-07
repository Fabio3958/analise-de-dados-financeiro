import requests


def recupera_taxa_selic():
    """ Função simples para recuperar a taxa selic convertida para decimal. """

    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json"
    response = requests.get(url).json()
    return float(response[0]["valor"])/100
