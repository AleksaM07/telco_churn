WITH cleaned AS (
  SELECT raw
  FROM {{ ref('raw_crossref_parquet') }}
  WHERE raw IS NOT NULL
    AND LENGTH(TRIM(raw)) > 0
    AND TRY_CAST(raw AS JSON) IS NOT NULL
),
parsed AS (
  SELECT
    JSON_EXTRACT_STRING(raw, '$.DOI') AS work_id,
    JSON_EXTRACT(raw, '$.author') AS authors_json
  FROM cleaned
)
SELECT * FROM cleaned