# 💊 Farmácia HBR — Catálogo e pedidos online

Aplicação acadêmica de uma farmácia virtual com **Flask e MySQL**. Reúne catálogo de produtos, carrinho em sessão, cadastro de clientes, endereços e um fluxo de pagamento simulado.

## Funcionalidades

- Catálogo com busca por nome ou marca e página de detalhes.
- Cadastro, login e logout de clientes.
- Carrinho com inclusão, remoção e alteração de quantidades.
- Registro de pedidos e endereço de entrega.
- Histórico de pedidos do cliente.
- Confirmação de pagamento simulada, sem integração com uma operadora.
- Cadastro e edição de produtos por administradores, com upload de imagens.
- Atualização do estoque durante a finalização do pedido.

## Tecnologias

| Camada | Ferramentas |
| --- | --- |
| Back-end | Python, Flask, Flask-MySQLdb |
| Persistência | MySQL, consultas SQL via MySQLdb |
| Interface | HTML, Jinja2 e arquivos de template |
| Sessões e uploads | Sessão do Flask, Werkzeug |

## Como executar

### 1. Preparar o ambiente

Tenha Python, pip, Git e MySQL instalados.

```bash
git clone https://github.com/Loadingzs/Conict.git
cd Conict
python -m venv .venv
```

No PowerShell, ative com `.\.venv\Scripts\Activate.ps1`. No Linux/macOS, use `source .venv/bin/activate`.

```bash
python -m pip install flask flask-mysqldb
```

`Flask-MySQLdb` depende de `mysqlclient`. Se a instalação falhar, confira os requisitos nativos de compilação e bibliotecas cliente do MySQL no seu sistema.

### 2. Criar o banco

Na raiz do projeto, abra o cliente MySQL:

```bash
mysql -u root -p
```

Dentro do cliente:

```sql
SOURCE Conict.sql;
```

O script cria o banco `sistema_farmacia`, tabelas, produtos iniciais e as colunas adicionais `imagem` e `tipo`. Execute-o em uma base nova: o script contém operações que não são idempotentes.

### 3. Configurar e iniciar

Em `main.py`, ajuste `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD` e `MYSQL_DB` para seu ambiente. Defina também uma chave de sessão própria em `app.secret_key`.

```bash
python main.py
```

Abra <http://localhost:5000> e crie uma conta em `/cadastro`.

Para testar o painel administrativo, altere o tipo de uma conta de teste no banco:

```sql
UPDATE clientes SET tipo = 'admin' WHERE email = 'seu-email-de-teste@example.com';
```

Saia da sessão e entre novamente para carregar o novo perfil.

## Estrutura

```text
Conict/
├── main.py             # Rotas, sessões, consultas SQL e uploads
├── Conict.sql          # Estrutura e dados iniciais
├── templates/          # Catálogo, autenticação, pedidos e administração
└── static/uploads/     # Imagens de produtos
```

## Roteiro de verificação

1. Cadastre um cliente e faça login.
2. Busque um produto, abra os detalhes e adicione-o ao carrinho.
3. Altere a quantidade e conclua o pedido com endereço.
4. Confirme o pagamento simulado e consulte `/meus-pedidos`.
5. Com a conta administrativa, cadastre e edite um produto.

## Estado atual

O projeto usa sessões do Flask e SQL direto; não utiliza Flask-Login nem SQLAlchemy. As senhas de clientes ainda são comparadas e armazenadas em texto simples. A aplicação é um protótipo de estudo: hash de senhas, validações de estoque, proteção dos formulários e testes automatizados são próximos passos.

## Autor

**Maykon Dias** · [GitHub](https://github.com/Loadingzs) · [LinkedIn](https://www.linkedin.com/in/maykondias/)
