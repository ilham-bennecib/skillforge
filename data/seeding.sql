BEGIN;

TRUNCATE "role", "customer", "cfaemployee_contact", "cfaemployee_candidate","cfaemployee_news", "course_training", "candidate_training",
"student", "certificate", "event", "task", "news", "cfaemployee", "candidate", "contact", "course", "session", "training", "structure", "field", 
"company" RESTART IDENTITY;


-- Insertion des profils
INSERT INTO "role" ("name", "permissions") VALUES
('employé cfa', '{"create": true, "read": true, "update": true, "delete": true}'),
('interlocuteur', '{"create": true, "read": true, "update": true, "delete": true}'),
('étudiant', '{"create": true, "read": true, "update": true, "delete": true}'),
('trainer','{"read": true}'),
('candidat', '{"read": true}');

-- Insertion des utilisateurs
INSERT INTO "customer" ("lastName", "firstName", "email", "phone", "directory", "roleId") VALUES
('Doe', 'John', 'john.doe@example.com', 1234567890, 'dir1', 1),
('Smith', 'Jane', 'jane.smith@example.com', 9876543210, 'dir2', 2),
('Brown', 'Alice', 'alice.brown@example.com', 1122334455, 'dir3', 3),
('Taylor', 'James', 'james.taylor@example.com', 2233445566, 'dir4', 1),
('Clark', 'Emily', 'emily.clark@example.com', 3344556677, 'dir5', 2),
('Johnson', 'David', 'david.johnson@example.com', 4455667788, 'dir6', 3),
('Evans', 'Olivia', 'olivia.evans@example.com', 5566778899, 'dir7', 1);

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
INSERT INTO "cfaemployee" ("position", "matricule", "password", "structureId", "userId") VALUES
('Formateur', 123456, 'cfaemppass', 1, 1),
('Responsable Administratif', 987654, 'adminpass', 2, 2),
('Directeur', 654321, 'dirpass', 3, 3),
('Secrétaire', 321654, 'secpass', 4, 4),
('Conseiller', 987321, 'conspass', 5, 5),
('Gestionnaire', 654987, 'gestpass', 6, 6),
('Comptable', 123987, 'comptpass', 7, 7);

-- Insertion des sessions
INSERT INTO "session" ("name", "referent", "tutor", "trainingId") VALUES
('Session Informatique', 1, 1, 1),
('Session Électronique', 2, 2, 2),
('Session Mécanique', 3, 3, 3),
('Session Biologie', 4, 4, 4),
('Session Chimie', 5, 5, 5),
('Session Physique', 6, 6, 6),
('Session Mathématiques', 7, 7, 7);

-- Insertion des cours
INSERT INTO "course" ("name", "trainer") VALUES
('Cours de Programmation', 1),
('Cours de Circuits Électroniques', 2),
('Cours de Mécanique des Fluides', 3),
('Cours de Biologie Cellulaire', 4),
('Cours de Chimie Organique', 5),
('Cours de Physique Quantique', 6),
('Cours de Mathématiques Avancées', 7);

-- Insertion des contacts
INSERT INTO "contact" ("position", "companyId", "userId", "password" ) VALUES
('Responsable RH', 1, 2, 'password123' ),
('Directeur', 2, 1, 'adminpass' ),
('Chef de Projet', 3, 3, 'projpass'),
('Responsable des Achats', 4, 4, 'achatspass'),
('Ingénieur Qualité', 5, 5, 'qualpass'),
('Technicien', 6, 6, 'techpass'),
('Directeur Financier', 7, 7, 'finpass');

-- Insertion des candidats
INSERT INTO "candidate" ("lastDiploma", "dateOfBirth", "address", "userId") VALUES
('Baccalauréat', '2000-01-01', '789 Avenue des Étudiants', 3),
('Licence en Informatique', '1995-05-05', '456 Rue de la vie', 2),
('Master en Mécanique', '1993-03-10', '123 Rue des Machines', 4),
('Doctorat en Biologie', '1988-10-20', '654 Rue des Sciences', 5),
('BTS en Chimie', '1992-09-30', '987 Rue des Expériences', 6),
('Licence en Physique', '1990-07-15', '321 Rue des Particules', 7),
('Master en Mathématiques', '1994-05-25', '159 Rue des Mathématiciens', 1);

-- Insertion des actualités
INSERT INTO "news" ("title", "description", "date") VALUES
('Nouvelle Formation Disponible', 'Une nouvelle formation en informatique est maintenant disponible.', '2024-06-01'),
('Changement de Coordonnées', 'Veuillez noter que notre adresse a changé.', '2024-06-05'),
('Nouvelle Session Mécanique', 'Découvrez notre nouvelle session en mécanique.', '2024-07-01'),
('Programme Biologie Mis à Jour', 'Le programme de formation en biologie a été mis à jour.', '2024-07-10'),
('Nouveau Formateur', 'Un nouveau formateur rejoint notre équipe.', '2024-08-15'),
('Mise à jour du Programme Chimie', 'Les modules de chimie ont été mis à jour pour la session à venir.', '2024-09-05'),
('Conférence en Physique', 'Participez à notre conférence sur la physique des particules.', '2024-09-20');

-- Insertion des tâches
INSERT INTO "task" ("title", "description", "date", "cfaemployeeId") VALUES
('Préparer les supports de cours', 'Créer des présentations pour le cours de programmation.', '2024-06-15', 1),
('Répondre aux appels', 'Gérer les appels entrants des candidats intéressés par la formation.', '2024-06-20', 2),
('Mettre à jour les supports', 'Mettre à jour les supports de cours en électronique.', '2024-07-05', 3),
('Gérer les inscriptions', 'Superviser les inscriptions pour la session de biologie.', '2024-07-15', 4),
('Planifier les examens', 'Organiser les dates des examens pour la session de chimie.', '2024-08-01', 5),
('Organiser la conférence', 'Coordonner la conférence de physique.', '2024-09-10', 6),
('Finaliser le programme de maths', 'Finaliser le programme pour la session de mathématiques.', '2024-10-01', 7);

-- Insertion des événements
INSERT INTO "event" ("title", "description", "date", "startTime", "endTime", "cfaemployeeId") VALUES
('Journée Portes Ouvertes', 'Venez découvrir nos locaux et nos formations.', '2024-07-15', '10:00:00', '17:00:00', 2),
('Séance Orientation', 'Informations sur nos programmes de formation.', '2024-08-01', '14:00:00', '16:00:00', 1),
('Forum des Métiers', 'Rencontrez nos anciens élèves et découvrez leurs métiers.', '2024-09-01', '09:00:00', '12:00:00', 3),
('Conférence en Biologie', 'Participez à notre conférence sur la biologie moléculaire.', '2024-09-15', '11:00:00', '14:00:00', 4),
('Atelier Chimie', 'Atelier pratique sur la chimie organique.', '2024-10-10', '13:00:00', '15:00:00', 5),
('Conférence en Physique', 'Participez à notre conférence sur la physique quantique.', '2024-11-05', '10:00:00', '12:00:00', 6),
('Séminaire Mathématiques', 'Séminaire sur les mathématiques avancées.', '2024-11-20', '14:00:00', '16:00:00', 7);

-- Insertion des étudiants
INSERT INTO "student" ("password", "companyId", "sessionId", "candidateId") VALUES
('studentpass', 1, 1, 1),
('studpass2', 2, 2, 2),
('studpass3', 3, 3, 3),
('studpass4', 4, 4, 4),
('studpass5', 5, 5, 5),
('studpass6', 6, 6, 6),
('studpass7', 7, 7, 7);

-- Insertion des certificats
INSERT INTO "certificate" ("title", "description", "date", "status", "type", "level", "studentId") VALUES
('Certificat de Fin de Formation', 'Obtenu à la fin de la formation en informatique.', '2024-12-31', 'Validé', 'Formation Continue', 'Avancé', 1),
('Certificat de Participation', 'Participant à la session sur les circuits électroniques.', '2024-10-15', 'En cours de validation', 'Formation Professionnelle', 'Débutant', 2),
('Certificat de Fin de Formation', 'Obtenu à la fin de la formation en mécanique.', '2025-02-01', 'Validé', 'Formation Continue', 'Avancé', 3),
('Certificat de Participation', 'Participant à la session de biologie.', '2025-03-10', 'En cours de validation', 'Formation Continue', 'Intermédiaire', 4),
('Certificat de Fin de Formation', 'Obtenu à la fin de la formation en chimie.', '2025-04-30', 'Validé', 'Formation Continue', 'Intermédiaire', 5),
('Certificat de Fin de Formation', 'Obtenu à la fin de la formation en physique.', '2025-06-30', 'Validé', 'Formation Continue', 'Avancé', 6),
('Certificat de Participation', 'Participant à la session de mathématiques.', '2025-07-31', 'En cours de validation', 'Formation Continue', 'Débutant', 7);

-- Insertion des relations N:N

-- cfaemployee_contact
INSERT INTO "cfaemployee_contact" ("cfaemployeeId", "contactId", "exchange") VALUES
(1, 2, 'contacté auj'),
(2, 1, 'contacté auj'),
(3, 3, 'contacté auj'),
(4, 4, 'contacté auj'),
(5, 5, 'contacté auj'),
(6, 6, 'contacté auj'),
(7, 7, 'contacté auj');

-- cfaemployee_candidate
INSERT INTO "cfaemployee_candidate" ("cfaemployeeId", "candidateId") VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7);

-- Cours - Formation
INSERT INTO "course_training" ("courseId", "trainingId") VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7);

-- Candidat - Formation
INSERT INTO "candidate_training" ("candidateId", "trainingId") VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7);

-- cfaemployee_news
INSERT INTO "cfaemployee_news" ("cfaemployeeId", "newsId") VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7);

COMMIT;

