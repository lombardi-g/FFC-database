from scraping import scrape_match_summary

def assertURL():
    print("Colar link da súmula, confirmar com Enter: ")
    while True:
        pasted_URL = input("")
        if pasted_URL.startswith("https://egol.fcf.com.br/SISGOL"):
            return pasted_URL
        else:
            print("Inválido")


if __name__ == "__main__":
    validURL = assertURL()
    scrape_match_summary(validURL)
    print("\nConcluído.")