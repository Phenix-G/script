#!/bin/bash

# 备份原始的sshd配置文件
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak

# 修改sshd配置文件以保持长连接
sudo sed -i 's/#TCPKeepAlive yes/TCPKeepAlive yes/' /etc/ssh/sshd_config
sudo sed -i 's/#ClientAliveInterval 0/ClientAliveInterval 60/' /etc/ssh/sshd_config
sudo sed -i 's/#ClientAliveCountMax 3/ClientAliveCountMax 720/' /etc/ssh/sshd_config

# 重启sshd服务以应用更改
if command -v systemctl >/dev/null 2>&1; then
    sudo systemctl restart sshd
elif command -v service >/dev/null 2>&1; then
    sudo service sshd restart
else
    echo "无法找到systemctl或service命令，请手动重启sshd服务。"
    exit 1
fi

echo "sshd配置已更新，现在将保持长连接。"
