-- Basic relational schema for the source you selected in docs/data_contract.yaml
-- Adjust column names/types to match what you found in Task 2.2 profiling.

CREATE TABLE IF NOT EXISTS customers (
    customer_id     VARCHAR PRIMARY KEY,
    -- add remaining columns based on your profiling results
    created_at      TIMESTAMP
);

-- Example of a second table if you want to show a relationship (optional)
-- CREATE TABLE IF NOT EXISTS orders (
--     order_id     VARCHAR PRIMARY KEY,
--     customer_id  VARCHAR REFERENCES customers(customer_id),
--     order_date   TIMESTAMP,
--     amount       NUMERIC
-- );
