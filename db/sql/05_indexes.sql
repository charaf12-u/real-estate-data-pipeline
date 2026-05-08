--> location ( city , district )
CREATE INDEX IF NOT EXISTS idx_ml_city
ON ml_schema.dataset_ml(city);

CREATE INDEX IF NOT EXISTS idx_ml_district
ON ml_schema.dataset_ml(district);


--> price 
CREATE INDEX IF NOT EXISTS idx_ml_price
ON ml_schema.dataset_ml(price);


--> important numeric features
CREATE INDEX IF NOT EXISTS idx_ml_surface
ON ml_schema.dataset_ml(surface);

CREATE INDEX IF NOT EXISTS idx_ml_price_m2
ON ml_schema.dataset_ml(price_per_m2);

CREATE INDEX IF NOT EXISTS idx_ml_city_price
ON ml_schema.dataset_ml(city, price);