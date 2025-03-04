$ErrorActionPreference = "Stop"

Write-Host "Bắt đầu cài đặt project..."

if ($IsWindows) {
    $python = Get-Command python -ErrorAction SilentlyContinue
    if (-not $python) {
        Write-Host "Python chưa được cài đặt. Hãy cài đặt Python từ https://www.python.org/downloads/"
        Exit 1
    }
} else {
    if (-not (Get-Command python3 -ErrorAction SilentlyContinue)) {
        Write-Host "Python chưa được cài đặt. Đang tiến hành cài đặt..."
        sudo apt update && sudo apt install -y python3 python3-venv python3-pip
    }
}

if (-not (Test-Path "flask-tiny-app")) {
    Write-Host "Cloning repository..."
    git clone https://github.com/VuTrinhNguyenHoang/flask-tiny-app.git
}

Set-Location flask-tiny-app

Write-Host "Tạo môi trường ảo..."
if ($IsWindows) {
    python -m venv venv
    .\venv\Scripts\Activate
} else {
    python3 -m venv venv
    source venv/bin/activate
}

Write-Host "Cập nhật pip..."
python -m pip install --upgrade pip
Write-Host "Cài đặt các thư viện cần thiết..."
pip install -r requirements.txt

Write-Host "Chạy ứng dụng..."
python main.py
