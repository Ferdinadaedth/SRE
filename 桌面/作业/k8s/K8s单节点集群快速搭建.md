# K8s单节点集群快速搭建 #

首先利用sealos下载并解压好sealos

```
$ wget https://github.com/labring/sealos/releases/download/v4.1.4/sealos_4.1.4_linux_amd64.tar.gz \
   && tar zxvf sealos_4.1.4_linux_amd64.tar.gz sealos && chmod +x sealos && mv sealos /usr/bin
```

然后进入文件夹执行以下命令

```
./sealos run docker.io/labring/kubernetes:v1.25.0 labring/helm:v3.11.2 labring/calico:v3.24.1 --single
```

然后允许master运行pod

```
kubectl taint nodes --all node-role.kubernetes.io/control-plane:NoSchedule-
```

