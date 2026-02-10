# Este é um jogo de adivinhar o número
import random

secretNumber = random.randint(1,20)
print('Estou pensando em um número entre 1 e 20.')

#Peça para o jogador adivinhar 6 vezes
for guessesTaken in range(1,7):
    print('Chute um número')
    guess = int(input())

    if guess < secretNumber:
        print('Chutou baixo..')
    elif guess > secretNumber:
        print('Chutou alto..')
    else:
        break #Esse é o palpite correto

if guess == secretNumber:
    print('Boa! Você acertou em '+str(guessesTaken)+' tentativas!')

else:
    print('Deu ruim! O número que eu estava pensando era o '+str(secretNumber))
