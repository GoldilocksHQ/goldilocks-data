-- Create schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS people;

-- Create educations table
CREATE TABLE people.educations (
    id SERIAL PRIMARY KEY,
    people_id UUID REFERENCES people.identities(people_id) ON DELETE CASCADE,
    educational_establishment TEXT,
    diploma TEXT,
    specialization TEXT,
    start_date DATE,
    end_date DATE,
    priority INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create education_web_addresses table
CREATE TABLE people.education_web_addresses (
    id SERIAL PRIMARY KEY,
    education_id INTEGER REFERENCES people.educations(id) ON DELETE CASCADE,
    url TEXT,
    rank INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create certifications table
CREATE TABLE people.certifications (
    id SERIAL PRIMARY KEY,
    people_id UUID REFERENCES people.identities(people_id) ON DELETE CASCADE,
    name TEXT,
    description TEXT,
    authority TEXT,
    reference TEXT,
    date DATE,
    start_date DATE,
    end_date DATE,
    priority INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create certification_web_addresses table
CREATE TABLE people.certification_web_addresses (
    id SERIAL PRIMARY KEY,
    certification_id INTEGER REFERENCES people.certifications(id) ON DELETE CASCADE,
    url TEXT,
    rank INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create memberships table
CREATE TABLE people.memberships (
    id SERIAL PRIMARY KEY,
    people_id UUID REFERENCES people.identities(people_id) ON DELETE CASCADE,
    title TEXT,
    description TEXT,
    reference TEXT,
    name TEXT,
    start_date DATE,
    end_date DATE,
    location TEXT,
    priority INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create membership_web_addresses table
CREATE TABLE people.membership_web_addresses (
    id SERIAL PRIMARY KEY,
    membership_id INTEGER REFERENCES people.memberships(id) ON DELETE CASCADE,
    url TEXT,
    rank INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create publications table
CREATE TABLE people.publications (
    id SERIAL PRIMARY KEY,
    people_id UUID REFERENCES people.identities(people_id) ON DELETE CASCADE,
    name TEXT,
    description TEXT,
    reference TEXT,
    issue TEXT,
    date DATE,
    priority INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create publication_web_addresses table
CREATE TABLE people.publication_web_addresses (
    id SERIAL PRIMARY KEY,
    publication_id INTEGER REFERENCES people.publications(id) ON DELETE CASCADE,
    url TEXT,
    rank INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create patents table
CREATE TABLE people.patents (
    id SERIAL PRIMARY KEY,
    people_id UUID REFERENCES people.identities(people_id) ON DELETE CASCADE,
    name TEXT,
    issue TEXT,
    number TEXT,
    date DATE,
    start_date DATE,
    end_date DATE,
    priority INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create patent_web_addresses table
CREATE TABLE people.patent_web_addresses (
    id SERIAL PRIMARY KEY,
    patent_id INTEGER REFERENCES people.patents(id) ON DELETE CASCADE,
    url TEXT,
    rank INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create awards table
CREATE TABLE people.awards (
    id SERIAL PRIMARY KEY,
    people_id UUID REFERENCES people.identities(people_id) ON DELETE CASCADE,
    name TEXT,
    description TEXT,
    issue TEXT,
    date DATE,
    priority INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for all tables
CREATE TRIGGER update_educations_updated_at
    BEFORE UPDATE ON people.educations
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_education_web_addresses_updated_at
    BEFORE UPDATE ON people.education_web_addresses
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_certifications_updated_at
    BEFORE UPDATE ON people.certifications
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_certification_web_addresses_updated_at
    BEFORE UPDATE ON people.certification_web_addresses
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_memberships_updated_at
    BEFORE UPDATE ON people.memberships
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_membership_web_addresses_updated_at
    BEFORE UPDATE ON people.membership_web_addresses
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_publications_updated_at
    BEFORE UPDATE ON people.publications
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_publication_web_addresses_updated_at
    BEFORE UPDATE ON people.publication_web_addresses
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_patents_updated_at
    BEFORE UPDATE ON people.patents
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_patent_web_addresses_updated_at
    BEFORE UPDATE ON people.patent_web_addresses
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_awards_updated_at
    BEFORE UPDATE ON people.awards
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Create indexes for better query performance
CREATE INDEX idx_educations_people_id ON people.educations(people_id);
CREATE INDEX idx_education_web_addresses_education_id ON people.education_web_addresses(education_id);
CREATE INDEX idx_certifications_people_id ON people.certifications(people_id);
CREATE INDEX idx_certification_web_addresses_certification_id ON people.certification_web_addresses(certification_id);
CREATE INDEX idx_memberships_people_id ON people.memberships(people_id);
CREATE INDEX idx_membership_web_addresses_membership_id ON people.membership_web_addresses(membership_id);
CREATE INDEX idx_publications_people_id ON people.publications(people_id);
CREATE INDEX idx_publication_web_addresses_publication_id ON people.publication_web_addresses(publication_id);
CREATE INDEX idx_patents_people_id ON people.patents(people_id);
CREATE INDEX idx_patent_web_addresses_patent_id ON people.patent_web_addresses(patent_id);
CREATE INDEX idx_awards_people_id ON people.awards(people_id);
