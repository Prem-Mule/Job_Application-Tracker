-- create_database.sql

-- Applicants table
CREATE TABLE IF NOT EXISTS applicants (
    applicant_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT
);

-- Jobs table
CREATE TABLE IF NOT EXISTS jobs (
    job_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    location TEXT,
    posting_date DATE
);

-- Applications table
CREATE TABLE IF NOT EXISTS applications (
    application_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    applicant_id INTEGER,
    job_id INTEGER,
    application_date DATE,
    status TEXT,
    FOREIGN KEY (applicant_id) REFERENCES applicants(applicant_id),
    FOREIGN KEY (job_id) REFERENCES jobs(job_id)
);
