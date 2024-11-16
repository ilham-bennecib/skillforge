BEGIN;

TRUNCATE "role", "customer", "cfaemployee_contact", "course_training", "candidate_training",
"student", "certificate", "event", "task", "news", "cfaemployee", "candidate", "contact", "course", "session", "training", "structure", "field", 
"company" RESTART IDENTITY;

-- Insertion des profils
INSERT INTO "role" ("name", "permissions") VALUES
('employé cfa', '{"create": true, "read": true, "update": true, "delete": true}'),
('interlocuteur', '{"create": true, "read": true, "update": true, "delete": true}'),
('étudiant', '{"create": true, "read": true, "update": true, "delete": true}'),
('trainer', '{"read": true}'),
('candidat', '{"read": true}');

-- Insertion des utilisateurs avec mot de passe
INSERT INTO "customer" ("lastName", "firstName", "email", "phone", "directory", "roleId", "password") VALUES
('Doe', 'John', 'john.doe@example.com', 1234567890, 'dir1', 1, '$2b$12$saltedpasswordhash1'),
('Smith', 'Jane', 'jane.smith@example.com', 9876543210, 'dir2', 2, '$2b$12$saltedpasswordhash2'),
('Brown', 'Alice', 'alice.brown@example.com', 1122334455, 'dir3', 3, '$2b$12$saltedpasswordhash3'),
('Taylor', 'James', 'james.taylor@example.com', 2233445566, 'dir4', 1, '$2b$12$saltedpasswordhash4'),
('Clark', 'Emily', 'emily.clark@example.com', 3344556677, 'dir5', 2, '$2b$12$saltedpasswordhash5'),
('Johnson', 'David', 'david.johnson@example.com', 4455667788, 'dir6', 3, '$2b$12$saltedpasswordhash6'),
('Evans', 'Olivia', 'olivia.evans@example.com', 5566778899, 'dir7', 1, '$2b$12$saltedpasswordhash7');

-- Insertion des secteurs d'activité (field)
INSERT INTO "field" ("name") VALUES
('Informatique'),
('Électronique'),
('Mécanique'),
('Biologie'),
('Chimie'),
('Physique'),
('Mathématiques');

-- Insertion des structures
INSERT INTO "structure" ("name", "address", "siret", "description", "directory", "fieldId") VALUES
('CFA Informatique', '123 Rue Informatique', '12345678901234', 'Centre de formation en informatique', 'dirCFA1', 1),
('CFA Électronique', '456 Rue de Électronique', '98765432109876', 'Centre de formation en électronique', 'dirCFA2', 2),
('CFA Mécanique', '789 Rue de la Mécanique', '11223344556677', 'Centre de formation en mécanique', 'dirCFA3', 3),
('CFA Biologie', '101 Rue de la Biologie', '22114455667788', 'Centre de formation en biologie', 'dirCFA4', 4),
('CFA Chimie', '202 Rue de la Chimie', '33225566778899', 'Centre de formation en chimie', 'dirCFA5', 5),
('CFA Physique', '303 Rue de la Physique', '44336677889911', 'Centre de formation en physique', 'dirCFA6', 6),
('CFA Mathématiques', '404 Rue des Mathématiques', '55447788991122', 'Centre de formation en mathématiques', 'dirCFA7', 7);

-- Insertion des entreprises
INSERT INTO "company" ("status", "structureId") VALUES
('Prospect', 1),
('Partenaire', 2),
('Prospect', 3),
('Partenaire', 4),
('Prospect', 5),
('Partenaire', 6),
('Prospect', 7);

-- Insertion des formations (training)
INSERT INTO "training" ("name", "price", "startDate", "endDate", "type", "directory", "fieldId", "structureId") VALUES
('Formation Informatique avancée', 5000.00, '2024-07-01', '2024-12-31', 'Formation continue', 'dirTraining1', 1, 1),
('Formation Électronique de base', 3000.00, '2024-08-01', '2024-11-30', 'Formation professionnelle', 'dirTraining2', 2, 2),
('Formation Mécanique', 4500.00, '2024-09-01', '2025-01-31', 'Formation continue', 'dirTraining3', 3, 3),
('Formation Biologie', 4000.00, '2024-10-01', '2025-03-31', 'Formation continue', 'dirTraining4', 4, 4),
('Formation Chimie avancée', 5500.00, '2024-11-01', '2025-04-30', 'Formation continue', 'dirTraining5', 5, 5),
('Formation Physique des Particules', 6000.00, '2025-01-01', '2025-06-30', 'Formation continue', 'dirTraining6', 6, 6),
('Formation Mathématiques', 3200.00, '2025-02-01', '2025-07-31', 'Formation continue', 'dirTraining7', 7, 7);

-- Insertion des employés CFA
INSERT INTO "cfaemployee" ("position", "matricule", "structureId", "userId") VALUES
('Formateur', 123456, 1, 1),
('Responsable Administratif', 987654, 2, 2),
('Directeur', 654321, 3, 3),
('Secrétaire', 321654, 4, 4),
('Conseiller', 987321, 5, 5),
('Gestionnaire', 654987, 6, 6),
('Comptable', 123987, 7, 7);

-- Insertion des relations restantes...

COMMIT;
