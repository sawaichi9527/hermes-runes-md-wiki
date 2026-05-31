create extension if not exists vector;

create table if not exists documents (
  id bigserial primary key,
  project text not null,
  source_path text not null,
  title text,
  sha256 text not null,
  bytes integer not null default 0,
  mtime timestamptz,
  content text not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (project, source_path)
);

create table if not exists chunks (
  id bigserial primary key,
  document_id bigint not null references documents(id) on delete cascade,
  project text not null,
  source_path text not null,
  chunk_index integer not null,
  content text not null,
  token_estimate integer not null default 0,
  content_tsv tsvector generated always as (
    to_tsvector('simple', coalesce(content, ''))
  ) stored,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (document_id, chunk_index)
);

create table if not exists embeddings (
  id bigserial primary key,
  chunk_id bigint not null references chunks(id) on delete cascade,
  project text not null,
  model text not null,
  dimension integer not null,
  embedding vector(384),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (chunk_id, model)
);

create index if not exists idx_documents_project on documents(project);
create index if not exists idx_documents_source_path on documents(source_path);
create index if not exists idx_chunks_project on chunks(project);
create index if not exists idx_chunks_source_path on chunks(source_path);
create index if not exists idx_chunks_content_tsv on chunks using gin(content_tsv);
create index if not exists idx_embeddings_project on embeddings(project);
create index if not exists idx_embeddings_chunk_id on embeddings(chunk_id);
