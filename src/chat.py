from search import search_prompt

def main():
    try:
        while True:
            # Solicitar pergunta do usuário (formato exato da especificação)
            print("Faça sua pergunta:")
            print()
            question = input("PERGUNTA: ").strip()
            
            # Verificar se usuário quer sair
            if question.lower() in ['quit', 'exit', 'sair', 'q', '']:
                break
            
            # Processar pergunta usando search.py
            try:
                response = search_prompt(question)
                print(f"RESPOSTA: {response}")
                print()
                print("---")
                print()
            except Exception as e:
                print("RESPOSTA: Não tenho informações necessárias para responder sua pergunta.")
                print(f"\nErro: {e}")
                print()
                print("---")
                print()
                
    except KeyboardInterrupt:
        print("\n\nSaindo...")
    except Exception as e:
        print(f"\nErro: {e}")
        print("Verifique se:")
        print("- O banco PostgreSQL está rodando (docker compose up -d)")
        print("- Os documentos foram ingeridos (python src/ingest.py)")
        print("- As variáveis de ambiente estão configuradas")

if __name__ == "__main__":
    main()