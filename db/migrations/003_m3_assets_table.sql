create table if not exists assets (
  id bigserial primary key,
  document_id bigint references documents(id) on delete cascade,
  project text not null,
  source_path text not null,
  asset_type text not null,
  mime_type text,
  file_path text,
  sha256 text,
  width integer,
  height integer,
  page_number integer,
  slide_number integer,
  bbox jsonb,
  caption text,
  ocr_text text,
  vision_summary text,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists idx_assets_project on assets(project);
create index if not exists idx_assets_source_path on assets(source_path);
create index if not exists idx_assets_type on assets(asset_type);
create index if not exists idx_assets_metadata_gin on assets using gin(metadata);
