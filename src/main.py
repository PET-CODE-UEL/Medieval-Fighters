import pygame
from pygame import mixer
from configuracoes import *
from lutador import Lutador

mixer.init()
pygame.init()

# Criando a janela do jogo
janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Fighter")

# Barra de Vida dos Lutadores
def barra_vida(player, vida, x, y):
    razao = vida / 200
    pygame.draw.rect(janela, VERMELHO_ESCURO, (x - 5, y - 5, 410, 45))
    pygame.draw.rect(janela, VERDE_ESCURO, (x, y, 400, 35))
    pygame.draw.rect(janela, VERDE, (x, y, 400 * razao, 35))
    
# setando FPS
clock = pygame.time.Clock()

# Carregando Musicas e Sons
pygame.mixer.music.load("suporte/audios/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(0, 0, 500)

espada_fx = pygame.mixer.Sound("suporte/audios/sword.wav")
espada_fx.set_volume(0.5)

magia_fx = pygame.mixer.Sound("suporte/audios/magic.wav")
magia_fx.set_volume(0.75)

# Carregamento do Plano de Fundo
PF_Imagem = pygame.image.load("suporte/imagens/background/florest.jpg").convert_alpha()

# Carregando as Sprites
cavaleiro_sheet = pygame.image.load("suporte/imagens/warrior/Sprites/warrior.png").convert_alpha()
necromante_sheet = pygame.image.load("suporte/imagens/wizard/Sprites/wizard.png").convert_alpha()

# Carregando a Vitoria
vitoria_img = pygame.image.load("suporte/imagens/icons/victory.png").convert_alpha()

# Definindo o n° de Frames por Animação
CAVALEIRO_ANIMATION_FRAME = [10, 8, 1, 7, 7, 3, 7]
NECROMANTE_ANIMATIO_FRAME = [8, 8, 1, 8, 8, 3, 7]

# Definindo Fontes
numeros_fonte = pygame.font.Font("suporte/fontes/turok.ttf", 100)
pontuacao_fonte = pygame.font.Font("suporte/fontes/turok.ttf", 30)



# Função para desenhar Textos
def draw_Texto(texto, fonte, cor, x, y):
    img = fonte.render(texto, True, cor)
    janela.blit(img, (x, y))

# Função para desenhar o Plano de Fundo
def draw_pf():
    escala_PF = pygame.transform.scale(PF_Imagem, (LARGURA, ALTURA)) # Convertendo o tamanho da imagem == a tamanho da janela
    janela.blit(escala_PF, (0, 0))
    
# Criando Jogadores
lutador_1 = Lutador(1, 200,310, False, NECROMANTE_DADOS, necromante_sheet, NECROMANTE_ANIMATIO_FRAME, magia_fx)
lutador_2 = Lutador(2, 700,310, True, CAVALEIRO_DADOS, cavaleiro_sheet, CAVALEIRO_ANIMATION_FRAME, espada_fx)



# Game Loop:
while ATIVO:
    clock.tick(FPS)
    # Plano de Fundo
    draw_pf()
    
    # Mostrando a barra de Vida
    barra_vida(lutador_1.player ,lutador_1.vida, 15, 15)
    barra_vida(lutador_2.player ,lutador_2.vida, 580, 15)
    draw_Texto("P1:  " + str(PONTUAÇÃO[0]), pontuacao_fonte, VERMELHO_ESCURO, 20, 60)
    draw_Texto("P2:  " + str(PONTUAÇÃO[1]), pontuacao_fonte, VERMELHO_ESCURO, 580, 60)    
    if INICIO_CONTADOR <= 0:
        # movimento dos Lutadores
        lutador_1.movimento(lutador_2, RODADA)
        lutador_2.movimento(lutador_1, RODADA)
    else:
        # Exibição do Contador de Tempo
        draw_Texto(str(INICIO_CONTADOR), numeros_fonte, VERMELHO, LARGURA/2, ALTURA/3)
        
        # Atualização do Contador de Tempo
        if (pygame.time.get_ticks() - ULTIMA_NUMERO) >= 1000:
            INICIO_CONTADOR -= 1
            ULTIMA_NUMERO = pygame.time.get_ticks()

    # Animando Lutadores
    lutador_1.update()
    lutador_2.update()    
    
    # Desenhando Lutadores
    lutador_1.draw(janela)
    lutador_2.draw(janela)
    

    # Verificação da Derrota dos Jogadores
    if RODADA == False:
        if lutador_1.vivo == False:
            PONTUAÇÃO[1] += 1
            RODADA = True
            RODADA_FIM = pygame.time.get_ticks()
        elif lutador_2.vivo == False:
            PONTUAÇÃO[0] += 1
            RODADA = True
            RODADA_FIM = pygame.time.get_ticks()        
    else:
        # Exibição da Imagem de Vitoria
        janela.blit(vitoria_img, (360, 150))
        if pygame.time.get_ticks() - RODADA_FIM > RODADA_NOVA:
            RODADA = False
            
            INICIO_CONTADOR = 4
            lutador_1 = Lutador(1, 200,310, False, NECROMANTE_DADOS, necromante_sheet, NECROMANTE_ANIMATIO_FRAME, magia_fx)
            lutador_2 = Lutador(2, 700,310, True, CAVALEIRO_DADOS, cavaleiro_sheet, CAVALEIRO_ANIMATION_FRAME, espada_fx)
    
    
    # Eventos...
    for event in pygame.event.get():
        # Botão para fechar
        if event.type == pygame.QUIT:
            ATIVO = False

    # Atualização de Tela
    pygame.display.update()

# Fim de Jogo
pygame.quit()