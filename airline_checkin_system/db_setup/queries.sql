CREATE TABLE trips (
   trip_id SERIAL PRIMARY KEY,
   name text
);

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name text
);

CREATE TABLE seats (
   seat_id SERIAL PRIMARY KEY,
   seat CHAR(4),
   trip_id int REFERENCES trips,
   user_id int REFERENCES users
);
