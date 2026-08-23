DROP TABLE IF EXISTS support_tickets;

CREATE TABLE support_tickets (
    ticket_id       INTEGER PRIMARY KEY,
    customer_id     VARCHAR NOT NULL,
    category        VARCHAR NOT NULL,
    priority        VARCHAR NOT NULL,
    assigned_agent  VARCHAR,
    opened_at       TIMESTAMP NOT NULL,
    resolved_at     TIMESTAMP,
    status          VARCHAR NOT NULL
);