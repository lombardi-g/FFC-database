class Interface:

    @staticmethod
    def welcome():
        print(f"Cole o link da súmula, depois confirme com ENTER")
        print("Campeonato Catarinense: ")

    # Escolher diferentes campeonatos e formatos de súmula?
    # @staticmethod
    # def choose_mode():
    #     print("What would you like to do?")
    #     print("1 - Campeonato Catarinense")
    #     print("2 - BG Prime")
    #     print("3 - Copa SC")
    #     while True:
    #         try:
    #             user_choice = input("Enter 1 or 2 to select option: ")
    #             assert user_choice in ["1", "2"]
    #             break
    #         except AssertionError:
    #             print("Invalid option! Please try again...")
    #     return user_choice

    @classmethod
    def assert_URL():
        while True:
                pasted_URL = input("")
                if pasted_URL.startswith("https://egol.fcf.com.br/"):
                    return pasted_URL
                else:
                    print("Inválido!")
