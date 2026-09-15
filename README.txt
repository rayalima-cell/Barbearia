BARBEARIA NAVALHA DE OURO
Sistema web de consulta de agendamentos

CURSO
Técnico em Desenvolvimento de Sistemas

UNIDADE CURRICULAR
Programação de Aplicativos

DOCENTE
Lucas Grandeaux

INTEGRANTES
1. [Ray Aryel Duarte de Lima]
2. [Cauã Claus Gomes Schunke]
3. [Guilherme Henrique]


1. OBJETIVO

Implementar os requisitos técnicos do trabalho usando Python,
MySQL, Flask, Jinja2 e programação orientada a objetos.

Funcionalidades:
- Página inicial com o total de agendamentos.
- Listagem ordenada por data e horário.
- Filtros por Agendado, Concluído e Cancelado.
- Detalhes de um agendamento.
- Tratamento de agendamento não encontrado.
- Tratamento de indisponibilidade do banco.

Os registros iniciais são inseridos pelo arquivo banco.sql.
Esta versão não possui telas de cadastro, edição ou exclusão.


2. PRÉ-REQUISITOS

- Python 3.10 ou superior.
- MySQL Server 8.0.16 ou superior.
- MySQL Workbench.
- Terminal e editor de código.

Observação:
O Workbench é uma ferramenta de administração.
O MySQL Server também precisa estar instalado e iniciado.


3. PREPARAR O BANCO

1. Abra o MySQL Workbench.
2. Conecte-se ao servidor MySQL.
3. Abra o arquivo banco.sql.
4. Execute o script completo.
5. Atualize a lista de schemas.
6. Confira o banco barbearia e a tabela agendamentos.

O script contém 8 registros fictícios:
- 3 Concluído.
- 2 Cancelado.
- 3 Agendado.

Execute o script de instalação apenas uma vez.
Ele pressupõe que a tabela agendamentos ainda não existe.

Não reexecute o script inteiro em um banco já inicializado:
a criação da tabela falhará e, dependendo da forma de execução,
as inserções seguintes poderão duplicar os dados.

O script não contém comandos para apagar dados existentes.


4. CONFIGURAR A CONEXÃO

Abra config.py e confira:

host: localhost
port: 3306
user: seu usuário MySQL
password: sua senha MySQL
database: barbearia

Também é possível usar as variáveis de ambiente:
DB_HOST
DB_PORT
DB_USER
DB_PASSWORD
DB_NAME

Não compartilhe senhas reais em repositórios ou no ZIP.
Antes da entrega, substitua a senha por um exemplo.


5. CRIAR O AMBIENTE VIRTUAL

Abra o terminal dentro da pasta barberaria.

Windows:
    python -m venv .venv
    .venv\Scripts\activate.bat

O comando de ativação acima é para o Prompt de Comando (CMD).

Windows PowerShell:
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1

Se a ativação for bloqueada, use diretamente:
    .\.venv\Scripts\python.exe -m pip install -r requirements.txt
    .\.venv\Scripts\python.exe app.py

Linux/macOS:
    python3 -m venv .venv
    source .venv/bin/activate


6. INSTALAR AS DEPENDÊNCIAS

Com o ambiente virtual ativado:

    python -m pip install -r requirements.txt


7. EXECUTAR O SISTEMA

Com o MySQL iniciado e o ambiente virtual ativado:

    python app.py

Abra no navegador:

    http://127.0.0.1:5000

Para encerrar, pressione Ctrl+C no terminal.

O servidor incluído é para desenvolvimento e avaliação local,
não para publicação em produção.


8. ROTAS

/                                 Página inicial
/agendamentos                     Todos os agendamentos
/agendamentos/status/Agendado      Filtro de agendados
/agendamentos/status/Concluído     Filtro de concluídos
/agendamentos/status/Cancelado     Filtro de cancelados
/agendamento/1                    Detalhe do registro de ID 1

Para navegar entre os filtros, use os links da página.


9. ORGANIZAÇÃO DO CÓDIGO

config.py:
    Configurações e credenciais do banco.

banco.py:
    Função conectar().

models.py:
    Classe Agendamento e conversão entre objetos e tuplas.
    As tuplas incluem o ID como primeiro campo.

agendamentos.py:
    Consultas SQL e transformação dos resultados em objetos.
    Cada consulta fecha cursor e conexão em finally.

app.py:
    Rotas Flask, filtros Jinja2 e tratamento de erros.

templates/:
    Páginas HTML com Jinja2.

static/style.css:
    Aparência e adaptação para telas menores.

tests/test_sistema.py:
    Testes unitários do modelo e das rotas.

banco.sql:
    Criação do banco, tabela e registros de exemplo.


10. EXECUTAR OS TESTES

Dentro da pasta barberaria, com o ambiente virtual ativado:

    python -m unittest discover -s tests -v

Os testes usam consultas simuladas e não precisam de MySQL ativo.
Não substituem a verificação de integração com o banco real.


11. VERIFICAÇÃO MANUAL COM O MYSQL

Após importar o SQL e iniciar a aplicação:

1. Acesse a página inicial: o total deve ser 8.
2. Abra Agendamentos: devem aparecer os 8 registros.
3. Confira a ordenação por data e horário.
4. Filtre Concluído: devem aparecer 3 linhas verdes.
5. Filtre Cancelado: devem aparecer 2 linhas vermelhas.
6. Filtre Agendado: devem aparecer 3 linhas normais.
7. Abra os detalhes de um registro e confira todos os dados.
8. Acesse /agendamento/999: deve informar que não foi encontrado.


12. ENTREGA

1. Preencha os nomes dos três integrantes neste README.
2. Confira as configurações e faça a verificação manual.
3. Remova credenciais reais antes de compartilhar.
4. Compacte a pasta barberaria em um arquivo ZIP.
5. Inclua banco.sql, README.txt e todos os arquivos do projeto.
6. Não inclua .venv, __pycache__ ou arquivos locais da IDE.