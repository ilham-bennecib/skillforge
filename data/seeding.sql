BEGIN;

-- Réinitialiser les tables
TRUNCATE "role", "customer", "field", "structure", "company", "training", 
"course", "contact", "candidate", "cfaemployee", "session", 
"news", "task", "event", "student", "certificate", 
"cfaemployee_contact", "course_training", "candidate_training" 
RESTART IDENTITY;

-- Insertion des rôles
INSERT INTO "role" ("name", "permissions") VALUES
('employé cfa', '{"create": true, "read": true, "update": true, "delete": true}'),
('interlocuteur', '{"create": true, "read": true, "update": true, "delete": true}'),
('étudiant', '{"read": true}'),
('candidat', '{"read": true}'),
('trainer', '{"read": true, "update": true}');

-- Insertion des utilisateurs
INSERT INTO "customer" ("lastName", "firstName", "email", "password", "phone", "directory", "roleId") VALUES
('Doe', 'John', 'john.doe@example.com', '$2b$12$saltedpasswordhash1', 1234567890, 'dir1', 1),
('Smith', 'Jane', 'jane.smith@example.com', '$2b$12$saltedpasswordhash2', 9876543210, 'dir2', 2),
('Brown', 'Alice', 'alice.brown@example.com', '$2b$12$saltedpasswordhash3', 1122334455, 'dir3', 3),
('Taylor', 'James', 'james.taylor@example.com', NULL, 2233445566, 'dir4', 4),
('Clark', 'Emily', 'emily.clark@example.com', '$2b$12$saltedpasswordhash4', 3344556677, 'dir5', 5);

-- Insertion des secteurs d'activité
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
('CFA Informatique', '123 Rue Informatique', '12345678901234', 'Formation en informatique', 'dirCFA1', 1),
('CFA Mécanique', '456 Rue Mécanique', '98765432109876', 'Formation en mécanique', 'dirCFA2', 3);

-- Insertion des entreprises
INSERT INTO "company" ("status", "structureId") VALUES
('Prospect', 1),
('Partenaire', 2);

-- Insertion des formations
INSERT INTO "training" ("name", "price", "startDate", "endDate", "type", "directory", "fieldId", "structureId") VALUES
('Formation Programmation', 5000, '2024-01-01', '2024-06-30', 'Formation continue', 'dirTraining1', 1, 1),
('Formation Mécanique Avancée', 4500, '2024-03-01', '2024-08-31', 'Formation professionnelle', 'dirTraining2', 3, 2);

-- Insertion des cours
INSERT INTO "course" ("name", "trainer") VALUES
('Cours Python', 1),
('Cours Mécanique des Fluides', 2);

-- Insertion des contacts
INSERT INTO "contact" ("position", "companyId", "userId") VALUES
('Responsable RH', 1, 2),
('Directeur Technique', 2, 3);

-- Insertion des candidats
INSERT INTO "candidate" ("lastDiploma", "dateOfBirth", "address", "userId") VALUES
('BTS Informatique', '2000-05-15', '123 Rue des Étudiants', 3),
('Licence Mécanique', '1998-08-20', '456 Avenue des Sciences', 4);

-- Insertion des employés CFA
INSERT INTO "cfaemployee" ("position", "matricule", "structureId", "userId") VALUES
('Formateur', 123456, 1, 1),
('Responsable Administratif', 654321, 2, 2);

-- Insertion des sessions
INSERT INTO "session" ("name", "referent", "tutor", "trainingId") VALUES
('Session Python', 1, 1, 1),
('Session Mécanique', 2, 2, 2);

-- Insertion des actualités
INSERT INTO "news" ("title", "description", "date") VALUES
('Nouvelle Formation en Programmation', 'Inscrivez-vous maintenant', '2023-12-15'),
('Session Mécanique Ouverte', 'Rejoignez-nous pour la prochaine session', '2024-01-10');

-- Insertion des tâches
INSERT INTO "task" ("title", "description", "date", "cfaemployeeId") VALUES
('Préparer supports cours', 'Créer supports Python', '2023-12-01', 1);

-- Insertion des événements
INSERT INTO "event" ("title", "description", "date", "startTime", "endTime", "cfaemployeeId") VALUES
('Journée Portes Ouvertes', 'Venez visiter', '2024-01-20', '10:00', '16:00', 1);

-- Insertion des étudiants
INSERT INTO "student" ("companyId", "sessionId", "candidateId") VALUES
(1, 1, 1),
(2, 2, 2);

-- Insertion des certificats
INSERT INTO "certificate" ("title", "description", "date", "status", "type", "level", "studentId") VALUES
('Certificat Programmation', 'Complété avec succès', '2024-07-01', 'Validé', 'Formation Continue', 'Avancé', 1);

-- Insertion des relations N:N

-- cfaemployee_contact
INSERT INTO "cfaemployee_contact" ("cfaemployeeId", "contactId", "exchange") VALUES
(1, 1, 'Contact RH pour discussion programme'),
(2, 2, 'Discussion avec Directeur Technique');

-- course_training
INSERT INTO "course_training" ("courseId", "trainingId") VALUES
(1, 1),
(2, 2);

-- candidate_training
INSERT INTO "candidate_training" ("candidateId", "trainingId") VALUES
(1, 1),
(2, 2);

COMMIT;
