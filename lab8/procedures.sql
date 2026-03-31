-- 1. Добавление или Обновление (Upsert)
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE first_name = p_name) THEN
        UPDATE contacts SET phone = p_phone WHERE first_name = p_name;
    ELSE
        INSERT INTO contacts(first_name, phone) VALUES (p_name, p_phone);
    END IF;
END;
$$ LANGUAGE plpgsql;

-- 2. Удаление
CREATE OR REPLACE PROCEDURE delete_contact(p_value VARCHAR)
AS $$
BEGIN
    DELETE FROM contacts WHERE first_name = p_value OR phone = p_value;
END;
$$ LANGUAGE plpgsql;

-- 3. Массовая вставка с валидацией
CREATE OR REPLACE PROCEDURE insert_many_contacts(
    IN p_names TEXT[],
    IN p_phones TEXT[],
    INOUT invalid_data TEXT[] DEFAULT '{}'
)
AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(p_names, 1) LOOP
        IF p_phones[i] ~ '^[0-9]{11,15}$' THEN
            IF EXISTS (SELECT 1 FROM contacts WHERE first_name = p_names[i]) THEN
                UPDATE contacts SET phone = p_phones[i] WHERE first_name = p_names[i];
            ELSE
                INSERT INTO contacts(first_name, phone) VALUES (p_names[i], p_phones[i]);
            END IF;
        ELSE
            invalid_data := array_append(invalid_data, p_names[i] || ' - ' || p_phones[i]);
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;