# -*- coding: utf-8 -*-

"""
******************************************************************************
plotMap.py - Módulo para auxiliar na plotagem de mapas com dados

Autor   : Nelson Rossi Bittencourt
Versão  : 0.132
Licença : MIT
Dependências: matplotlib e cartopy
******************************************************************************
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature

# TODO: implementar as demais características do mapa.


# Classes

class Mapa:
    """
    Classe Mapa - Define o layout do mapa a plotar.

    É utilizado nas rotinas 'plotarMapa' e 'loadMapTemplate'.

    Também poderá ser instanciada pelo usuário para criar modelos de mapas próprios ou modelos de mapas lidos de arquivos.

    """

    def __init__(self):
        #self.mapa_nome = ''
        #self.mapa_tipo = ''
        self.mapa_coordenadas = []
        self.mapa_tipo = ''
        self.barraCores_titulo = ''
        self.barraCores_orientacao = ''
        self.barraCores_valores = []
        self.barraCores_codigos = []
        self.barraCores_posicao = ''
        self.barraCores_corMinimo = ''
        self.barraCores_corMaximo = ''
        self.barraCores_dist = 0
        self.barraCores_tam = 0


class ArquivoShape:
    """
    Classe ArquivoShape - Representa as características de um arquivo tipo 'shape file' para inserção em um mapa.

    Para criar uma nova instância dessa classe é preciso fornecer o nome completo do arquivo 'shp'.

    Esta classe permite que um mesmo arquivo shape seja utilizado em diversos mapas, sem o overhead causado
    pela leitura do arquivo diversas vezes.

    """

    def __init__(self, nomeArquivo, corFace='none', corLinha='gray', espLinha=0.5):
        self.shape_feature = ShapelyFeature(Reader(nomeArquivo).geometries(), ccrs.PlateCarree(),
                                            facecolor=corFace, edgecolor=corLinha, linewidth=espLinha,)


# Funções

def plotarMapa(titulo, lons, lats, dados, modeloMapa, destino='', shapeFile=-1):
    """
    Plota um mapa considerando os dados fornecidos.

    Argumentos
    ----------
    titulo : Título do mapa;

    lons : Lista com as longitutes;

    lats : Lista com as latitudes;

    dados : Lista com os dados a plotar;        

    modeloMapa  : string ou objeto tipo 'Mapa'. 
        A string deve conter um nome de arquivo de template válido.
        Mapa deve conter uma instância do tipo 'Mapa' válida.

    destino : (Opcional) Nome do arquivo de saída para a figura. Se não declarado, exibe mapa na tela.

    shapeFile   : (Opcional) Deve ser fornecido:
        O nome do arquivo tipo 'shp' para leitura do disco

        ou um objeto tipo 'ArquivoShape' instanciado previamente

        ou uma lista contendo uma combinação de strings e objetos tipo 'ArquivoShape'

    Retorno
    -------    
        Nenhum.    
    """

    # Verifica o tipo de argumento passado em 'modeloMapa'.

    tipoModelo = type(modeloMapa)
    if tipoModelo is str:
        myMap = loadMapTemplate(modeloMapa)
    elif tipoModelo is Mapa:
        myMap = modeloMapa
    else:
        raise NameError(
            "O argumento 'modeloMapa' deve ser uma string ou um tipo 'Mapa'!")

    # Fecha uma figura anterior, se houver.
    plt.close()

    # Determina o tamanho do gráfico no console do Python.
    fig = plt.figure(figsize=(5, 5))

    # Detemina tipo de projeção.
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    # Delimita o mapa.
    ax.set_extent(myMap.mapa_coordenadas, ccrs.PlateCarree())

    # Adiciona algumas caracteristica no mapa.
    # Talvez, no primeiro uso, o 'matplotlib'/'cartopy' execute o download de mapas com as características requeridas.
    ax.add_feature(cartopy.feature.LAND)
    ax.add_feature(cartopy.feature.COASTLINE)
    ax.add_feature(cartopy.feature.BORDERS)

    # Adiciona arquivos tipo 'shape' ao mapa.
    # Lista que conterá (ou não) strings, 'ArquivosShape' ou uma combinação.
    newList = []

    # Caso 'shapeFile' não seja uma lista, cria uma lista.
    if (type(shapeFile)) is not list:
        newList.append(shapeFile)
    else:
        newList = shapeFile

    # Para cada item da lista 'newList', verifica o tipo e adiciona a característica no mapa
    for item in newList:
        tipoItem = type(item)
        if tipoItem is ArquivoShape:
            ax.add_feature(item.shape_feature)
        elif tipoItem is str:
            tmp = ArquivoShape(item)
            ax.add_feature(tmp.shape_feature)

    # Variáveis auxiliares para ajuste do mapa de cores
    infbound = None
    supbound = None
    extend = 'neither'

    # Ajusta código de cores se necessário.
    if (myMap.barraCores_corMinimo != '-1') and (myMap.barraCores_corMaximo != '-1'):
        extend = 'both'
        infbound = myMap.barraCores_corMinimo
        supbound = myMap.barraCores_corMaximo
    elif (myMap.barraCores_corMinimo != '-1'):
        extend = 'min'
        infbound = myMap.barraCores_corMinimo
    else:
        extend = 'max'
        supbound = myMap.barraCores_corMaximo

    # Cria mapa de cores.
    cmap = (mpl.colors.ListedColormap(myMap.barraCores_codigos).with_extremes(
        over=supbound, under=infbound))

    # Cria o índice de cores do mapa
    norm = mpl.colors.BoundaryNorm(myMap.barraCores_valores, cmap.N)

    # Cria o gráfico de acordo com o tipo selecionado.
    if (myMap.mapa_tipo == 'contornos'):
        filled = ax.contourf(lons, lats, dados, levels=myMap.barraCores_valores,
                             cmap=cmap, norm=norm, extend=extend, transform=ccrs.PlateCarree())
    elif (myMap.mapa_tipo == 'xy'):
        filled = ax.scatter(lons, lats, c=dados, s=50, alpha=1, cmap=cmap,
                            norm=norm, edgecolors='black', transform=ccrs.PlateCarree())
    else:
        raise NameError(
            "Tipo de mapa (mapa_tipo) inválido! Verifique o arquivo de template.")

    # Ajusta a barra de cores, se houver.
    if myMap.barraCores_orientacao != "none":

        cbar = fig.colorbar(
            filled,
            orientation=myMap.barraCores_orientacao,
            label=myMap.barraCores_titulo,
            spacing='uniform',
            pad=myMap.barraCores_dist,
            fraction=myMap.barraCores_tam,
            location=myMap.barraCores_posicao,
            extendfrac='auto',
        )

        cbar.set_ticks(myMap.barraCores_valores)

    # Define título do gráfico.
    plt.title(titulo)

    # Adiciona grid.
    g1 = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                      linewidth=1, color='gray', alpha=0.5, linestyle='--')
    g1.top_labels = False
    g1.right_labels = False
    g1.xlabel_style = {'size': 9, 'color': 'blue', 'weight': 'bold'}
    g1.ylabel_style = {'size': 9, 'color': 'red', 'weight': 'bold'}

    # Mostra na tela ou salva em arquivo.
    if destino == '':
        plt.show(block=True)

    else:
        fig.savefig(destino)


def loadMapTemplate(arquivoTemplateMapa):
    """
    Lê as características de um modelo de mapa a partir de um arquivo de texto formatado.

    Argumentos
    ----------

    arquivoTemplateMapa : nome do arquivo contendo template do Mapa.
        Este arquivo deve seguir, estritamente, o formato estabelecido.

    Retorno
    -------
    objeto Mapa (ver definição da classe 'Mapa' neste arquivo).        

    """

    # Lista com as linhas lidas do arquivo de template de um mapa.
    lines = []

    # Número de linhas válidas esperado.
    check_valid_lines = 11

    # Contador de linhas válidas.
    valid_lines = 0

    # Número da linha atual que está sendo lida
    num_line = 0

    # Dicionário com dados lidos.
    map_dict = {}

    # Abre arquivo e lê as linhas válidas.
    # O caracter '#' é utilizado para comentários no arquivo de template.
    # Se o número de linhas válidas for diferente do esperado, lança uma exceção.
    try:

        with open(arquivoTemplateMapa, 'r') as f:

            for line in f:
                line = line.rstrip()
                num_line = num_line + 1
                prefix = line.strip()

                if len(prefix) > 0 and prefix[0] != '#':
                    if (':' in line):
                        lines.append(line)
                        valid_lines = valid_lines + 1
                        listValues = line.split(':')
                        map_dict[listValues[0]] = listValues[1]
                    else:
                        raise NameError("Linha inválida no arquivo de template '{}'. Verique a linha {}.".format(
                            arquivoTemplateMapa, num_line))

    except:
        raise NameError("Erro ao tentar abrir o arquivo de template para o mapa [{}]!\nVerifique o caminho completo do arquivo e tente novamente.".format(
            arquivoTemplateMapa))

    # Verifica se o arquivo contem o número de linhas válidas.
    if valid_lines != check_valid_lines:
        raise NameError("O arquivo de template '{}' contêm {} linhas válidas, quando o esperado são {} linhas.".format(
            arquivoTemplateMapa, valid_lines, check_valid_lines))

    # Aloca os valores em um objeto do tipo 'Mapa'
    # TODO: Comentar alocações abaixo, se necessário
    local_map = Mapa()

    try:
        local_map.mapa_tipo = map_dict['mapa_tipo']

        local_map.barraCores_orientacao = map_dict['barra_cores_orientacao']
        local_map.barraCores_titulo = map_dict['barra_cores_titulo']

        local_map.barraCores_corMinimo = map_dict['barra_cores_corMinimo']
        local_map.barraCores_corMaximo = map_dict['barra_cores_corMaximo']

        local_map.barraCores_posicao = map_dict['barra_cores_posicao']
        local_map.barraCores_codigos = map_dict['barra_cores_codigos'].split(
            ',')

        local_map.barraCores_dist = float(map_dict['barra_cores_dist'])
        local_map.barraCores_tam = float(map_dict['barra_cores_tam'])

        tmp = map_dict['barra_cores_valores'].split(',')
        local_map.barraCores_valores = [float(i) for i in tmp]

        tmp = map_dict['mapa_coordenadas'].split(',')
        local_map.mapa_coordenadas = [float(i) for i in tmp]

    except:
        raise NameError("Erro ao tentar interpretar o arquivo de template [{}] para o mapa!\nVerifique a sintaxe do arquivo e tente novamente.".format(
            arquivoTemplateMapa))

    return(local_map)
