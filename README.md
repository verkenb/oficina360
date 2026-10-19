# Oficina360

Sistema web demonstrativo para gestão de peças e estoque de pequenas oficinas. O projeto foi pensado como portfólio para praticar Python, Django, banco de dados relacionais, validação de regras de negócio e testes automatizados.

> **Status:** versão inicial (0.1.0). A aplicação é local e usa SQLite para facilitar o primeiro contato. Ainda não é um sistema pronto para uso comercial ou produção.

## Funcionalidades da versão 0.1.0

- Painel com total de peças, estoque baixo, fornecedores e valor estimado do estoque.
- Cadastro e edição de peças com código único, categoria, unidade, custo e estoque mínimo.
- Cadastro de fornecedores.
- Registro de entradas e saídas de peças.
- Bloqueio de saídas maiores que a quantidade disponível.
- Histórico das movimentações.
- Busca por código, nome, categoria ou fornecedor.
- Avisos de peças no estoque mínimo ou abaixo dele.
- Interface responsiva em português.
- Testes automatizados para as regras de estoque e páginas principais.

## Tecnologias

- Python 3.11 ou superior (testado como alvo de desenvolvimento com Django 5.2)
- Django 5.2
- SQLite
- HTML e CSS
- Django Test Framework

## Como executar no Windows

### 1. Instale o Python

Instale Python 3.11 ou superior e marque a opção **Add Python to PATH** durante a instalação. Confira no terminal:

```powershell
python --version
```

### 2. Entre na pasta do projeto

Abra o PowerShell na pasta em que você extraiu/clonou o repositório:

```powershell
cd oficina360
```

### 3. Crie e ative um ambiente virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a ativação do ambiente, você pode usar o Prompt de Comando e executar:

```bat
.venv\Scripts\activate.bat
```

### 4. Instale as dependências

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 5. Prepare o banco de dados

```powershell
python manage.py migrate
```

### 6. Inicie o servidor local

```powershell
python manage.py runserver
```

Abra no navegador: <http://127.0.0.1:8000/>

Para encerrar o servidor, use `Ctrl+C` no terminal.

## Como testar

Com o ambiente virtual ativado:

```powershell
python manage.py test
```

## Primeiros passos dentro da aplicação

1. Abra **Fornecedores** e cadastre um fornecedor (opcional).
2. Abra **Peças e estoque** e cadastre uma peça.
3. Abra **Movimentações** e registre uma **Entrada** para definir a quantidade inicial.
4. Registre saídas conforme as peças forem usadas.
5. Consulte o painel para verificar o nível de estoque e os alertas.

A quantidade não é editada diretamente pelo formulário da peça: ela é atualizada por movimentações, para manter um histórico coerente.

## Estrutura do projeto

```text
oficina360/
├── config/                 # Configurações e URLs do Django
├── estoque/                # Modelos, formulários, views e regras do estoque
│   ├── migrations/         # Histórico de estrutura do banco
│   ├── services.py         # Regra transacional de entrada/saída
│   └── tests.py            # Testes automatizados
├── static/css/style.css    # Estilos da interface
├── templates/              # Templates HTML
├── manage.py
├── requirements.txt
└── README.md
```

## Próximas melhorias

- Ordens de serviço e vínculo entre serviço, moto/veículo e peças consumidas.
- Autenticação, perfis de usuário e permissões.
- Paginação das listagens e filtros por período.
- Exportação de relatórios CSV/PDF.
- API REST documentada.
- Docker e configuração de PostgreSQL.
- Pipeline de integração contínua para executar os testes a cada alteração.

## Segurança e limitações

Esta versão é destinada a aprendizado e demonstração local. Não exponha o servidor de desenvolvimento à internet. Antes de publicar em produção, configure uma chave secreta fora do código, desative `DEBUG`, defina hosts permitidos, use HTTPS, implemente autenticação/permissões e configure banco de dados e backups apropriados.

## Licença

Distribuído sob a licença MIT. Consulte o arquivo `LICENSE`.
