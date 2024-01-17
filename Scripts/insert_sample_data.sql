-- sample insert Queries
-- Sample Applicants
INSERT INTO applicants (name, email, phone) VALUES
    ('John Doe', 'john.doe@email.com', '123-456-7890'),
    ('Jane Smith', 'jane.smith@email.com', '987-654-3210');

-- Sample Jobs
INSERT INTO jobs (title, company, location, posting_date) VALUES
    ('Software Engineer', 'Tech Co.', 'City A', '2024-01-01'),
    ('Marketing Specialist', 'Marketing Inc.', 'City B', '2024-02-01');

-- Sample Applications
INSERT INTO applications (applicant_id, job_id, application_date, status) VALUES
    (1, 1, '2024-01-10', 'Pending'),
    (2, 2, '2024-02-15', 'Rejected'),
    (1, 2, '2024-02-20', 'Accepted');
