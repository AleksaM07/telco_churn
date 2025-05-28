WITH cleaned AS (
        SELECT 
            raw
        FROM {{ ref('raw_crossref_parquet') }}
        WHERE raw IS NOT NULL 
          AND LENGTH(TRIM(raw)) > 0  -- Exclude empty strings
          AND TRY_CAST(raw AS JSON) IS NOT NULL  -- Keep only valid JSON rows
    ),
    parsed AS (
        SELECT
            JSON_EXTRACT_STRING(raw, '$.DOI') AS doi,
            JSON_EXTRACT_STRING(raw, '$.title[0]') AS title,
            JSON_EXTRACT_STRING(raw, '$.publisher') AS publisher,
            JSON_EXTRACT_STRING(raw, '$.indexed.date-time') AS indexed_at,
            CAST(JSON_EXTRACT_STRING(raw, '$.published-print.date-parts[0][0]') AS INT) AS year,
            CAST(JSON_EXTRACT_STRING(raw, '$.published-print.date-parts[0][1]') AS INT) AS month,
            CAST(JSON_EXTRACT_STRING(raw, '$.published-print.date-parts[0][2]') AS INT) AS day
        FROM cleaned
    )
    SELECT
        doi,
        title,
        publisher,
        indexed_at,
        make_date(year, month, day) AS published_date
    FROM parsed