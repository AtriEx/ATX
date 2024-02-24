# Database Reference

We host our database using [supabase](https://supabase.com/). Here is documentation for all the tables and an sql command to quickly setup your own supabase instance.

## Tables

### `stock_info`
General information about stocks. For price, check `stock_price`.
| Column Name  | Type | Description |
| ------------ | ---- | ----------- |
| id           | int8 | Primary key |
| name         | text |             |
| image        | text |             |
| total_shares | int8 |             |

### `profiles`
Information about user profiles. Does not contain auth information.
| Column Name | Type       | Description             |
| ----------- | ---------- | ----------------------- |
| userId      | int8       | Primary key             |
| joined_at   | timestampz |                         |
| username    | text       |                         |
| balance     | int8       |                         |
| networth    | int8       |                         |
| comments    | text[]     | Comments about the user |


### `stock_price`
General information about stocks. For price, check `stock_price`.
| Column Name | Type | Description   |
| ----------- | ---- | ------------- |
| stockId     | int8 | stock_info.id |
| stock_price | int8 |               |

### `contributors`
Data about contributors.
| Column Name | Type | Description                              |
| ----------- | ---- | ---------------------------------------- |
| id          | int8 | Primary key                              |
| name        | text |                                          |
| description | text | Description for the "meet the team" page |
| image       | text |                                          |
| role        | text | Role for the "meet the team" page        |

### `flags`
User flags such as achievements or badges.
| Column Name | Type | Description |
| ----------- | ---- | ----------- |
| id          | int8 | Primary key |
| name        | text |             |
| description | text |             |
| image       | text |             |
| type        | text |             |

### `market_State`
Historical information on whether or not the market is open.
| Column Name  | Type       | Description   |
| ------------ | ---------- | ------------- |
| id           | int8       | Primary key   |
| changed_last | timestampz |               |
| state        | bool       | true = active |


### `portfolio`
All the stocks that users own.
| Column Name | Type   | Description                  |
| ----------- | ------ | ---------------------------- |
| stockId     | int8   | Primary key. stock_info.id   |
| userId      | uuid   | Primary key. profiles.userId |
| quantity    | int8   |                              |
| price_avg   | float8 |                              |

### `rel_user_flags`
Which users have what flags.
| Column Name | Type | Description               |
| ----------- | ---- | ------------------------- |
| flagId      | int8 | Primary key. flags.id     |
| userid      | uuid | Primary key. users.userId |

### `active_buy_sell`
Where the currently tradable orders are.
| Column Name | Type      | Description              |
| ----------- | --------- | ------------------------ |
| id          | int8      | Primary key              |
| time_posted | timestamp |                          |
| buy_or_sell | bool      | true = buy, false = sell |
| price       | int8      | Price of the order       |
| expirey     | timestamp |                          |
| quantity    | int8      |                          |
| stockId     | int8      | stock_info.id            |
| userId      | int8      | profiles.userId          |
| Id          | int8      |                          |
| orderid     | uuid      |                          |

### `inactive_buy_sell`
Where expired and fulfilled orders go.
| Column Name   | Type      | Description              |
| ------------- | --------- | ------------------------ |
| id            | int8      | Primary key              |
| delisted_time | timestamp |                          |
| userId        | int8      | profiles.userId          |
| buy_or_sell   | bool      | true = buy, false = sell |
| time_posted   | timestamp |                          |
| price         | int8      |                          |
| expirey       | timestamp |                          |
| quantity      | int8      |                          |
| completed     | bool      | false = expired          |
| stockId       | int8      | stock_info.id            |
| orderId       | uuid      |                          |

### `stock_price_history_daily`
Historical stock prices, new row on change to stock price.
| Column Name | Type       | Description   |
| ----------- | ---------- | ------------- |
| id          | int8       | Primary key   |
| changed_at  | timestampz |               |
| price       | int8       |               |
| stockId     | int8       | stock_info.id |


### `stock_price_history_weekly`
Hourly stock price - only kept for 7 days and then cut off.
| Column Name     | Type      | Description   |
| --------------- | --------- | ------------- |
| id              | int8      | Primary key   |
| starting_hour   | timestamp |               |
| stockId         | int8      | stock_info.id |
| average_price   | float8    |               |
| highest_price   | int8      |               |
| lowest_price    | int8      |               |
| opening_price   | int8      |               |
| closing_price   |           |               |
| volume_of_sales | int8      |               |

### `stock_price_history_monthly`
Stores data over 1 day blocks.
| Column Name     | Type      | Description   |
| --------------- | --------- | ------------- |
| id              | int8      | Primary key   |
| starting_hour   | timestamp |               |
| stockId         | int8      | stock_info.id |
| average_price   | float8    |               |
| highest_price   | int8      |               |
| lowest_price    | int8      |               |
| opening_price   | int8      |               |
| closing_price   |           |               |
| volume_of_sales | int8      |               |

## Table Setup SQL
<details>
    <summary>Click me</summary>
    <!-- TODO -->
</details>