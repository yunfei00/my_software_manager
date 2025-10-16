#!/bin/bash
# ===========================================
# Django 部署脚本 for Ubuntu + Nginx + Gunicorn
# 项目目录: /opt/my_software_manager
# ===========================================

PROJECT_NAME="my_software_manager"
PROJECT_DIR="/opt/${PROJECT_NAME}"
VENV_DIR="${PROJECT_DIR}/venv"
SOCK_PATH="${PROJECT_DIR}/${PROJECT_NAME}.sock"

echo ">>> 更新系统并安装依赖..."
sudo apt update -y && sudo apt upgrade -y
sudo apt install -y python3 python3-venv python3-pip git nginx

echo ">>> 创建虚拟环境并安装依赖..."
cd $PROJECT_DIR
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    pip install django gunicorn
fi

echo ">>> 执行数据库迁移和静态文件收集..."
python manage.py migrate
python manage.py collectstatic --noinput

echo ">>> 创建 Gunicorn systemd 服务..."
sudo tee /etc/systemd/system/gunicorn.service > /dev/null <<EOF
[Unit]
Description=Gunicorn daemon for Django project
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=${PROJECT_DIR}
ExecStart=${VENV_DIR}/bin/gunicorn --workers 3 --bind unix:${SOCK_PATH} ${PROJECT_NAME}.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

echo ">>> 配置 Nginx 代理..."
sudo tee /etc/nginx/sites-available/${PROJECT_NAME} > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        root ${PROJECT_DIR};
    }

    location /media/ {
        root ${PROJECT_DIR};
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:${SOCK_PATH};
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/${PROJECT_NAME} /etc/nginx/sites-enabled
sudo nginx -t && sudo systemctl restart nginx

echo ">>> 部署完成！"

echo "现在你可以访问： http://$(curl -s ifconfig.me)"
echo "Gunicorn 服务状态: sudo systemctl status gunicorn"
