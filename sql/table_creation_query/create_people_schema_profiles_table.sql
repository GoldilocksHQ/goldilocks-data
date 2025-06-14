-- Create schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS people;

-- Create profiles table
CREATE TABLE people.profiles (
    people_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    summary TEXT,
    languages TEXT[],
    expertises TEXT[],
    tags TEXT[],
    prior_industries TEXT[],
    raw_location TEXT,
    headline TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create gender table
CREATE TABLE people.genders (
    id SERIAL PRIMARY KEY,
    people_id UUID REFERENCES people.profiles(people_id) ON DELETE CASCADE,
    gender TEXT,
    confidence_score FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create social_links table
CREATE TABLE people.social_links (
    id SERIAL PRIMARY KEY,
    people_id UUID REFERENCES people.profiles(people_id) ON DELETE CASCADE,
    name TEXT,
    url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create status table
CREATE TABLE people.statuses (
    id SERIAL PRIMARY KEY,
    people_id UUID REFERENCES people.profiles(people_id) ON DELETE CASCADE,
    status TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create emails table
CREATE TABLE people.emails (
    id SERIAL PRIMARY KEY,
    people_id UUID REFERENCES people.profiles(people_id) ON DELETE CASCADE,
    email TEXT,
    priority INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create phones table
CREATE TABLE people.phones (
    id SERIAL PRIMARY KEY,
    people_id UUID REFERENCES people.profiles(people_id) ON DELETE CASCADE,
    phone TEXT,
    ddi BOOLEAN,
    dnc BOOLEAN,
    type TEXT,
    carrier TEXT,
    priority INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create addresses table
CREATE TABLE people.addresses (
    id SERIAL PRIMARY KEY,
    people_id UUID REFERENCES people.profiles(people_id) ON DELETE CASCADE,
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

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for all tables
CREATE TRIGGER update_profiles_updated_at
    BEFORE UPDATE ON people.profiles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_genders_updated_at
    BEFORE UPDATE ON people.genders
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_social_links_updated_at
    BEFORE UPDATE ON people.social_links
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_statuses_updated_at
    BEFORE UPDATE ON people.statuses
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_emails_updated_at
    BEFORE UPDATE ON people.emails
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_phones_updated_at
    BEFORE UPDATE ON people.phones
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_addresses_updated_at
    BEFORE UPDATE ON people.addresses
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Create indexes for better query performance
CREATE INDEX idx_genders_people_id ON people.genders(people_id);
CREATE INDEX idx_social_links_people_id ON people.social_links(people_id);
CREATE INDEX idx_statuses_people_id ON people.statuses(people_id);
CREATE INDEX idx_emails_people_id ON people.emails(people_id);
CREATE INDEX idx_phones_people_id ON people.phones(people_id);
CREATE INDEX idx_addresses_people_id ON people.addresses(people_id);
