# Examining the database in SQL injection attacks

---

## Xem loại và phiên bản của DB

| Database type | Query |
|---|---|
| Microsoft, MySQL | SELECT @@version |
| Oracle | SELECT * FROM v$version |
| PostgreSQL | SELECT version() |

## Liệt kê nội dung của các table trong DB

- Hầu hết các loại DB (ngoại trừ Oracle) đều có thể xem xét thông tin của tất cả các bảng trong cơ sở dữ liệu: `SELECT * FROM information_schema.tables`.

Thông thường nó sẽ trả về: 

| TABLE_CATALOG | TABLE_SCHEMA | TABLE_NAME | TABLE_TYPE|
|---------------|--------------|------------|-----------|
| MyDatabase    | dbo          | Products   | BASE TABLE   |
| MyDatabase    | dbo          | Users      | BASE TABLE   |
| MyDatabase    | dbo          | Feedback   | BASE TABLE   |

Ở đây thông báo có 3 bảng mang tên `Products`,`Users` và `Feedback`.

Ta có thể liệt kê tất cả các cột có trong bảng `Users`:
```sql
SELECT * FROM information_schema.columns WHERE table_name='Users' 
```

Kết quả có dạng:

| TABLE_CATALOG | TABLE_SCHEMA | TABLE_NAME | COLUMN_NAME | DATA_TYPE   |
|---------------|--------------|------------|-------------|---------|
| MyDatabase    | dbo          | Users      | UserId      | int         |
| MyDatabase    | dbo          | Users      | Username    | varchar     |
| MyDatabase    | dbo          |Users       | Password    | varchar     |

## Trường hợp riêng Oracle

- List all table:
```sql
SELECT * FROM all_tables
```
- List column:
```sql
SELECT * FROM all_tab_columns WHERE table_name = 'USERS'
```

