BEGIN;
 TRUNCATE  "user", "cfaEmployee_contact", "cfaEmployee_candidate", "course_training", "candidate_training", "cfaEmployee_news", 
"student", "certificate", "event", "task", "news", "cfaEmployee", "candidate", "contact", "course", "session", "training", "structure", "field", 
"company" RESTART IDENTITY;

-- Insertion de 5 utilisateurs dans la table 'user'
INSERT INTO "user" ("lastName", "firstName", "email", "phone", "directory", "role")
VALUES
    ('Doe', 'John', 'john.doe@example.com', 1234567890, '/home/johndoe', 'admin'),
    ('Smith', 'Jane', 'jane.smith@example.com', 1234567891, '/home/janesmith', 'user'),
    ('Brown', 'Charlie', 'charlie.brown@example.com', 1234567892, '/home/charliebrown', 'user'),
    ('Johnson', 'Emily', 'emily.johnson@example.com', 1234567893, '/home/emilyjohnson', 'manager'),
    ('Williams', 'Chris', 'chris.williams@example.com', 1234567894, '/home/chriswilliams', 'user');

-- Insérer des données dans la table "field" (secteur d'activité)
INSERT INTO "field" ("name", "createdAt")
VALUES
    ('Informatique', CURRENT_TIMESTAMP),
    ('Finance', CURRENT_TIMESTAMP),
    ('Santé', CURRENT_TIMESTAMP);

-- Insérer des données dans la table "structure" (entités)
INSERT INTO "structure" ("name", "address", "siret", "description", "directory", "role", "fieldId", "createdAt")
VALUES
    ('Startup Tech', '123 rue de la Technologie', '12345678901234', 'Startup dans le domaine de la technologie.', '/startup_tech', 'Admin', 1, CURRENT_TIMESTAMP),
    ('Banque XYZ', '8 avenue des Finances', '98765432109876', 'Banque internationale.', '/banque_xyz', 'Admin', 2, CURRENT_TIMESTAMP),
    ('Centre Médical ABC', '15 rue des Soins', '56789012345678', 'Centre médical multidisciplinaire.', '/centre_medical_abc', 'Admin', 3, CURRENT_TIMESTAMP);

-- Insérer des données dans la table "company" (entreprises)
INSERT INTO "company" ("status", "password", "structureId", "createdAt")
VALUES
    ('Active', 'password123', 1, CURRENT_TIMESTAMP),
    ('Active', 'password456', 2, CURRENT_TIMESTAMP),
    ('Active', 'password789', 3, CURRENT_TIMESTAMP);

-- Insérer des données dans la table "training" (formations)
INSERT INTO "training" ("name", "price", "startDate", "endDate", "type", "directory", "userId", "fieldId", "structureId", "createdAt")
VALUES
    ('Développement Web', 1500.00, '2024-05-01', '2024-06-01', 'Formation professionnelle', '/web_dev', 1, 1, 1, CURRENT_TIMESTAMP),
    ('Finance et Investissements', 2000.00, '2024-06-01', '2024-07-01', 'Formation certifiante', '/finance', 2, 2, 2, CURRENT_TIMESTAMP),
    ('Soins Infirmiers Avancés', 2500.00, '2024-07-01', '2024-08-01', 'Formation diplômante', '/nursing', 3, 3, 3, CURRENT_TIMESTAMP);

-- Insérer des données dans la table "session" (sessions de formation)
INSERT INTO "session" ("name", "referent", "trainingId", "createdAt")
VALUES
    ('Session Printemps 2024', 1, 1, CURRENT_TIMESTAMP),
    ('Session Été 2024', 2, 2, CURRENT_TIMESTAMP),
    ('Session Automne 2024', 3, 3, CURRENT_TIMESTAMP);

-- Insérer des données dans la table "course" (cours)
INSERT INTO "course" ("name", "trainer", "createdAt")
VALUES
    ('Introduction au HTML et CSS', 1, CURRENT_TIMESTAMP),
    ('Gestion de Portefeuille', 2, CURRENT_TIMESTAMP),
    ('Soins Avancés en Traumatologie', 3, CURRENT_TIMESTAMP);

-- Insérer des données dans la table "contact" (interlocuteurs)
INSERT INTO "contact" ("position", "companyId", "userId", "createdAt")
VALUES
    ('Responsable RH', 1, 1, CURRENT_TIMESTAMP),
    ('Directeur Financier', 2, 2, CURRENT_TIMESTAMP),
    ('Directeur Médical', 3, 3, CURRENT_TIMESTAMP);

-- Insérer des données dans la table "candidate" (candidats)
INSERT INTO "candidate" ("lastDiploma", "dateOfBirth", "address", "userId", "createdAt")
VALUES
    ('Baccalauréat Scientifique', '1995-03-15', '15 avenue des Études', 4, CURRENT_TIMESTAMP),
    ('Licence en Économie', '1990-07-20', '20 rue de la Finance', 5, CURRENT_TIMESTAMP),
    ('Diplôme d''Infirmier', '1993-11-10', '10 rue des Soins', 6, CURRENT_TIMESTAMP);

-- Insérer des données dans la table "cfaEmployee" (employés du CFA)
INSERT INTO "cfaEmployee" ("position", "matricule", "cfa", "userId", "createdAt")
VALUES
    ('Formateur Web', 123456, 1, 7, CURRENT_TIMESTAMP),
    ('Expert Financier', 789012, 2, 8, CURRENT_TIMESTAMP),
    ('Infirmier Chef', 345678, 3, 9, CURRENT_TIMESTAMP);

-- Insérer des données dans la table "news" (actualités)
INSERT INTO "news" ("title", "description", "date", "createdAt")
VALUES
    ('Nouvelle Collaboration avec Startup Tech', 'La société Startup Tech annonce un partenariat avec une grande entreprise de technologie.', '2024-05-01', CURRENT_TIMESTAMP),
    ('Banque XYZ Acquiert une Banque Rival', 'La banque XYZ finalise l''acquisition de son principal concurrent, renforçant ainsi sa position sur le marché.', '2024-06-01', CURRENT_TIMESTAMP),
    ('Centre Médical ABC reçoit une Subvention pour la Recherche', 'Le Centre Médical ABC se voit octroyer une subvention de recherche importante pour l''étude de nouvelles thérapies.', '2024-07-01', CURRENT_TIMESTAMP);

-- Insérer des données dans la table "task" (tâches)
INSERT INTO "task" ("title", "description", "date", "cfaEmployeeId", "createdAt")
VALUES
    ('Préparer le Cours sur les Frameworks CSS', 'Créer des supports de cours et des exercices pratiques pour la prochaine session de formation.', '2024-05-15', 1, CURRENT_TIMESTAMP),
    ('Analyser les Données de Marché', 'Effectuer une analyse approfondie des tendances du marché financier pour orienter les stratégies d''investissement.', '2024-06-10', 2, CURRENT_TIMESTAMP),
    ('Planifier la Formation sur les Urgences', 'Élaborer un programme de formation complet sur les interventions en cas d''urgence médicale.', '2024-07-05', 3, CURRENT_TIMESTAMP);

-- Insérer des données dans la table "event" (événements)
INSERT INTO "event" ("title", "description", "date", "startTime", "endTime", "cfaEmployeeId", "createdAt")
VALUES
    ('Atelier sur les Technologies Web', 'Une journée d''ateliers pratiques sur les dernières technologies de développement web.', '2024-05-20', '09:00', '17:00', 1, CURRENT_TIMESTAMP),
    ('Conférence sur l''Investissement Responsable', 'Un événement d''une demi-journée réunissant des experts pour discuter des meilleures pratiques en matière d''investissement responsable.', '2024-06-15', '14:00', '18:00', 2, CURRENT_TIMESTAMP),
    ('Formation sur les Soins Post-Opératoires', 'Une formation intensive sur les soins post-opératoires et la gestion des complications.', '2024-07-10', '10:00', '16:00', 3, CURRENT_TIMESTAMP);

-- Insérer des données dans la table "student" (étudiants)
INSERT INTO "student" ("password", "companyId", "sessionId", "candidateId", "createdAt")
VALUES
    ('password123', 1, 1, 1, CURRENT_TIMESTAMP),
    ('password456', 2, 2, 2, CURRENT_TIMESTAMP),
    ('password789', 3, 3, 3, CURRENT_TIMESTAMP);

-- Insérer des données dans la table "certificate" (certificats)
INSERT INTO "certificate" ("title", "description", "date", "status", "type", "level", "studentId", "createdAt")
VALUES
    ('Certificat de Développeur Web', 'Certificat délivré suite à la réussite de la formation en développement web.', '2024-06-30', 'Validé', 'Professionnel', 'Avancé', 1, CURRENT_TIMESTAMP),
    ('Certificat en Finance Avancée', 'Certificat décerné après la réussite de l''examen en finance avancée.', '2024-07-31', 'En Attente', 'Certification', 'Expert', 2, CURRENT_TIMESTAMP),
    ('Certificat de Soins Avancés', 'Certificat de compétence en soins avancés délivré par le Centre Médical ABC.', '2024-08-30', 'Validé', 'Diplôme', 'Avancé', 3, CURRENT_TIMESTAMP);

-- Insérer des données dans les tables de liaison pour les cardinalités N:N

-- employee_contact
INSERT INTO "cfaEmployee_contact" ("cfaEmployeeId", "contactId", "createdAt")
VALUES
    (1, 1, CURRENT_TIMESTAMP),
    (2, 2, CURRENT_TIMESTAMP),
    (3, 3, CURRENT_TIMESTAMP);

-- employee_candidate
INSERT INTO "cfaEmployee_candidate" ("cfaEmployeeId", "candidateId", "createdAt")
VALUES
    (1, 1, CURRENT_TIMESTAMP),
    (2, 2, CURRENT_TIMESTAMP),
    (3, 3, CURRENT_TIMESTAMP);

-- course_training
INSERT INTO "course_training" ("courseId", "trainingId", "createdAt")
VALUES
    (1, 1, CURRENT_TIMESTAMP),
    (2, 2, CURRENT_TIMESTAMP),
    (3, 3, CURRENT_TIMESTAMP);

-- candidate_training
INSERT INTO "candidate_training" ("candidateId", "trainingId", "createdAt")
VALUES
    (1, 1, CURRENT_TIMESTAMP),
    (2, 2, CURRENT_TIMESTAMP),
    (3, 3, CURRENT_TIMESTAMP);

-- employee_news
INSERT INTO "cfaEmployee_news" ("cfaEmployeeId", "newsId", "createdAt")
VALUES
    (1, 1, CURRENT_TIMESTAMP),
    (2, 2, CURRENT_TIMESTAMP),
    (3, 3, CURRENT_TIMESTAMP);


COMMIT;