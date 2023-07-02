CREATE EXTENSION vector;

CREATE TABLE documents(
    id bigserial PRIMARY KEY,
    content text,
    metadata jsonb,
    embedding vector(1536)
);

CREATE OR REPLACE FUNCTION match_documents(query_embedding vector(1536), match_count int DEFAULT NULL, FILTER jsonb DEFAULT '{}')
    RETURNS TABLE(
        id bigint,
        content text,
        metadata jsonb,
        similarity float)
    LANGUAGE plpgsql
    AS $$
    # variable_conflict use_column
BEGIN
    RETURN query
    SELECT
        id,
        content,
        metadata,
        1 -(documents.embedding <=> query_embedding) AS similarity
    FROM
        documents
    WHERE
        metadata @> FILTER
    ORDER BY
        documents.embedding <=> query_embedding
    LIMIT match_count;
END
$$;

