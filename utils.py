import os

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def get_int_input(prompt, valid_options=None, error_msg="Entrada inválida."):
    """Solicita uma entrada de inteiro do usuário e continua tentando até ser válida."""
    while True:
        try:
            val = int(input(prompt))
            if valid_options and val not in valid_options:
                print(f"{error_msg} Opções válidas: {valid_options}")
                continue
            return val
        except ValueError:
            print(f"{error_msg} Deve ser um número inteiro.")
            if valid_options:
                print(f"Opções válidas: {valid_options}")
