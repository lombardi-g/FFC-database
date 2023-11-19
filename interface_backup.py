from scraping import scrape_match_summary, excel_file
import time, sys

def assertURL():
    print("Colar link da súmula, confirmar com Enter: ")
    while True:
        pasted_URL = input("")
        if pasted_URL.startswith("https://egol.fcf.com.br/SISGOL"):
            return pasted_URL
        else:
            print("Inválido, colar link da súmula da FCF")


if __name__ == "__main__":
    try:
        print(f'Leitor de súmulas da FCF.\nPara funcionamento correto:\n- A base de dados deve estar com o nome: {excel_file}\n- O arquivo {excel_file} e este programa devem estar na mesma pasta\n')
        validURL = assertURL()
        scrape_match_summary(validURL)
        print("\nConcluído.")
    except FileNotFoundError:
        print(f'\nO arquivo não está na pasta ou nome {excel_file} está incorreto.')
        time.sleep(3)
    except KeyboardInterrupt:
        print("\nOperação cancelada.")
    except AttributeError:
        print("Erro na leitura da súmula.")
        time.sleep(1)
    
    time.sleep(2)
    sys.exit()