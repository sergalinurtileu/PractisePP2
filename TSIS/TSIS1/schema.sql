-- 1. Создание таблиц
CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    birthday DATE,
    group_id INTEGER REFERENCES groups(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS phones (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
    phone VARCHAR(20) NOT NULL,
    type VARCHAR(20) -- Здесь можно добавить CHECK (type IN ('mobile', 'work', 'home'))
);

-- 2. Твои процедуры (добавь те, что мы писали)
CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
AS $$
BEGIN
    INSERT INTO phones (contact_id, phone, type)
    VALUES ((SELECT id FROM contacts WHERE first_name = p_contact_name LIMIT 1), p_phone, p_type);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR)
AS $$
DECLARE v_group_id INT;
BEGIN
    INSERT INTO groups (name) VALUES (p_group_name) ON CONFLICT (name) DO NOTHING;
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
    UPDATE contacts SET group_id = v_group_id WHERE first_name = p_contact_name;
END;
$$ LANGUAGE plpgsql;

-- 3. Твои функции
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(name VARCHAR, email VARCHAR, group_n VARCHAR, phones TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT c.first_name, c.email, g.name, STRING_AGG(p.phone || ' (' || p.type || ')', ', ')
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.first_name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%'
    GROUP BY c.id, g.name;
END;
$$ LANGUAGE plpgsql;

-- Функция для пагинации (которую использует твой Python код)
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(name VARCHAR, email VARCHAR, bday DATE) AS $$
BEGIN
    RETURN QUERY
    SELECT first_name, email, birthday
    FROM contacts
    ORDER BY first_name
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;