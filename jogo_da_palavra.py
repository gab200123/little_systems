#Este jogo tem o intuito de um indivíduo inserir uma palavra e o outro vai tentar acertar.
#Posteriormente, podemos fazer o cadastro de dicas para fácil identificação da palavra.
import getpass
import random

pal_sec = getpass.getpass('Digite CUIDADOSAMENTE a palavra secreta: \n')

while ' ' in pal_sec or len(pal_sec) <= 1:
  getpass.getpass('Digite CUIDADOSAMENTE apenas UMA PALAVRA secreta: \n')

print(f'A palavra secreta tem {len(pal_sec)} letras')
lista_pal_sec = list(pal_sec)
check_pal_sec = ['_'] * len(pal_sec)

ofensa = ["bobalhão", "folgado", "trapalhão", "zé ruela", "tontão", "maluco beleza", "cabeça de vento", "pirado", "figuraça", "engraçadinho", "atrapalhado", "sem noção", "bicho grilo", "doido varrido", "fanfarrão", "cabeça de abóbora", "burraldo", "cabeça de farinha", "bicho papão", "chato pra caramba", "bagunceiro", "saco de risada", "mentiroso profissional", "tigre de papel", "abestalhado", "bunda mole", "vagabundo com diploma", "mestre do caos", "rei da zoeira", "bicho papão de papel", "o rei do improvável", "liso como sabão", "cavalo de fogo", "zumbi de pijama"]

iniciar = 'n'

if iniciar == 'n':
  iniciar = input(f'Deseja iniciar, {random.choice(ofensa)}?? [s] ou [n] \n').lower()

  while iniciar == 'n':
    iniciar = input(f'Vai jogar ou não, {random.choice(ofensa)}?? [s] ou [n] \n').lower()

  if iniciar == 's':
    
    while check_pal_sec != lista_pal_sec:
      deci_usu = input(f'Deseja escolher uma letra[l] ou chutar a palavra[p], {random.choice(ofensa)}?? \n').lower()
      
      if deci_usu == 'l':
        let_usu = input('Bota aí a letra que tu quer. \n').lower()
        
        if len(let_usu) > 1 or len(let_usu) <= 0:
          let_usu = input(f'Deixa de palhaçada e digita UMA letra, {random.choice(ofensa)}!! \n').lower()
          
        for i in range(0, len(lista_pal_sec)):
          
          if let_usu in lista_pal_sec[i]:
            check_pal_sec[i] = let_usu
            
            if check_pal_sec == lista_pal_sec:
              print(f'Parabéns!! Era {pal_sec} mesmo, quem vê até pensa que é esperto um {random.choice(ofensa)} desse. Acabou!')
              exit()
        print(f'A palavra está assim agora: {check_pal_sec}')
            
      elif deci_usu == 'p':
        pal_usu = input(f'Diz a palavra que tu ACHA que é: \n').lower()
        
        if pal_usu == pal_sec:
          print(f'Parabéns!! Era {pal_sec} mesmo, quem vê até pensa que é esperto um {random.choice(ofensa)} desse. Acabou!')
          exit()

        else:
          print('Errooooooooouuuuu! KKKKKKKKKKKKKKKK')
