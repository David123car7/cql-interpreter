# main.py

from interpreter import load_observacoes

def main():
    data = load_observacoes("observacoes.csv")
    # agora 'data' está disponível para o teu lexer/parser/interpreter
    print("Dados carregados:", data)

    # exemplo de uso: processar cada linha
    for row in data:
        print("Linha:", row)

if __name__ == "__main__":
    main()
