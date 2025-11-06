@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ====================================
echo    Mở Project với NetBeans
echo ====================================
echo.

REM Đường dẫn NetBeans 13
set "NETBEANS_PATH=C:\Program Files\NetBeans-13\netbeans\bin\netbeans64.exe"

REM Kiểm tra đường dẫn có tồn tại không
if not exist "!NETBEANS_PATH!" (
    echo [LỖI] Không tìm thấy NetBeans tại: !NETBEANS_PATH!
    echo.
    pause
    exit /b 1
)

echo [OK] Đã tìm thấy NetBeans
echo.

REM Liệt kê các project trong thư mục hiện tại
echo Đang tìm kiếm project...
echo.

set count=0
set /a index=0

REM Tìm các thư mục có file nbproject (NetBeans project)
for /d %%D in (*) do (
    if exist "%%D\nbproject" (
        set /a index+=1
        set "project[!index!]=%%D"
        echo [!index!] %%D
        set /a count+=1
    )
)

if !count! equ 0 (
    echo [THÔNG BÁO] Không tìm thấy project NetBeans nào trong thư mục hiện tại.
    echo.
    pause
    exit /b 0
)

echo.
echo Tìm thấy !count! project(s).
echo.

REM Hỏi người dùng muốn mở project nào
echo Chọn hành động:
echo [A] Mở tất cả project
echo [S] Chọn project cụ thể
echo [Q] Thoát
echo.
set /p "choice=Nhập lựa chọn của bạn: "

if /i "!choice!"=="Q" (
    echo Đã hủy.
    exit /b 0
)

if /i "!choice!"=="A" (
    echo.
    echo Đang mở tất cả project...
    for /l %%i in (1,1,!index!) do (
        echo Mở project: !project[%%i]!
        start "" "!NETBEANS_PATH!" --open "%CD%\!project[%%i]!"
        timeout /t 2 /nobreak >nul
    )
    echo.
    echo Hoàn tất!
) else if /i "!choice!"=="S" (
    echo.
    set /p "selected=Nhập số thứ tự project (1-!index!): "
    
    if defined project[!selected!] (
        echo Đang mở project: !project[!selected!]!
        start "" "!NETBEANS_PATH!" --open "%CD%\!project[!selected!]!"
        echo Hoàn tất!
    ) else (
        echo [LỖI] Lựa chọn không hợp lệ.
    )
) else (
    echo [LỖI] Lựa chọn không hợp lệ.
)

echo.
pause