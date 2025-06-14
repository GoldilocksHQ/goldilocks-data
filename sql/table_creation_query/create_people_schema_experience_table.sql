-- Create schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS people;

-- Create experiences table
CREATE TABLE people.experiences (
    id SERIAL PRIMARY KEY,
    people_id UUID REFERENCES people.identities(people_id) ON DELETE CASCADE,
    job_title TEXT,
    start_date DATE,
    end_date DATE,
    summary TEXT,
    current BOOLEAN,
    priority INTEGER,
    raw_location TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create job_title_details table
CREATE TABLE people.job_title_details (
    id SERIAL PRIMARY KEY,
    experience_id INTEGER REFERENCES people.experiences(id) ON DELETE CASCADE,
    raw_job_title TEXT,
    raw_job_title_language_code TEXT,
    raw_job_title_language_detection_confidence_score FLOAT,
    raw_translated_job_title TEXT,
    raw_translated_job_title_language_code TEXT,
    normalized_job_title_id INTEGER,
    normalized_job_title TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create job_functions table
CREATE TABLE people.job_functions (
    id SERIAL PRIMARY KEY,
    experience_id INTEGER REFERENCES people.experiences(id) ON DELETE CASCADE,
    level1_code TEXT,
    level1_name TEXT,
    level1_confidence_score FLOAT,
    level2_code TEXT,
    level2_name TEXT,
    level2_confidence_score FLOAT,
    level3_code TEXT,
    level3_name TEXT,
    level3_confidence_score FLOAT,
    priority INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create job_seniority table
CREATE TABLE people.job_seniority (
    id SERIAL PRIMARY KEY,
    experience_id INTEGER REFERENCES people.experiences(id) ON DELETE CASCADE,
    job_level TEXT,
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
CREATE TRIGGER update_experiences_updated_at
    BEFORE UPDATE ON people.experiences
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_job_title_details_updated_at
    BEFORE UPDATE ON people.job_title_details
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_job_functions_updated_at
    BEFORE UPDATE ON people.job_functions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_job_seniority_updated_at
    BEFORE UPDATE ON people.job_seniority
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Create indexes for better query performance
CREATE INDEX idx_experiences_people_id ON people.experiences(people_id);
CREATE INDEX idx_job_title_details_experience_id ON people.job_title_details(experience_id);
CREATE INDEX idx_job_functions_experience_id ON people.job_functions(experience_id);
CREATE INDEX idx_job_seniority_experience_id ON people.job_seniority(experience_id);
