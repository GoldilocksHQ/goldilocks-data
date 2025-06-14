-- Create schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS organisation;

-- Create offices table
CREATE TABLE organisation.offices (
    office_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organisation_id UUID REFERENCES organisation.identities(organisation_id) ON DELETE CASCADE,
    neuron360_office_id TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create office_addresses table
CREATE TABLE organisation.office_addresses (
    id SERIAL PRIMARY KEY,
    office_id UUID REFERENCES organisation.offices(office_id) ON DELETE CASCADE,
    last_modified_date TIMESTAMP,
    formatted_address TEXT,
    street_address TEXT,
    place_id TEXT,
    lat FLOAT,
    lng FLOAT,
    accuracy TEXT,
    confidence_score FLOAT,
    quality TEXT,
    administrative_area_level_1 TEXT,
    administrative_area_level_2 TEXT,
    administrative_area_level_3 TEXT,
    administrative_area_level_4 TEXT,
    administrative_area_level_5 TEXT,
    continent TEXT,
    country TEXT,
    country_code TEXT,
    establishment TEXT,
    locality TEXT,
    postal_code TEXT,
    postal_town TEXT,
    premise TEXT,
    county TEXT,
    state TEXT,
    city TEXT,
    street TEXT,
    street_number TEXT,
    sublocality TEXT,
    subpremise TEXT,
    score FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create office_industries table
CREATE TABLE organisation.office_industries (
    id SERIAL PRIMARY KEY,
    office_id UUID REFERENCES organisation.offices(office_id) ON DELETE CASCADE,
    industry_id TEXT,
    code2 TEXT,
    name2 TEXT,
    code3 TEXT,
    name3 TEXT,
    code4 TEXT,
    name4 TEXT,
    code5 TEXT,
    name5 TEXT,
    code6 TEXT,
    name6 TEXT,
    standard TEXT,
    activity_priority INTEGER,
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
CREATE TRIGGER update_offices_updated_at
    BEFORE UPDATE ON organisation.offices
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_office_addresses_updated_at
    BEFORE UPDATE ON organisation.office_addresses
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_office_industries_updated_at
    BEFORE UPDATE ON organisation.office_industries
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Create indexes for better query performance
CREATE INDEX idx_offices_organisation_id ON organisation.offices(organisation_id);
CREATE INDEX idx_offices_neuron360_office_id ON organisation.offices(neuron360_office_id);
CREATE INDEX idx_office_addresses_office_id ON organisation.office_addresses(office_id);
CREATE INDEX idx_office_industries_office_id ON organisation.office_industries(office_id);
