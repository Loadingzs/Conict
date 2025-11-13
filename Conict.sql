CREATE DATABASE IF NOT EXISTS sistema_farmacia;
USE sistema_farmacia;

-- Tabela para Clientes (sem dados de endereço)
CREATE TABLE clientes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    telefone VARCHAR(20),
    data_nascimento DATE
);

-- Tabela separada para Endereços
CREATE TABLE enderecos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cliente_id INT NOT NULL,
    cep VARCHAR(9) NOT NULL,
    logradouro VARCHAR(255) NOT NULL,
    numero VARCHAR(10) NOT NULL,
    complemento VARCHAR(100),
    bairro VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    estado CHAR(2) NOT NULL
);


CREATE TABLE produtos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    marca VARCHAR(100),
    descricao TEXT,
    preco_venda DECIMAL(10,2) NOT NULL
);

CREATE TABLE estoque (
    id INT PRIMARY KEY AUTO_INCREMENT,
    produto_id INT NOT NULL,
    quantidade INT NOT NULL DEFAULT 0,
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);

CREATE TABLE pedidos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cliente_id INT,
    endereco_entrega_id INT, -- Agora referencia o endereço específico
    data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pendente', 'pago', 'enviado', 'entregue', 'cancelado') DEFAULT 'pendente',
    total DECIMAL(10,2),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (endereco_entrega_id) REFERENCES enderecos(id)
);

CREATE TABLE pedido_itens (
    id INT PRIMARY KEY AUTO_INCREMENT,
    pedido_id INT,
    produto_id INT,
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE,
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);

INSERT INTO produtos (nome, marca, descricao, preco_venda) VALUES 
('Paracetamol', 'Tylenol', 'Analgésico e antitérmico', 12.50),
('Dipirona', 'Novalgina', 'Analgésico e antitérmico', 8.90),
('Shampoo', 'Johnson', 'Shampoo infantil', 15.90),
('Ibuprofeno', 'Advil', 'Anti-inflamatório para dores musculares', 18.75),
('Omeprazol', 'Losec', 'Protetor gástrico para azia e má digestão', 24.90),
('Vitamina C', 'Redoxon', 'Suplemento vitamínico para imunidade', 32.50),
('Soro Fisiológico', 'Emcur', 'Solução para limpeza nasal e ocular', 6.80),
('Curativo Adesivo', 'Band-Aid', 'Curativos para pequenos ferimentos', 9.45);

INSERT INTO estoque (produto_id, quantidade) VALUES 
(1, 100), (2, 150), (3, 80), (4, 60), (5, 120), (6, 90), (7, 200), (8, 180);


-- Adicionar colunas necessárias
ALTER TABLE produtos ADD COLUMN imagem VARCHAR(255) DEFAULT 'default.jpg';
ALTER TABLE clientes ADD COLUMN tipo ENUM('cliente', 'admin') DEFAULT 'cliente';

-- Tornar um usuário admin (substitua pelo ID do seu usuário)
UPDATE clientes SET tipo = 'admin' WHERE id = 1;