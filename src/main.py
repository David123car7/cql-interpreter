from files import load_file

def main():
    dados = load_file("estacoes.csv")
    print("Dados carregados com sucesso!")

    for linha in dados:
        print(linha)

if __name__ == "__main__":
    main()
