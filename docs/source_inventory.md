# Source Inventory

## 1. customers.csv
- Source name: customers.csv
- Source-system type: Web/app signup form, likely backed by a customer database or CRM
- Data format: CSV
- Structured / semi-structured / unstructured: Structured
- Expected update pattern: Signups happen continuously, but this file is a batch snapshot refreshed on a regular schedule
- Likely acquisition method: Direct file read (pandas.read_csv), assumed to be exported into a shared location
- Schema location or schema owner: Owned by the system that manages signups (CRM/app database); no formal schema file included
- Possible primary/business key: customer_id
- Potential schema-evolution risk: A new column could be added (e.g. loyalty_tier), or customer_segment could gain new categories, breaking code that assumes a fixed set of columns/values
- Potential data-quality risk: 2 duplicate rows found during profiling; email values could have invalid formats since there's no validation on a raw CSV export

## 2. orders.json
- Source name: orders.json
- Source-system type: Order management system (e.g. an e-commerce backend)
- Data format: JSON
- Structured / semi-structured / unstructured: Semi-structured (nested shipping object)
- Expected update pattern: Orders happen continuously, but this file is a batch snapshot refreshed on a regular schedule
- Likely acquisition method: Direct file read (pandas.read_json), assumed to be exported from the order system
- Schema location or schema owner: Owned by the order management system; no formal schema file included
- Possible primary/business key: order_id
- Potential schema-evolution risk: The nested shipping object could gain new fields or change structure, breaking code written for today's shape
- Potential data-quality risk: The nested shipping object breaks naive processing (duplicate-checking crashed on it in Task 2.2); total_amount could contain negative values or lack clear currency context

## 3. products.parquet
- Source name: products.parquet
- Source-system type: Product management system or inventory catalog
- Data format: Parquet
- Structured / semi-structured / unstructured: Structured
- Expected update pattern: Catalog fields (name, category, brand) change infrequently. stock_quantity changes frequently with every order and restock, so this file goes stale quickly if not refreshed often
- Likely acquisition method: Direct file read (pandas.read_parquet), assumed to be exported from the product system
- Schema location or schema owner: Owned by the product management system; no formal schema file included
- Possible primary/business key: product_id
- Potential schema-evolution risk: category is a fixed set of values that could expand without updating downstream code; a new column could also be added
- Potential data-quality risk: No duplicates found, but unit_price of 0 or negative, negative stock_quantity, or weight_kg of 0 would all indicate bad or missing values

## 4. REST API
- Source name: JSONPlaceholder /posts endpoint
- Source-system type: Public mock REST API for testing and classroom exercises
- Data format: JSON
- Structured / semi-structured / unstructured: Structured (flat JSON objects)
- Expected update pattern: Static, rarely changes; fixed demo content rather than live data
- Likely acquisition method: HTTP GET via the requests library, parsing the JSON response
- Schema location or schema owner: Owned and documented by JSONPlaceholder, external to this project
- Possible primary/business key: id (uniquely identifies each post; userId is the author's ID, not unique per post)
- Potential schema-evolution risk: As a third-party API, there's no control over its structure. Field names, the endpoint, or response format could change, or the API could go offline
- Potential data-quality risk: Content is placeholder text with no real meaning and doesn't reflect realistic production patterns, so pipeline logic built against it may not generalize
- Retrieved at (UTC): 2026-08-23T15:48:11.337134+00:00

## 5. PostgreSQL table (support_tickets)
- Source name: support_tickets
- Source-system type: Relational database (PostgreSQL)
- Data format: Relational table
- Structured / semi-structured / unstructured: Structured
- Expected update pattern: Likely append-heavy, with periodic updates to status/resolved_at as tickets are worked
- Likely acquisition method: Direct SQL query/connection (e.g. via SQLAlchemy or psycopg2)
- Schema location or schema owner: Defined in sql/seed_support_tickets.sql; owned by the support system
- Possible primary/business key: ticket_id (primary key); customer_id links back to customers
- Potential schema-evolution risk: New ticket categories or status values could be added without updating downstream code
- Potential data-quality risk: assigned_agent and resolved_at are nullable. Unassigned or unresolved tickets need explicit handling rather than being assumed complete

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