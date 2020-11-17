# Audience Data Generator

A script to create dummy data for Audience Studio on Treasure Data.

You can create a database (if not exists) including the following tables:

- `users`
- `cities`
- `behavior_1`
- `behavior_2`
- `attribute_1`
- `attribute_2`

## How to use

### Set up

Prerequisites:

- Python 3.6+
- pip 19.02+

We recomment to install after creating virtual environment as the following: 

```shell script
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv)$ pip install git+https://github.com/chezou/audience_generator
```

Or, you can install with `--user` option.

```shell script
$ pip install --user git+https://github.com/chezou/audience_generator
```

### Usage

Set `TD_API_KEY` for your master API key and `TD_API_SERVER` for your API endpoint as environment variables.

```bash
$ export TD_API_KEY="1234/XXXXXXXXXX"
$ export TD_API_SERVER="api.treasuredata.com"
$ audience_generator my_db
```

You can see detailed option with `--help` option.

```shell script
Usage: audience_generator [OPTIONS] DATABASE

  Create dummy data for Audience Studio in a database.

  Target tables are: users, cities, behavior_1, and behavior_2.

  Target database will be created automatically if not exists.

Options:
  -s, --api-server TEXT    Treasure Data API Endpoint
  -n, --user-size INTEGER  Target order of generated users. Must be bewteen 11
                           to 100000000

  -o, --overwrite          Recreate target tables
  -d, --dry-run            Check query with dry run. Set -vv to show query.
  -v, --verbose
  --help                   Show this message and exit.
```

## The dummy data examples

### users table

This table consists of `time`, `td_client_id`, `email`, and `country` columns.

- `email` column can be `a`, `b`, or `c` randomly
- `country` can be `japan`, `usa`, `canada`. The ratio of them is japan:usa:canada = 2:3:1.

The example table looks like:

|time|td_client_id|email|country|
|:---|:---|:----|:---|
|1000010|8fc00148-4309-4337-8b7f-89472cf9a6e5|c|japan|
|1000009|a2a61a1a-1ba7-4195-d96c-de92bded5648|b|japan|
|1000007|2239f4b6-c5b8-40af-9838-48bedb6e08e7|a|canada|
|1000006|e69b4154-c45f-4ac3-8529-975bf93a51dc|c|usa|

### cities table

This table consists of `name`, `cn`, `fanoutn`, and `time`.

The example table looks like:

|name|cn|fanoutn|time|
|:---|:---|:---|:---|
|Abidjan1|Abidjan|1|1585294664|
|Abilene1|Abilene|1|1585294664|
|Rabat9|Rabat|9|1585294664|
|Raleigh9|Raleigh|9|1585294664|

### behavior_1 table

This table consists of `time`, `test_city_name`, and `td_client_id`.

- By using `td_client_id`, you can join with `users` table
- You can join with `cities` table with joining `behavior_1.test_city_name` and `cities.name`.

The example table looks like:

|time|test_city_name|td_client_id|
|:---|:---|:---|
|8146810|Ulaanbaatar7|3e590038-7f2b-4634-dc32-ea7fa82436cc|
|8119605|Adamstown10|3dd6aff9-0f25-49c9-ecd5-fa6b72cf0bea|
|7974002|Luxembourg6|8e25a0db-97ca-46a8-ae9c-e0b03ab54cab|

### behavoir_2 table

This table consists of `time`, `test_city_name`, `td_client_id`, and `opts`.

- `opts` can be an integer from `0` to `2`
- By using `td_client_id`, you can join with `users` table
- You can join with `cities` table with joining `behavior_2.test_city_name` and `cities.name`.

The example table looks like:

|time|test_city_name|td_client_id|opts|
|:---|:---|:---|:---|
|8376800|Beirut9|dddc1ac8-a68d-4c11-d477-2fb58908b23f|1|
|8266808|Prague5|7ad27e8e-adce-4537-ecf2-d43e4f3ed5bd|0|
|8234002|Palikir9|621c1386-5f7e-44ea-af4d-acd3020349eb|0|
|8204000|Rio Rancho4|dddc1ac8-a68d-4c11-d477-2fb58908b23f|2|

### attribute_1 table

This table consists of `time`, `td_client_id`, `country`, `td_os`, and `td_language`.

- `country` is the same field as `users` table
- `td_os` contains `Linux`, `Windows`, `macOS`, `iOS`, and `Android`. The ratio is 1:1:1:2:2.
- `td_language` contains `ja_JP`, `en_GB`, and `en_US`. The ratio is 2:1:1.

|time|country|td_client_id|td_os|td_language|
|:---|:---|:---|:---|:---|
|8376800|japan|dddc1ac8-a68d-4c11-d477-2fb58908b23f|Windows|en_US|
|8266808|canada|7ad27e8e-adce-4537-ecf2-d43e4f3ed5bd|Android|ja_JP|
|8234002|usa|621c1386-5f7e-44ea-af4d-acd3020349eb|iOS|ja_JP|
|8204000|usa|dddc1ac8-a68d-4c11-d477-2fb58908b23f|macOS|en_GB|

### attribute_2 table

This table consists of `td_client_id`, `age`, `item_count`, `ctr`, and `time`.

- `td_client_id` is nullable. The ratio is determined by `non_null_rate` option
- `age` is a random number which can be from 0 to 60
- `item_count` is a random number which can be from 0 to 5
- `ctr` is a random number from 0.0 to 1.0

|time|td_client_id|age|item_count|ctr|
|:---|:---|:---|:---|:---|
|8376800|dddc1ac8-a68d-4c11-d477-2fb58908b23f|36|1|0.994594137517313|
|8266808|7ad27e8e-adce-4537-ecf2-d43e4f3ed5bd|54|2|0.58730152122260440.5873015212226044|
|8234002|621c1386-5f7e-44ea-af4d-acd3020349eb|17|1|0.6011213596629439|
|8204000|dddc1ac8-a68d-4c11-d477-2fb58908b23f|6|2|0.7007648809644941|
