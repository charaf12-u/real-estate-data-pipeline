--> fact table

CREATE TABLE IF NOT EXISTS bi_schema.fact_annonce (
    id SERIAL PRIMARY KEY,
    url TEXT,
    price DOUBLE PRECISION,
    surface DOUBLE PRECISION,
    price_per_m2 DOUBLE PRECISION,
    price_category TEXT,
    luxury_flag INT,
    rooms_density DOUBLE PRECISION,
    bathrooms_per_room DOUBLE PRECISION,
    localisation_id INT,
    caracteristiques_id INT,
    temps_id INT,

    CONSTRAINT unique_url UNIQUE (url),

    CONSTRAINT fk_localisation
        FOREIGN KEY (localisation_id)
        REFERENCES bi_schema.dim_localisation(id),

    CONSTRAINT fk_caracteristiques
        FOREIGN KEY (caracteristiques_id)
        REFERENCES bi_schema.dim_caracteristiques(id),

    CONSTRAINT fk_temps
        FOREIGN KEY (temps_id)
        REFERENCES bi_schema.dim_temps(id)
);