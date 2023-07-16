## k8s 集群配置单点redis数据库+NFS持久化 ##

- 在k8s集群中的每个节点安装nfs-utils

```shell
yum install nfs-utils -y
```

- 选择一台机器创建共享总目录(为了方便，这里选择主节点)

```shell
mkdir -p /data/nfs
```

- 编辑配置 `vim /etc/exports`

```shell
/data/nfs *(rw,no_root_squash)
```

- 重启服务并验证

```shell
# 使配置生效
systemctl restart nfs &&
systemctl enable nfs

# 查看
showmount -e
```

- 为需要持久化的服务创建子目录（必须创建）

```shell
mkdir -p /data/nfs/redis
```

### 2.2 创建PV&PVC

- pv不用指定命名空间
- pvc需要指定命名空间，默认为default
- 若有配置hosts映射，可使用映射名代替

```text
# vim 1-pv_pvc.yaml
----------------------------------------------

apiVersion: v1
kind: PersistentVolume
metadata:
  name: redis-pv
spec:
  capacity:
    storage: 10Gi
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: redis-nfs
  nfs:
    path: /data/nfs/redis
    server: 172.16.62.20
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: redis-pvc
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: redis-nfs
```

- 安装

```text
kubectl apply -f 1-pv_pvc.yaml
```

![img](https://pic1.zhimg.com/80/v2-b4194bca912dd67c95d41870e9e91138_720w.webp)



## 3. K8S部署

### 3.1 ConfigMap

- 设置密码：`requirepass 123456`

```text
vim 2-configmap.yaml
-----------------------------------

apiVersion: v1
kind: ConfigMap
metadata:
  name: redis
data:
  redis.conf: |+
    requirepass 123456
    protected-mode no
    port 6379
    tcp-backlog 511
    timeout 0
    tcp-keepalive 300
    daemonize no
    supervised no
    pidfile /var/run/redis_6379.pid
    loglevel notice
    logfile ""
    databases 16
    always-show-logo yes
    save 900 1
    save 300 10
    save 60 10000
    stop-writes-on-bgsave-error yes
    rdbcompression yes
    rdbchecksum yes
    dbfilename dump.rdb
    dir /data
    slave-serve-stale-data yes
    slave-read-only yes
    repl-diskless-sync no
    repl-diskless-sync-delay 5
    repl-disable-tcp-nodelay no
    slave-priority 100
    lazyfree-lazy-eviction no
    lazyfree-lazy-expire no
    lazyfree-lazy-server-del no
    slave-lazy-flush no
    appendonly no
    appendfilename "appendonly.aof"
    appendfsync everysec
    no-appendfsync-on-rewrite no
    auto-aof-rewrite-percentage 100
    auto-aof-rewrite-min-size 64mb
    aof-load-truncated yes
    aof-use-rdb-preamble no
    lua-time-limit 5000
    slowlog-log-slower-than 10000
    slowlog-max-len 128
    latency-monitor-threshold 0
    notify-keyspace-events Ex
    hash-max-ziplist-entries 512
    hash-max-ziplist-value 64
    list-max-ziplist-size -2
    list-compress-depth 0
    set-max-intset-entries 512
    zset-max-ziplist-entries 128
    zset-max-ziplist-value 64
    hll-sparse-max-bytes 3000
    activerehashing yes
    client-output-buffer-limit normal 0 0 0
    client-output-buffer-limit slave 256mb 64mb 60
    client-output-buffer-limit pubsub 32mb 8mb 60
    hz 10
    aof-rewrite-incremental-fsync yes
```

### 3.2 Deployment

- ConfigMap生成的配置文件放置于容器内`/etc/redis/redis.conf`
- 使挂载的ConfigMap生效：`command: ["redis-server","/etc/redis/redis.conf"]`
- 将容器的`/data`持久化到`redis-pvc`，即/data/nfs/redis`下

```text
vim 3-deployment.yaml
---------------------------------

apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  labels:
    app: redis
spec:
  strategy:
    type: Recreate
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
      annotations:
        version/date: "20210310"
        version/author: "lc"
    spec:
      containers:
      - name: redis
        image: redis
        imagePullPolicy: Always
        command: ["redis-server","/etc/redis/redis.conf"]
        ports:
        - containerPort: 6379
        volumeMounts:
        - name: redis-config
          mountPath: /etc/redis/redis.conf
          subPath: redis.conf
        - name: redis-persistent-storage
          mountPath: /data
      volumes:
      - name: redis-config
        configMap:
          name: redis
          items:
          - key: redis.conf
            path: redis.conf
      - name: redis-persistent-storage
        persistentVolumeClaim:
          claimName: redis-pvc
```

### 3.3 Service

- 通过NodePort方式暴露服务

```text
vim 4-service.yaml
---------------------------------

kind: Service
apiVersion: v1
metadata:
  name: redis
spec:
  type: NodePort
  selector:
    app: redis
  ports:
  - port: 6379
    targetPort: 6379
```
