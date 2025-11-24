💊 Farmácia HBR — Sistema de Pedidos Online
https://img.shields.io/badge/Python-3.8+-blue?logo=python
https://img.shields.io/badge/Flask-2.0+-green?logo=flask
https://img.shields.io/badge/MySQL-8.0+-blue?logo=mysql
https://img.shields.io/badge/Tailwind-CSS-38B2AC?logo=tailwind-css
https://img.shields.io/badge/License-MIT-yellow

Um sistema web completo de e-commerce para farmácia, desenvolvido em Python (Flask) e MySQL.
Permite o gerenciamento completo de usuários, produtos e pedidos, com autenticação segura e interface responsiva.

🎯 Visão Geral
O Farmácia HBR é um projeto acadêmico e prático voltado ao aprendizado de desenvolvimento web full stack.
O sistema cobre desde o cadastro de clientes até a simulação do checkout e confirmação de pedidos.

https://via.placeholder.com/800x400/4F46E5/FFFFFF?text=Farm%C3%A1cia+HBR+Dashboard

✨ Funcionalidades
🔐 Autenticação & Segurança
✅ Cadastro de usuários com validação

✅ Login seguro com hash de senha

✅ Dados completos (CPF, endereço, gênero)

✅ Sessões protegidas

🛍️ Catálogo & Produtos
✅ Exibição dinâmica de medicamentos

✅ Busca e filtros de produtos

✅ Detalhes completos dos produtos

✅ Categorização inteligente

🛒 Carrinho & Checkout
✅ Adicionar/remover itens do carrinho

✅ Alterar quantidades em tempo real

✅ Cálculo automático de totais

✅ Simulação de pagamento

✅ Cálculo de frete fixo

📱 Interface & UX
✅ Design responsivo (mobile-first)

✅ Layout moderno com Tailwind CSS

✅ Navegação intuitiva

✅ Feedback visual interativo

🛠️ Tecnologias
Backend
Tecnologia	Função
<img src="https://img.icons8.com/color/48/000000/python.png" width="20"/> Python	Linguagem principal
<img src="https://img.icons8.com/color/48/000000/flask.png" width="20"/> Flask	Framework web
🔐 Flask-Login	Gerenciamento de sessões
🧩 SQLAlchemy	ORM database
🗄️ PyMySQL	Driver MySQL
Frontend
Tecnologia	Função
🧱 HTML5 + Jinja2	Templates dinâmicos
🎨 Tailwind CSS	Framework CSS utility-first
⚡ JavaScript	Interatividade
Banco de Dados
Tecnologia	Função
<img src="https://img.icons8.com/color/48/000000/mysql.png" width="20"/> MySQL	Banco de dados relacional
🚀 Instalação e Execução
Pré-requisitos
Python 3.8+

MySQL 8.0+

Git

1️⃣ Clonar o Repositório
bash
git clone https://github.com/seu-usuario/farmacia-hbr.git
cd farmacia-hbr
2️⃣ Configurar Ambiente Virtual
bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
3️⃣ Instalar Dependências
bash
pip install -r requirements.txt
4️⃣ Configurar Banco de Dados
bash
# Conectar ao MySQL e executar:
mysql -u root -p < database/schema.sql
5️⃣ Configurar Variáveis de Ambiente
bash
cp .env.example .env
# Editar .env com suas configurações
6️⃣ Executar Aplicação
bash
python app.py
Acesse: http://localhost:5000

📁 Estrutura do Projeto
text
farmacia-hbr/
├── app.py                 # Aplicação principal Flask
├── config.py             # Configurações
├── requirements.txt      # Dependências Python
├── database/
│   ├── schema.sql       # Esquema do banco
│   └── seeds.sql        # Dados iniciais
├── templates/           # Templates Jinja2
│   ├── base.html       # Layout base
│   ├── index.html      # Página inicial
│   └── ...
├── static/
│   ├── css/           # Estilos customizados
│   ├── js/            # Scripts JavaScript
│   └── images/        # Imagens e ícones
└── README.md
🗄️ Modelo de Dados
sql
usuarios (id, nome, email, cpf, senha_hash, endereco, genero, data_cadastro)
produtos (id, nome, descricao, preco, categoria, estoque, imagem)
pedidos (id, usuario_id, total, status, data_pedido)
itens_pedido (id, pedido_id, produto_id, quantidade, preco_unitario)
👤 Usuários de Demonstração
Tipo	Email	Senha
Administrador	admin@farmacia.com	admin123
Cliente	cliente@exemplo.com	cliente123
🎨 Screenshots
Página Inicial	Carrinho	Checkout
https://via.placeholder.com/300x200/4F46E5/FFFFFF?text=Home	https://via.placeholder.com/300x200/10B981/FFFFFF?text=Carrinho	https://via.placeholder.com/300x200/F59E0B/FFFFFF?text=Checkout
🤝 Contribuição
Contribuições são bem-vindas! Siga esses passos:

Fork o projeto

Crie uma branch (git checkout -b feature/nova-funcionalidade)

Commit suas mudanças (git commit -m 'Adiciona nova funcionalidade')

Push para a branch (git push origin feature/nova-funcionalidade)

Abra um Pull Request

📝 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

👨‍💻 Desenvolvedor
Seu Nome
https://img.shields.io/badge/GitHub-100000?logo=github
https://img.shields.io/badge/LinkedIn-0077B5?logo=linkedin

🙏 Agradecimentos
Equipe de desenvolvimento

Professores e orientadores

Comunidade Flask

Tailwind CSS

<div align="center">
⭐️ Não esqueça de dar uma estrela no repositório se você gostou!
</div>
📞 Dúvidas? Abra uma issue no GitHub.

🐛 Encontrou um bug? Reporte aqui.

💡 Tem uma ideia? Adoraríamos ouvir suas sugestões!

<div align="center">
Desenvolvido com ❤️ para a disciplina de Desenvolvimento Web

</div>
