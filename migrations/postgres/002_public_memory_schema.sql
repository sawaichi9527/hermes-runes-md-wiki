-- Hermes Runes MD Wiki public memory schema baseline.
-- Idempotent schema for fresh-user PostgreSQL trial-run databases.

CREATE TABLE IF NOT EXISTS public.documents (
  id bigserial PRIMARY KEY,
  project text NOT NULL,
  source_path text NOT NULL,
  title text,
  sha256 text,
  bytes bigint,
  mtime timestamptz,
  content text,
  content_type text NOT NULL DEFAULT 'markdown',
  parser text,
  parser_version text,
  metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
  is_deleted boolean NOT NULL DEFAULT false,
  deleted_at timestamptz,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (project, source_path)
);

CREATE TABLE IF NOT EXISTS public.chunks (
  id bigserial PRIMARY KEY,
  document_id bigint NOT NULL REFERENCES public.documents(id) ON DELETE CASCADE,
  project text NOT NULL,
  source_path text NOT NULL,
  chunk_index integer NOT NULL,
  content text NOT NULL,
  embedding vector(768),
  token_estimate integer,
  content_type text NOT NULL DEFAULT 'text',
  section_heading text,
  metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (document_id, chunk_index)
);

CREATE INDEX IF NOT EXISTS documents_project_source_idx
  ON public.documents(project, source_path)
  WHERE is_deleted = false;

CREATE INDEX IF NOT EXISTS documents_metadata_gin_idx
  ON public.documents USING gin(metadata);

CREATE INDEX IF NOT EXISTS chunks_project_source_idx
  ON public.chunks(project, source_path);

CREATE INDEX IF NOT EXISTS chunks_document_idx
  ON public.chunks(document_id);

CREATE INDEX IF NOT EXISTS chunks_metadata_gin_idx
  ON public.chunks USING gin(metadata);
