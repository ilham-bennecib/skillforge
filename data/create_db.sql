BEGIN;

DROP TABLE IF EXISTS "role", "cfaEmployee_contact", "cfaEmployee_candidate","cfaemployee_contact", "cfaemployee_candidate", "course_training","cfaEmployee_news",  "candidate_training", "cfaemployee_news", 
"student", "certificate", "event", "task", "news", "cfaEmployee", "cfaemployee", "candidate", "contact", "course", "session", "training", "structure", "field", 
"company", "user", "appUser", "customer";

DROP SEQUENCE IF EXISTS "cfaEmployee_contact_id_seq", "cfaemployee_contact_id_seq", "cfaEmployee_candidate_id_seq", "structure_id_seq", "cfaemployee_candidate_id_seq", "course_training_id_seq", "candidate_training_id_seq", "cfaemployee_news_id_seq", 
"student_id_seq", "certificate_id_seq", "event_id_seq", "task_id_seq", "news_id_seq", "cfaEmployee_id_seq", "cfaemployee_id_seq", "candidate_id_seq", "contact_id_seq", "course_id_seq", "session_id_seq", "training_id_seq", "field_id_seq", 
"company_id_seq", "user_id_seq", "appUser_id_seq", "customer_id_seq";

-- Création de la table 'roles' avec une colonne JSON pour les permissions
CREATE TABLE IF NOT EXISTS "role" (
    "id" INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL UNIQUE,
    "permissions" JSONB NOT NULL DEFAULT '[]',
    "createdAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMPTZ 
);

-- Création de la table customer
CREATE TABLE IF NOT EXISTS "customer" (
    "id" INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "lastName" VARCHAR(250) NOT NULL,
    "firstName" VARCHAR(250) NOT NULL,
    "email" VARCHAR(250) NOT NULL UNIQUE,
    "phone" BIGINT NOT NULL UNIQUE,
    "directory" VARCHAR(250) NOT NULL UNIQUE,
    "roleId" INT NOT NULL REFERENCES "role"("id") ON DELETE CASCADE,
    "createdAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMPTZ 
);

-- Création de la table field (secteur d'activité)
CREATE TABLE IF NOT EXISTS "field" (
    "id" INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "name" VARCHAR(250) NOT NULL,
    "createdAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMPTZ
);

-- Création de la table structure
CREATE TABLE IF NOT EXISTS "structure" (
    "id" INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "name" VARCHAR(250) NOT NULL,
    "address" TEXT,
    "siret" VARCHAR(20),
    "description" TEXT,
    "directory" VARCHAR(250) NOT NULL,
    "fieldId" INT NOT NULL REFERENCES "field"("id") ON DELETE CASCADE,
    "createdAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMPTZ
);

-- Création de la table company
CREATE TABLE IF NOT EXISTS "company" (
    "id" INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "status" VARCHAR(50),
    "structureId" INT NOT NULL REFERENCES "structure"("id") ON DELETE CASCADE,
    "createdAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMPTZ
);

-- Création de la table training
CREATE TABLE IF NOT EXISTS "training" (
    "id" INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "name" VARCHAR(250) NOT NULL,
    "price" DECIMAL(10, 2) NOT NULL,
    "startDate" DATE NOT NULL,
    "endDate" DATE NOT NULL,
    "type" VARCHAR(50),
    "directory" VARCHAR(250) NOT NULL,
    "fieldId" INT NOT NULL REFERENCES "field"("id") ON DELETE CASCADE,
    "structureId" INT NOT NULL REFERENCES "structure"("id") ON DELETE CASCADE,
    "createdAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMPTZ
);

-- Création de la table course
CREATE TABLE IF NOT EXISTS "course" (
    "id" INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "name" VARCHAR(250) NOT NULL,
    "trainer" INT NOT NULL REFERENCES "customer"("id") ON DELETE CASCADE,
    "createdAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMPTZ
);

-- Création de la table contact (interlocuteur)
CREATE TABLE IF NOT EXISTS "contact" (
    "id" INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "position" VARCHAR(250),
    "companyId" INT NOT NULL REFERENCES "company"("id") ON DELETE CASCADE,
    "userId" INT NOT NULL REFERENCES "customer"("id") ON DELETE CASCADE,
    "password" TEXT NOT NULL,
    "createdAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMPTZ
);

-- Création de la table candidate
CREATE TABLE IF NOT EXISTS "candidate" (
    "id" INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "lastDiploma" VARCHAR(250) NOT NULL,
    "dateOfBirth" DATE NOT NULL,
    "address" TEXT NOT NULL,
    "userId" INT NOT NULL REFERENCES "customer"("id") ON DELETE CASCADE,
    "createdAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMPTZ
);

-- Création de la table cfaemployee
CREATE TABLE IF NOT EXISTS "cfaemployee" (
    "id" INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "position" VARCHAR(250),
    "matricule" INTEGER NOT NULL,
    "password" TEXT NOT NULL,
    "structureId" INT NOT NULL REFERENCES "structure"("id") ON DELETE CASCADE,
    "userId" INT NOT NULL REFERENCES "customer"("id") ON DELETE CASCADE,
    "createdAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMPTZ
);

-- Création de la table session
CREATE TABLE IF NOT EXISTS "session" (
    "id" INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "name" VARCHAR(250) NOT NULL,
    "referent" INT NOT NULL REFERENCES "cfaemployee"("id") ON DELETE CASCADE,
    "tutor" INT NOT NULL REFERENCES "customer"("id") ON DELETE CASCADE,
    "trainingId" INT NOT NULL REFERENCES "training"("id") ON DELETE CASCADE,
    "createdAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMPTZ
);

-- Création de la table news
CREATE TABLE IF NOT EXISTS "news" (
    "id" INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "title" VARCHAR(250) NOT NULL,
    "description" TEXT,
    "date" DATE NOT NULL,
    "createdAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMPTZ
);

-- Création de la table task
CREATE TABLE IF NOT EXISTS "task" (
    "id" INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "title" VARCHAR(200) NOT NULL,
    "description" TEXT,
    "date" DATE,
    "cfaemployeeId" INT NOT NULL REFERENCES "cfaemployee"("id") ON DELETE CASCADE,
    "createdAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMPTZ
);

-- Création de la table event
CREATE TABLE IF NOT EXISTS "event" (
    "id" INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "title" VARCHAR(250) NOT NULL,
    "description" TEXT,
    "date" DATE NOT NULL,
    "startTime" TIME NOT NULL,
    "endTime" TIME NOT NULL,
    "cfaemployeeId" INT NOT NULL REFERENCES "cfaemployee"("id") ON DELETE CASCADE,
    "createdAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMPTZ
);

-- Création de la table student
CREATE TABLE IF NOT EXISTS "student" (
    "id" INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "password" VARCHAR(100) NOT NULL,
    "companyId" INT NOT NULL REFERENCES "company"("id") ON DELETE CASCADE,
    "sessionId" INT NOT NULL REFERENCES "session"("id") ON DELETE CASCADE,
    "candidateId" INT NOT NULL REFERENCES "candidate"("id") ON DELETE CASCADE,
    "createdAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMPTZ
);

-- Création de la table certificate
CREATE TABLE IF NOT EXISTS "certificate" (
    "id" INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "title" VARCHAR(250) NOT NULL,
    "description" TEXT,
    "date" DATE NOT NULL,
    "status" VARCHAR(50) NOT NULL,
    "type" VARCHAR(50),
    "level" VARCHAR(50),
    "studentId" INT NOT NULL REFERENCES "student"("id") ON DELETE CASCADE,
    "createdAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMPTZ
);

-- Création des tables de liaison pour les cardinalités N:N

-- cfaemployee_contact
CREATE TABLE IF NOT EXISTS "cfaemployee_contact" (
    "id" INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "cfaemployeeId" INT NOT NULL REFERENCES "cfaemployee"("id") ON DELETE CASCADE,
    "contactId" INT NOT NULL REFERENCES "contact"("id") ON DELETE CASCADE,
    "exchange" TEXT NOT NULL,
    "createdAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMPTZ
);

-- course_training
CREATE TABLE IF NOT EXISTS "course_training" (
    "id" INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "courseId" INT NOT NULL REFERENCES "course"("id") ON DELETE CASCADE,
    "trainingId" INT NOT NULL REFERENCES "training"("id") ON DELETE CASCADE,
    "createdAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMPTZ
);

-- candidate_training
CREATE TABLE IF NOT EXISTS "candidate_training" (
    "id" INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "candidateId" INT NOT NULL REFERENCES "candidate"("id") ON DELETE CASCADE,
    "trainingId" INT NOT NULL REFERENCES "training"("id") ON DELETE CASCADE,
    "createdAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMPTZ
);



COMMIT;
