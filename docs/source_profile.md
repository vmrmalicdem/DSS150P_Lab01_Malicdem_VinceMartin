# Source Profile — Interpretation

Run `python src/profile_sources.py` first (it writes `data/evidence/profile_report.txt`),
then write your own interpretation below. Do not paste raw pandas output here —
this section is your analysis of what the numbers mean for a future pipeline.

## customers.csv
## customers.csv
1. Observation: 2 fully duplicated rows were found among the 250 records.
   Why it matters: Duplicate customer records could inflate counts in downstream reporting (e.g. double-counting a customer's activity) and should be deduplicated before loading into a production system, ideally with a check on customer_id or email.
2. Observation: The email column has 3 missing values and city has 2 missing values.
   Why it matters: Contact and location fields being incomplete means any pipeline that depends on emailing customers or segmenting by location needs to explicitly handle nulls (e.g. filter them out or flag them) rather than assuming every row is usable.

## orders.json
## orders.json
1. Observation: The nested `shipping` object caused a TypeError when running a standard duplicate-check (df.duplicated()), because pandas can't hash nested dict values.
   Why it matters: Any pipeline treating this file as a simple flat table will break on operations like deduplication or grouping unless the nested shipping fields are first flattened or extracted into their own columns.
2. Observation: No missing values were found in any column.
   Why it matters: This is a positive sign for completeness, but it's worth verifying this holds up as the file grows — a clean sample now doesn't guarantee future exports stay complete, especially for optional fields like shipping details.

## products.parquet
## products.parquet
1. Observation: No duplicate rows and no missing values were found across all 200 products.
   Why it matters: This is a strong sign of a well-maintained source, but completeness alone doesn't guarantee correctness — the values themselves (e.g. unit_price, stock_quantity, weight_kg) still need range checks, since a non-null value like a price of 0 or negative stock would pass a completeness check but still be invalid.
2. Observation: category is a text field with a limited set of repeated values, functioning like an informal category list rather than a strictly enforced schema.
   Why it matters: Without a formal constraint (like a database enum or foreign key to a categories table), new or inconsistent category values (typos, new categories) could be introduced
