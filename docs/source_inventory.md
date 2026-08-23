# Source Inventory

For each source, fill in every field below in your own words.

## 1. customers.csv
- Source name:
- Source-system type:
- Data format: CSV
- Structured / semi-structured / unstructured:
- Expected update pattern:
- Likely acquisition method:
- Schema location or schema owner:
- Possible primary/business key:
- Potential schema-evolution risk:
- Potential data-quality risk:

## 2. orders.json
- Source name:
- Source-system type:
- Data format: JSON
- Structured / semi-structured / unstructured:
- Expected update pattern:
- Likely acquisition method:
- Schema location or schema owner:
- Possible primary/business key:
- Potential schema-evolution risk:
- Potential data-quality risk:

## 3. products.parquet
- Source name:
- Source-system type:
- Data format: Parquet
- Structured / semi-structured / unstructured:
- Expected update pattern:
- Likely acquisition method:
- Schema location or schema owner:
- Possible primary/business key:
- Potential schema-evolution risk:
- Potential data-quality risk:

## 4. REST API
- Source name:
- Source-system type:
- Data format: JSON
- Structured / semi-structured / unstructured:
- Expected update pattern:
- Likely acquisition method:
- Schema location or schema owner:
- Possible primary/business key:
- Potential schema-evolution risk:
- Potential data-quality risk:
- Retrieved at (UTC): Retrieved at (UTC): 2026-08-23T15:48:11.337134+00:00

## 5. PostgreSQL table (support_tickets)
- Source name: support_tickets
- Source-system type: Relational database (PostgreSQL)
- Data format: Relational table
- Structured / semi-structured / unstructured: Structured
- Expected update pattern: Likely append-heavy (new tickets created continuously), with periodic updates to status/resolved_at as tickets are worked
- Likely acquisition method: Direct SQL query/connection to the database (e.g. via SQLAlchemy or psycopg2)
- Schema location or schema owner: Defined in sql/seed_support_tickets.sql; owned by the support/customer service system
- Possible primary/business key: ticket_id (primary key); customer_id links back to the customers source
- Potential schema-evolution risk: New ticket categories or status values could be added without updating downstream code that expects a fixed set
- Potential data-quality risk: assigned_agent and resolved_at are nullable — unassigned or unresolved tickets need to be handled explicitly rather than assumed complete

Schema:
| Column | Type | Nullable |
|---|---|---|
| ticket_id | integer | NO |
| customer_id | character varying | NO |
| category | character varying | NO |
| priority | character varying | NO |
| assigned_agent | character varying | YES |
| opened_at | timestamp without time zone | NO |
| resolved_at | timestamp without time zone | YES |
| status | character varying | NO |

Row count: 250