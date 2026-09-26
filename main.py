from datetime import datetime
import urllib.request
import subprocess
import time
import os


def git_status():
    clear()
    subprocess.run(["git", "status"])
    input("Pressione ENTER para voltar ao menu")


def git_push():
    clear() 
    date= datetime.now()
    subprocess.run(["git", "add", "."])
    response_commit= subprocess.run(["git", "commit", "-m", f"{date.day}/{date.month}/{date.year}"], capture_output=True, text=True)
    if response_commit.returncode != 0:
            print("Nada para commitar (ou erro no commit):")
            print(response_commit.stderr)
    else:
        print("Commitado com sucesso!")
    response_push= subprocess.run(["git", "push"], capture_output= True, text= True)
    if response_push.returncode != 0:
        print("Erro ao fazer push:")
        print(response_push.stderr)
    else:
        print("Push feito com sucesso!")
    input("Pressione ENTER para voltar ao menu")

def git_pull():
    clear()
    verify_response= verify_update_local
    if verify_response:
        subprocess.run(["git", "stash"], capture_output=True, text=True)
    response= subprocess.run(["git", "pull"], capture_output=True, text=True)
    if response.returncode != 0:
        print("Erro ao fazer pull:")
        print(response.stderr)
    else:
        print("Atulização feita com sucesso")
    if verify_response:
        subprocess.run(["git", "stash", "pop"], capture_output=True, text=True)
    input("Ação finalizada. Pressione ENTER para voltar ao menu")

	
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def pull_cloud():
    print("Puxando arquivos da nuvem, aguarde alguns instantes!")
    subprocess.run(["git", "fetch"], capture_output= True)
    clear()

def open_repository():
    clear()
    
    url_repository= ((subprocess.run (["git", "remote", "-v"], capture_output= True, text=True)).stdout)
    url_repository= url_repository[url_repository.find("h"):(url_repository.find("(")-1)]
    response_open_link= subprocess.run(f"start {url_repository}", shell= True, capture_output=True, text=True)
    if response_open_link.returncode != 0:
        print("Erro ao tentar abrir o repositorio:")
        print(response_open_link.stderr)
    else:
        print("Repositorio aberto com sucesso")
        input("Ação finalizada. Pressione ENTER para voltar ao menu")

def verify_update_cloud():
    response= subprocess.run(["git", "status"], capture_output= True, text= True)
    if "Your branch is up to date with" in response.stdout:
        return False
    else:
        return True

def verify_update_local():
    response= subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if response.stdout != "":
        return True
    else:
        return False

def verify_update_all():
    response_update_cloud= verify_update_cloud()
    response_update_local= verify_update_local()
    return {"response_cloud": response_update_cloud, "response_local": response_update_local}

def verify_network():
    try:
        urllib.request.urlopen("https://google.com", timeout=3)
        return True
    except Exception:
        return False

def default_layout():
    print("-"*35)
    print(" Gerenciamento de Save do Obsidian")
    print("-"*35)
    print("Opções: ")
    print(" 1- Ver status\n",
        "2- Fazer salvamento no GitHub\n",
        "3- Fazer Atualização do conteúdo local\n",
        "4- Abrir repositorio no GitHub\n",
        "5- Fechar terminal")

if __name__ == "__main__":
    pull_cloud()
    while(True):
        clear()

        print("Verificando conexão com a internet...")
        responde_network= verify_network()
        if responde_network == False:
            timer= 4
            for i in range(timer):
                clear()
                print("Não foi possivel encontrar uma conexção com a internet")
                print(f"Esse terminal sera fechado em: {timer}")
                timer-=1
                time.sleep(1)
            break
        else:
            default_layout()
            response_update_all= verify_update_all()

            if (response_update_all["response_cloud"]) and (response_update_all["response_local"]):
                print("AVISO: a versão em nuvem e a local tem atulizações.\nTalvez isso pode gerar conflito!")
                response_conflict= input("Deseja resolver esse conflito? (y/n) > ").replace(" ", "").lower()
                if "y" == response_conflict:
                    git_pull()
                    clear()
                    default_layout()
                else:
                    clear()
                    default_layout()
                    print("AVISO: A versão local do conteudo tem atulizações!")
            elif response_update_all["response_local"]:
                print("AVISO: A versão local do conteudo tem atulizações!")
            elif response_update_all["response_cloud"]:
                print("AVISO: A versão em nuvem do conteudo tem atualizações!")

            option_resp= input("Escolha uma opção: ")
            if option_resp == "1":
                git_status()
            elif option_resp == "2":
                git_push()
            elif option_resp == "3":
                git_pull()
            elif option_resp == "4":
                open_repository()
            elif option_resp == "5":
                break
            else:
                clear()
                print(f"Selecione uma opção valida!")
                time.sleep(2)