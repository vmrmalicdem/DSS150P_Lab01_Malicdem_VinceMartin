"""
Task 2.2 - Profile customers.csv, orders.json, and products.parquet.

Prints, for each source:
- file name and size
- row/column counts
- column names in original order
- inferred dtype per column
- null counts per column
- duplicate row count
- distinct value counts per column (skipped for unhashable/list-like columns)
- first five records
- min/max for numeric columns
- earliest/latest for date-like columns (best-effort parse)

Also writes a combined text report to data/evidence/profile_report.txt
so you have something to paste into docs/source_profile.md and to keep
as evidence.
"""

from pathlib import Path
import sys
import pandas as pd

RAW = Path("data/raw")
EVIDENCE = Path("data/evidence")
EVIDENCE.mkdir(parents=True, exist_ok=True)

DATE_LIKE_HINTS = ("date", "time", "created", "updated", "dob", "timestamp")


def is_probably_date_column(col_name: str) -> bool:
    lowered = col_name.lower()
    return any(hint in lowered for hint in DATE_LIKE_HINTS)


def try_parse_dates(series: pd.Series) -> pd.Series | None:
    try:
        parsed = pd.to_datetime(series, errors="coerce", utc=False)
        # If everything failed to parse, treat as not a date column
        if parsed.notna().sum() == 0:
            return None
        return parsed
    except Exception:
        return None


def distinct_count(series: pd.Series):
    try:
        return series.nunique(dropna=True)
    except TypeError:
        # Unhashable types (e.g. lists/dicts from nested JSON)
        return "N/A (unhashable/nested type)"


def profile_dataframe(name: str, df: pd.DataFrame, file_path: Path, report_lines: list[str]) -> None:
    size_bytes = file_path.stat().st_size
    size_kb = size_bytes / 1024

    report_lines.append(f"\n{'=' * 70}")
    report_lines.append(f"SOURCE: {name}")
    report_lines.append(f"{'=' * 70}")
    report_lines.append(f"File size: {size_bytes:,} bytes ({size_kb:,.2f} KB)")
    report_lines.append(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
    report_lines.append(f"Columns (original order): {list(df.columns)}")

    report_lines.append("\n--- Dtypes ---")
    for col, dtype in df.dtypes.items():
        report_lines.append(f"  {col}: {dtype}")

    report_lines.append("\n--- Null counts ---")
    nulls = df.isna().sum()
    for col, n in nulls.items():
        report_lines.append(f"  {col}: {n}")

    try:
        dup_count = df.duplicated().sum()
    except TypeError:
        # Some columns contain unhashable types (e.g. nested dicts/lists from
        # JSON sources like a nested "shipping" object). Fall back to comparing
        # string representations of each row instead.
        dup_count = df.astype(str).duplicated().sum()
    report_lines.append(f"\nFully duplicated rows: {dup_count}")

    report_lines.append("\n--- Distinct value counts ---")
    for col in df.columns:
        report_lines.append(f"  {col}: {distinct_count(df[col])}")

    report_lines.append("\n--- First five records ---")
    report_lines.append(df.head().to_string())

    report_lines.append("\n--- Numeric column min/max ---")
    numeric_cols = df.select_dtypes(include="number").columns
    if len(numeric_cols) == 0:
        report_lines.append("  (no numeric columns)")
    for col in numeric_cols:
        report_lines.append(f"  {col}: min={df[col].min()}, max={df[col].max()}")

    report_lines.append("\n--- Date-like column earliest/latest (best-effort parse) ---")
    date_candidates = [c for c in df.columns if is_probably_date_column(c)]
    if not date_candidates:
        report_lines.append("  (no obviously date-like column names found)")
    for col in date_candidates:
        parsed = try_parse_dates(df[col])
        if parsed is None:
            report_lines.append(f"  {col}: could not parse as dates")
        else:
            report_lines.append(f"  {col}: earliest={parsed.min()}, latest={parsed.max()}")

    # Console echo (kept concise; full detail is in the report file)
    print(f"\n=== {name} ===")
    print("shape:", df.shape)
    print("columns:", list(df.columns))
    print("duplicate rows:", dup_count)
    print(df.head())


def main() -> None:
    report_lines: list[str] = []

    sources = {}

    customers_path = RAW / "customers.csv"
    orders_path = RAW / "orders.json"
    products_path = RAW / "products.parquet"

    missing = [p for p in (customers_path, orders_path, products_path) if not p.exists()]
    if missing:
        print("ERROR: missing expected raw files:", [str(p) for p in missing])
        print("Place customers.csv, orders.json, and products.parquet under data/raw/ first.")
        sys.exit(1)

    sources["customers.csv"] = (pd.read_csv(customers_path), customers_path)
    sources["orders.json"] = (pd.read_json(orders_path), orders_path)
    sources["products.parquet"] = (pd.read_parquet(products_path), products_path)

    for name, (df, path) in sources.items():
        profile_dataframe(name, df, path, report_lines)

    report_text = "\n".join(report_lines)
    out_path = EVIDENCE / "profile_report.txt"
    out_path.write_text(report_text, encoding="utf-8")
    print(f"\nFull profile report written to {out_path}")


if __name__ == "__main__":
    main()
