CREATE TABLE services
(
    id SERIAL,
    description TEXT,
    geom geometry,
    lat float,
    lng float,
    PRIMARY KEY (id)
);
