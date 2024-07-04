from datetime import datetime
import os
import shutil
from pathlib import Path

ROOT_PATH = Path(__file__).parent

def log_transacao(func):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        data_hora = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(ROOT_PATH / "log.txt", "a") as arquivo:
                arquivo.write(
                    f"[{data_hora}] Função {func.__name__} executada com argumentos {args} e {kwargs}."
                    f"Retornou {resultado}\n"
                )

        except FileNotFoundError as exc:
            print(f"Não foi possível abrir o arquivo: {exc}")

        except IOError as exc:
            print(f"Erro ao abrir o arquivo: {exc}")

        except Exception as exc:
            print(f"Algum problema ocorreu ao tentar abrir o arquivo: {exc}")


        print(f"{datetime.now()}: {func.__name__.upper()}")
        return resultado
    return envelope