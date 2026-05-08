

--> Dim_Localisation
CREATE TABLE IF NOT EXISTS bi_schema.dim_localisation (
    id SERIAL PRIMARY KEY,
    city TEXT,
    district TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    geo_level TEXT,

    CONSTRAINT unique_location UNIQUE (city, district)
);


--> Dim_Caracteristiques
CREATE TABLE IF NOT EXISTS bi_schema.dim_caracteristiques (
    id SERIAL PRIMARY KEY,
    bedrooms INT,
    bathrooms INT,
    floor INT,
    size_category TEXT,

    CONSTRAINT unique_carac UNIQUE (bedrooms, bathrooms, floor, size_category)
);


--> Dim_Temps
CREATE TABLE IF NOT EXISTS bi_schema.dim_temps (
    id SERIAL PRIMARY KEY,
    scraped_at TIMESTAMP,
    published_time TIMESTAMP,
    year INT,
    month INT,
    day INT,

    CONSTRAINT unique_time UNIQUE (scraped_at, published_time)
);