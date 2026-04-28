# -*- coding: utf-8 -*-
"""
app/db/queries.py

All the psql queries for database transactions.
"""

# Built-in module imports
from typing import Any, Dict, List, Optional
import re

# 3rd party module imports
from psycopg2.extensions import connection

########################### SQL STRINGS FOR SELECTS ###########################
GET_COUNTRIES = """
SELECT id, name
FROM countries
WHERE countries.name = %s;
"""

GET_OWNERS = """
SELECT
    o.id,
    o.name,
    o.country_id
FROM owners o
JOIN countries c
    ON o.country_id = c.id
WHERE owners.name = %s;
"""

GET_BUILDERS = """
SELECT
    b.name,
    b.country_id,
    b.founded,
    b.shutdown
FROM builders b
JOIN countries c
    ON b.country_id = c.id
WHERE builders.name = %s;
"""

GET_SHIP_STATUSES = """
SELECT id, status
FROM ship_statuses
WHERE ship_statuses.name = %s;
"""

GET_SHIP_TYPES = """
SELECT id, ship_type
FROM ship_types
WHERE countries.name = %s;
"""

GET_SHIP_CLASSES = """
SELECT id, ship_class
FROM ship_classes
WHERE ship_classes.name = %s;
"""

GET_ENGINE_TYPE = """
SELECT id, engine_type
FROM engine_types
WHERE engine_types.name = %s;
"""

GET_SHIPS = """
SELECT s.id, s.name, s.imo,
    s.date_built, s.builder_id, s.owner_id,
    s.ship_type_id, s.ship_class_id,
    s.date_comissioned, s.ship_status_id,
    s.date_decomissioned, s.date_scrapped_or_sunk,
    s.length_m, s.beam_m, s.draft_m,
    s.gross_tonnage, s.displacement_full_t, s.displacement_std_t,
    s.engine_type_id, s.no_engines, s.no_screws, s.engine_shp,
    s.speed, s.crew
FROM ships s
JOIN builders b
    ON s.builder_id = b.id
JOIN owners o
    ON s.owner_id = o.id
JOIN ship_types t
    ON s.ship_type_id = t.id
JOIN ship_classes c
    ON s.ship_class_id = c.id
JOIN ship_statuses st
    ON s.ship_status_id = st.id
JOIN engine_types e
    ON s.engine_type_id = e.id
WHERE ships.name = %s;
"""

########################### SQL STRINGS FOR INSERTS ###########################
INSERT_COUNTRY = """
INSERT INTO countries (name)
VALUES (%s)
RETURNING id;
"""

INSERT_BUILDER = """
INSERT INTO builders (name, country_id)
VALUES (%s, %s)
RETURNING id;
"""

INSERT_OWNER = """
INSERT INTO owners (name, country_id)
VALUES (%s, %s)
RETURNING id;
"""

INSERT_SHIP_STATUS = """
INSERT INTO ship_statuses (ship_status)
VALUES (%s)
RETURNING id;
"""

INSERT_SHIP_TYPE = """
INSERT INTO ship_types (ship_type)
VALUES (%s)
RETURNING id;
"""

INSERT_SHIP_CLASS = """
INSERT INTO ship_classes (ship_class)
VALUES (%s)
RETURNING id;
"""

INSERT_ENGINE_TYPE = """
INSERT INTO engine_types (engine_type)
VALUES (%s)
RETURNING id;
"""

INSERT_SHIP = """
INSERT INTO ships
(name, imo, date_built, builder_id, owner_id, ship_type_id, ship_class_id,
date_comissioned, ship_status_id, date_decomissioned, date_scrapped_or_sunk,
length_m, beam_m, draft_m, gross_tonnage, displacement_full_t,
displacement_std_t, engine_type_id, no_engines, no_screws, engine_shp, speed,
crew)
VALUES (%s, %s, %s, %s, %s, %s, %s,
%s, %s, %s, %s,
%s, %s, %s, %s, %s,
%s, %s, %s, %s, %s, %s,
%s)
RETURNING id;
"""

############################## SELECT OPERATIONS ##############################
def get_country(conn: connection, name: str = None) -> Optional[Dict[str, Any]]:
    """
    Fetches countries by name.

    Args:
        conn (connection): Handle for psql database connection.
        name (str): Name of the country to fetch.

    Returns:
        Optional[Dict[str, Any]]: Dict object from RealDictCursor containing
            record whose name matches name. None if no match is found.
    """
    # Format name string
    if name is None:
        name = "*"
    else:
        name = re.sub(r"\s+", "_", name.lower())
    with conn.cursor() as cur:
        cur.execute(GET_COUNTRIES, (name,))
        return cur.fetchall()

def get_builder(conn: connection, name: str = None) -> Optional[Dict[str, Any]]:
    """
    Fetches builders by name.

    Args:
        conn (connection): Handle for psql database connection.
        name (str): Name of the builder to fetch.

    Returns:
        Optional[Dict[str, Any]]: Dict object from RealDictCursor containing
            record whose name matches name. None if no match is found.
    """
    # Format name string
    if name is None:
        name = "*"
    else:
        name = re.sub(r"\s+", "_", name.lower())
    with conn.cursor() as cur:
        cur.execute(GET_BUILDERS, (name,))
        return cur.fetchall()

def get_owner(conn: connection, name: str = None) -> Optional[Dict[str, Any]]:
    """
    Fetches owners by name.

    Args:
        conn (connection): Handle for psql database connection.
        name (str): Name of the onwer to fetch.

    Returns:
        Optional[Dict[str, Any]]: Dict object from RealDictCursor containing
            record whose name matches name. None if no match is found.
    """
    # Format name string
    if name is None:
        name = "*"
    else:
        name = re.sub(r"\s+", "_", name.lower())
    with conn.cursor() as cur:
        cur.execute(GET_OWNERS, (name,))
        return cur.fetchall()

# EOF
