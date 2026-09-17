import os
from random import choice, randint
from constants import *
from scenes import *
from utils import get_int_input, clear_screen

ENEMY_DATA = {
    draw_skeleton_room: {"name": "Esqueleto", "hp": 10},
    draw_zombie_room:   {"name": "Zumbi",     "hp": 15},
    draw_werewolf_room: {"name": "Lobisomem", "hp": 20},
    draw_slime_room:    {"name": "Slime",     "hp": 5},
}

def play_game():
    player_name = create_player()
    if not player_name:
        return
    
    intro_jogo()
    run_cenario(player_name)

def main():
    while True:
        clear_screen()
        print('UMA BUSCA CRISTALIZADA\n\n')
        print("\n---------------\n| |1-Iniciar| |\n---------------\n| |2-Regras | |\n---------------\n| | 3-Sair  | |\n---------------\n")
        
        entrar = get_int_input('\nEscolha aqui a opção: ', [1, 2, 3])
        
        if entrar == 1:
            play_game()
            if not restart():
                break
        elif entrar == 2:
            regras()
        elif entrar == 3:
            clear_screen()
            print("Obrigado por jogar!\nAté próximas aventuras")
            break

def regras():
    clear_screen()
    print('Olá jogador!\nBem vindo ao jogo, as regras são simples\nentão não se preocupe\n\n1- Você é um guerreiro que tem que livrar o mundo do mal do Rei Caveira\n e pegar de volta o Cristal Mágico\n2- Você andará pelas salas e sempre com a opção de continuar ou não\n3- Vão ter salas com itens escondidos ou com monstros para lutar\n4- Tente achar o Rei Caveira, mas cuidado! Você pode não achar ele\nTenha um ótimo jogo\n')
    get_int_input('|4-Voltar|\n', [4], "Aperte 4 para sair!")

def restart():
    clear_screen()
    print("\n\n----------------------------------------------------------------------------------------------------")
    print('Quer reiniciar?\n------     ------\n|1-SIM |   |2-NÂO |\n ------     ------\n')
    quer = get_int_input("Escolha: ", [1, 2])
    if quer == 1:
        return True
    else:
        clear_screen()
        print('Até a próxima!')
        return False

def create_player():
    clear_screen()
    print('Vamos começar\nVocê é Garoto ou Garota?\n')
    print(draw_player_selection())
    escolha = get_int_input('Insira aqui: ', [1, 2])
    
    gender = "garoto" if escolha == 1 else "garota"
    nome = input(f'Então {gender}, insira seu nome:\n')
    print(f'Bem vindo {nome}')
    return nome

def intro_jogo():
    clear_screen()
    print('---------------------------------------------------------------------------------------')
    print('')
    print('Então, você entrou na Caverna das Almas\nPara derrotar o Rei Caveira e pegar seu Cristal Mágico!\n')
    get_int_input('Aperte 1 para continuar: ', [1], "Tem que apertar 1!")

def get_status_title(prefix, level, hp, coins, damages):
    return f"{prefix}  |  Lv: {level}  Hp: {hp}  Moedas: {coins}  Dano: {damages[0]}/{damages[1]}"

def draw_screen_state(sala_title, sala_text, feedback=""):
    clear_screen()
    print("------------------------------------------------------------------------------------------------")
    print(sala_title)
    print(sala_text)
    if feedback:
        print("\n=========================================")
        print(feedback)
    print("=========================================")

def run_battle(player_name, life, level, damages, inimigo_hp, enemy_name, draw_room_func, sala_prefix, coins, is_boss=False):
    feedback = ""
    
    while inimigo_hp > 0 and life > 0:
        # Atualiza o desenho e os títulos dinamicamente para cada turno
        sala_title = get_status_title(sala_prefix, level, life, coins, damages)
        sala_text = draw_room_func(player_name, enemy_hp=inimigo_hp)
        
        draw_screen_state(sala_title, sala_text, feedback)
        
        if not is_boss:
            print('-----------------    ------------------\n| | 1-Atacar  | |    | |   2-Fugir  | |\n-----------------    ------------------\n')
            decisao = get_int_input('Escolha aqui: ', [1, 2])
        else:
            print('\n -----------------\n| | 1-Atacar  | |\n -----------------\n')
            decisao = get_int_input('Escolha aqui: ', [1])
        
        if decisao == 2:
            feedback = 'Sua coragem foi dizimada,\ne você foge da batalha com vergonha...\n'
            sala_text = draw_room_func(player_name, enemy_hp=inimigo_hp)
            sala_title = get_status_title(sala_prefix, level, life, coins, damages)
            draw_screen_state(sala_title, sala_text, feedback)
            get_int_input('Aperte 1 para continuar: ', [1])
            break
            
        elif decisao == 1:
            golpe = choice(['Acertou!', 'Errou...'])
            
            if golpe == 'Acertou!':
                acerto = choice(['Um golpe de um guerreiro!', 'Acertou bem na cabeça!', 'Foi super efetivo!'])
                dano_causado = choice(damages)
                inimigo_hp -= dano_causado
                
                if inimigo_hp <= 0:
                    inimigo_hp = 0 # não mostrar hp negativo
                    if is_boss:
                        return (life, level, damages, True)
                    
                    level += 1
                    life += LEVEL_UP_HP_BONUS
                    msg_vitoria = f">>> {golpe}\n{acerto}\n"
                    if dano_causado == damages[1]:
                        msg_vitoria += f'CRÍTICO!!!\n'
                    msg_vitoria += f"Você causou {dano_causado} de dano e derrotou o monstro!\n\n"
                    
                    if level >= 2:
                        old_damages = list(damages)
                        damages = [damages[0] + 1, damages[1] + 1]
                        msg_vitoria += f'Seus ataques aumentaram!\nNormal: {old_damages[0]} -> {damages[0]}\nCrítico: {old_damages[1]} -> {damages[1]}\n'
                    
                    msg_vitoria += f'\nSubiu de nível!!\n{level - 1} -> {level}\nSua vida aumentou!!\n{life - LEVEL_UP_HP_BONUS} -> {life}\n\nVocê está mais forte!\nVocê ganhou!\n'
                    
                    sala_title = get_status_title(sala_prefix, level, life, coins, damages)
                    sala_text = draw_room_func(player_name, enemy_hp=inimigo_hp)
                    draw_screen_state(sala_title, sala_text, msg_vitoria)
                    
                    print('Quer continuar?\n ------     ------\n|1-SIM |   |2-NÂO |\n ------     ------\n')
                    continua = get_int_input('Escreva aqui: ', [1, 2])
                    if continua == 1:
                        return (life, level, damages, True)
                    else:
                        print('Você sai da caverna...\n')
                        return (life, level, damages, False)
                else:
                    feedback = f">>> {golpe}\n{acerto}\n"
                    if dano_causado == damages[0]:
                        feedback += f'-{dano_causado} de vida do {enemy_name}\n'
                    else:
                        feedback += f'CRÍTICO!!!\n-{dano_causado} de vida do {enemy_name}\n'
                        
            else:
                erro = choice(['Essa doeu...', 'Revide!', 'Não deixe a morte vencer!'])
                
                if is_boss:
                    dano_inimigo = choice([5, 6, 8])
                else:
                    dano_inimigo = choice([1, 2, 3])
                    
                life -= dano_inimigo
                if life <= 0:
                    life = 0
                
                feedback = f">>> {golpe}\n{erro}\n"
                
                if life <= 0:
                    msg_derrota = feedback + '\nCom o sangue na garganta...\nvocê se lembra da sua aventura até aqui...\nfoi um bom guerreiro...\n\nVocê perdeu...\n'
                    if is_boss:
                        msg_derrota += '\nO Rei caveira dominou o mundo...\n'
                    
                    sala_title = get_status_title(sala_prefix, level, life, coins, damages)
                    sala_text = draw_room_func(player_name, enemy_hp=inimigo_hp)
                    draw_screen_state(sala_title, sala_text, msg_derrota)
                    get_int_input('Aperte 1 para continuar: ', [1])
                    return (0, level, damages, False)
                else:
                    if dano_inimigo in [1, 5]:
                        feedback += f'O {enemy_name} devolveu... Ai!\n-{dano_inimigo} de HP\n'
                    elif dano_inimigo in [2, 6]:
                        feedback += f'Boa jogada do {enemy_name}...\n-{dano_inimigo} de HP\n'
                    else:
                        feedback += f'Nossa, foi crítico...\n-{dano_inimigo} de HP\n'

    return (life, level, damages, True)

def handle_chest_room(player_name, life, level, coins, damages, sala_prefix):
    feedback = 'Um Baú no canto... Suspeito'
    sala_title = get_status_title(sala_prefix, level, life, coins, damages)
    sala_text = draw_chest_room(player_name)
    
    draw_screen_state(sala_title, sala_text, feedback)
    print('Quer dar uma olhada?\n ------     ------\n|1-SIM |   |2-NÂO |\n ------     ------\n')
    olhar = get_int_input('Escolha aqui: ', [1, 2])
    
    if olhar == 1:
        if randint(1, 100) <= 30:
            inimigo_hp = 30
            enemy_name = "Mímico"
            sala_text = draw_mimic_room(player_name, enemy_hp=inimigo_hp)
            feedback = "Você abre o baú... Mas ele tem dentes!\nO baú respira??\nEle te mordeu!! -7 de HP\n"
            life -= 7
            if life <= 0: life = 0
            
            if life <= 0:
                feedback += '\nVocê foi devorado pelo mímico!'
                sala_title = get_status_title(sala_prefix, level, life, coins, damages)
                draw_screen_state(sala_title, sala_text, feedback)
                get_int_input('Aperte 1 para continuar: ', [1])
                return (life, level, coins, damages, False)
                
            feedback += '\nOh não! É um MÍMICO,\nprepare-se para a batalha!'
            life, level, damages, continuou = run_battle(
                player_name, life, level, damages, inimigo_hp, enemy_name, draw_mimic_room, sala_prefix, coins, False
            )
            if not continuou:
                return (life, level, coins, damages, False)
            
            feedback = "Você derrotou o Mímico!"
            # volta ao normal
            sala_text = draw_mimic_room(player_name, enemy_hp=0)
        else:
            if choice(['achou', 'nada']) == 'achou':
                obj = choice(['objeto', 'moeda', 'nada'])
                if obj == 'objeto':
                    if choice(['poção', 'veneno']) == 'poção':
                        feedback = 'Você achou uma poção de vida!\nSeu Hp aumentou +5\n'
                        life += 5
                    else:
                        feedback = 'Você tomou veneno!\nSeu Hp diminuiu -3\n'
                        life -= 3
                elif obj == 'moeda':
                    moeda = choice([1, 5, 25, 40, 65, 100])
                    coins += moeda
                    feedback = f'Você achou moedas!\nVocê tem: ${coins}\n'
                else:
                    feedback = 'Você não encontra nada,\nmas a constante sensação de ser observado...\nnão deixa você!'
            else:
                feedback = 'Não era nada!\n'
    else:
        feedback = 'Você decide ignorar o baú.'

    if life <= 0:
        life = 0
        feedback += '\nVocê morreu envenenado!'
        sala_title = get_status_title(sala_prefix, level, life, coins, damages)
        draw_screen_state(sala_title, sala_text, feedback)
        get_int_input('Aperte 1 para continuar: ', [1])
        return (life, level, coins, damages, False)
        
    sala_title = get_status_title(sala_prefix, level, life, coins, damages)
    draw_screen_state(sala_title, sala_text, feedback)
    print('Quer continuar explorando a caverna?\n ------     ------\n|1-SIM |   |2-NÂO |\n ------     ------\n')
    continua = get_int_input('Escreva aqui: ', [1, 2])
    if continua == 2:
        draw_screen_state(sala_title, sala_text, 'Devido às dificuldades, você decide sair da caverna.')
        get_int_input('Aperte 1 para continuar: ', [1])
        return (life, level, coins, damages, False)
        
    return (life, level, coins, damages, True)

def run_cenario(player_name):
    cont = 0
    life = INITIAL_HP
    level = INITIAL_LEVEL
    coins = INITIAL_COINS
    damages = list(INITIAL_DAMAGES)
    
    while cont < MAX_ROOMS:
        sala_funcs = [draw_chest_room, draw_skeleton_room, draw_zombie_room, draw_werewolf_room, draw_slime_room]
        sala_choice_func = choice(sala_funcs)
        
        cont += 1
        sala_prefix = f"Sala {cont}"
        
        if sala_choice_func == draw_chest_room:
            life, level, coins, damages, continuou = handle_chest_room(
                player_name, life, level, coins, damages, sala_prefix
            )
        else:
            inimigo_info = ENEMY_DATA[sala_choice_func]
            life, level, damages, continuou = run_battle(
                player_name, life, level, damages, 
                inimigo_hp=inimigo_info["hp"], 
                enemy_name=inimigo_info["name"], 
                draw_room_func=sala_choice_func, 
                sala_prefix=sala_prefix,
                coins=coins,
                is_boss=False
            )
            
        if not continuou:
            return

    boss(player_name, life, level, coins, damages)

def boss(player_name, hp, lv, mn, dano):
    sala_prefix = "Sala Final!"
    
    if randint(1, 100) <= 80:
        bosslife = hp + BOSS_HP_BONUS
        sala_text = draw_boss_room(player_name, enemy_hp=bosslife)
        sala_title = get_status_title(sala_prefix, lv, hp, mn, dano)
        
        feedback = 'Você está frente a frente com o inimigo mais forte!\nPrepare-se para...\nA BATALHA FINAL!\n'
        draw_screen_state(sala_title, sala_text, feedback)
        get_int_input('Aperte 1 para continuar: ', [1])
        
        hp, lv, dano, continuou = run_battle(
            player_name, hp, lv, dano, 
            inimigo_hp=bosslife, 
            enemy_name="Rei Caveira", 
            draw_room_func=draw_boss_room, 
            sala_prefix=sala_prefix,
            coins=mn,
            is_boss=True
        )
        
        if hp > 0 and continuou:
            sala_text = draw_boss_room(player_name, enemy_hp=0)
            sala_title = get_status_title(sala_prefix, lv, hp, mn, dano)
            feedback = 'Subiu de nível!!\nSua vida máxima aumentou!!\nVocê ganhou!\n\nVocê livrou o mundo desse mal!\nRecuperou o cristal mágico'
            draw_screen_state(sala_title, sala_text, feedback + draw_crystal())
            get_int_input('Aperte 1 para encerrar: ', [1])
    else:
        sala_text = draw_exit_room(player_name)
        sala_title = get_status_title(sala_prefix, lv, hp, mn, dano)
        feedback = '\nVocê achou a saída, mas não encontrou o Cristal mágico...\nSua aventura foi em vão...\nMas você ganhou bastante experiência.\n\nO Rei caveira dominou o mundo...\n'
        draw_screen_state(sala_title, sala_text, feedback)
        get_int_input('Aperte 1 para encerrar: ', [1])

    clear_screen()
    print("=========================================")
    print(f'Seu level final: {lv}\nSeu HP final: {hp}\nQuantas moedas você tem: {mn}')
    print("=========================================")
    get_int_input('Aperte 1 para continuar: ', [1])

if __name__ == "__main__":
    main()
