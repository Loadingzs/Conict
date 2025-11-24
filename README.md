# 💊 Farmácia HBR — Sistema de Pedidos Online

Um sistema web de e-commerce simplificado para uma **farmácia**, desenvolvido em **Python (Flask)** e **MySQL**.  
Permite o gerenciamento completo de **usuários, produtos e pedidos**, com autenticação segura e interface responsiva.

---

## 🧠 Visão Geral

O **Farmácia HBR** é um projeto acadêmico e prático voltado ao aprendizado de **desenvolvimento web full stack**.  
O sistema cobre desde o **cadastro de clientes** até a **simulação do checkout** e **confirmação de pedidos**.

---

## ✨ Principais Funcionalidades

| Funcionalidade | Descrição |
|----------------|------------|
| 🔐 **Autenticação de Usuário** | Cadastro e login seguro (com hash de senha, CPF, endereço e gênero). |
| 💊 **Catálogo de Medicamentos** | Exibição dinâmica dos produtos vindos do banco de dados MySQL. |
| 🛒 **Carrinho de Compras** | Adicionar, remover e alterar quantidades (salvo em sessão). |
| 💳 **Checkout Simulado** | Cálculo de frete fixo e simulação de pagamento. |
| 📱 **Design Responsivo** | Layout moderno adaptável para dispositivos móveis usando **Tailwind CSS**. |
| 👤 **Painel do Usuário** | Exibe nome, endereço e informações de envio após o pedido. |

---

## 🧰 Tecnologias Utilizadas

**Backend**
- 🐍 Python (Flask)
- 🔐 Flask-Login
- 🧩 SQLAlchemy / PyMySQL

**Frontend**
- 🧱 HTML5 + Jinja2 Templates
- 🎨 Tailwind CSS (CDN)

**Banco de Dados**
- 🗄️ MySQL

---

## ⚙️ Instalação e Execução

### 1️⃣ Clonar o repositório
```bash
git clone https://github.com/seu-usuario/farmacia-hbr.git
cd farmacia-hbr
