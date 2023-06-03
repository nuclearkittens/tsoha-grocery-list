CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    uom TEXT NOT NULL-- unit of measurement
    cat_id INTEGER REFERENCES categories
);

CREATE TABLE grocery_list (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users ON DELETE RESTRICT,
    created_at DATE
);

CREATE TABLE grocery_list_items (
    item_id INTEGER REFERENCES items ON DELETE RESTRICT,
    list_id INTEGER REFERENCES grocery_list ON DELETE CASCADE,
    quantity INTEGER
);