-- PROCEDURE: add_phone
-- Adds a new phone record for a specific contact identified by their first name.
-- If multiple contacts have the same name, it targets the first one found (LIMIT 1).
CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
AS $$
BEGIN
    INSERT INTO phones (contact_id, phone, type)
    VALUES ((SELECT id FROM contacts WHERE first_name = p_contact_name LIMIT 1), p_phone, p_type);
END;
$$ LANGUAGE plpgsql;

-- PROCEDURE: move_to_group
-- Assigns a contact to a group. If the group does not exist, it is created automatically.
-- Uses ON CONFLICT to prevent duplicate group names.
CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR)
AS $$
DECLARE v_group_id INT;
BEGIN
    -- Ensure the group exists
    INSERT INTO groups (name) VALUES (p_group_name) ON CONFLICT (name) DO NOTHING;
    
    -- Retrieve the ID of the group
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
    
    -- Update the contact record
    UPDATE contacts SET group_id = v_group_id WHERE first_name = p_contact_name;
END;
$$ LANGUAGE plpgsql;

-- FUNCTION: search_contacts
-- Performs a case-insensitive search across names, emails, and phone numbers.
-- Returns a table with aggregated phone numbers for a clean console display.
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