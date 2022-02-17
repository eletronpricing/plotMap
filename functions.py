"""Biblioteca de funcoes para plotagem de mapas
    """

import glob
import os
import sys
import numpy as np
import struct
import pandas as pd
from plotMap.plotMap import ArquivoShape, plotarMapa
from datetime import datetime, timedelta


dir_path = os.path.dirname(os.path.realpath(__file__))

# Nome do arquivo com parâmetros do mapa.
mapTemplate = os.path.join(dir_path, 'templates/ChuvaPrevistaONS.dat')
mapTemplate2 = os.path.join(dir_path, 'templates/AnomaliaWxmaps.dat')

# Objeto 'ArquivoShape' com os Estados do Brasil e bacias.
shapeEstadosBrasil = ArquivoShape(
    nomeArquivo=os.path.join(dir_path, 'shapes/BRA_adm1.shp'), corLinha='gray', espLinha=0.1)
shapeBaciasBrasil = ArquivoShape(
    nomeArquivo=os.path.join(dir_path, 'shapes/Bacias.shp'), corLinha='blue', espLinha=0.3)
listaShapes = [shapeEstadosBrasil, shapeBaciasBrasil]


def lista_input():
    """Monta lista de arquivos na pasta input

    Returns:
        list: lista de arquivos 
    """
    input_folder = os.path.join(os.getcwd(), 'input')

    if os.path.isdir(input_folder):
        listainputs = glob.glob(os.path.join(input_folder, '*.*'))
        # return [os.path.split(i)[1] for i in listainputs] if listainputs else sys.exit("\nATENCAO: NAO HA ARQUIVOS DE CHUVA EM ./input. VERIFIQUE A PASTA\n")
        return [i for i in listainputs] if listainputs else sys.exit("\nATENCAO: NAO HA ARQUIVOS DE CHUVA EM ./input. VERIFIQUE A PASTA\n")


def check_nomearquivo(arquivo_input):
    """Verifica se o arquivo de chuva esta no mesmo formato definido pelo ONS

    Args:
        arquivo_input (string): caminho para o arquivo no formato MAPA_pDDMMYYaDDMMYY.dat
    """

    try:
        nome_arquivo = os.path.split(arquivo_input)[1]
        nome_mapa = nome_arquivo.split('_')[0]
        data_rodada = datetime.strptime(
            nome_arquivo.split('_')[1][1:7], "%d%m%y")
        data_previsao = datetime.strptime(
            nome_arquivo.split('_')[1][8:14], "%d%m%y")

        return True

    except:
        return False


def check_nomearquivo_acc(arquivo_input):
    """Verifica se o arquivo de chuva acumulada esta no formato MAPA_pDDMMYYaDDMMYYaDDMMYY.dat

    Args:
        arquivo_input (string): caminho para o arquivo
    """

    try:
        nome_arquivo = os.path.split(arquivo_input)[1]
        nome_mapa = nome_arquivo.split('_')[0]
        data_rodada = datetime.strptime(
            nome_arquivo.split('_')[1][1:7], "%d%m%y")
        data_previsao_ini = datetime.strptime(
            nome_arquivo.split('_')[1][8:14], "%d%m%y")
        data_previsao_fim = datetime.strptime(
            nome_arquivo.split('_')[1][15:21], "%d%m%y")

        return True

    except:
        return False


def check_nomearquivo_diff(arquivo_input):
    """Verifica se o arquivo de diferencial de chuva esta no formato MAPA_pDDMMYYpDDMMYYaDDMMYY.dat

    Args:
        arquivo_input (string): caminho para o arquivo
    """

    try:
        nome_arquivo = os.path.split(arquivo_input)[1]
        nome_mapa = nome_arquivo.split('_')[0]
        data_rodada1 = datetime.strptime(
            nome_arquivo.split('_')[1][1:7], "%d%m%y")
        data_rodada2 = datetime.strptime(
            nome_arquivo.split('_')[1][8:14], "%d%m%y")
        data_previsao_ini = datetime.strptime(
            nome_arquivo.split('_')[1][15:21], "%d%m%y")

        return True

    except:
        return False


def deleta_arquivos(nome_pasta):
    """Deleta arquivos da pasta informada (input ou output)

    Args:
        nome_pasta (string): nome da pasta
    """
    validos = {'input', 'output'}
    if nome_pasta not in validos:
        sys.exit(f"Pasta {nome_pasta} nao encontrada. Saindo do programa.")

    print(f"Deletando arquivos na pasta {nome_pasta}...")
    name_folder = os.path.join(os.getcwd(), nome_pasta)

    old_files = glob.glob(os.path.join(name_folder, "*"))
    for f in old_files:
        os.remove(f)


def dados_Mapa(arquivo_input):
    """Retorna informacoes basicas do arquivo de chuva

    Args:
        arquivo_input (string): caminho para o arquivo
    """

    nome_arquivo = os.path.split(arquivo_input)[1]

    nome_mapa = nome_arquivo.split('_')[0]
    data_rodada = datetime.strptime(
        nome_arquivo.split('_')[1][1:7], "%d%m%y").strftime('%d/%m/%Y')
    data_previsao_ini = (datetime.strptime(
        nome_arquivo.split('_')[1][8:14], "%d%m%y") - timedelta(1)).strftime('%d/%m/%Y')
    data_previsao_fim = datetime.strptime(
        nome_arquivo.split('_')[1][8:14], "%d%m%y").strftime('%d/%m/%Y')

    return nome_mapa, data_rodada, data_previsao_ini, data_previsao_fim


def dados_Mapa_acc(arquivo_input):
    """Retorna informacoes basicas do arquivo de chuva acumulada

    Args:
        arquivo_input (string): caminho para o arquivo
    """

    nome_arquivo = os.path.split(arquivo_input)[1]

    nome_mapa = nome_arquivo.split('_')[0]
    data_rodada = datetime.strptime(
        nome_arquivo.split('_')[1][1:7], "%d%m%y").strftime('%d/%m/%Y')
    data_previsao_ini = (datetime.strptime(
        nome_arquivo.split('_')[1][8:14], "%d%m%y") - timedelta(1)).strftime('%d/%m/%Y')
    data_previsao_fim = (datetime.strptime(
        nome_arquivo.split('_')[1][15:21], "%d%m%y")).strftime('%d/%m/%Y')

    return nome_mapa, data_rodada, data_previsao_ini, data_previsao_fim


def dados_Mapa_diff(arquivo_input):
    """Retorna informacoes basicas do arquivo de diferencial de chuva 

    Args:
        arquivo_input (string): caminho para o arquivo
    """

    nome_arquivo = os.path.split(arquivo_input)[1]

    nome_mapa = nome_arquivo.split('_')[0]
    data_rodada1 = datetime.strptime(
        nome_arquivo.split('_')[1][1:7], "%d%m%y").strftime('%d/%m/%Y')
    data_rodada2 = datetime.strptime(
        nome_arquivo.split('_')[1][8:14], "%d%m%y").strftime('%d/%m/%Y')
    data_previsao_ini = (datetime.strptime(
        nome_arquivo.split('_')[1][15:21], "%d%m%y") - timedelta(1)).strftime('%d/%m/%Y')
    try:
        data_previsao_fim = (datetime.strptime(
            nome_arquivo.split('_')[1][15:21], "%d%m%y")).strftime('%d/%m/%Y')
    except:
        data_previsao_fim = datetime.strptime(
            nome_arquivo.split('_')[1][15:21], "%d%m%y").strftime('%d/%m/%Y')

    return nome_mapa, data_rodada1, data_rodada2, data_previsao_ini, data_previsao_fim


def plotMapaONS(arquivo_input='', arquivo_output=''):
    """Plota mapa a partir de arquivos .dat no formato ONS

    Raises:
        NameError: [description]
    """

    # apaga arquivos antigos na pasta de output
    deleta_arquivos('output')

    # se nao for informado um arquivo de entrada, serao considerados os arquivos constantes da pasta 'input'
    if arquivo_input == '':
        lista_arquivos = lista_input()
    else:
        lista_arquivos = [arquivo_input]

    for arquivo in lista_arquivos:

        # verifica se o arquivo esta no formato correto, do contrario vai para o proximo
        if not check_nomearquivo(arquivo):
            print(
                f"O arquivo {arquivo} nao esta no formato ONS. Este arquivo nao sera plotado")
            continue
        else:
            nome_mapa, data_rodada, data_previsao_ini, data_previsao_fim = dados_Mapa(
                arquivo)

        # abre arquivo e salva em dataframe
        try:
            df = pd.read_csv(arquivo, header=None, delim_whitespace=True)
        except:
            raise NameError(
                'Erro ao tentar abrir/acessar arquivo: {}'.format(arquivo))

        # nomeia colunas
        df.columns = ['lon', 'lat', 'mm']
        # sorting requerido pelo modulo de plotagem
        df = df.sort_values(['lat', 'lon'])

        # colunas para listas
        lons = df['lon'].tolist()
        lats = df['lat'].tolist()
        chuva = df['mm'].tolist()

        # remove duplicados das listas de lon e lat. Soh eh necessario inputar as listas de latitude e longitude.
        # A funcao plotarmapa se encarrega de fazer a combinacao das series
        lons = list(dict.fromkeys(lons))
        lats = list(dict.fromkeys(lats))

        # Converte listas de lon e lat em arrays numpy
        lons = np.array(lons, dtype=float)
        lats = np.array(lats, dtype=float)

        # Transforma a lista 'chuva' em uma matriz e altera o seu 'formato' para compatibilidade com a o número de longitudes
        # e latitudes. Veja o método 'reshape' do 'numpy' para maiores detalhes.
        chuva = np.array(chuva, dtype=float)
        chuva = np.reshape(chuva, (len(lats), -1))

        # Define o titulo do mapa a partir do nome do arquivo ONS (nomemapa_pDDMMYYaDDMMYY.dat)
        titulo_mapa = f'Modelo {nome_mapa}\nPrecipitacao entre 12Z {data_previsao_ini} ate 12Z {data_previsao_fim}\nPrevisao das 00Z do dia {data_rodada}'

        # define o nome do arquivo de output
        if arquivo_output == '':
            arquivo_destino = 'output/' + \
                os.path.splitext(os.path.split(arquivo)[1])[0] + '.png'
        else:
            arquivo_destino = arquivo_output

        print(f"Plotando mapa do arquivo {os.path.split(arquivo)[1]}...")

        plotarMapa(titulo=titulo_mapa,
                   lons=lons,
                   lats=lats,
                   dados=chuva,
                   modeloMapa=mapTemplate,
                   destino=arquivo_destino,
                   shapeFile=listaShapes
                   )


def plotMapaONS_acc(arquivo_input='', arquivo_output=''):
    """Plota mapa a partir de arquivos .dat de chuva acumulada no formato ONS

    Raises:
        NameError: [description]
    """

    # apaga arquivos antigos na pasta de output
    deleta_arquivos('output')

    # se nao for informado um arquivo de entrada, serao considerados os arquivos constantes da pasta 'input'
    if arquivo_input == '':
        lista_arquivos = lista_input()
    else:
        lista_arquivos = [arquivo_input]

    for arquivo in lista_arquivos:

        # verifica se o arquivo esta no formato correto, do contrario vai para o proximo
        if not check_nomearquivo_acc(arquivo):
            print(
                f"O arquivo {arquivo} nao esta no formato ONS. Este arquivo nao sera plotado")
            continue
        else:
            nome_mapa, data_rodada, data_previsao_ini, data_previsao_fim = dados_Mapa_acc(
                arquivo)

        # abre arquivo e salva em dataframe
        try:
            df = pd.read_csv(arquivo, header=None, delim_whitespace=True)
        except:
            raise NameError(
                'Erro ao tentar abrir/acessar arquivo: {}'.format(arquivo))

        # nomeia colunas
        df.columns = ['lon', 'lat', 'mm']
        # sorting requerido pelo modulo de plotagem
        df = df.sort_values(['lat', 'lon'])

        # colunas para listas
        lons = df['lon'].tolist()
        lats = df['lat'].tolist()
        chuva = df['mm'].tolist()

        # remove duplicados das listas de lon e lat. Soh eh necessario inputar as listas de latitude e longitude.
        # A funcao plotarmapa se encarrega de fazer a combinacao das series
        lons = list(dict.fromkeys(lons))
        lats = list(dict.fromkeys(lats))

        # Converte listas de lon e lat em arrays numpy
        lons = np.array(lons, dtype=float)
        lats = np.array(lats, dtype=float)

        # Transforma a lista 'chuva' em uma matriz e altera o seu 'formato' para compatibilidade com a o número de longitudes
        # e latitudes. Veja o método 'reshape' do 'numpy' para maiores detalhes.
        chuva = np.array(chuva, dtype=float)
        chuva = np.reshape(chuva, (len(lats), -1))

        # Define o titulo do mapa a partir do nome do arquivo ONS (nomemapa_pDDMMYYaDDMMYY.dat)
        titulo_mapa = f'Modelo {nome_mapa}\nPrecipitacao entre 12Z {data_previsao_ini} ate 12Z {data_previsao_fim}\nPrevisao das 00Z do dia {data_rodada}'

        # define o nome do arquivo de output
        if arquivo_output == '':
            arquivo_destino = 'output/' + \
                os.path.splitext(os.path.split(arquivo)[1])[0] + '.png'
        else:
            arquivo_destino = arquivo_output

        print(f"Plotando mapa do arquivo {os.path.split(arquivo)[1]}...")

        plotarMapa(titulo=titulo_mapa,
                   lons=lons,
                   lats=lats,
                   dados=chuva,
                   modeloMapa=mapTemplate,
                   destino=arquivo_destino,
                   shapeFile=listaShapes
                   )


def plotMapaONS_diff(arquivo_input='', arquivo_output=''):
    """Plota mapa a partir de arquivos .dat de diferencial de chuva no formato ONS

    Raises:
        NameError: [description]
    """

    # apaga arquivos antigos na pasta de output
    deleta_arquivos('output')

    # se nao for informado um arquivo de entrada, serao considerados os arquivos constantes da pasta 'input'
    if arquivo_input == '':
        lista_arquivos = lista_input()
    else:
        lista_arquivos = [arquivo_input]

    for arquivo in lista_arquivos:

        # verifica se o arquivo esta no formato correto, do contrario vai para o proximo
        if not check_nomearquivo_diff(arquivo):
            print(
                f"O arquivo {arquivo} nao esta no formato ONS. Este arquivo nao sera plotado")
            continue
        else:
            nome_mapa, data_rodada1, data_rodada2, data_previsao_ini, data_previsao_fim = dados_Mapa_diff(
                arquivo)

        # abre arquivo e salva em dataframe
        try:
            df = pd.read_csv(arquivo, header=None, delim_whitespace=True)
        except:
            raise NameError(
                'Erro ao tentar abrir/acessar arquivo: {}'.format(arquivo))

        # nomeia colunas
        df.columns = ['lon', 'lat', 'mm']
        # sorting requerido pelo modulo de plotagem
        df = df.sort_values(['lat', 'lon'])

        # colunas para listas
        lons = df['lon'].tolist()
        lats = df['lat'].tolist()
        chuva = df['mm'].tolist()

        # remove duplicados das listas de lon e lat. Soh eh necessario inputar as listas de latitude e longitude.
        # A funcao plotarmapa se encarrega de fazer a combinacao das series
        lons = list(dict.fromkeys(lons))
        lats = list(dict.fromkeys(lats))

        # Converte listas de lon e lat em arrays numpy
        lons = np.array(lons, dtype=float)
        lats = np.array(lats, dtype=float)

        # Transforma a lista 'chuva' em uma matriz e altera o seu 'formato' para compatibilidade com a o número de longitudes
        # e latitudes. Veja o método 'reshape' do 'numpy' para maiores detalhes.
        chuva = np.array(chuva, dtype=float)
        chuva = np.reshape(chuva, (len(lats), -1))

        # Define o titulo do mapa a partir do nome do arquivo ONS (nomemapa_pDDMMYYaDDMMYY.dat)
        titulo_mapa = f'Modelo {nome_mapa}\nAnomalia % entre 12Z {data_previsao_ini} ate 12Z {data_previsao_fim}\nPrevisoes das 00Z do dia {data_rodada1} vs dia {data_rodada2}'

        # define o nome do arquivo de output
        if arquivo_output == '':
            arquivo_destino = 'output/' + \
                os.path.splitext(os.path.split(arquivo)[1])[0] + '.png'
        else:
            arquivo_destino = arquivo_output

        print(f"Plotando mapa do arquivo {os.path.split(arquivo)[1]}...")

        plotarMapa(titulo=titulo_mapa,
                   lons=lons,
                   lats=lats,
                   dados=chuva,
                   modeloMapa=mapTemplate2,
                   destino=arquivo_destino,
                   shapeFile=listaShapes
                   )


if __name__ == '__main__':
    plotMapaONS()
    # print(lista_input())
