#!/bin/bash
INSTALLER_NAME=wordpress
ARCHIVE_URL="https://cn.wordpress.org/latest-zh_CN.tar.gz"
ARCHIVE_DIRNAME="wordpress"                                                             #命名变量及其初始化

DB_PASSWD="$(dd if=/dev/urandom | (base64 -w0 2> /dev/null || base64 2> /dev/null) | dd bs=1 count=16 2>/dev/null)"              #输入数据，如果数据不在字符集中或输入超出16个字符则丢入黑洞

root_need(){                                                                                                  #创建函数
   if [[ $EUID -ne 0 ]]; then     #如果不是该进程创建者或者root用户
   	echo "Error:This script must be run as root!" 1>&2 #标准输出
        exit 1   #退出码
   fi
}

welcome(){                       #创建函数
    echo "Hello! This is a simple script to deploy a LNMP environment."
    echo "And it also automatically install wordpress for you."
    echo "You should first set your domain name with an A DNS record to this server." #提示信息
    echo
    echo "Here is the database credentials we generated for you."
    echo "PLEASE CAREFULLY SAVE THEM! VERY IMPORTANT!"
    echo "Database name: ${INSTALLER_NAME}"    
    echo "Database user: ${INSTALLER_NAME}"
    echo "Database pass: ${DB_PASSWD}"     #输入密码
    echo           
    echo "Press enter key to continue..."
    read -n 1   #输入并检测字符串长度是否不为 0，不为 0 返回 true
}

change_source(){              #换源
    sed -i 's#archive.ubuntu.com#mirrors.tuna.tsinghua.edu.cn#g' /etc/apt/sources.list && \
    sed -i 's#ports.ubuntu.com#mirrors.tuna.tsinghua.edu.cn#g' /etc/apt/sources.list && \
    sed -i 's#security.ubuntu.com#mirrors.tuna.tsinghua.edu.cn#g' /etc/apt/sources.list && \
    apt update && return 0 #更新之后直接返回0  
    return 1   
}

install_software(){
    apt install -y wget gnupg git curl && \       # 下载url，wget,gnupg,git,curl

MariaDB Server Package

​    echo "deb [arch=amd64,arm64,ppc64el] http://mirrors.tuna.tsinghua.edu.cn/mariadb/repo/10.5/ubuntu focal main" > /etc/apt/sources.list.d/mariadb.list && \              #为系统添加源
​    wget -O - 'http://keyserver.ubuntu.com/pks/lookup?op=get&search=0xF1656F24C74CD1D8' | apt-key add && \#使用wget下载keyserver服务器
​    apt update && \#更新
​    apt install -y nginx php7.4-fpm php7.4-mysql php7.4-mbstring php7.4-gd php7.4-curl php7.4-xml php7.4-xmlrpc php7.4-iconv mariadb-server && return 0     #基于ubuntu安装扩展工具然后返回0
​    return 1
}

start_database(){ 

systemctl start mariadb     #启动Mariadb的 systemd 服务

​    while ! mysqladmin ping --silent; do     #检查服务器状态，是否可用

sleep(1)     #不可用时休息一毫秒

​    done
​    echo "CREATE DATABASE \`${INSTALLER_NAME}\` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci; GRANT ALL PRIVILEGES ON \`${INSTALLER_NAME}\`.* TO '${INSTALLER_NAME}'@'localhost' IDENTIFIED BY '$DB_PASSWD';" | mysql#创建数据库，设置字符集，并给登陆账号赋予所有权限
}

query_option(){
    printf "The port you want to use? [default=80]"  #输入要使用的端口  

  read -r port < /dev/tty  #输入端口
    if [ -z "$port" ]; then    #如果输入值为空，则为真
        port=80
    fi
    printf "The https port you want to use? (type 0 to disable https) [default=443]"#想要的https端口
    read -r sslport < /dev/tty   #输入
    if [ -z "$port" ]; then  #如果输入值为空，则为真

​        sslport=443
​    fi
​    if [ "$sslport" = "0" ]; then 
​        sslport=0
​    fi
​    printf "The domain name you want to use? [default=]"#想用的域名

_
    read -r domain < /dev/tty#输入
    if [ -z "$domain" ]; then   #如果为空
        domain=_
    fi

    ssl_enabled=1
    if [ "$sslport" = "0" ] || [ "$domain" = "_" ]; then
        ssl_enabled=0
    fi
}

do_nginx_config(){
    cat > /etc/nginx/conf.d/${INSTALLER_NAME}.conf <<EOF  #创建新文件并设置
server {
    listen ${port};#监听端口
    #DISABLE_SSL_PREFIX listen ${sslport} ssl http2;
    #DISABLE_SSL_PREFIX ssl_certificate /var/www/ssl/${domain}/public.cer;
    #DISABLE_SSL_PREFIX ssl_certificate_key /var/www/ssl/${domain}/private.key;
    server_name ${domain};
    index index.php;#网站骨架
    root /var/www/${INSTALLER_NAME};#将你的用户加入root并赋予权限
    location = /favicon.ico {  #访问该网站
        log_not_found off; #忽略favicon.ico日志
        access_log off;#关闭访问日志
    }
    location = /robots.txt {#访问网站
        allow all;    #允许所有访问
        log_not_found off;#忽略favicon.ico日志
        access_log off;#关闭访问日志
    }
    location / {

#This is cool because no php is touched for static content.

#include the "?\$args" part so non-default permalinks doesn't break when using query string

​        try_files \$uri \$uri/ /index.php?\$args;#解析两个文件若解析到则返回第一个，若没有解析到则向

index.php发起跳转

​    }
​    location ~ \.php\$ {
​        #NOTE: You should have "cgi.fix_pathinfo = 0;" in php.ini
​        include snippets/fastcgi-php.conf;
​        fastcgi_pass unix:/var/run/php/php7.4-fpm.sock;#  fastcgi_pass unix的配置
​        fastcgi_intercept_errors on;#表示接收fastcgi输出的http 1.0 response code，指出错误页面
​        fastcgi_buffers 16 16k;#本地需要用的缓冲区的数量和大小来缓冲fastcgi的应答
​        fastcgi_buffer_size 32k;#应答第一部分需要缓冲区大小
​    }
​    location ~* \.(js|css|png|jpg|jpeg|gif|ico)\$ {#用来转发动态请求到后端应用服务器
​        expires max;#设置图片过期时长为30天
​        log_not_found off;#忽略favicon.ico日志
​    }
​    gzip on;#开启gzip
}
EOF
​    systemctl restart nginx#重启
​    if [ "$ssl_enabled" = "1" ]; then
​        echo "Dowlnoading certbot..."
​        git clone https://codechina.csdn.net/mirrors/acmesh-official/acme.sh.git ~/.acme.sh# 拷贝一个项目到本地
​        echo "Issueing certificate..."
​        mkdir -p /var/www/ssl/${domain}#创建文件
​        (~/.acme.sh/acme.sh --issue --server letsencrypt -d "${domain}" -w /var/www/${INSTALLER_NAME} \#生成免费的ssl证书
​            --key-file "/var/www/ssl/${domain}/private.key" --fullchain-file "/var/www/ssl/${domain}/public.cer" --reloadcmd "systemctl force-reload nginx" \
​        && sed -i 's/#DISABLE_SSL_PREFIX\ //g' /etc/nginx/conf.d/${INSTALLER_NAME}.conf \
​	&& systemctl force-reload nginx) || echo "apply the certification fail!"
​    fi
}

1. 如果解析到，返回第一个，
2. 如果都没有解析到，向127.0.0.1/index.html发起请求跳转

root_need#函数调用
welcome#函数调用

change_source#换源
if [ $? -eq 0 ]; then#查看上个命令的退出状态
    echo "Change source success to tsinghua.edu.cn"
    
else
    echo "Change source failed, use the default source."
fi

install_software#调用函数
if [ $? -eq 0 ]; then#查看上个命令的退出状态
    echo "Install software success"
else
    echo "Install software failed"
    exit 1
fi

systemctl disable apache2 #开机时禁用
systemctl enable nginx php7.4-fpm mariadb#开机时启动
systemctl stop nginx#停止进程

start_database || (echo "Start database failed" && exit 1)#调用函数

cd /var/www/ && \  #进入目录
wget -O - "${ARCHIVE_URL}" | tar -xzf - && \日志信息写入文件
mv "${ARCHIVE_DIRNAME}" "${INSTALLER_NAME}" && \ #重命名
chown -R www-data:www-data "${INSTALLER_NAME}" && \#chown 更改web目录权限root为www-data

query_option#调用函数

do_nginx_config#调用函数

echo "Here is the database credentials we generated for you, shown again."  #流程开始
echo "PLEASE CAREFULLY SAVE THEM! VERY IMPORTANT!"
echo "Database name: ${INSTALLER_NAME}"
echo "Database user: ${INSTALLER_NAME}"
echo "Database pass: ${DB_PASSWD}" 
