CREATE DATABASE IF NOT EXISTS barbearia
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE barbearia;

SET NAMES utf8mb4;

CREATE TABLE agendamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente VARCHAR(100) NOT NULL,
    telefone VARCHAR(20),
    servico VARCHAR(100),
    preco DECIMAL(10, 2),
    barbeiro VARCHAR(50),
    data DATE NOT NULL,
    horario VARCHAR(5),
    status VARCHAR(20) NOT NULL DEFAULT 'Agendado',

    CONSTRAINT chk_agendamentos_status
        CHECK (status IN ('Agendado', 'Concluído', 'Cancelado')),

    CONSTRAINT chk_agendamentos_preco
        CHECK (preco IS NULL OR preco >= 0),

    INDEX idx_agendamentos_data_horario (data, horario),
    INDEX idx_agendamentos_status (status)
) ENGINE = InnoDB;

-- Dados fictícios para avaliação do sistema.
INSERT INTO agendamentos
    (cliente, telefone, servico, preco, barbeiro, data, horario, status)
VALUES
    (
        'João Silva',
        '(47) 99911-0001',
        'Corte tradicional',
        35.00,
        'Carlos',
        '2026-05-04',
        '09:00',
        'Concluído'
    ),
    (
        'Pedro Santos',
        '(47) 99911-0002',
        'Corte e barba',
        60.00,
        'Rafael',
        '2026-05-04',
        '10:00',
        'Concluído'
    ),
    (
        'Lucas Oliveira',
        '(47) 99911-0003',
        'Barba',
        30.00,
        'Bruno',
        '2026-05-05',
        '14:00',
        'Cancelado'
    ),
    (
        'Marcos Souza',
        '(47) 99911-0004',
        'Corte degradê',
        40.00,
        'Carlos',
        '2026-05-06',
        '08:30',
        'Concluído'
    ),
    (
        'Gabriel Costa',
        '(47) 99911-0005',
        'Corte e barba',
        60.00,
        'Rafael',
        '2026-05-07',
        '11:00',
        'Agendado'
    ),
    (
        'Felipe Almeida',
        '(47) 99911-0006',
        'Corte tradicional',
        35.00,
        'Bruno',
        '2026-05-07',
        '15:30',
        'Agendado'
    ),
    (
        'André Pereira',
        '(47) 99911-0007',
        'Barba',
        30.00,
        'Carlos',
        '2026-05-08',
        '09:30',
        'Cancelado'
    ),
    (
        'Ricardo Lima',
        '(47) 99911-0008',
        'Corte degradê',
        40.00,
        'Rafael',
        '2026-05-08',
        '16:00',
        'Agendado'
    );

-- Consulta opcional para conferir os registros.
SELECT *
FROM agendamentos
ORDER BY data, horario, id;

