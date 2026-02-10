#Estudo para praticar o uso do in dentro de listas
my_pets = ["Pug","Negao","Sofia"]
name = input("Entre um nome de pet: ")
if name not in my_pets:
    print(f"Eu não tenho um pet chamado {name}")
else:
    print(f"Correto! {name} é o nome do meu pet.")
