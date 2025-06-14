-- Create schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS organisation;

-- Create identities table
CREATE TABLE organisation.identities (
    organisation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    neuron360_company_id TEXT,
    name TEXT,
    domain TEXT,
    logo_url TEXT,
    industry TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create index on id for faster lookups
CREATE INDEX idx_identities_id ON organisation.identities(id);

-- Add trigger to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_identities_updated_at
    BEFORE UPDATE ON organisation.identities
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
