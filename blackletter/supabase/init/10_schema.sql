-- Owners are Supabase auth users (auth.uid()).
create table if not exists contracts (
  id uuid primary key default gen_random_uuid(),
  owner uuid not null,
  file_path text not null,
  created_at timestamptz not null default now()
);

create table if not exists jobs (
  id uuid primary key default gen_random_uuid(),
  contract_id uuid not null references contracts(id) on delete cascade,
  status text not null default 'queued', -- queued|running|done|error
  created_at timestamptz not null default now()
);

create table if not exists findings (
  id uuid primary key default gen_random_uuid(),
  job_id uuid not null references jobs(id) on delete cascade,
  verdict text not null,   -- Pass|Weak|Missing|Needs Review
  snippet text,
  embedding vector(1536),
  created_at timestamptz not null default now()
);
