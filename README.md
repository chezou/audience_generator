# Audience Data Generator

A script to create dummy data for Audience Studio on Treasure Data.

You can create a database (if not exists) including the following tables:

- `users`
- `cities`
- `behavior_1`
- `behavior_2`

## How to use

### Set up

Prerequisites:

- Python 3.6+
- pip 19.02+

```shell script
$ pip install 
```

### Usage

Set `TD_API_KEY` for your master API key and `TD_API_SERVER` for your API endpoint as environment variables.

```bash
$ export TD_API_KEY="1234/XXXXXXXXXX"
$ epoxrt TD_API_SERVER="api.treasuredata.com"
$ audience_generator my_db
```

You can use `--overwrite` or `-o` option to drop existing tables.

```shell script
$ audience_generator my_db -o
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
