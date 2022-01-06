import pygame  # Importa biblioteca
from pygame.locals import *  # Importa tudo do módulo locals
from sys import exit  # Importa função para fechar o jogo
import os  # Importa biblioteca
from random import randrange, choice  # Importa módulo da biblioteca, Choice escolhe um N de um intervalo de lista

pygame.init()  # Inicia método pygame
pygame.mixer.init()  # Inicia método som

diretorio_principal = os.path.dirname(__file__)  # Recebe o caminho absoluto da pasta do script
diretorio_imagens = os.path.join(diretorio_principal, 'imagens')  # Recebe caminho da pasta principal com pasta imagens
diretorio_sons = os.path.join(diretorio_principal, 'sons')  # Recebe caminho da pasta principal com pasta sons

largura = 640  # Define largura para tela
altura = 480  # Define altura para tela
branco = (255, 255, 255)  # Define cor branca, podendo ser usado no jogo, inclusive para tela
preto = (0, 0, 0)  # Define cor preto, podendo ser usado no jogo, inclusive para tela

tela = pygame.display.set_mode((largura, altura))  # Cria tela do jogo
pygame.display.set_caption("Dino Game")  # Nome tela

sprite_sheet = pygame.image.load(os.path.join(diretorio_imagens, 'dinogame.png')).convert_alpha()  # Recebe spritesheet

som_colisao = pygame.mixer.Sound(os.path.join(diretorio_sons, 'sons_death_sound.wav'))  # Recebe o som da colisão
som_colisao.set_volume(1)  # Configura volume da colisão

som_pontuacao =pygame.mixer.Sound(os.path.join(diretorio_sons, 'sons_score_sound.wav'))  # Recebe o som da pontuação
som_pontuacao.set_volume(1)  # Configura volume da colisão

colidiu = False  # Varíavel antes de colidir com objetos recebe falso

escolha_obstaculo = choice([0, 1])  # Recebe função que escolhe 0 ou 1 para obstáculo

pontos = 0

velocidade_jogo = 10  # Velocidade referente a 10 pixel por frame

def exibe_mensagem(msg, tamanho, cor): # Cria função para exibir mensagem de pontuação e game over
    fonte = pygame.font.SysFont('comicsansms', tamanho, True, False)  # Define fonte (fonte, tamanho, negrito e itálico)
    mensagem = f'{msg}'  # Formata string para mensagem
    texto_formatado = fonte.render(mensagem, True, cor)  # Junção da fonte com a mensagem (mensagem, cerrilhado, cor)
    return texto_formatado

def reiniciar_jogo():
    global pontos, velocidade_jogo, colidiu, escolha_obstaculo  # Variáveis globais
    pontos = 0
    velocidade_jogo = 10
    colidiu = False
    dino.rect.y = altura - 56 - 96 // 2  # Altura do abjeto
    dino.pulo = False
    dino_voador.rect.x = largura
    cacto.rect.x = largura
    escolha_obstaculo = choice([0, 1])  # Recebe função que escolhe 0 ou 1 para obstáculo


class Dino(pygame.sprite.Sprite):  # Classe chamada dinogame que herda atributos e métodos da classe sprite/pygame
    def __init__(self):  # Cria método construtor
        pygame.sprite.Sprite.__init__(self)  # Inicializa a classe
        self.som_pulo = pygame.mixer.Sound(os.path.join(diretorio_sons, 'sons_jump_sound.wav'))  # Recebe o som de pulo
        self.som_pulo.set_volume(1)  # Configura volume
        self.imagens_dinossauro = []  # Cria lista
        for i in range(3):  # Loop que vai de 0 a 3, que recorta o frame da spritesheet (Linha X Y e Coluna X Y)
            img = sprite_sheet.subsurface((i * 32, 0), (32, 32))  # Recorta o frame da spritesheet (Linha e Coluna )
            img = pygame.transform.scale(img, (32 * 3, 32 * 3))  # Tranforma a escala da imagem (em 3 vezes).
            self.imagens_dinossauro.append(img)  # Adiciona na lista a imagem (sprite)

        self.index_lista = 0  # Define posição da imagem atual
        self.image = self.imagens_dinossauro[self.index_lista]  # Define a imagem, que contêm a sprite atual
        self.rect = self.image.get_rect()  # O 'rect' pega o retangulo onde fica a imagem na tela
        self.mask = pygame.mask.from_surface(self.image)  # Cria uma mascara da sprite do dinossauro
        self.pos_y_inicial = altura - 56 - 96 // 2  # Altura do objeto
        self.rect.center = (100, altura - 56)  # Define a posição que será exibido a imagem contida no retângulo.
        self.pulo = False  # Pulo recebe falso

    def pular(self):  # Cria método pular
        self.pulo = True  # Dentro do método pulo é verdadeiro
        self.som_pulo.play()  # Define som para pulo

    def update(self):  # Cria animação das sprites
        if self.pulo == True:  # Se pulo for verdadeiro
            if self.rect.y <= 200:  # Se posição vertical for menor ou igual a 200 pixel
                self.pulo = False  # Se entrar na condição, pulo recebe falso
            self.rect.y -= 20  # Posição vertical recebe -20 pixel
        else:  # Senão
            if self.rect.y < self.pos_y_inicial:  # Se posição vertical for menor que posição vertical inicial
                self.rect.y += 20  # Posição vertical recebe +20 pixel
            else:  # Senão, faça
                self.rect.y = self.pos_y_inicial  # Posição vertical recebe posição vertical inicial

        if self.index_lista > 2:  # Se posição atual for maior que 2
            self.index_lista = 0  # Se condição verdadeira, variável recebe 07
        self.index_lista += + 0.25  # A variável receberá a posição + valor (ajuda controlar velocidade das sprites)
        self.image = self.imagens_dinossauro[int(self.index_lista)]  # Cria o indice das sprites


class Nuvens(pygame.sprite.Sprite):  # Classe que vai mostrar as aleatoriamente as nuvens na tela
    def __init__(self):  # Cria método construtor
        pygame.sprite.Sprite.__init__(self)  # Inicializa a classe
        self.image = sprite_sheet.subsurface((7 * 32, 0), (32, 32))  # Recorta o frame da spritesheet (Linha e Coluna )
        self.image = pygame.transform.scale(self.image, (32 * 3, 32 * 3))  # Tranforma a escala da imagem (se precisar)
        self.rect = self.image.get_rect()  # O 'rect' pega o retangulo onde fica a imagem na tela
        self.rect.y = randrange(50, 200, 50)  # Sorteia um número aleatório de um intervalo para posição Y para nuvem
        self.rect.x = largura - randrange(30, 300, 90)  # Sorteia um número de um intervalo para posição X para nuvem

    def update(self):  # Cria animação das sprites
        if self.rect.topright[0] < 0:  # Condição se a nuvem chegar no canto esquerdo
            self.rect.x = largura  # Se codição verdadeira, nuvem volta para canto direito da tela
            self.rect.y = randrange(50, 200, 50)  # Sorteia um número de um intervalo para posição Y para nuvem
        self.rect.x -= velocidade_jogo  # Movimenta só no eixo X - 10 pixel para esquerda


class Chao(pygame.sprite.Sprite):  # Classe que vai mostrar o chão na tela
    def __init__(self, pos_x):  # Cria método construtor
        pygame.sprite.Sprite.__init__(self)  # Inicializa a classe
        self.image = sprite_sheet.subsurface((6 * 32, 0), (32, 32))  # Recorta o frame da spritesheet (Linha e Coluna )
        self.image = pygame.transform.scale(self.image, (32 * 2, 32 * 2))  # Tranforma a escala da imagem (se precisar)
        self.rect = self.image.get_rect()  # O 'rect' pega o retangulo onde fica a imagem na tela
        self.rect.y = altura - 64  # Recebe valor para posição Y para nuvem
        self.rect.x = pos_x * 64  # Recebe valor para posição X para nuvem

    def update(self):  # Cria animação das sprites
        if self.rect.topright[0] < 0:  # Condição se a nuvem chegar no canto esquerdo
            self.rect.x = largura  # Se codição verdadeira, nuvem volta para canto direito da tela
        self.rect.x -= 10  # Movimenta só no eixo X - 10 pixel para esquerda


class Cacto(pygame.sprite.Sprite):  # Classe que vai mostrar o Cacto na tela
    def __init__(self):  # Cria método construtor
        pygame.sprite.Sprite.__init__(self)  # Inicializa a classe
        self.image = sprite_sheet.subsurface((5 * 32, 0), (32, 32))  # Recorta o frame da spritesheet (Linha e Coluna )
        self.image = pygame.transform.scale(self.image, (32 * 2, 32 * 2))  # Tranforma a escala da imagem (se precisar)
        self.rect = self.image.get_rect()  # O 'rect' pega o retangulo onde fica a imagem na tela
        self.mask = pygame.mask.from_surface(self.image)  # Cria uma mascara para sprite
        self.escolha = escolha_obstaculo  # Vai receber 0 ou 1 (intervalo de uma lista de obstáculos)
        self.rect.center = (largura, altura - 46)  # Recebe valor para posição Y para nuvem
        self.rect.x = largura

    def update(self):  # Cria animação das sprites
        if self.escolha == 0:
            if self.rect.topright[0] < 0:  # Condição se o objeto chegar no canto esquerdo
                self.rect.x = largura  # Se codição verdadeira, nuvem volta para canto direito da tela
            self.rect.x -= velocidade_jogo  # Movimenta só no eixo X - 10 pixel para esquerda


class DinoVoador(pygame.sprite.Sprite):  # Classe que vai mostrar o Dino Voador na tela
    def __init__(self):  # Cria método construtor
        pygame.sprite.Sprite.__init__(self)  # Inicializa a classe
        self.imagens_dinossauro = []
        for i in range(3, 5):  # Loop com interação de 3 a 4 (para no 5)
            img = sprite_sheet.subsurface((i * 32, 0), (32, 32))  # Recorta as sprites
            img = pygame.transform.scale(img, (32 * 3, 32 * 3))  # Transforma scala em 3 vezes o tamanho
            self.imagens_dinossauro.append(img)  # Adiciona na lista imagens_dinossauro

        self.index_lista = 0  # Variável index_lista
        self.image = self.imagens_dinossauro[self.index_lista]  # Recebe o indice da imagem do dino voador
        self.mask = pygame.mask.from_surface(self.image)  # Para verificar colisão
        self.escolha = escolha_obstaculo  # Vai receber 0 ou 1 (intervalo de uma lista de obstáculos)
        self.rect = self.image.get_rect()  # Recebe o retangulo onde está a sprite
        self.rect.center = (largura, 300)  # Posiciona sprite a partir de seu centro
        self.rect.x = largura

    def update(self):  # Cria animação das sprites
        if self.escolha == 1:
            if self.rect.topright[0] < 0:  # Condição se o objeto chegar no canto esquerdo
                self.rect.x = largura  # Se codição verdadeira, objeto volta para canto direito da tela
            self.rect.x -= velocidade_jogo  # Movimenta só no eixo X - 10 pixel para esquerda

            if self.index_lista > 1:  # Se posição atual for maior que 2
                self.index_lista = 0  # Se condição verdadeira, variável recebe 07
            self.index_lista += + 0.25  # A variável receberá a posição + valor (ajuda controlar velocidade das sprites)
            self.image = self.imagens_dinossauro[int(self.index_lista)]  # Cria o indice das sprites


todas_as_sprites = pygame.sprite.Group()  # Variável que recebe um grupo para armazenar sprites que serão instanciadas
dino = Dino()  # Cria um objeto a partir da classe para desenhar objeto na tela
todas_as_sprites.add(dino)  # Adiciona o objeto da classe no grupo todas_as_sprites

for i in range(4):  # Loop com intervalo 4
    nuvem = Nuvens()  # Instancia o objeto nuvem
    todas_as_sprites.add(nuvem)  # Adiciona ao grupo todas as sprites

for i in range(largura * 2 // 64):  # Loop com intervalo 10 (640/64=10)
    chao = Chao(i)  # Cria um objeto a partir da classe para desenhar sprite na tela
    todas_as_sprites.add(chao)  # Adiciona o objeto da classe no grupo todas_as_sprites

cacto = Cacto()  # Cria um objeto a partir da classe para desenhar sprite na tela
todas_as_sprites.add(cacto)  # Adiciona o objeto da classe no grupo todas_as_sprites

dino_voador = DinoVoador()  # Cria um objeto a partir da classe para desenhar sprite na tela
todas_as_sprites.add(dino_voador)

grupo_obstaculos = pygame.sprite.Group()  # Cria o grupo obstáculo
grupo_obstaculos.add(cacto)
grupo_obstaculos.add(dino_voador)

relogio = pygame.time.Clock()  # Define o tempo para controlar taxa de frames do jogo

while True:  # Cria o loop principal, onde fica todas as ações do jogo
    relogio.tick(30)  # Define taxa de frame do jogo
    tela.fill(branco)  # Pinta tela toda de preto
    for event in pygame.event.get():  # Cria loop dos eventos capturados
        if event.type == QUIT:  # Se o tipo do evento for sair
            pygame.quit()  # Chama a função para sair do pygame
            exit()  # Executa função para fechar janela
        if event.type == KEYDOWN:  # Condição em caso de tecla pressionada
            if event.key == K_SPACE and colidiu == False:  # Condição em caso de tecla espaço pressionada
                if dino.rect.y != dino.pos_y_inicial:  # Se posição vertical do dino for diferente que a inicial
                    pass  # Não faz nada
                else:  # Senão
                    dino.pular()  # Em caso da tecla espaço pressionada, chama método pular

            if event.key == K_r and colidiu == True:  # Condição em caso de tecla pressionada
                reiniciar_jogo()

    colisoes = pygame.sprite.spritecollide(dino, grupo_obstaculos, False, pygame.sprite.collide_mask)  # Cria a colisão

    todas_as_sprites.draw(tela)  # Desenha o objeto sapo na tela

    if cacto.rect.topright[0] <= 0 or dino_voador.rect.topright[0] <= 0:  # Se cacto ou dino voador sairem da tela
        escolha_obstaculo = choice([0, 1])  # Ecolha entre os intervalos
        cacto.rect.x = largura  # Cacto volta para início
        dino_voador.rect.x = largura  # dino voador volta para o início
        cacto.escolha = escolha_obstaculo
        dino_voador.escolha = escolha_obstaculo

    if colisoes and colidiu == False:  # Se aconteceer a colisão e colidiu for falso
        som_colisao.play()  # Toca som da colisão
        colidiu = True  # Variável troca para verdadeiro

    if colidiu == True:  # Se variável verdadeira
        if pontos % 100 == 0:  # Se resto da divisão igual a 0
            pontos += 1  # Incrementa +1
        game_over = exibe_mensagem('Game Over!', 40, preto)  # Exibe função mensagem
        tela.blit(game_over, (largura//2, altura // 2))  # Exibe mensagem na posição
        restart = exibe_mensagem('Precione "r" para reiniciar!', 20, preto)  # Exibe mensagem para reiniciar jogo
        tela.blit(restart, (largura//2, (altura // 2) + 60))  # Exibe mensagem na posição abaixo da mensagem game over
    else:  # Senão
        pontos += 1  # Incrementa + 1 para cada atualização como pontos
        todas_as_sprites.update()  # Atualiza as sprites do jogo
        texto_pontos = exibe_mensagem(pontos, 40, preto)  # Variável da função para exibir mensagem formatada

    if pontos % 100 == 0:  # Se o resto da divisão for igual a 0
        som_pontuacao.play()  # Toca som dos pontos
        if velocidade_jogo >= 23:  # Velocidade escolhida pela possibilidade de jogabilidade (velocidade máxima)
            velocidade_jogo += 0.5  # Não encrementa na velocidade máxima
        else:
            velocidade_jogo += 1  # Aumenta velocidade + 1

        print(velocidade_jogo)




    tela.blit(texto_pontos, (520, 30))  # Exibe mensagem (mensagem, posição)

    pygame.display.flip()  # Atualiza a tela
