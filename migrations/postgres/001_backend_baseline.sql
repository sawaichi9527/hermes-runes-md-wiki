-- Hermes Runes MD Wiki PostgreSQL backend baseline migration.
-- This migration is intentionally small and idempotent.
-- The external PostgreSQL Docker stack owns service startup, database creation,
-- user/password/volume lifecycle, and optional service-level extension init.
-- Hermes Runes MD Wiki owns application schema migration.

CREATE EXTENSION IF NOT EXISTS vector;

-- Keep this migration lightweight. Application-specific tables should be added
-- through later idempotent migrations as the P0 schema contract evolves.
