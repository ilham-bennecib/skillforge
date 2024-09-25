BEGIN;

TRUNCATE "role", "customer", "cfaEmployee_contact", "cfaEmployee_candidate", "course_training", "candidate_training", "cfaEmployee_news", 
"student", "certificate", "event", "task", "news", "cfaEmployee", "candidate", "contact", "course", "session", "training", "structure", "field", 
"company" RESTART IDENTITY;


-- Insertion des profils
INSERT INTO "role" ("name", "permissions") VALUES
('employé cfa', '{"create": true, "read": true, "update": true, "delete": true}'),
('interlocuteur', '{"create": true, "read": true, "update": true, "delete": true}'),
('étudiant', '{"read": true}');

-- Insertion des utilisateurs
INSERT INTO "customer" ("lastName", "firstName", "email", "phone", "directory", "roleId") VALUES
('Doe', 'John', 'john.doe@example.com', 1234567890, 'dir1', 1),
('Smith', 'Jane', 'jane.smith@example.com', 9876543210, 'dir2', 2),
('Brown', 'Alice', 'alice.brown@example.com', 1122334455, 'dir3', 3);

-- Insertion des secteurs d'activité (field)
INSERT INTO "field" ("name") VALUES
('Informatique'),
('Électronique');

-- Insertion des structures
INSERT INTO "structure" ("name", "address", "siret", "description", "directory", "fieldId") VALUES
('CFA Informatique', '123 Rue Informatique', '12345678901234', 'Centre de formation en informatique', 'dirCFA1', 1),
('CFA Électronique', '456 Rue de Électronique', '98765432109876', 'Centre de formation en électronique', 'dirCFA2', 2);

-- Insertion des entreprises
INSERT INTO "company" ("status", "structureId") VALUES
('Active', 1),
('Inactive', 2);

-- Insertion des formations (training)
INSERT INTO "training" ("name", "price", "startDate", "endDate", "type", "directory", "fieldId", "structureId") VALUES
('Formation Informatique avancée', 5000.00, '2024-07-01', '2024-12-31', 'Formation continue', 'dirTraining1', 1, 1),
('Formation Électronique de base', 3000.00, '2024-08-01', '2024-11-30', 'Formation professionnelle', 'dirTraining2', 2, 2);

-- Insertion des employés CFA
INSERT INTO "cfaEmployee" ("position", "matricule", "password", "cfa", "roleId", "userId") VALUES
('Formateur', 123456, 'cfaemppass', 1, 1, 1),
('Responsable Administratif', 987654, 'adminpass', 2, 1, 2);

-- Insertion des sessions
INSERT INTO "session" ("name", "referent", "tutor", "trainingId") VALUES
('Session Informatique', 1, 1, 1),
('Session Électronique', 2, 2, 2);

-- Insertion des cours
INSERT INTO "course" ("name", "trainer") VALUES
('Cours de Programmation', 1),
('Cours de Circuits Électroniques', 2);

-- Insertion des contacts
INSERT INTO "contact" ("position", "companyId", "userId", "password", "roleId") VALUES
('Responsable RH', 1, 2, 'password123', 2),
('Directeur', 2, 1, 'adminpass', 1);

-- Insertion des candidats
INSERT INTO "candidate" ("lastDiploma", "dateOfBirth", "address", "userId") VALUES
('Baccalauréat', '2000-01-01', '789 Avenue des Étudiants', 3),
('Licence en Informatique', '1995-05-05', '456 Rue de la vie', 2);



-- Insertion des actualités
INSERT INTO "news" ("title", "description", "date") VALUES
('Nouvelle Formation Disponible', 'Une nouvelle formation en informatique est maintenant disponible.', '2024-06-01'),
('Changement de Coordonnées', 'Veuillez noter que notre adresse a changé.', '2024-06-05');

-- Insertion des tâches
INSERT INTO "task" ("title", "description", "date", "cfaEmployeeId") VALUES
('Préparer les supports de cours', 'Créer des présentations pour le cours de programmation.', '2024-06-15', 1),
('Répondre aux appels', 'Gérer les appels entrants des candidats intéressés par la formation.', '2024-06-20', 2);

-- Insertion des événements
INSERT INTO "event" ("title", "description", "date", "startTime", "endTime", "cfaEmployeeId") VALUES
('Journée Portes Ouvertes', 'Venez découvrir nos locaux et nos formations.', '2024-07-15', '10:00:00', '17:00:00', 2),
('Séance Orientation', 'Informations sur nos programmes de formation.', '2024-08-01', '14:00:00', '16:00:00', 1);

-- Insertion des étudiants
INSERT INTO "student" ("password", "companyId", "roleId", "sessionId", "candidateId") VALUES
('studentpass', 1, 3, 1, 1),
('studpass2', 2, 3, 2, 2);

-- Insertion des certificats
INSERT INTO "certificate" ("title", "description", "date", "status", "type", "level", "studentId") VALUES
('Certificat de Fin de Formation', 'Obtenu à la fin de la formation en informatique.', '2024-12-31', 'Validé', 'Formation Continue', 'Avancé', 1),
('Certificat de Participation', 'Participant à la session sur les circuits électroniques.', '2024-10-15', 'En cours de validation', 'Formation Professionnelle', 'Débutant', 2);

-- Insertion des relations N:N

-- Employé CFA - Contact
INSERT INTO "cfaEmployee_contact" ("cfaEmployeeId", "contactId") VALUES
(1, 2),
(2, 1);

-- Employé CFA - Candidat
INSERT INTO "cfaEmployee_candidate" ("cfaEmployeeId", "candidateId") VALUES
(1, 1),
(2, 2);

-- Cours - Formation
INSERT INTO "course_training" ("courseId", "trainingId") VALUES
(1, 1),
(2, 2);

-- Candidat - Formation
INSERT INTO "candidate_training" ("candidateId", "trainingId") VALUES
(1, 1),
(2, 2);

-- Employé CFA - Actualité
INSERT INTO "cfaEmployee_news" ("cfaEmployeeId", "newsId") VALUES
(1, 1),
(2, 2);

COMMIT;
