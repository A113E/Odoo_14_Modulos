# Puntos importantes

# Cuando se instala el modulo:

# Odoo a partir del modelo crea un Tabla en la BD

CREATE TABLE project_project (
/_ Campos automaticos
id INTEGER PRIMARY KEY,
name VARCHAR NOT NULL,
customer_id INTEGER REFERENCES res_partner(id),
start_date DATE,
end_date DATE,
state VARCHAR,
is_late BOOLEAN, -- Este se recalcula, no siempre es consistente
/_ Campso automaticos
create_date TIMESTAMP,
create_uid INTEGER REFERENCES res_users(id),
write_date TIMESTAMP,
write_uid INTEGER REFERENCES res_users(id)
);
