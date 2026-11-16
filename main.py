
import pygame
import random
import math
import os

pygame.init()

# Configurações da janela
LARGURA = 480
ALTURA = 650
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Fuga dos Obstáculos - Space Escape")

relogio = pygame.time.Clock()

# Cores
BRANCO = (255, 255, 255)
CIANO = (60, 230, 255)
AZUL = (20, 70, 160)
ROXO = (145, 65, 230)
VERMELHO = (240, 75, 80)
DOURADO = (255, 205, 60)
FUNDO = (5, 10, 28)

# Fontes
fonte_titulo = pygame.font.SysFont("arial", 38, bold=True)
fonte = pygame.font.SysFont("arial", 24, bold=True)
fonte_pequena = pygame.font.SysFont("arial", 17)

# Recorde salvo em arquivo
ARQUIVO_RECORDE = "recorde.txt"

def carregar_recorde():
    try:
        with open(ARQUIVO_RECORDE, "r") as arquivo:
            return int(arquivo.read())
    except:
        return 0

def salvar_recorde(valor):
    with open(ARQUIVO_RECORDE, "w") as arquivo:
        arquivo.write(str(valor))

recorde = carregar_recorde()

# Estrelas do fundo
estrelas = []

for i in range(90):
    estrelas.append([
        random.randint(0, LARGURA),
        random.randint(0, ALTURA),
        random.randint(1, 3),
        random.uniform(0.5, 2)
    ])

def desenhar_fundo():
    tela.fill(FUNDO)

    for estrela in estrelas:
        x, y, tamanho, velocidade = estrela

        pygame.draw.circle(
            tela,
            (160, 210, 255),
            (int(x), int(y)),
            tamanho
        )

        estrela[1] += velocidade

        if estrela[1] > ALTURA:
            estrela[1] = 0
            estrela[0] = random.randint(0, LARGURA)

def texto(mensagem, fonte_usada, cor, x, y):
    imagem = fonte_usada.render(mensagem, True, cor)
    retangulo = imagem.get_rect(center=(x, y))
    tela.blit(imagem, retangulo)

def desenhar_foguete(x, y):
    # Chamas
    pontos_fogo = [
        (x + 15, y + 42),
        (x + 25, y + 65 + random.randint(0, 8)),
        (x + 35, y + 42)
    ]

    pygame.draw.polygon(tela, (255, 140, 30), pontos_fogo)

    # Asas
    pygame.draw.polygon(
        tela, ROXO,
        [(x + 13, y + 32), (x, y + 52), (x + 15, y + 46)]
    )

    pygame.draw.polygon(
        tela, ROXO,
        [(x + 37, y + 32), (x + 50, y + 52), (x + 35, y + 46)]
    )

    # Corpo
    pygame.draw.polygon(
        tela, CIANO,
        [(x + 25, y), (x + 43, y + 43), (x + 7, y + 43)]
    )

    # Janela
    pygame.draw.circle(tela, (15, 40, 80), (x + 25, y + 25), 7)
    pygame.draw.circle(tela, BRANCO, (x + 25, y + 25), 7, 2)

def desenhar_meteoro(meteoro):
    x = meteoro["x"]
    y = meteoro["y"]
    raio = meteoro["raio"]

    pygame.draw.circle(
        tela, (110, 30, 45),
        (int(x + raio), int(y + raio)), raio
    )

    pygame.draw.circle(
        tela, VERMELHO,
        (int(x + raio - 4), int(y + raio - 5)), raio - 4
    )

    pygame.draw.circle(
        tela, (120, 35, 35),
        (int(x + raio - 5), int(y + raio - 4)), 4
    )

    pygame.draw.circle(
        tela, (120, 35, 35),
        (int(x + raio + 6), int(y + raio + 5)), 5
    )

def desenhar_moeda(moeda):
    x = int(moeda["x"])
    y = int(moeda["y"])

    pygame.draw.circle(tela, (170, 105, 10), (x, y), 14)
    pygame.draw.circle(tela, DOURADO, (x, y), 11)
    pygame.draw.circle(tela, (255, 240, 150), (x, y), 7, 2)

    texto("$", fonte_pequena, (130, 80, 10), x, y)

def desenhar_painel(pontos, recorde):
    pygame.draw.rect(tela, (12, 25, 55), (10, 10, 460, 48), border_radius=12)
    pygame.draw.rect(tela, CIANO, (10, 10, 460, 48), 2, border_radius=12)

    texto(f"PONTOS: {pontos}", fonte_pequena, BRANCO, 115, 34)
    texto(f"RECORDE: {recorde}", fonte_pequena, DOURADO, 355, 34)

def botao(mensagem, y):
    retangulo = pygame.Rect(105, y, 270, 55)

    pygame.draw.rect(tela, AZUL, retangulo, border_radius=14)
    pygame.draw.rect(tela, CIANO, retangulo, 2, border_radius=14)

    texto(mensagem, fonte, BRANCO, 240, y + 27)

    return retangulo

def novo_jogo():
    return {
        "jogador_x": 215,
        "jogador_y": 545,
        "pontos": 0,
        "meteor os": [],
        "moedas": [],
        "tempo": 0,
        "velocidade": 4
    }

# Estado inicial
estado = "menu"
jogador_x = 215
jogador_y = 545
pontos = 0
meteoros = []
moedas = []
tempo = 0
velocidade = 4

# Áreas de colisão
def colisao(rect1, rect2):
    return rect1.colliderect(rect2)

# Loop principal
executando = True

while executando:

    relogio.tick(60)

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            executando = False

        if evento.type == pygame.MOUSEBUTTONDOWN:

            if estado == "menu":
                if botao_inicio.collidepoint(evento.pos):
                    estado = "jogando"
                    jogador_x = 215
                    pontos = 0
                    meteoros = []
                    moedas = []
                    tempo = 0
                    velocidade = 4

            elif estado == "fim":
                if botao_reiniciar.collidepoint(evento.pos):
                    estado = "jogando"
                    jogador_x = 215
                    pontos = 0
                    meteoros = []
                    moedas = []
                    tempo = 0
                    velocidade = 4

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                executando = False

            if evento.key == pygame.K_RETURN:
                if estado in ("menu", "fim"):
                    estado = "jogando"
                    jogador_x = 215
                    pontos = 0
                    meteoros = []
                    moedas = []
                    tempo = 0
                    velocidade = 4

    teclas = pygame.key.get_pressed()

    desenhar_fundo()

    if estado == "menu":

        texto("SPACE ESCAPE", fonte_titulo, CIANO, 240, 210)
        texto("FUGA DOS OBSTACULOS", fonte, BRANCO, 240, 265)
        texto("Desvie dos meteoros!", fonte_pequena, BRANCO, 240, 330)
        texto("Colete moedas e aumente sua pontuacao!", fonte_pequena, DOURADO, 240, 360)

        botao_inicio = botao("INICIAR JOGO", 430)

        texto("Use as setas ou A e D para mover", fonte_pequena, CIANO, 240, 525)
        texto("ESC para sair", fonte_pequena, BRANCO, 240, 560)

    elif estado == "jogando":

        tempo += 1

        # Movimento do foguete
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            jogador_x -= 6

        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            jogador_x += 6

        jogador_x = max(0, min(LARGURA - 50, jogador_x))

        # A dificuldade aumenta com o tempo
        velocidade = 4 + pontos // 100

        # Criar meteoros
        if tempo % 48 == 0:
            raio = random.randint(17, 26)

            meteoros.append({
                "x": random.randint(0, LARGURA - raio * 2),
                "y": -raio * 2,
                "raio": raio
            })

        # Criar moedas
        if tempo % 100 == 0:
            moedas.append({
                "x": random.randint(20, LARGURA - 20),
                "y": -20
            })

        # Atualizar meteoros
        for meteoro in meteoros[:]:
            meteoro["y"] += velocidade

            desenhar_meteoro(meteoro)

            area_meteoro = pygame.Rect(
                meteoro["x"], meteoro["y"],
                meteoro["raio"] * 2,
                meteoro["raio"] * 2
            )

            area_jogador = pygame.Rect(
                jogador_x + 7, jogador_y,
                36, 45
            )

            if colisao(area_jogador, area_meteoro):
                estado = "fim"

            if meteoro["y"] > ALTURA:
                meteoros.remove(meteoro)

        # Atualizar moedas
        for moeda in moedas[:]:
            moeda["y"] += 4

            desenhar_moeda(moeda)

            area_moeda = pygame.Rect(
                moeda["x"] - 13,
                moeda["y"] - 13,
                26, 26
            )

            area_jogador = pygame.Rect(
                jogador_x + 7, jogador_y,
                36, 45
            )

            if colisao(area_jogador, area_moeda):
                pontos += 10
                moedas.remove(moeda)

            elif moeda["y"] > ALTURA:
                moedas.remove(moeda)

        # Pontos por sobreviver
        if tempo % 10 == 0:
            pontos += 1

        # Atualizar recorde
        if pontos > recorde:
            recorde = pontos
            salvar_recorde(recorde)

        desenhar_foguete(jogador_x, jogador_y)
        desenhar_painel(pontos, recorde)

    elif estado == "fim":

        texto("FIM DE JOGO!", fonte_titulo, VERMELHO, 240, 230)
        texto(f"Sua pontuacao: {pontos}", fonte, BRANCO, 240, 300)
        texto(f"Recorde: {recorde}", fonte, DOURADO, 240, 345)

        botao_reiniciar = botao("JOGAR NOVAMENTE", 430)

        texto("Pressione ENTER para reiniciar", fonte_pequena, CIANO, 240, 525)
        texto("ESC para sair", fonte_pequena, BRANCO, 240, 560)

    pygame.display.flip()

pygame.quit()
