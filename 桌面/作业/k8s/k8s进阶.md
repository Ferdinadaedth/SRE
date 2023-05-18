# level0

配置文件

```shell
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
spec:
  containers:
  - image: nginx
    name: web-server
    volumeMounts:
    - name: hostpath-volume
      mountPath: /var/log/nginx
  volumes:
  - name: hostpath-volume
    hostPath:
      path: /var/log/nginx
      type: Directory
```

![image-20230506233759390](https://gitee.com/ferdinandaedth/ferdinand/raw/master/image-20230506233759390.png)

# level1 #

首先创建持久卷，我是直接通过kuboard面板创建的.我创建的持久卷名字为nfs.

pv配置文件

```shell
apiVersion: v1
kind: PersistentVolume
metadata:
  name: nfs-pv
spec:
  capacity:
    storage: 5Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Recycle
  storageClassName: nfs
  mountOptions:
    - hard
    - nfsvers=4.1
  nfs:
    path: /root/nfs_root
    server: 10.0.24.12
```

pvc配置文件

```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: nfs-pvc
spec:
  storageClassName: nfs
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 5Gi
```

pod配置文件

```shell
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pv-pod
spec:
  volumes:
    - name: nginx-pv-storage
      persistentVolumeClaim:
        claimName: nfs-pvc
  containers:
    - name: nginx
      image: nginx
      ports:
        - containerPort: 80
          name: nginx-server
      volumeMounts:
        - mountPath: /var/log/nginx
          name: nginx-pv-storage
```

![image-20230505234352311](https://gitee.com/ferdinandaedth/ferdinand/raw/master/image-20230505234352311.png)

![image-20230505234846680](https://gitee.com/ferdinandaedth/ferdinand/raw/master/image-20230505234846680.png

![image-20230506175806882](https://gitee.com/ferdinandaedth/ferdinand/raw/master/image-20230506175806882.png)

# level2 #

实例 WordPress 部署。WordPress容器挂载了 持久卷在网站数据文件。环境变量集 上面定义的MySQL服务的名称，WordPress将通过服务访问数据库。

mysql的pv

```
apiVersion: v1
kind: PersistentVolume
metadata:
  name: mysql-pv
spec:
  capacity:
    storage: 20Gi
  accessModes:
    - ReadWriteOnce
  nfs:
    server: 116.204.83.122
    path: /root/nfs_root/mysql
```

wordpress的pv

```
apiVersion: v1
kind: PersistentVolume
metadata:
  name: wordpress-pv
spec:
  capacity:
    storage: 20Gi
  accessModes:
    - ReadWriteOnce
  nfs:
    server: 116.204.83.122
    path: /root/nfs_root/wordpress
```



```shell
apiVersion: v1
kind: Service
metadata:
  name: wordpress
  namespace: wordpress
spec:
  type: NodePort
  selector:
    app: wordpress
  ports:
  - name: wordpressport
    protocol: TCP
    port: 8080
    targetPort: 80
apiVersion: v1
kind: Service
metadata:
  name: wordpress
  labels:
    app: wordpress
spec:
  ports:
    - port: 8080
      targetPort: 80
  selector:
    app: wordpress
    tier: frontend
  type: NodePort
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: wp-pv-claim
  labels:
    app: wordpress
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: "nfs"
  resources:
    requests:
      storage: 20Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: wordpress
  labels:
    app: wordpress
spec:
  selector:
    matchLabels:
      app: wordpress
      tier: frontend
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        app: wordpress
        tier: frontend
    spec:
      containers:
      - image: wordpress:4.8-apache
        name: wordpress
        env:
        - name: WORDPRESS_DB_HOST
          value: "127.0.0.1:3306"
        - name: WORDPRESS_DB_PASSWORD
          value: "123456"
        ports:
        - containerPort: 80
          name: wordpress
        volumeMounts:
        - name: wordpress-persistent-storage
          mountPath: /var/www/html
      - image: mysql:5.6
        name: mysql
        env:
        - name: MYSQL_ROOT_PASSWORD
          value: "123456"
        ports:
        - containerPort: 3306
          name: mysql
        volumeMounts:
        - name: mysql-persistent-storage
          mountPath: /var/lib/mysql
      volumes:
      - name: wordpress-pv
        persistentVolumeClaim:
          claimName: wp-pv-claim
      - name: mysql-pv
        persistentVolumeClaim:
          claimName: mysql-pv-claim
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pv-claim
  labels:
    app: wordpress
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: "nfs"
  resources:
    requests:
      storage: 20Gi
```

最后由于不知名原因狠狠的失败

# level5 #

分别给两个节点打上污点

```
kubectl taint node master node-type=production:NoSchedule
```

```
kubectl taint node node1 node-type=test:NoSchedule
```

创建两个Deployment，每个Deployment代表一个环境

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: taint-test
  labels:
    app: taint-test
spec:
  replicas: 1
  selector:
    matchLabels:
      app: taint-test
  template:
    metadata:
      labels:
        app: taint-test
    spec:
      containers:
      - image: nginx
        name: nginx
      tolerations:
      - key: node-type
        operator: Equal
        value: production
        effect: NoSchedule
```

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: taint-test1
  labels:
    app: taint-test1
spec:
  replicas: 1
  selector:
    matchLabels:
      app: taint-test1
  template:
    metadata:
      labels:
        app: taint-test1
    spec:
      containers:
      - image: nginx
        name: nginx
      tolerations:
      - key: node-type
        operator: Equal
        value: test
        effect: NoSchedule
```

![image-20230515202619199](https://gitee.com/ferdinandaedth/ferdinand/raw/master/image-20230515202619199.png)

测试了一个，成功调度到相应的节点

# level 6 #

service配置文件

```shell
apiVersion: v1
kind: Service
metadata:
  name: {{ include "nginx-chart.fullname" . }}
  labels:
    {{- include "nginx-chart.labels" . | nindent 4 }}
spec:
  type: {{ .Values.service.type }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: http
      protocol: TCP
      name: http
  selector:
    {{- include "nginx-chart.selectorLabels" . | nindent 4 }}

```

deployment配置文件

```shell
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "nginx-chart.fullname" . }}
  labels:
    {{- include "nginx-chart.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "nginx-chart.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      {{- with .Values.podAnnotations }}
      annotations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      labels:
        {{- include "nginx-chart.selectorLabels" . | nindent 8 }}
    spec:
      {{- with .Values.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      serviceAccountName: {{ include "nginx-chart.serviceAccountName" . }}
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      containers:
        - name: {{ .Chart.Name }}
          securityContext:
            {{- toYaml .Values.securityContext | nindent 12 }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - name: http
              containerPort: {{ .Values.service.port }}
              protocol: TCP
          livenessProbe:
            httpGet:
              path: /
              port: http
          readinessProbe:
            httpGet:
              path: /
              port: http
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
      {{- with .Values.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
                       
            
```

验证结果

![image-20230509144336898](https://gitee.com/ferdinandaedth/ferdinand/raw/master/image-20230509144336898.png)

# level7 #

![image-20230508184248831](https://gitee.com/ferdinandaedth/ferdinand/raw/master/image-20230508184248831.png)