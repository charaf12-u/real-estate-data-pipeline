CREATE TABLE IF NOT EXISTS ml_schema.dataset_ml (
    id SERIAL PRIMARY KEY,

    url TEXT,

    price DOUBLE PRECISION,
    surface DOUBLE PRECISION,
    bedrooms INT,
    bathrooms INT,
    floor INT,

    city TEXT,
    district TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,

    price_per_m2 DOUBLE PRECISION,
    size_category TEXT,
    price_category TEXT,
    luxury_flag INT,
    rooms_density DOUBLE PRECISION,
    bathrooms_per_room DOUBLE PRECISION,

    CONSTRAINT unique_ml UNIQUE (url)
);