
import pygame
import random
import os
from pygame import mixer
mixer.init()
pygame.init()

# medidas da tela
LARGURA_TELA = 400
ALTURA_TELA = 600


# criando a tela
screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption('space burrico')

# cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
AZULBB = (153, 217, 234)
RED = (255, 0, 0)
DARK_BLUE = (17, 49, 179)

# definir a q taxas o bonequinho mexe
clock = pygame.time.Clock()

# funções
SCROLL_TRESH = 200  # altura da linha
GRAVIDADE = 1  # velocidade q o burro cai
MAX_PLATAFORMAS = 8  # quantidade de plataformas
scroll = 0
bg_scroll = 0
gameOver = False
efeitoLegen = 0
tela_venceu = False
start = True
score = 0
FPS = 60
# loop do jogo
run = True
flag = True
dif = 1
fase_update = 3500
restart_game = False


# MUSIQUINHAS
pygame.mixer.music.load('All Star.wav')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

win = pygame.mixer.Sound('Won!.wav')
win.set_volume(0.6)
death = pygame.mixer.Sound('morte.wav')
death.set_volume(0.6)

# score
if os.path.exists('score.txt'):
    with open('score.txt', 'r') as file:
        highScore = int(file.read())
else:
    highScore = 0

# fontes
fonteP = pygame.font.SysFont('lucida console', 20)
fonteG = pygame.font.SysFont('lucida console', 24)
fonteS = pygame.font.SysFont('lucida console', 20)

# load images

# fazendo load da imagem. precisa colocar ela pra rodar dentro do jogo com o blit.
bg_image = pygame.image.load('ceunovo3.png').convert_alpha()
bg_image2 = pygame.image.load('bg2.png').convert_alpha()
bg_image3 = pygame.image.load('fundo3.4.jpg').convert_alpha()
boneco_image = pygame.image.load('burro/Donkey.gif').convert_alpha()
plataforma_image = pygame.image.load('pt1.png').convert_alpha()
nave_image = pygame.image.load('My project2tes3.2.png').convert_alpha()
venceu_img = pygame.image.load('burico.png').convert_alpha()

# função para texto na tela


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# função para desenhar info na tela


def draw_panel(dif):
    pygame.draw.rect(screen, BLACK, (0, 0, LARGURA_TELA, 30))
    # inicio, fim, largura da linha
    pygame.draw.line(screen, WHITE, (0, 30), (LARGURA_TELA, 30), 2)
    draw_text('SCORE: ' + str(score), fonteS, WHITE, 0, 0)
    draw_text(f'{dif}° LEVEL', fonteS, WHITE, 170, 0)

# função p desenhar o fundo


def draw_bg(scroll, textura):
    screen.blit(textura, (0, 0 + scroll))
    screen.blit(textura, (0, -600 + scroll))

# player class


class Player():
    def __init__(self, x, y):
        self.image = pygame.transform.scale(
            boneco_image, (45, 45))  # tamanho do burro
        self.width = 42  # tamanho do retangulo
        self.height = 42  # tamanho do retangulo
        # criando o retangulo
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)  # argumentos para jumpy
        self.vel_y = 0  # velocidade
        self.flip = False  # faz com q o burro vire

    def move(self):
        # resetar variaveis
        scroll = 0
        dx = 0
        dy = 0

        # keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            dx = -10  # "velocidade" q ele anda
            self.flip = True
        if key[pygame.K_d]:
            dx = 10  # "velocidade" q ele anda
            self.flip = False

        # gravidade
        self.vel_y += GRAVIDADE
        dy += self.vel_y

        # certificar q o burrico n saia da tela
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > LARGURA_TELA:
            dx = LARGURA_TELA - self.rect.right

        # colisão com as plataformas
        for plataforma in grupo_de_plataforma:
            # colisão na direção y
            if plataforma.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # checando se o burro ta acima da plataforma
                if self.rect.bottom < plataforma.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = plataforma.rect.top  # o boneco fica em cima da pltaforma
                        dy = 0
                        self.vel_y = -20

        
        #colisao com o chao   
        if self.rect.bottom + dy > ALTURA_TELA:
            dy = 0
            self.vel_y = -20
        

        # checar se o burro pulou para o topo da tela
        if self.rect.top <= SCROLL_TRESH:  # se o burro ultrapassar a linha, preciso "rolar" o jogo
            # se o burro estiver pulando
            if self.vel_y < 0:  # por conta desse if o jogo vai "rolar" pra baixo
                scroll = -dy  # o jogo vai "rolar" pra baixo na mesma velocidade q o burro se move pra cima

        # atualizar a posição do retangulo
        self.rect.x += dx
        self.rect.y += dy + scroll

        # atualizar mask
        self.mask = pygame.mask.from_surface(self.image)
        return scroll

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False),
                    (self.rect.x - 5, self.rect.y - 5))  # desenhando o personagem
        # pygame.draw.rect(screen, WHITE, self.rect, 2)retangulo do pernonagem

# plataforma class


class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(
            plataforma_image, (width, 5))  # tamanho da plataforma
        self.rect = self.image.get_rect()  # tamanho do retangulo
        self.rect.x = x  # coordenada, localização
        self.rect.y = y  # coordenada

    def update(self, scroll):
        # atualizar a posição vertical da plataforma
        self.rect.y += scroll

        # CHECAR SE A PLATAFORMA SAIU DA TELA
        if self.rect.top > ALTURA_TELA:
            self.kill()  # apaga a plataforma caso ela tenha sumido da tela fazendo com q sejam criadas novas plataformas


class nave(pygame.sprite.Sprite):
    def __init__(self, LARGURA_TELA, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.direcao = random.choice([-1, 1])  # da p fazer a nave da de ré
        if self.direcao == -1:
            self.flip = True
        else:
            self.flip = False

        self.image = pygame.transform.scale(nave_image, (50, 50))
        self.image = pygame.transform.flip(nave_image, self.flip, False)
        self.rect = self.image.get_rect()

        if self.direcao == 1:
            self.rect.x = 0
        else:
            self.rect.x = LARGURA_TELA
        self.rect.y = y

    def update(self, scroll):
        self.rect.x += self.direcao * 2  # MOVE A NAVE
        self.rect.y += scroll

        # checar se saiu da tela
        if self.rect.right < 0 or self.rect.left > LARGURA_TELA:
            self.kill()


# JOGADOR
jumpy = Player(LARGURA_TELA // 2, ALTURA_TELA - 150)  # posição do burro

# criar grupos de sprites
grupo_de_plataforma = pygame.sprite.Group()
grupo_nave = pygame.sprite.Group()

# criar plataforma inicia-la
# tamanho da plataforma 1
plataforma = Plataforma(LARGURA_TELA // 2 - 50, ALTURA_TELA - 50, 100)
grupo_de_plataforma.add(plataforma)

# loop do jogo
while run:

    clock.tick(FPS)  # velocidade q o burro se move
    if start:
        if gameOver == False and score <= 51000 and tela_venceu != True:
            scroll = jumpy.move()  # sem isso o burro n ultrapassa aquela linha

            # colocando fundo p rodar
            bg_scroll += scroll
            if bg_scroll >= 600:
                # tenho dois fundos, um atrás do outro. após os dois rodarem, a variavel reseta (se torna 0) e começa tudo de novo
                bg_scroll = 0

            # gerar plataformas
            if len(grupo_de_plataforma) < MAX_PLATAFORMAS:
                # largura da plataforma é atualizada de acordo como o aumento da dificuldade
                p_w = random.randint(60, 80)-(dif*4)
                # posição da plataforma no eixo x
                p_x = random.randint(0, LARGURA_TELA - p_w)
                # determina a altura das plataformas, tendo como base a primeira plataforma criada. posição da primeira plataforma - um numero aleatorio
                p_y = plataforma.rect.y - random.randint(80, 120)
                # POSIÇÕES DAS PLATAFORMAS, X E Y. LARGURA DA PLATAFORMA
                plataforma = Plataforma(p_x, p_y, p_w)
                grupo_de_plataforma.add(plataforma)

            # atualizar plataformas
            grupo_de_plataforma.update(scroll)

            # gerar inimigos
            if len(grupo_nave) == 0 and score > 5500:
                inimigo = nave(LARGURA_TELA, 20, 1.5)
                grupo_nave.add(inimigo) #adiciona o foguinho

            # atualizar nave
            grupo_nave.update(scroll)

            # atualizar score
            if scroll > 0:
                score += scroll
            # mudanças de fases
            if score > fase_update:
                flag = False
                if dif < 35:
                    dif += 1

                fase_update += 3500

            # onde a mudança das skin do jogo de acordo com a fase e flag aconteçem
            if flag:
                draw_bg(bg_scroll, bg_image)  # mapa ceu
                plataforma_image = pygame.image.load('pt1.png').convert_alpha()

            else:
                plataforma_image = pygame.image.load(
                    'pt2.png').convert_alpha()  # mapa espacial
                draw_bg(bg_scroll, bg_image2)

            if fase_update > 25000:
                draw_bg(bg_scroll, bg_image3)  # mapa hell
                plataforma_image = pygame.image.load(
                    'plat3.png').convert_alpha()
                bg_scroll = 0
                nave_image = pygame.image.load(
                    'Meu Projeto (1).png').convert_alpha()
                
            

            # desenhar linha de high score
            pygame.draw.line(screen, WHITE, (0, score - highScore + SCROLL_TRESH),
                             (LARGURA_TELA, score - highScore + SCROLL_TRESH), 3)
            draw_text('HIGH SCORE', fonteS, WHITE, LARGURA_TELA -
                      130, score - highScore + SCROLL_TRESH)

            # desenhando o sprite :)
            grupo_de_plataforma.draw(screen)
            grupo_nave.draw(screen)
            jumpy.draw()

            # desenhar painel
            draw_panel(dif)

            if jumpy.rect.top > ALTURA_TELA:
                gameOver = True
                pygame.mixer.music.stop()
                death.play()
            if pygame.sprite.spritecollide(jumpy, grupo_nave, False, pygame.sprite.collide_mask):
                gameOver = True #morre com foguinho
                pygame.mixer.music.stop()
                death.play()
        else:
            if efeitoLegen < LARGURA_TELA:
                efeitoLegen += 5
                for i in range(0, 6, 2):
                    pygame.draw.rect(
                        screen, BLACK, (0, i * 100,  efeitoLegen, 100))
                    pygame.draw.rect(
                        screen, BLACK, (LARGURA_TELA - efeitoLegen, (i + 1)*100, LARGURA_TELA, 100))

            else:
                draw_text('GAME OVER!', fonteG, AZULBB, 130, 200)
                draw_text('SCORE: ' + str(score), fonteG, AZULBB, 130, 250)
                draw_text('PRESSIONE ENTER PARA SAIR :)',
                          fonteS, AZULBB, 40, 300)

                # atualizar high score
                if score > highScore:
                    highScore = score
                    with open('score.txt', 'w') as file:
                        file.write(str(highScore))

                key = pygame.key.get_pressed()
                if key[pygame.K_RETURN]:
                    run = False
                    pygame.quit()

        if score >= 50000 and tela_venceu != True:

            tela_venceu = True
            if tela_venceu:
                pygame.mixer.music.stop()
                win.play()
            if tela_venceu == True:
                key = pygame.key.get_pressed()
            if key[pygame.K_RETURN]:
                pygame.quit()
                run = False
        if tela_venceu:
            screen.blit(venceu_img, (0, 0))

    # manipulador de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # sair do jogo
            # atualizar high score
            if score > highScore:
                highScore = score
                with open('score.txt', 'w') as file:
                    file.write(str(highScore))
            run = False
        
     # Adicione este bloco para verificar se a tecla Enter foi pressionada
    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        if gameOver or tela_venceu:
            restart_game = True

    # Reiniciar o jogo se a flag restart_game estiver ativada
    if restart_game:
        # Reinicie as variáveis relevantes aqui
        scroll = 0
        bg_scroll = 0
        gameOver = False
        efeitoLegen = 0
        tela_venceu = False
        start = True
        score = 0
        # loop do jogo
        run = True
        flag = True
        dif = 1
        fase_update = 3500
        restart_game = False

        #-----------------------------------------
        # JOGADOR
        jumpy = Player(LARGURA_TELA // 2, ALTURA_TELA - 150)  # posição do burro
        # criar grupos de sprites
        grupo_de_plataforma = pygame.sprite.Group()
        grupo_nave = pygame.sprite.Group()

        # criar plataforma inicia-la
        # tamanho da plataforma 1
        plataforma = Plataforma(LARGURA_TELA // 2 - 50, ALTURA_TELA - 50, 100)
        grupo_de_plataforma.add(plataforma)

        # Reinicie outros valores conforme necessário
        pygame.mixer.music.load('All Star.wav')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

        # Reinicie os grupos de sprite
        

        # Reinicie a posição inicial e outros valores do jogador (jumpy)
       #jumpy.reset()  # Suponha que você tenha um método reset() na sua classe jumpy

        # Desative a flag de reinicialização
        restart_game = False

    pygame.display.update()  # atualizando a tela

pygame.quit()