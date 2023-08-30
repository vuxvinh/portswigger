# Blind_SQL_injection

- `Blind SQL injection` là một phần của SQL injection, tuy nhiên các phản hồi HTTP của nó không chứa kết quả của truy vấn SQL hoặc không hiển thị bất cứ lỗi nào của cơ sở dữ liệu.

## Khai thác Blind SQL injection bằng phương pháp kích hoạt các phản hồi có điều kiện

- Thông thường đối với một trang web sẽ sử dụng `Cookie` để quản lý người dùng. Nếu một Cookie của một người sử dụng cũ sẽ được trang web trả về kết quả `Welcome back`.
- Ta có thể dựa vào điều này để tấn công `Blind SQL`.
- Đầu tiên Mình thử kiểm tra xem trang web có trả về kết quả nếu truy vấn sai hay không.

```sql
' AND 1=1 -- 
' AND 1=2 --
```

- Với truy vấn đầu tiên ta thấy nó đã trả về kết quả `Welcome back` suy ra ta có thể khai thác được. Query có dạng:

```sql
SELECT TrackingId FROM TrackedUsers WHERE TrackingId = 'u5YD3PapBcR4lN3e7Tj4'
```

- Mình sẽ sử dụng hàm `SUBSTRING` để kiểm tra từng kí tự ở từng vị trí xem nó có đúng không, nếu kí tự đó thỏa mãn thì nó sẽ trả về kết quả là `Welcome back`.

```sql
xyz' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) > 'm
```

- Ở đây sau khi tìm được độ dài của flag bằng 20 mình đã brute force các request tạo ra length đúng của từng vị trí password rồi ghép lại.

![](pic1.png)

- Mình sẽ sử dụng 2 paypoad ứng với 2 vị trí, kiểu brute force là Cluster Bomb.

![](pic2.png)

