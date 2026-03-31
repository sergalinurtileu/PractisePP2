-- 1. Поиск по паттерну
CREATE OR REPLACE FUNCTION search_contacts(pattern TEXT)
RETURNS TABLE(f_name VARCHAR, f_phone VARCHAR)
AS $$
BEGIN
    RETURN QUERY
    SELECT p.first_name, p.phone
    FROM contacts p
    WHERE p.first_name ILIKE '%' || pattern || '%'
       OR p.phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

-- 2. Пагинация
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(f_name VARCHAR, f_phone VARCHAR)
AS $$
BEGIN
    RETURN QUERY
    SELECT p.first_name, p.phone
    FROM contacts p
    ORDER BY p.first_name
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;