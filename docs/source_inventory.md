# Source Inventory

For each source, fill in every field below in your own words.

## 1. customers.csv
- Source name: customers.csv
- Source-system type: Web/app signup form, likely backed by a customer database or CRM
- Data format: CSV
- Structured / semi-structured / unstructured: Structured
- Expected update pattern: Signups happen continuously, but this file is a batch export/snapshot — likely refreshed daily or on some regular schedule
- Likely acquisition method: Direct file read (pandas.read_csv) — file assumed to already be exported/dropped into a shared location like a folder, S3 bucket, or SFTP drop
- Schema location or schema owner: Owned by whatever system manages signups (CRM/app database); no formal schema file included in this lab
- Possible primary/business key: customer_id
- Potential schema-evolution risk: A new column could be added (e.g. loyalty_tier), or existing categorical values (like customer_segment) could gain new categories — breaking code that assumes a fixed set of columns/values
- Potential data-quality risk: 2 duplicate rows found during profiling; email values could have invalid formats (typos, missing @, malformed addresses) since there's no validation enforced on a raw CSV export

## 2. orders.json
- Source name: orders.json
- Source-system type: Order management system (e.g. e-commerce backend that processes and tracks orders)
- Data format: JSON
- Structured / semi-structured / unstructured: Semi-structured (nested shipping object)
- Expected update pattern: Orders happen continuously in real life, but this file represents a batch export/snapshot, likely refreshed on a regular schedule (e.g. daily)
- Likely acquisition method: Direct file read (pandas.read_json) — file assumed to be exported/dropped from the order management system into a shared location
- Schema location or schema owner: Owned by the order management system; no formal schema file included in this lab
- Possible primary/business key: order_id
- Potential schema-evolution risk: The nested shipping object could gain new fields (e.g. a tracking_number added later) or have its structure changed, which would break code written to expect today's exact nested shape
- Potential data-quality risk: The nested shipping object breaks naive processing (e.g. duplicate-checking crashed on it, per Task 2.2); total_amount could contain negative values (e.g. refunds mixed into order data) or lack clear currency/unit context, making downstream calculations unreliable

## 3. products.parquet
- Source name: products.parquet
- Source-system type: Product management system / inventory catalog (e.g. a PIM or the e-commerce platform's product database)
- Data format: Parquet
- Structured / semi-structured / unstructured: Structured
- Expected update pattern: Product catalog fields (name, category, brand) change infrequently — new products are added occasionally. But stock_quantity changes very frequently, decreasing with every order and increasing on restock — so this file is likely a snapshot that goes stale quickly if not refreshed often
- Likely acquisition method: Direct file read (pandas.read_parquet) — file assumed to be exported from the product management system into a shared location
- Schema location or schema owner: Owned by the product management system; no formal schema file included in this lab
- Possible primary/business key: product_id
- Potential schema-evolution risk: category represents a fixed set of values that could expand over time (new categories added without updating downstream code that assumes a known list); a new column could also be added (e.g. a new product attribute)
- Potential data-quality risk: No duplicate rows were found, but numeric fields carry risk: unit_price of 0 or negative doesn't make sense for a sellable product, stock_quantity shouldn't logically go negative (would signal a sync/calculation bug), and weight_kg of 0 could mean the weight was never actually recorded rather than truly weighing nothing

## 4. REST API
- Source name: JSONPlaceholder /posts endpoint
- Source-system type: Public fake/mock REST API for testing and classroom exercises
- Data format: JSON
- Structured / semi-structured / unstructured: Structured (flat JSON objects)
- Expected update pattern: Static/rarely changes — fixed demo content rather than live production data
- Likely acquisition method: HTTP GET request via the requests library (requests.get()), parsing the JSON response
- Schema location or schema owner: Owned/documented by JSONPlaceholder (third-party, external to this project)
- Possible primary/business key: id (uniquely identifies each post; userId is a foreign key to the author, not unique per post)
- Potential schema-evolution risk: Being a third-party public API, there's no control over its structure — field names, endpoint URL, or response format could change, or the API could be deprecated/go offline entirely
- Potential data-quality risk: Content (title/body) is placeholder/lorem-ipsum text with no real semantic meaning; data doesn't reflect realistic production patterns, so pipeline logic built against it may not generalize to real data
- Retrieved at (UTC): 2026-08-23T15:48:11.337134+00:00

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