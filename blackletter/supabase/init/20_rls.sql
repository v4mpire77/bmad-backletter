alter table contracts enable row level security;
alter table jobs enable row level security;
alter table findings enable row level security;

-- Contract ownership
create policy "contracts_owner_select" on contracts
for select using (auth.uid() = owner);
create policy "contracts_owner_insert" on contracts
for insert with check (auth.uid() = owner);

-- Jobs readable if you own the parent contract
create policy "jobs_owner_select" on jobs
for select using (
  exists (
    select 1 from contracts c
    where c.id = jobs.contract_id and c.owner = auth.uid()
  )
);

-- Findings readable if you own the job's contract
create policy "findings_owner_select" on findings
for select using (
  exists (
    select 1
    from jobs j
    join contracts c on c.id = j.contract_id
    where j.id = findings.job_id and c.owner = auth.uid()
  )
);
