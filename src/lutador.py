import pygame
from configuracoes import SPEED, LARGURA, GRAVIDADE, ALTURA, INDIGO, COOLDAWN

class Lutador():
    def __init__(self, player, x, y, flip, dados, sprite_sheet, animation_frame, som):
        self.player = player
        self.tamanho = dados[0]
        self.imagem_escala = dados[1]
        self.offset = dados[2]
        self.virar = flip
        self.animation_lista = self.carregando_Imgaens(sprite_sheet, animation_frame)
        self.acao = 0 # 0 (ocioso), 1 (correr), 2 (pular), 3 (ataque 1), 4 (ataque 2), 5 (hit), 6 (morte)
        self.frame_index = 0
        self.imagem = self.animation_lista[self.acao][self.frame_index]
        self.contador = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.correr = False
        self.pular = False
        self.atacar = False
        self.ataque_tipo = 0
        self.tempo_de_ataque = 0
        self.hit = False
        self.vivo = True
        self.som_ataque = som
        self.vida = 200
        
    def carregando_Imgaens(self, spritesheet, animation_frame):
        # Extraindo as imagens do spritesheet
        animation_lista = []
        for y, animation in enumerate(animation_frame):
                
            temp_imagem_lista = []
            for x in range(animation):
                temp_img = spritesheet.subsurface(x * self.tamanho, y * self.tamanho, self.tamanho, self.tamanho)
                temp_imagem_lista.append(pygame.transform.scale(temp_img, (self.tamanho * self.imagem_escala, self.tamanho * self.imagem_escala)))
            animation_lista.append(temp_imagem_lista)
        return animation_lista
            
    def movimento(self, inimigo, RODADA):
        dx = 0
        dy = 0
        self.correr = False
        self.ataque_tipo = 0
        
        # Get keypress
        key = pygame.key.get_pressed()
        
        # verificação de players
        if self.player == 1:
            
            # só poderar executar as outras ações quando não estiver atacando
            if self.atacar == False and self.vivo == True and RODADA == False:
                
                # Movimento
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.correr = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.correr = True
                
                # Pulo
                if key[pygame.K_w] and self.pular == False:
                    self.vel_y = -30
                    self.pular = True
                    
                # Ataques    
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.Ataque(inimigo)
                
                    # Determinando o tipo de Ataque
                    if key[pygame.K_r]:
                        self.ataque_tipo = 1
                    
                    if key[pygame.K_t]:
                        self.ataque_tipo = 2    
                
                # Visão dos Jogadores
                if inimigo.rect.centerx > self.rect.centerx:
                    self.virar = False
                else:
                    self.virar = True  
                
                # Aplicando o tempo de ataque no ataque
                if self.tempo_de_ataque > 0:
                    self.tempo_de_ataque -= 1          
        
        if self.player == 2:
            
            # só poderar executar as outras ações quando não estiver atacando
            if self.atacar == False and self.vivo == True and RODADA == False:
                
                # Movimento
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.correr = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.correr = True
                
                # Pulo
                if key[pygame.K_UP] and self.pular == False:
                    self.vel_y = -30
                    self.pular = True
                    
                # Ataques    
                if key[pygame.K_KP1] or key[pygame.K_KP2]:
                    self.Ataque(inimigo)
                
                    # Determinando o tipo de Ataque
                    if key[pygame.K_KP1]:
                        self.ataque_tipo = 1
                    
                    if key[pygame.K_KP2]:
                        self.ataque_tipo = 2    
                
                # Visão dos Jogadores
                if inimigo.rect.centerx > self.rect.centerx:
                    self.virar = False
                else:
                    self.virar = True  
                
                # Aplicando o tempo de ataque no ataque
                if self.tempo_de_ataque > 0:
                    self.tempo_de_ataque -= 1  
            
            
            
            
               
        # Aplicando Gravidade
        self.vel_y += GRAVIDADE
        dy += self.vel_y
            
        # Limite de Tela
        if self.rect.left + dx < 0:
            dx = -self.rect.left

        if self.rect.right + dx > LARGURA:
            dx = LARGURA - self.rect.right

        if self.rect.bottom + dy > ALTURA - 80:
            self.vel_y = 0
            self.pular = False
            dy = ALTURA - 80 - self.rect.bottom
            
            
        # Atualizar movimebto
        self.rect.x += dx
        self.rect.y += dy
        
    # Atualizar Animações
    def update(self):
        # Verificação de Performace
        if self.vida <= 0:
            self.vida = 0
            self.vivo = False
            self.atualizar_Acao(6) # Morreu
        elif self.hit == True:
            self.atualizar_Acao(5) # Tomou dano
        elif self.atacar == True:
            if self.ataque_tipo == 1:
                self.atualizar_Acao(3) # Ataque 1
            elif self.ataque_tipo == 2:
                self.atualizar_Acao(4) # Ataque 2
        elif self.pular == True:
            self.atualizar_Acao(2) # Pular
        elif self.correr == True:
            self.atualizar_Acao(1) # Correr
        else:
            self.atualizar_Acao(0) # Parado
        
        # Atualizando Imagem
        self.imagem = self.animation_lista[self.acao][self.frame_index]
        
        # Verificando o temo de Atualização
        if pygame.time.get_ticks() - self.contador > COOLDAWN:
            self.frame_index += 1
            self.contador = pygame.time.get_ticks()
        # Verificação (fim da animação)
        if self.frame_index >= len(self.animation_lista[self.acao]):
            # Verificação se o jogador está morto
            if self.vivo == False:
                self.frame_index = len(self.animation_lista[self.acao]) - 1
            else:
                self.frame_index = 0
                # Verificação de Execução de Ataques
                if self.acao == 3 or self.acao == 4:
                    self.atacar = False
                    self.tempo_de_ataque = 40
                # Verificação se foi levado Dano
                if self. acao == 5:
                    self.hit = False
                    # Verificação se o jogador estava no meio de um ataque
                    self.atacar = False
                    self.tempo_de_ataque = 30
        
    def Ataque(self, inimigo):
        if self.tempo_de_ataque == 0 and self.hit == False:
            # Executando o Ataque
            self.atacar = True
            self.som_ataque.play()
            attacking_rect = pygame.Rect(self.rect.centerx - (2.5 * self.rect.width * self.virar),
                                        self.rect.y, 2.5 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(inimigo.rect):
                inimigo.vida -= 40
                inimigo.hit = True
        
    
    def atualizar_Acao(self, nova_acao):
        if nova_acao != self.acao:
            self.acao = nova_acao
            # Atualizar configurações de Animações
            self.frame_index = 0
            self.contador = pygame.time.get_ticks()
        
    def draw(self, surface):
        img = pygame.transform.flip(self.imagem, self.virar, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.imagem_escala), self.rect.y - (self.offset[1] * self.imagem_escala)))