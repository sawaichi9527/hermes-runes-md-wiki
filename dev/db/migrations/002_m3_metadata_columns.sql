alter table documents
  add column if not exists content_type text not null default 'markdown',
  add column if not exists parser text,
  add column if not exists parser_version text,
  add column if not exists metadata jsonb not null default '{}'::jsonb,
  add column if not exists is_deleted boolean not null default false,
  add column if not exists deleted_at timestamptz;

alter table chunks
  add column if not exists content_type text not null default 'text',
  add column if not exists section_heading text,
  add column if not exists metadata jsonb not null default '{}'::jsonb;

create index if not exists idx_documents_content_type on documents(content_type);
create index if not exists idx_documents_is_deleted on documents(is_deleted);
create index if not exists idx_chunks_content_type on chunks(content_type);
create index if not exists idx_documents_metadata_gin on documents using gin(metadata);
create index if not exists idx_chunks_metadata_gin on chunks using gin(metadata);
