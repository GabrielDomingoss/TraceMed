-- Script para popular o banco TraceMed

-- Usuários
INSERT INTO users (id, name, email, password, role) VALUES (1, 'Admin User', 'admin@tracemed.com', '$2b$12$A3Crs7T10V1jENIoIL1yEepkkdT99yoZqqFLgKk9WDkLkA3Fb5N7W', 'admin');
INSERT INTO users (id, name, email, password, role) VALUES (2, 'Técnico João', 'joao@tracemed.com', '$2b$12$A3Crs7T10V1jENIoIL1yEepkkdT99yoZqqFLgKk9WDkLkA3Fb5N7W', 'tecnico');
INSERT INTO users (id, name, email, password, role) VALUES (3, 'Técnica Maria', 'maria@tracemed.com', '$2b$12$A3Crs7T10V1jENIoIL1yEepkkdT99yoZqqFLgKk9WDkLkA3Fb5N7W', 'tecnico');
INSERT INTO users (id, name, email, password, role) VALUES (4, 'Enfermeira Ana', 'ana@tracemed.com', '$2b$12$A3Crs7T10V1jENIoIL1yEepkkdT99yoZqqFLgKk9WDkLkA3Fb5N7W', 'enfermeiro');
INSERT INTO users (id, name, email, password, role) VALUES (5, 'Enfermeiro Lucas', 'lucas@tracemed.com', '$2b$12$A3Crs7T10V1jENIoIL1yEepkkdT99yoZqqFLgKk9WDkLkA3Fb5N7W', 'enfermeiro');

-- Materiais
INSERT INTO materials (id, nome, tipo, data_validade, serial) VALUES (1, 'Pinça Cirúrgica', 'Instrumento Cirúrgico', '2026-03-25', 'PIN-001');
INSERT INTO materials (id, nome, tipo, data_validade, serial) VALUES (2, 'Bisturi', 'Instrumento de Corte', '2026-03-25', 'BIS-002');
INSERT INTO materials (id, nome, tipo, data_validade, serial) VALUES (3, 'Seringa 20ml', 'Descartável', '2026-03-25', 'SER-003');
INSERT INTO materials (id, nome, tipo, data_validade, serial) VALUES (4, 'Gaze Estéril', 'Material de Curativo', '2026-03-25', 'GAZ-004');
INSERT INTO materials (id, nome, tipo, data_validade, serial) VALUES (5, 'Luvas Cirúrgicas', 'EPIs', '2026-03-25', 'LUV-005');
