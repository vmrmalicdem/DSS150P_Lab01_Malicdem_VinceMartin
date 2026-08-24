CREATE SCHEMA IF NOT EXISTS lab;

CREATE TABLE IF NOT EXISTS lab.customers (
    customer_id      VARCHAR PRIMARY KEY,
    first_name       TEXT NOT NULL,
    last_name        TEXT NOT NULL,
    email            TEXT,
    city             TEXT,
    signup_date      DATE,
    customer_segment TEXT NOT NULL,
    CONSTRAINT ck_customer_segment_valid CHECK (
        customer_segment IN ('Retail', 'Professional', 'SME', 'Student')
    )
);