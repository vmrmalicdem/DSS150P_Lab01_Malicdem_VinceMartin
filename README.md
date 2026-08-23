# DSS150P Lab 01 — Local Data Engineering Workspace

**Student Name:** Malicdem, Vince Martin R.
**Section:** DSS150P - CM17
**Date Started:** August 23, 2026

## REST API endpoint (from LMS)
<`https://jsonplaceholder.typicode.com/posts`>

## How to run this project

1. Create and activate the virtual environment (see project setup notes).
2. `pip install -r requirements.txt`
3. `docker compose up -d` to start PostgreSQL.
4. `python src/verify_environment.py` to confirm the DB connection.
5. Place `customers.csv`, `orders.json`, `products.parquet` into `data/raw/`.
6. `python src/profile_sources.py` to profile the three files.
7. Set `API_URL` in `src/inspect_api.py`, then run it to fetch and save the API snapshot.
8. Run the queries in `sql/01_create_schema.sql` against the `dss150p_lab` database.
9. Fill out all files under `docs/`.

## Folder structure

See lab guide Section 3 for the required structure.
