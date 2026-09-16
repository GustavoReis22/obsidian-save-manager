import subprocess


url_repository= ((subprocess.run (["git", "remote", "-v"], shell= True, capture_output= True, text=True)).stdout)
url_repository= url_repository[url_repository.find("h"):(url_repository.find("(")-1)]
response_open_link= subprocess.run(f"start {url_repository}", shell=True, capture_output=True, text=True)
if response_open_link.returncode != 0:
    print("Erro ao tentar abrir o repositorio:")
    print(response_open_link.stderr)
else:
    print("Repositorio aberto com sucesso")
    input("Ação finalizada. Pressione ENTER para voltar ao menu")