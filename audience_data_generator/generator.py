import logging
import os
import sys

import click
import pytd


USERS_SQL = """\
CREATE TABLE IF NOT EXISTS users AS
WITH seq AS (
  SELECT 1400000000 + t2.time*{adjustment_coef}+t1.time AS time
  FROM UNNEST(SEQUENCE(0, {sequence_end_from})) AS t1(time)
  CROSS JOIN UNNEST(SEQUENCE(0, {sequence_end})) AS t2(time)
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

ATTRIBUTE1_SQL = """\
CREATE TABLE IF NOT EXISTS attribute_1 AS
SELECT
  users.td_client_id AS td_client_id
  , (ARRAY ['japan', 'japan', 'usa', 'usa', 'usa', 'canada'])[RAND(6) + 1] AS country
  , (ARRAY ['Linux', 'Windows', 'iOS', 'iOS', 'macOS', 'Android', 'Android'])[RAND(7) + 1] AS td_os
  , (ARRAY ['ja_JP', 'en_GB', 'en_US', 'ja_JP'])[RAND(4) + 1] AS td_language
  , users.time + RAND(90) * 86400 AS time
FROM users
"""

# This attribute has NULL id key
ATTRIBUTE2_SQL = """\
CREATE TABLE IF NOT EXISTS attribute_2 AS
SELECT
  IF(RAND() < {non_null_rate}, users.td_client_id, NULL) as td_client_id
  , RANDOM(60) AS age
  , RANDOM(5) AS item_count
  , RANDOM() AS ctr
  , users.time + RAND(90) * 86400 AS time
FROM users
"""


class AudienceGenerator:
    TARGET_TABLES = [
        "users",
        "cities",
        "behavior_1",
        "behavior_2",
        "attribute_1",
        "attribute_2",
    ]
    MAX_ADJUSTMENT_COEF = 100_000_000

    def __init__(
        self,
        api_key,
        api_server,
        database,
        user_size,
        non_null_rate,
        verbose,
        overwrite,
        dry_run,
    ):
        self.client = pytd.Client(
            apikey=api_key, endpoint=api_server, database=database
        )
        self.database = database
        self.overwrite = overwrite
        self.dry_run = dry_run

        if user_size < 100 or user_size > self.MAX_ADJUSTMENT_COEF:
            raise ValueError(f"user_size should be between 100 to 100000000")

        self.user_size = user_size
        self.non_null_rate = non_null_rate

        if verbose > 2:
            verbose = 2
        levels = {0: logging.WARN, 1: logging.INFO, 2: logging.DEBUG}

        self.logger = logging.getLogger(__name__)
        ch = logging.StreamHandler()
        self.logger.setLevel(levels[verbose])
        ch.setLevel(levels[verbose])
        self.logger.addHandler(ch)

    def create_table_with_query(self, table, query):
        self.logger.debug(f"Execute query:\n{query}")

        if self.client.exists(self.database, table):
            self.logger.warning(f"Table {self.database}.{table} exists. Skip creating")
        elif not self.dry_run:
            self.logger.info(f"Creating `{self.database}.{table}` table")
            self.client.query(query)

    def run(self):
        if self.dry_run:
            self.logger.info("Running with dry-run mode")
        else:
            self.client.create_database_if_not_exists(self.database)

            if self.overwrite:
                for table in self.TARGET_TABLES:
                    if self.client.exists(self.database, table):
                        self.client.api_client.delete_table(self.database, table)

        if self.user_size > 100_000:
            sequence_end_from = int(self.user_size / 10_000) - 1
            sequence_end = 10_000
        else:
            sequence_end_from = 9
            sequence_end = int(self.user_size / 10)

        adjustment_coef = int(self.MAX_ADJUSTMENT_COEF / sequence_end)
        sequence_end = sequence_end - 1

        formatted_sql = USERS_SQL.format(
            adjustment_coef=adjustment_coef,
            sequence_end=sequence_end,
            sequence_end_from=sequence_end_from,
        )
        self.create_table_with_query("users", formatted_sql)
        self.create_table_with_query("cities", CITIES_SQL)
        self.create_table_with_query("behavior_1", BEHAVIOR1_SQL)
        self.create_table_with_query("behavior_2", BEHAVIOR2_SQL)
        self.create_table_with_query("attribute_1", ATTRIBUTE1_SQL)
        self.create_table_with_query(
            "attribute_2", ATTRIBUTE2_SQL.format(non_null_rate=self.non_null_rate)
        )

        # Check if target tables are created
        succeeded = True
        for table in self.TARGET_TABLES:
            if not self.client.exists(self.database, table):
                succeeded = False
                self.logger.error(f"{self.database}.{table} doesn't exist")

        if succeeded:
            self.logger.info("Generated tables")
        else:
            self.logger.error("Failed to generate tables")

        return succeeded


@click.command()
@click.argument("database")
@click.option(
    "-s",
    "--api-server",
    envvar="TD_API_SERVER",
    default="https://api.treasuredata.com",
    help="Treasure Data API Endpoint",
)
@click.option(
    "-n",
    "--user-size",
    default=1000,
    help="Target order of generated users. Must be between 100 to 100000000",
)
@click.option(
    "-r",
    "--non-null-rate",
    default=0.001,
    help="Non null rate for td_client_id in attribute_2 table",
)
@click.option("-o", "--overwrite", is_flag=True, help="Recreate target tables")
@click.option(
    "-d",
    "--dry-run",
    is_flag=True,
    help="Check query with dry run. Set -vv to show query.",
)
@click.option("-v", "--verbose", count=True)
def create_dummy_data(
    database, api_server, user_size, non_null_rate, overwrite, dry_run, verbose
):
    """Create dummy data for Audience Studio in a database.

    Target tables are users, cities, behavior_1, and behavior_2, attribute_1,
    and attribute_2.

    Target database will be created automatically if not exists.
    """

    generator = AudienceGenerator(
        api_key=os.environ["TD_API_KEY"],
        api_server=api_server,
        database=database,
        user_size=user_size,
        non_null_rate=non_null_rate,
        overwrite=overwrite,
        dry_run=dry_run,
        verbose=verbose,
    )
    succeeded = generator.run()
    if not succeeded:
        sys.exit(1)


if __name__ == "__main__":
    create_dummy_data()
