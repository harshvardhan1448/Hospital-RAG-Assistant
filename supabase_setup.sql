-- ============================================================================
-- Hospital RAG Assistant - Supabase Setup Script
-- ============================================================================
-- Run this script in your Supabase SQL Editor to set up the database
-- Reference: https://supabase.com/dashboard -> Your Project -> SQL Editor
-- ============================================================================

-- Step 1: Enable pgvector extension (for vector operations)
-- This allows us to store and search embeddings
CREATE EXTENSION IF NOT EXISTS vector;

-- Step 2: Create the documents table
-- This table stores document chunks with their embeddings
CREATE TABLE IF NOT EXISTS documents (
  -- Primary key
  id BIGSERIAL PRIMARY KEY,
  
  -- Document metadata
  filename TEXT NOT NULL,                    -- Name of uploaded PDF
  chunk_index INTEGER,                       -- Position of chunk in document
  page TEXT,                                 -- Page number for source attribution
  content TEXT,                              -- Actual text content of chunk
  
  -- Vector embedding (384 dimensions for all-MiniLM-L6-v2)
  embedding vector(384),
  
  -- Additional metadata as JSON
  metadata JSONB DEFAULT '{}'::jsonb,
  
  -- Timestamps
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Step 3: Create indexes for better performance
-- Index for vector similarity search using cosine distance
CREATE INDEX IF NOT EXISTS documents_embedding_idx ON documents 
USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Index for filename-based filtering
CREATE INDEX IF NOT EXISTS documents_filename_idx ON documents(filename);

-- Index for full-text search (optional, for hybrid search)
CREATE INDEX IF NOT EXISTS documents_content_idx ON documents USING GIN (to_tsvector('english', content));

-- Step 4: Create RPC function for similarity search
-- This function is used by the Python backend to find similar chunks
CREATE OR REPLACE FUNCTION match_documents(
  query_embedding text,
  match_count int DEFAULT 5
) RETURNS TABLE (
  id bigint,
  content text,
  similarity float8,
  page text,
  metadata jsonb,
  filename text
) LANGUAGE plpgsql AS $$
DECLARE
  embedding_vector vector;
BEGIN
  -- Cast the text parameter to vector type
  embedding_vector := query_embedding::vector;
  
  RETURN QUERY
  SELECT
    documents.id,
    documents.content,
    1 - (documents.embedding <=> embedding_vector) as similarity,
    documents.page,
    documents.metadata,
    documents.filename
  FROM documents
  WHERE documents.embedding IS NOT NULL
  ORDER BY documents.embedding <=> embedding_vector
  LIMIT match_count;
END;
$$ SECURITY DEFINER;

-- Step 5: Create function for delete documents by filename
CREATE OR REPLACE FUNCTION delete_documents(
  p_filename text
) RETURNS integer AS $$
DECLARE
  deleted_count int;
BEGIN
  DELETE FROM documents WHERE filename = p_filename;
  GET DIAGNOSTICS deleted_count = ROW_COUNT;
  RETURN deleted_count;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Step 6: Enable Row Level Security (RLS) for production
-- For development, you can disable this. For production, set strict policies
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- Create a permissive policy for select (allows all reads in dev)
CREATE POLICY "Enable select for all users" ON documents
  AS PERMISSIVE FOR SELECT
  USING (true);

-- Create a permissive policy for insert (allows all inserts in dev)
CREATE POLICY "Enable insert for all users" ON documents
  AS PERMISSIVE FOR INSERT
  WITH CHECK (true);

-- Create a permissive policy for delete (allows all deletes in dev)
CREATE POLICY "Enable delete for all users" ON documents
  AS PERMISSIVE FOR DELETE
  USING (true);

-- ============================================================================
-- Verification Queries
-- ============================================================================
-- Run these to verify your setup:

-- Check table exists and has correct structure
-- SELECT column_name, data_type FROM information_schema.columns 
-- WHERE table_name='documents';

-- Check indexes were created
-- SELECT indexname FROM pg_indexes WHERE tablename='documents';

-- Check functions were created
-- SELECT routine_name FROM information_schema.routines 
-- WHERE routine_schema='public' AND routine_name IN ('match_documents', 'delete_documents');

-- ============================================================================
-- Notes for Users:
-- ============================================================================
-- 1. Make sure pgvector extension is available in your Supabase project
-- 2. The embedding dimension (1536) matches text-embedding-3-small
-- 3. Change this if using a different embedding model:
--    - text-embedding-3-large uses 3072 dimensions
--    - other models may use different dimensions
-- 4. The IVFFLAT index is optimized for cosine distance similarity search
-- 5. For production, adjust RLS policies according to your security needs
-- 6. The match_documents function uses cosine distance (<=> operator)
-- ============================================================================
