from scraping import scrape_match_summary, excel_file

def assertURL():
    print("Colar link da súmula, confirmar com Enter: ")
    while True:
        pasted_URL = input("")
        if pasted_URL.startswith("https://egol.fcf.com.br/SISGOL"):
            return pasted_URL
        else:
            print("Inválido")


if __name__ == "__main__":
    print(f'Leitor de súmulas da FCF.\nPara funcionamento correto:\n1 - A base de dados deve estar com o nome: {excel_file}\n2 - O arquivo {excel_file} e este programa devem estar na mesma pasta\n')
    validURL = assertURL()
    scrape_match_summary(validURL)
    print("\nConcluído.")