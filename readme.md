python -m app.db.db_init =dbsetup
uvicorn app.main:app --reload
INSERT INTO users (id, email, first_name, last_name, date_of_birth, password, role)
VALUES
    (
        'a0b1c2d3-e4f5-6789-0a1b-2c3d4e5f6789', -- Mock UUID
        'admin@size.ba', -- Email
        'Hamza', -- First Name
        'Starcevic', -- Last Name
        '2002-01-03', -- Date of Birth (YYYY-MM-DD)
        'adminpass', -- Password (Hashed)
        'admin' -- Role
    );
