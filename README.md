# Java Test Runner Tool

🚀 **Công cụ tự động kiểm tra và chấm điểm chương trình Java**

Tool Python để tự động biên dịch, chạy và kiểm tra các test cases cho chương trình Java của bạn.

## 📋 Mục lục

- [Tính năng](#tính-năng)
- [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
- [Cài đặt](#cài-đặt)
- [Cấu trúc thư mục](#cấu-trúc-thư-mục)
- [Cách sử dụng](#cách-sử-dụng)
- [Định dạng Test Case](#định-dạng-test-case)
- [Ví dụ](#ví-dụ)
- [Troubleshooting](#troubleshooting)

## ✨ Tính năng

- ✅ **Tự động biên dịch** tất cả file `.java` trong thư mục source
- ✅ **Chạy test cases** tự động với input được định nghĩa trước
- ✅ **So sánh kết quả** linh hoạt với các tùy chọn:
  - `REMOVE_SPACES`: Bỏ qua khoảng trắng khi so sánh
  - `CASE_SENSITIVE`: So sánh có phân biệt hoa thường
- ✅ **Tính điểm tự động** cho từng test case
- ✅ **Báo cáo chi tiết** với tổng kết điểm số
- ✅ **Lọc output** - Chỉ lấy phần sau chữ "OUTPUT:" để so sánh
- ✅ **Hỗ trợ timeout** - Tránh chương trình chạy vô hạn

## 🔧 Yêu cầu hệ thống

- **Python**: 3.6 trở lên
- **Java JDK**: 8 trở lên (có `javac` và `java` trong PATH)
- **Hệ điều hành**: Windows, Linux, hoặc macOS

### Kiểm tra Java

Mở terminal/command prompt và chạy:

```bash
java -version
javac -version
```

Nếu hiển thị version thì đã cài đặt thành công.

## 📦 Cài đặt

1. **Tải file `test_runner.py`** về máy

2. **Không cần cài đặt thêm package** - Tool chỉ sử dụng thư viện chuẩn của Python

## 📁 Cấu trúc thư mục

Tool yêu cầu cấu trúc thư mục như sau:

```
Q3A/                          (Thư mục gốc của bạn)
├── test_runner.py            (Tool Python - đặt ở đây)
├── given/                    (Thư mục chứa code Java)
│   ├── src/                  
│   │   ├── main.java         (File chính có hàm main)
│   │   ├── Student.java
│   │   └── ProcessStudent.java
│   └── ...                   (Các file khác)
└── TestCases/                (Thư mục chứa test cases)
    ├── tc1.txt
    ├── tc2.txt
    └── tc3.txt
```

**Lưu ý quan trọng:**
- File `test_runner.py` phải nằm cùng cấp với thư mục `given` và `TestCases`
- Code Java phải nằm trong `given/src/`
- Test cases phải nằm trong `TestCases/` và có tên dạng `tc*.txt`

## 🚀 Cách sử dụng

### Bước 1: Mở Terminal/Command Prompt

```bash
cd C:\Users\Admin\Downloads\Q3\Q3\Q3A
```

Hoặc đường dẫn đến thư mục của bạn.

### Bước 2: Chạy tool

```bash
python test_runner.py
```

### Bước 3: Xem kết quả

Tool sẽ tự động:
1. Biên dịch tất cả file Java
2. Chạy từng test case
3. Hiển thị kết quả chi tiết
4. Tổng kết điểm số

## 📝 Định dạng Test Case

Mỗi file test case (ví dụ: `tc1.txt`) phải có định dạng:

```
INPUT:
<input_data_here>
OUTPUT:
<expected_output_here>
REMOVE_SPACES:
YES/NO
CASE_SENSITIVE:
YES/NO
MARK:
<điểm_số>
```

### Ví dụ Test Case (tc1.txt):

```
INPUT:
3
9
OUTPUT:
[(SE0004,Thuan,9.2);]
REMOVE_SPACES:
YES
CASE_SENSITIVE:
NO
MARK:
1.0
```

### Giải thích các trường:

- **INPUT**: Dữ liệu đầu vào cho chương trình (có thể nhiều dòng)
- **OUTPUT**: Kết quả mong đợi (chỉ phần sau chữ "OUTPUT:" trong output của Java)
- **REMOVE_SPACES**: 
  - `YES`: Bỏ qua tất cả khoảng trắng khi so sánh
  - `NO`: Giữ nguyên khoảng trắng
- **CASE_SENSITIVE**:
  - `YES`: Phân biệt chữ hoa/thường
  - `NO`: Không phân biệt chữ hoa/thường
- **MARK**: Điểm số cho test case này (số thực)

## 📊 Ví dụ Output

### Output mẫu khi chạy tool:

```
=== Biên dịch Java files ===
✓ Biên dịch thành công!

============================================================
BẮT ĐẦU CHẠY TEST CASES
============================================================

--- TC1 ---
Input: 3
9
Expected: [(SE0004,Thuan,9.2);]
Actual: [(SE0004,Thuan,9.2);]
✓ PASS
Điểm: 1.0/1.0

--- TC2 ---
Input: 2
An
Expected: [(SE0001,An,7.2);(SE0002,An,5.5);]
Actual: [(SE0001,An,7.2);(SE0002,An,5.5);]
✓ PASS
Điểm: 1.0/1.0

--- TC3 ---
Input: 1
Expected: [(SE0000,Ha,4.5);(SE0001,An,7.2);...]
Actual: [(SE0000,Ha,4.5);(SE0001,An,7.2);...]
✓ PASS
Điểm: 1.0/1.0

============================================================
TỔNG KẾT
============================================================
tc1: ✓ PASS - 1.0/1.0 điểm
tc2: ✓ PASS - 1.0/1.0 điểm
tc3: ✓ PASS - 1.0/1.0 điểm

Tổng điểm: 3.0/3.0
Tỷ lệ: 100.0%
============================================================
```

## 🔍 Troubleshooting

### Lỗi: "Không tìm thấy thư mục given"

**Nguyên nhân**: File `test_runner.py` không đặt đúng vị trí

**Giải pháp**: 
- Đảm bảo `test_runner.py` nằm cùng cấp với thư mục `given` và `TestCases`
- Kiểm tra lại đường dẫn khi chạy `cd`

### Lỗi: "javac is not recognized"

**Nguyên nhân**: Java JDK chưa được cài đặt hoặc chưa thêm vào PATH

**Giải pháp**:
1. Cài đặt Java JDK
2. Thêm Java vào PATH:
   - Windows: Thêm `C:\Program Files\Java\jdk-xx\bin` vào Environment Variables
   - Linux/Mac: Thêm vào `.bashrc` hoặc `.zshrc`

### Lỗi biên dịch Java

**Nguyên nhân**: Code Java có lỗi syntax

**Giải pháp**:
- Kiểm tra lại code Java
- Xem thông báo lỗi chi tiết trong output của tool

### Test case không PASS nhưng output giống nhau

**Nguyên nhân**: Có thể do khoảng trắng hoặc ký tự ẩn

**Giải pháp**:
- Thử đặt `REMOVE_SPACES: YES` trong test case
- Kiểm tra encoding của file (nên dùng UTF-8)

### Program timeout

**Nguyên nhân**: Chương trình Java chạy quá lâu hoặc bị treo

**Giải pháp**:
- Kiểm tra vòng lặp vô hạn trong code
- Timeout mặc định là 10 giây, có thể tăng trong code nếu cần

## 📞 Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra lại cấu trúc thư mục
2. Xem phần Troubleshooting
3. Kiểm tra định dạng test case
4. Đảm bảo Java đã cài đặt đúng

## 📄 License

MIT License - Free to use and modify

## 🤝 Đóng góp

Contributions, issues và feature requests đều được chào đón!

---

**Version**: 1.0.0  
**Author**: Created for Java testing automation  
**Last Updated**: 2025

---

## 🧪 PE Format Test Runner (pe_check.py)

Công cụ thứ hai dùng để chấm theo định dạng PE với cấu trúc 4 bài (1, 2, 3, 4), mỗi bài chạy bằng file `.jar` đặt trong `run/`. Công cụ đọc một file `tests.txt` duy nhất cho cả 4 bài.

### ✨ Tính năng chính

- **Cấu trúc PE 4 bài**: `1/`, `2/`, `3/`, `4/`, mỗi bài có `src/` (code Java) và `run/` (đặt `.jar` để chạy)
- **Một file tests.txt duy nhất**: gom test của 4 bài với khối `=== Q1 ===`, `=== Q2 ===`, ...
- **Nhiều test case/bài**: đánh số `--- TC1 ---`, `--- TC2 ---`, ...
- **Tự động chạy .jar**: tự dò `.jar` trong `run/` và chạy bằng `java -jar`
- **Timeout 10 giây**: tránh chương trình treo
- **So sánh linh hoạt**: `REMOVE_SPACES`, `CASE_SENSITIVE`
- **Báo cáo đẹp**: hiển thị từng test case và tổng kết điểm

### 📁 Cấu trúc thư mục yêu cầu

```
PE_Exam/
├── 1/
│   ├── src/      (code Java - không động vào)
│   └── run/      (file .jar để chạy test)
│       └── Q1.jar
├── 2/
│   ├── src/
│   └── run/
│       └── Q2.jar
├── 3/
│   ├── src/
│   └── run/
│       └── Q3.jar
├── 4/
│   ├── src/
│   └── run/
│       └── Q4.jar
├── tests.txt     (file test cho cả 4 bài)
└── pe_check.py   (tool Python - đặt ở đây)
```

### 📝 Định dạng tests.txt

File `tests.txt` chứa lần lượt 4 khối câu hỏi. Mỗi khối bắt đầu bằng tiêu đề:

- `=== Q1 ===`
- `=== Q2 ===`
- `=== Q3 ===`
- `=== Q4 ===`

Trong mỗi khối có nhiều test case, mỗi test case có dạng:

```
--- TC<number> ---
INPUT:
<nội_dung_input_có_thể_nhiều_dòng>
OUTPUT:
<kỳ_vọng_output>
REMOVE_SPACES:
YES|NO
CASE_SENSITIVE:
YES|NO
MARK:
<điểm_số>
```

Ví dụ rút gọn một test case:

```
--- TC1 ---
INPUT:
3
Nguyen Van A
20
Male
OUTPUT:
Student: Nguyen Van A, Age: 20, Gender: Male
REMOVE_SPACES:
NO
CASE_SENSITIVE:
YES
MARK:
2.5
```

Lưu ý:
- `REMOVE_SPACES: YES` sẽ loại toàn bộ khoảng trắng trước khi so sánh.
- `CASE_SENSITIVE: NO` sẽ không phân biệt hoa/thường.
- Tool chỉ lấy phần sau chữ `OUTPUT:` (nếu chương trình in kèm log trước đó).

### 🚀 Cách chạy

Windows PowerShell/CMD:

```bash
cd PE_Exam
python pe_check.py
```

Tool sẽ kiểm tra đủ thư mục `1..4` và file `tests.txt`, sau đó chạy từng `.jar` tương ứng.

### 🔍 Cách hoạt động

- Tự động tìm file `.jar` trong thư mục `run/` của từng bài; ưu tiên tên có chứa `dist`, nếu không sẽ lấy file đầu tiên.
- Chạy chương trình bằng `java -jar <jar_file>` với `timeout = 10s`.
- Nếu output có chứa chuỗi `OUTPUT:`, chỉ phần sau đó được dùng để so sánh.
- Tính điểm theo từng test case và tổng hợp điểm cuối.

### 🧯 Troubleshooting (PE)

- "Không tìm thấy file .jar": Kiểm tra đã build `.jar` và đặt vào `run/` đúng bài.
- "TIMEOUT - Chương trình chạy quá 10 giây": Rà soát vòng lặp vô hạn, tối ưu I/O.
- "Không tìm thấy tests.txt": Đặt file `tests.txt` cạnh `pe_check.py` theo đúng định dạng.
- Java không chạy được: đảm bảo `java -version` hoạt động trong terminal.

### 📦 File liên quan

- `pe_check.py`: Trình chạy bài PE theo `.jar` và `tests.txt`.

> Gợi ý: Bạn có thể copy mẫu nội dung `tests.txt` từ mục hướng dẫn trong repo hoặc từ đề thi để cập nhật nhanh.