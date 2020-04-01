import logging
import sys

import click
import pytd


USERS_SQL = """\
CREATE TABLE IF NOT EXISTS users AS
WITH seq AS (
  SELECT t2.time*10000+t1.time AS time
  FROM UNNEST(SEQUENCE(0, 10)) AS t1(time)
  CROSS JOIN UNNEST(SEQUENCE(0, 100)) AS t2(time)
)
SELECT
  LPAD(TO_BASE(RAND(4294966016),16),8,'0')||'-'||LPAD(TO_BASE(RAND(57914),16),4,'0')||'-4'||LPAD(TO_BASE(RAND(3121),16),3,'0')||'-'||LPAD(TO_BASE(RAND(28423)+32768,16),4,'0')||'-'||LPAD(TO_BASE(RAND(281474976704467),16),12,'0') AS td_client_id,
  (ARRAY ['a', 'b', 'c'])[RAND(3) + 1] AS email,
  (ARRAY ['japan', 'japan', 'usa', 'usa', 'usa', 'canada'])[RAND(6) + 1] AS country,
time
FROM seq
"""

CITIES_SQL = """\
CREATE TABLE IF NOT EXISTS cities AS
WITH fanout AS (
  SELECT n FROM UNNEST(SEQUENCE(1,10)) fanout0(n)
),
c AS (
  SELECT n FROM UNNEST(ARRAY [
'Abidjan', 'Abilene', 'Abu Dhabi', 'Abuja', 'Accra', 'Adamstown', 'Addis Ababa', 'Aden', 'Albuquerque', 'Algiers', 'Alofi', 'Amarillo', 'Amman', 'Amsterdam', 'Anaconda', 'Anchorage', 'Andorra la Vella', 'Ankara', 'Antananarivo', 'Apia', 'Arlington', 'Ashgabat', 'Asmara', 'Asunción', 'Athens', 'Atlanta', 'Augusta', 'Aurora', 'Austin', 'Avarua', 'Babbitt', 'Baghdad', 'Bakersfield', 'Baku', 'Baltimore', 'Bamako', 'Bandar Seri Begawan', 'Bangkok', 'Bangui', 'Banjul', 'Basseterre', 'Baton Rouge', 'Beaumont', 'Beijing', 'Beirut', 'Belgrade', 'Belmopan', 'Berlin', 'Bern', 'Birmingham', 'Bishkek', 'Bissau', 'Bloemfontein', 'Bogotá', 'Boise', 'Boulder City', 'Brades Estate', 'Brasília', 'Bratislava', 'Brazzaville', 'Bridgetown', 'Brownsville', 'Brussels', 'Bucharest', 'Buckeye', 'Budapest', 'Buenos Aires', 'Bunnell', 'Butte', 'Cairo', 'California City', 'Canberra', 'Cape Coral', 'Cape Town', 'Caracas', 'Caribou', 'Carson City', 'Casa Grande', 'Castries', 'Cetinje', 'Charleston', 'Charlotte', 'Charlotte Amalie', 'Chattanooga', 'Chesapeake', 'Chicago', 'Chișinău', 'Cincinnati', 'Clarksville', 'Cleveland', 'Cockburn Town', 'Colombo', 'Colorado Springs', 'Columbia', 'Columbus', 'Conakry', 'Copenhagen', 'Corpus Christi', 'Cotonou', 'Cusseta', 'Dakar', 'Dallas', 'Damascus', 'Dar es Salaam', 'Denton', 'Denver', 'Des Moines', 'Detroit', 'Dhaka', 'Dili', 'Djibouti', 'Dodoma', 'Doha', 'Dothan', 'Douglas', 'Dublin', 'Durham', 'Dushanbe', 'Edinburgh of the Seven Seas', 'Edmond', 'El Aioun', 'El Paso', 'El Reno', 'Ellsworth', 'Eloy', 'Episkopi Cantonment', 'Fayetteville', 'Fernley', 'Flying Fish Cove', 'Fort Wayne', 'Fort Worth', 'Freetown', 'Fremont', 'Fresno', 'Funafuti', 'Gaborone', 'George Town', 'Georgetown', 'Gibraltar', 'Gitega', 'Goodyear', 'Greensboro', 'Guatemala City', 'Gustavia', 'Hagåtña', 'Hamilton', 'Hanga Roa', 'Hanoi', 'Harare', 'Hargeisa', 'Hartsville', 'Havana', 'Helsinki', 'Henderson', 'Hibbing', 'Honiara', 'Houston', 'Huntsville', 'Independence', 'Indianapolis', 'Islamabad', 'Jackson', 'Jacksonville', 'Jakarta', 'Jamestown', 'Jarabulus', 'Jerusalem', 'Jonesboro', 'Juba', 'Juneau', 'Kabul', 'Kampala', 'Kansas City', 'Kathmandu', 'Khartoum', 'Kiev', 'Kigali', 'King Edward Point', 'Kingston', 'Kingstown', 'Kinshasa', 'Knoxville', 'Kuala Lumpur', 'Kutaisi', 'Kuwait City', 'La Paz', 'Lancaster', 'Laredo', 'Las Cruces', 'Las Vegas', 'Lawton', 'Lexington', 'Libreville', 'Lilongwe', 'Lima', 'Lincoln', 'Lisbon', 'Little Rock', 'Ljubljana', 'Lobamba', 'Lomé', 'London', 'Los Angeles', 'Louisville', 'Luanda', 'Lubbock', 'Lusaka', 'Luxembourg', 'Lynchburg', 'Madison', 'Madrid', 'Majuro', 'Malabo', 'Malé', 'Managua', 'Manama', 'Manila', 'Maputo', 'Marana', 'Marigot', 'Maseru', 'Mata-Utu', 'Mbabane', 'Memphis', 'Mesa', 'Mexico City', 'Milwaukee', 'Minsk', 'Mobile', 'Mogadishu', 'Monaco', 'Monrovia', 'Montevideo', 'Montgomery', 'Moroni', 'Moscow', 'Muscat', 'N''Djamena', 'Nairobi', 'Nashville', 'Nassau', 'Naypyidaw', 'New Delhi', 'New Orleans', 'New York City', 'Ngerulmud', 'Niamey', 'Nicosia', 'Nightmute', 'Norman', 'North Las Vegas', 'North Port', 'Nouakchott', 'Nouméa', 'Nukuʻalofa', 'Nur-Sultan', 'Nuuk', 'Oak Ridge', 'Oklahoma City', 'Omaha', 'Oranjestad', 'Orlando', 'Oslo', 'Ottawa', 'Ouagadougou', 'Pago Pago', 'Palestine', 'Palikir', 'Palm Coast', 'Palm Springs', 'Palmdale', 'Panama City', 'Papeete', 'Paramaribo', 'Paris', 'Peoria', 'Philadelphia', 'Philipsburg', 'Phnom Penh', 'Phoenix', 'Plymouth', 'Podgorica', 'Port Arthur', 'Port Louis', 'Port Moresby', 'Port St. Lucie', 'Port Vila', 'Port of Spain', 'Port-au-Prince', 'Portland', 'Porto-Novo', 'Prague', 'Praia', 'Presque Isle', 'Preston', 'Pretoria', 'Pristina', 'Putrajaya', 'Pyongyang', 'Quito', 'Rabat', 'Raleigh', 'Ramallah', 'Reno', 'Reykjavík', 'Riga', 'Rio Rancho', 'Riverside', 'Riyadh', 'Road Town', 'Rome', 'Roseau', 'Sacramento', 'Saipan', 'Salt Lake City', 'San Antonio', 'San Diego', 'San Jose', 'San José', 'San Juan', 'San Marino', 'San Salvador', 'Sana''a', 'Santiago', 'Santo Domingo', 'Sarajevo', 'Savannah', 'Scottsdale', 'Seattle', 'Seoul', 'Shreveport', 'Sierra Vista', 'Singapore', 'Sitka', 'Skopje', 'Sofia', 'Springfield', 'Sri Jayawardenepura Kotte', 'St. George''s', 'St. Helier', 'St. John''s', 'St. Marys', 'St. Peter Port', 'St. Pierre', 'Stanley', 'Stepanakert', 'Stockholm', 'Sucre', 'Suffolk', 'Sukhumi', 'Surprise', 'Suva', 'São Tomé', 'Taipei', 'Tallahassee', 'Tallinn', 'Tampa', 'Tarawa', 'Tashkent', 'Tbilisi', 'Tegucigalpa', 'Tehran', 'The Hague', 'The Valley', 'Thimphu', 'Tifariti', 'Tirana', 'Tiraspol', 'Tokyo', 'Toledo', 'Tripoli', 'Tskhinvali', 'Tucson', 'Tulsa', 'Tunis', 'Tórshavn', 'Ulaanbaatar', 'Unalaska', 'Vaduz', 'Valdez', 'Valletta', 'Valparaíso', 'Vatican City', 'Victoria', 'Vienna', 'Vientiane', 'Vilnius', 'Virginia Beach', 'Waco', 'Warsaw', 'Washington', 'Wellington', 'West Island', 'Wichita', 'Willemstad', 'Windhoek', 'Winston-Salem', 'Wrangell', 'Yamoussoukro', 'Yaoundé'
  ])
  c(n)
)
SELECT concat(c.n, cast(fanout.n as VARCHAR)) as name, c.n as cn, fanout.n as fanoutn
FROM c
CROSS JOIN fanout
"""

BEHAVIOR1_SQL = """\
CREATE TABLE IF NOT EXISTS behavior_1 AS
WITH fanout AS (
  SELECT n FROM UNNEST(SEQUENCE(1,5)) fanout0(n)
),
cities AS (
  SELECT array_agg(name) AS names FROM cities
)
SELECT
  cities.names[RAND(4000) + 1] AS test_city_name,
  users.td_client_id AS td_client_id,
  users.time + RAND(90) * 86400 AS time
FROM users
JOIN fanout ON RAND() < 0.8
JOIN cities ON true
"""

BEHAVIOR2_SQL = """\
CREATE TABLE IF NOT EXISTS behavior_2 AS
WITH fanout AS (
  SELECT n FROM UNNEST(SEQUENCE(1,5)) fanout0(n)
),
cities AS (
  SELECT array_agg(name) AS names FROM cities
)
SELECT
  cities.names[RAND(4000) + 1] AS test_city_name,
  users.td_client_id AS td_client_id,
  users.time + RAND(90) * 86400 AS time,
  RAND(3) AS opts
FROM users
JOIN fanout ON RAND() < 0.8
JOIN cities ON true
"""

TARGET_TABLES = ["users", "cities", "behavior_1", "behavior_2"]


@click.command()
@click.argument("database")
@click.option("-o", "--overwrite", is_flag=True, help="Recreate target tables")
def create_dummy_data(database, overwrite):
    """Create dummy data for Audience Studio in a database.

    Target tables are: users, cities, behavior_1, and behavior_2.

    Target database will be created automatically if not exists.
    """
    client = pytd.Client(database=database)
    client.create_database_if_not_exists(database)

    if overwrite:
        for table in TARGET_TABLES:
            if client.exists(database, table):
                client.api_client.delete_table(database, table)

    logging.info(f"Creating users table")
    client.query(USERS_SQL)
    logging.info(f"Creating cities table")
    client.query(CITIES_SQL)
    logging.info(f"Creating behavior1 table")
    client.query(BEHAVIOR1_SQL)
    logging.info(f"Creating behavior2 table")
    client.query(BEHAVIOR2_SQL)

    succeeded = True
    for table in TARGET_TABLES:
        if not client.exists(database, table):
            succeeded = False
            logging.error(f"{database}.{table} doesn't exist")

    if not succeeded:
        sys.exit(1)


if __name__ == "__main__":
    create_dummy_data()