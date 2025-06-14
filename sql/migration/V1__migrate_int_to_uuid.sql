-- =================================================================
--  SQL Migration Script
--  Changes all system-generated INTEGER primary keys to UUID.
--  It preserves existing data and relationships.
--
--  IMPORTANT:
--  1. BACK UP YOUR DATABASE before running this script.
--  2. This script should be run as a single transaction.
-- =================================================================

BEGIN;

-- == Step 1: Drop all relevant Foreign Key constraints =================

-- Drop FKs pointing to people.experiences
ALTER TABLE people.job_functions DROP CONSTRAINT IF EXISTS job_functions_experience_id_fkey;
ALTER TABLE people.job_seniority DROP CONSTRAINT IF EXISTS job_seniority_experience_id_fkey;
ALTER TABLE people.job_title_details DROP CONSTRAINT IF EXISTS job_title_details_experience_id_fkey;

-- Drop FKs pointing to people.certifications
ALTER TABLE people.certification_web_addresses DROP CONSTRAINT IF EXISTS certification_web_addresses_certification_id_fkey;

-- Drop FKs pointing to people.educations
ALTER TABLE people.education_web_addresses DROP CONSTRAINT IF EXISTS education_web_addresses_education_id_fkey;

-- Drop FKs pointing to people.memberships
ALTER TABLE people.membership_web_addresses DROP CONSTRAINT IF EXISTS membership_web_addresses_membership_id_fkey;

-- Drop FKs pointing to people.patents
ALTER TABLE people.patent_web_addresses DROP CONSTRAINT IF EXISTS patent_web_addresses_patent_id_fkey;

-- Drop FKs pointing to people.publications
ALTER TABLE people.publication_web_addresses DROP CONSTRAINT IF EXISTS publication_web_addresses_publication_id_fkey;


-- == Step 2: Alter column types from INTEGER to UUID =================
-- This uses a deterministic method to convert old integer IDs to UUIDs,
-- which preserves the relationships between tables.

-- Function to create a deterministic UUID from an integer
CREATE OR REPLACE FUNCTION uuid_from_int(id_val INTEGER)
RETURNS UUID AS $$
BEGIN
    RETURN (LPAD(to_hex(id_val), 32, '0'))::uuid;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Alter tables in 'people' schema
ALTER TABLE people.experiences ALTER COLUMN id DROP DEFAULT, ALTER COLUMN id SET DATA TYPE UUID USING (uuid_from_int(id)), ALTER COLUMN id SET DEFAULT gen_random_uuid();
ALTER TABLE people.job_functions ALTER COLUMN id DROP DEFAULT, ALTER COLUMN id SET DATA TYPE UUID USING (uuid_from_int(id)), ALTER COLUMN id SET DEFAULT gen_random_uuid();
ALTER TABLE people.job_seniority ALTER COLUMN id DROP DEFAULT, ALTER COLUMN id SET DATA TYPE UUID USING (uuid_from_int(id)), ALTER COLUMN id SET DEFAULT gen_random_uuid();
ALTER TABLE people.job_title_details ALTER COLUMN id DROP DEFAULT, ALTER COLUMN id SET DATA TYPE UUID USING (uuid_from_int(id)), ALTER COLUMN id SET DEFAULT gen_random_uuid();
ALTER TABLE people.job_functions ALTER COLUMN experience_id SET DATA TYPE UUID USING (uuid_from_int(experience_id));
ALTER TABLE people.job_seniority ALTER COLUMN experience_id SET DATA TYPE UUID USING (uuid_from_int(experience_id));
ALTER TABLE people.job_title_details ALTER COLUMN experience_id SET DATA TYPE UUID USING (uuid_from_int(experience_id));

ALTER TABLE people.certifications ALTER COLUMN id DROP DEFAULT, ALTER COLUMN id SET DATA TYPE UUID USING (uuid_from_int(id)), ALTER COLUMN id SET DEFAULT gen_random_uuid();
ALTER TABLE people.certification_web_addresses ALTER COLUMN id DROP DEFAULT, ALTER COLUMN id SET DATA TYPE UUID USING (uuid_from_int(id)), ALTER COLUMN id SET DEFAULT gen_random_uuid();
ALTER TABLE people.certification_web_addresses ALTER COLUMN certification_id SET DATA TYPE UUID USING (uuid_from_int(certification_id));

ALTER TABLE people.educations ALTER COLUMN id DROP DEFAULT, ALTER COLUMN id SET DATA TYPE UUID USING (uuid_from_int(id)), ALTER COLUMN id SET DEFAULT gen_random_uuid();
ALTER TABLE people.education_web_addresses ALTER COLUMN id DROP DEFAULT, ALTER COLUMN id SET DATA TYPE UUID USING (uuid_from_int(id)), ALTER COLUMN id SET DEFAULT gen_random_uuid();
ALTER TABLE people.education_web_addresses ALTER COLUMN education_id SET DATA TYPE UUID USING (uuid_from_int(education_id));

ALTER TABLE people.memberships ALTER COLUMN id DROP DEFAULT, ALTER COLUMN id SET DATA TYPE UUID USING (uuid_from_int(id)), ALTER COLUMN id SET DEFAULT gen_random_uuid();
ALTER TABLE people.membership_web_addresses ALTER COLUMN id DROP DEFAULT, ALTER COLUMN id SET DATA TYPE UUID USING (uuid_from_int(id)), ALTER COLUMN id SET DEFAULT gen_random_uuid();
ALTER TABLE people.membership_web_addresses ALTER COLUMN membership_id SET DATA TYPE UUID USING (uuid_from_int(membership_id));

ALTER TABLE people.patents ALTER COLUMN id DROP DEFAULT, ALTER COLUMN id SET DATA TYPE UUID USING (uuid_from_int(id)), ALTER COLUMN id SET DEFAULT gen_random_uuid();
ALTER TABLE people.patent_web_addresses ALTER COLUMN id DROP DEFAULT, ALTER COLUMN id SET DATA TYPE UUID USING (uuid_from_int(id)), ALTER COLUMN id SET DEFAULT gen_random_uuid();
ALTER TABLE people.patent_web_addresses ALTER COLUMN patent_id SET DATA TYPE UUID USING (uuid_from_int(patent_id));

ALTER TABLE people.publications ALTER COLUMN id DROP DEFAULT, ALTER COLUMN id SET DATA TYPE UUID USING (uuid_from_int(id)), ALTER COLUMN id SET DEFAULT gen_random_uuid();
ALTER TABLE people.publication_web_addresses ALTER COLUMN id DROP DEFAULT, ALTER COLUMN id SET DATA TYPE UUID USING (uuid_from_int(id)), ALTER COLUMN id SET DEFAULT gen_random_uuid();
ALTER TABLE people.publication_web_addresses ALTER COLUMN publication_id SET DATA TYPE UUID USING (uuid_from_int(publication_id));

-- Alter remaining 'people' tables with no outgoing FKs to other INT tables
ALTER TABLE people.addresses ALTER COLUMN id DROP DEFAULT, ALTER COLUMN id SET DATA TYPE UUID USING (uuid_from_int(id)), ALTER COLUMN id SET DEFAULT gen_random_uuid();
ALTER TABLE people.awards ALTER COLUMN id DROP DEFAULT, ALTER COLUMN id SET DATA TYPE UUID USING (uuid_from_int(id)), ALTER COLUMN id SET DEFAULT gen_random_uuid();
ALTER TABLE people.emails ALTER COLUMN id DROP DEFAULT, ALTER COLUMN id SET DATA TYPE UUID USING (uuid_from_int(id)), ALTER COLUMN id SET DEFAULT gen_random_uuid();
ALTER TABLE people.genders ALTER COLUMN id DROP DEFAULT, ALTER COLUMN id SET DATA TYPE UUID USING (uuid_from_int(id)), ALTER COLUMN id SET DEFAULT gen_random_uuid();
ALTER TABLE people.phones ALTER COLUMN id DROP DEFAULT, ALTER COLUMN id SET DATA TYPE UUID USING (uuid_from_int(id)), ALTER COLUMN id SET DEFAULT gen_random_uuid();
ALTER TABLE people.social_links ALTER COLUMN id DROP DEFAULT, ALTER COLUMN id SET DATA TYPE UUID USING (uuid_from_int(id)), ALTER COLUMN id SET DEFAULT gen_random_uuid();
ALTER TABLE people.statuses ALTER COLUMN id DROP DEFAULT, ALTER COLUMN id SET DATA TYPE UUID USING (uuid_from_int(id)), ALTER COLUMN id SET DEFAULT gen_random_uuid();

-- Alter tables in 'organisation' schema
ALTER TABLE organisation.employees ALTER COLUMN id DROP DEFAULT, ALTER COLUMN id SET DATA TYPE UUID USING (uuid_from_int(id)), ALTER COLUMN id SET DEFAULT gen_random_uuid();
ALTER TABLE organisation.industries ALTER COLUMN id DROP DEFAULT, ALTER COLUMN id SET DATA TYPE UUID USING (uuid_from_int(id)), ALTER COLUMN id SET DEFAULT gen_random_uuid();
ALTER TABLE organisation.office_addresses ALTER COLUMN id DROP DEFAULT, ALTER COLUMN id SET DATA TYPE UUID USING (uuid_from_int(id)), ALTER COLUMN id SET DEFAULT gen_random_uuid();
ALTER TABLE organisation.office_industries ALTER COLUMN id DROP DEFAULT, ALTER COLUMN id SET DATA TYPE UUID USING (uuid_from_int(id)), ALTER COLUMN id SET DEFAULT gen_random_uuid();
ALTER TABLE organisation.phones ALTER COLUMN id DROP DEFAULT, ALTER COLUMN id SET DATA TYPE UUID USING (uuid_from_int(id)), ALTER COLUMN id SET DEFAULT gen_random_uuid();
ALTER TABLE organisation.social_links ALTER COLUMN id DROP DEFAULT, ALTER COLUMN id SET DATA TYPE UUID USING (uuid_from_int(id)), ALTER COLUMN id SET DEFAULT gen_random_uuid();
ALTER TABLE organisation.web_addresses ALTER COLUMN id DROP DEFAULT, ALTER COLUMN id SET DATA TYPE UUID USING (uuid_from_int(id)), ALTER COLUMN id SET DEFAULT gen_random_uuid();


-- == Step 3: Re-create all Foreign Key constraints ====================

ALTER TABLE people.job_functions ADD CONSTRAINT job_functions_experience_id_fkey FOREIGN KEY (experience_id) REFERENCES people.experiences(id) ON DELETE CASCADE;
ALTER TABLE people.job_seniority ADD CONSTRAINT job_seniority_experience_id_fkey FOREIGN KEY (experience_id) REFERENCES people.experiences(id) ON DELETE CASCADE;
ALTER TABLE people.job_title_details ADD CONSTRAINT job_title_details_experience_id_fkey FOREIGN KEY (experience_id) REFERENCES people.experiences(id) ON DELETE CASCADE;

ALTER TABLE people.certification_web_addresses ADD CONSTRAINT certification_web_addresses_certification_id_fkey FOREIGN KEY (certification_id) REFERENCES people.certifications(id) ON DELETE CASCADE;
ALTER TABLE people.education_web_addresses ADD CONSTRAINT education_web_addresses_education_id_fkey FOREIGN KEY (education_id) REFERENCES people.educations(id) ON DELETE CASCADE;
ALTER TABLE people.membership_web_addresses ADD CONSTRAINT membership_web_addresses_membership_id_fkey FOREIGN KEY (membership_id) REFERENCES people.memberships(id) ON DELETE CASCADE;
ALTER TABLE people.patent_web_addresses ADD CONSTRAINT patent_web_addresses_patent_id_fkey FOREIGN KEY (patent_id) REFERENCES people.patents(id) ON DELETE CASCADE;
ALTER TABLE people.publication_web_addresses ADD CONSTRAINT publication_web_addresses_publication_id_fkey FOREIGN KEY (publication_id) REFERENCES people.publications(id) ON DELETE CASCADE;

-- Drop the temporary function
DROP FUNCTION uuid_from_int(INTEGER);

COMMIT;
