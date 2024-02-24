# Database Reference

## Tables

### `stock_info`
General information about stocks. For price, check `stock_price`.
| Column Name | Type | Description |
| ----------- | ---- | ----------- |

### `profiles`
Information about user profiles. Does not contain auth information.
| Column Name | Type | Description |
| ----------- | ---- | ----------- |

### `stock_price`
General information about stocks. For price, check `stock_price`.
| Column Name | Type | Description   |
| ----------- | ---- | ------------- |
| stockId     | int8 | stock_info.id |
| stock_price | int8 |               |

### `contributors`
Data about contributors
| Column Name | Type | Description |
| ----------- | ---- | ----------- |

### `flags`
User flags such as achievements or badges.
| Column Name | Type | Description |
| ----------- | ---- | ----------- |

### `market_State`
Historical information on whether or not the market is open
| Column Name | Type | Description |
| ----------- | ---- | ----------- |

### `portfolio`
All the stocks that users own.
| Column Name | Type | Description |
| ----------- | ---- | ----------- |

### `rel_user_flags`
Which users have what flags.
| Column Name | Type | Description |
| ----------- | ---- | ----------- |

### `active_buy_sell`
Where the currently tradable orders are.
| Column Name | Type      | Description              |
| ----------- | --------- | ------------------------ |
| id          | int8      |                          |
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
| Column Name | Type | Description |
| ----------- | ---- | ----------- |

<!-- TODO: History tables -->

## Table Setup SQL
<details>
    <summary>Click me</summary>
    <!-- TODO -->
</details>