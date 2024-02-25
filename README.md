# pygame

#### Índice
1. [Desenvolvimento](#Desenvolvimento)

## Desenvolvimento
1. Clone o repositorio com o comando ``git clone https://github.com/AndreFGard/erm.git``
2. É necessário instalar o pip. No linux, é possível fazer isso com um dos seguintes comandos:
     * ``sudo apt install python3-pip``
     * ``sudo pacman -S python-pip``
     * etc
3. baixe as dependências - apenas o pacote ``pygame``, **por enquanto**:
   * Ubuntu/debian:
   * ``pip install -r requirements.txt`` 
  *<details>
    *<summary>Archlinux e outras distros bleeding-edge</summary>
    *<br>
     Pode ser necessario instalar o modulo venv através do seu gerenciador de pacotes antes de executar este comando.
     ``python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt``
  *</details>
