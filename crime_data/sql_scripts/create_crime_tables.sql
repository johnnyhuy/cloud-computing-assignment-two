DROP TABLE crime_data.crimes_vic_by_council;
DROP TABLE crime_data.crimes_vic;
DROP TABLE crime_data.offence_subgroup;
DROP TABLE crime_data.offence_subdivision;
DROP TABLE crime_data.offence_subdivision;
DROP TABLE crime_data.offence_division;
DROP TABLE crime_data.suburbs;
DROP TABLE crime_data.councils;

CREATE TABLE crime_data.councils
(
    name             VARCHAR(45)  NOT NULL,
    seat             VARCHAR(45)  NULL,
    region           VARCHAR(45)  NOT NULL,
    year_established INT          NULL,
    land_area        INT          NOT NULL,
    population_2016  INT          NOT NULL,
    councillors      INT          NULL,
    notes            VARCHAR(255) NULL,
    PRIMARY KEY (name)
);


CREATE TABLE crime_data.suburbs
(
    name         VARCHAR(45) NOT NULL,
    postcode     VARCHAR(4)  NOT NULL,
    council_name VARCHAR(45) NOT NULL,
    PRIMARY KEY (name),
    FOREIGN KEY (council_name)
        REFERENCES crime_data.councils (name)
);

CREATE TABLE crime_data.offence_division
(
    code        VARCHAR(1)  NOT NULL,
    description VARCHAR(45) NULL,
    PRIMARY KEY (code)
);

CREATE TABLE crime_data.offence_subdivision
(
    offence_division_code VARCHAR(1)   NOT NULL,
    code                  INT          NOT NULL,
    description           VARCHAR(255) NULL,
    PRIMARY KEY (offence_division_code, code),
    FOREIGN KEY (offence_division_code)
        REFERENCES crime_data.offence_division (code)
);

CREATE TABLE crime_data.offence_subgroup
(
    offence_division_code    VARCHAR(1)   NOT NULL,
    offence_subdivision_code INT          NOT NULL,
    code                     INT          NOT NULL,
    description              VARCHAR(255) NULL,
    PRIMARY KEY (offence_division_code, offence_subdivision_code, code),
    FOREIGN KEY (offence_division_code, offence_subdivision_code)
        REFERENCES crime_data.offence_subdivision (offence_division_code, code)
);

CREATE TABLE crime_data.crimes_vic
(
    year_ending              INT         NOT NULL,
    postcode                 VARCHAR(4)  NOT NULL,
    suburb_name              VARCHAR(45) NOT NULL,
    offence_division_code    VARCHAR(1)  NOT NULL,
    offence_subdivision_code INT         NOT NULL,
    offence_subgroup         INT         NOT NULL,
    incidents_recorded       INT         NOT NULL,
    PRIMARY KEY (year_ending, postcode, suburb_name, offence_division_code, offence_subdivision_code, offence_subgroup),
    FOREIGN KEY (offence_division_code, offence_subdivision_code, offence_subgroup)
        REFERENCES crime_data.offence_subgroup (offence_division_code, offence_subdivision_code, code),
    FOREIGN KEY (suburb_name)
        REFERENCES crime_data.suburbs (name)
);

CREATE TABLE crime_data.crimes_vic_by_council
(
    year_ending                    INT           NOT NULL,
    police_service_area            VARCHAR(45)   NOT NULL,
    council_name                   VARCHAR(45)   NOT NULL,
    offence_division_code          VARCHAR(1)    NOT NULL,
    offence_subdivision_code       INT           NOT NULL,
    offence_subgroup               INT           NOT NULL,
    incidents_recorded             INT           NOT NULL,
    psa_rate_per_100000_population DECIMAL(6, 1) NOT NULL,
    lga_rate_per_100000_population DECIMAL(6, 1) NOT NULL,
    PRIMARY KEY (year_ending, council_name, offence_division_code, offence_subdivision_code, offence_subgroup),
    FOREIGN KEY (offence_division_code, offence_subdivision_code, offence_subgroup)
        REFERENCES crime_data.offence_subgroup (offence_division_code, offence_subdivision_code, code),
    FOREIGN KEY (council_name)
        REFERENCES crime_data.councils (name)
);
