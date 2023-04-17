# K8s中利用traefik配置nginx服务 #

#####  1.去云厂商那域名解析到你的服务器  #####

#####  2.服务器上安装k8s，并安装好traefik #####

#####   3.配置nginx，监听80端口，将服务入口流量打到k8s集群中Traefik的入口点  #####

#####  4.以IngressRoute + MiddleWare + Service + Deployment的模式部署服务  #####

#####  5.最后实现访问域名+后缀能直接访问到我们集群中的服务 #####

k8s配置文件

```
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: nginx-test
  name: nginx-test
spec:
  replicas: 1
  selector:
    matchLabels:
      app: test
  template:
    metadata:
      labels:
        app: test
    spec:
      containers:
      - name: pyweb
        image: nginx
        ports:
        - containerPort: 80

---
apiVersion: v1
kind: Service
metadata:
  labels:
    app: test
  name: svc
spec:
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: test

---
apiVersion: traefik.containo.us/v1alpha1
kind: Middleware
metadata:
  name: redirect-https-middleware
spec:
  redirectScheme:
    scheme: https

---
apiVersion: traefik.containo.us/v1alpha1
kind: IngressRoute
metadata:
  name: whoami-route-auto-tls
spec:
  entryPoints:
  - websecure
  routes:
  - match: Host(`newk8s.ferdinandaedth.top`)
    kind: Rule
    services:
      - name: svc
        port: 80

---
apiVersion: traefik.containo.us/v1alpha1
kind: IngressRoute
metadata:
  name: whoami3-route
spec:
  entryPoints:
  - web
  routes:
  - match: Host(`newk8s.ferdinandaedth.top`)
   kind: Rule
    services:
      - name: svc
        port: 80
    middlewares:
    - name: redirect-https-middleware
```

nginx配置文件

```
http {
  upstream my-domain {
    server traefik.namespace.svc.cluster.local:80;
  }
  server {
    listen 80 default_server;
    server_name newk8s.ferdinandaedth.top;
    index index.html;
    location / {
      proxy_pass http://newk8s.ferdinandaedth.top;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
  }
```

最终效果:

![image-20230417181906002](https://gitee.com/ferdinandaedth/ferdinand/raw/master/image-20230417181906002.png)

![image-20230417181924422](https://gitee.com/ferdinandaedth/ferdinand/raw/master/image-20230417181924422.png)