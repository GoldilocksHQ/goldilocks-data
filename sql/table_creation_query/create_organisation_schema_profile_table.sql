-- Create schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS organisation;

-- Create web_address table
CREATE TABLE organisation.web_addresses (
    id SERIAL PRIMARY KEY,
    organisation_id UUID REFERENCES organisation.identities(organisation_id) ON DELETE CASCADE,
    url TEXT,
    rank INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create employees table
CREATE TABLE organisation.employees (
    id SERIAL PRIMARY KEY,
    organisation_id UUID REFERENCES organisation.identities(organisation_id) ON DELETE CASCADE,
    number_of_employees INTEGER,
    number_of_employees_code TEXT,
    number_of_employees_min INTEGER,
    number_of_employees_max INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create social_links table
CREATE TABLE organisation.social_links (
    id SERIAL PRIMARY KEY,
    organisation_id UUID REFERENCES organisation.identities(organisation_id) ON DELETE CASCADE,
    linkedin_url TEXT,
    twitter_url TEXT,
    facebook_url TEXT,
    instagram_url TEXT,
    youtube_url TEXT,
    crunchbase_url TEXT,
    yelp_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create industries table
CREATE TABLE organisation.industries (
    id SERIAL PRIMARY KEY,
    organisation_id UUID REFERENCES organisation.identities(organisation_id) ON DELETE CASCADE,
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

-- Create phones table
CREATE TABLE organisation.phones (
    id SERIAL PRIMARY KEY,
    organisation_id UUID REFERENCES organisation.identities(organisation_id) ON DELETE CASCADE,
    phone TEXT,
    ddi BOOLEAN,
    dnc BOOLEAN,
    type TEXT,
    carrier TEXT,
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
CREATE TRIGGER update_web_addresses_updated_at
    BEFORE UPDATE ON organisation.web_addresses
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_employees_updated_at
    BEFORE UPDATE ON organisation.employees
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_social_links_updated_at
    BEFORE UPDATE ON organisation.social_links
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_industries_updated_at
    BEFORE UPDATE ON organisation.industries
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_phones_updated_at
    BEFORE UPDATE ON organisation.phones
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Create indexes for better query performance
CREATE INDEX idx_web_addresses_organisation_id ON organisation.web_addresses(organisation_id);
CREATE INDEX idx_employees_organisation_id ON organisation.employees(organisation_id);
CREATE INDEX idx_social_links_organisation_id ON organisation.social_links(organisation_id);
CREATE INDEX idx_industries_organisation_id ON organisation.industries(organisation_id);
CREATE INDEX idx_phones_organisation_id ON organisation.phones(organisation_id);
