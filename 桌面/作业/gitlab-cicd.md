# gitlab-cicd #

python项目文件目录`main.py`

```python
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'yx041110'
app.config['MYSQL_DB'] = 'mysql'

mysql = MySQL(app)

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cur.fetchone()
    cur.close()

    if user is None:
        return jsonify({'success': False, 'message': 'Invalid username or password'}), 401

    return jsonify({'success': True, 'message': 'Logged in successfully'})


if __name__ == '__main__':
    app.run(debug=True)

```

项目依赖包`requiremes.txt`

```
blinker==1.6.2
certifi==2023.5.7
charset-normalizer==3.1.0
click==8.1.3
colorama==0.4.6
Flask==2.3.2
Flask-MySQLdb==1.0.1
idna==3.4
itsdangerous==2.1.2
Jinja2==3.1.2
MarkupSafe==2.1.3
mysql==0.0.3
mysqlclient==2.1.1
PyMySQL==1.0.3
requests==2.31.0
urllib3==2.0.2
Werkzeug==2.3.4
```

`dockerfile`

```
FROM python:3.11


ADD . /pypj

RUN pip install -r /pypj/requirements.txt

CMD ["python", "/pypj/main.py"]

```

`test.yaml`

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: py-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: py-app
  template:
    metadata:
      labels:
        app: py-app
    spec:
      containers:
      - name: py-app
        image: ferdina/mynginx:pypj1
        ports:
        - containerPort: 80

```

` .gitlab-ci.yml`

```
stages:
  - build
  - deploy

imagebuilder:
  image: ferdina/mynginx:kaniko1
  stage: build
  variables:
    destination: ferdina/mynginx:pypj1
  script:
    - /kaniko/build-upload

deploy:
  image: 
    name: bitnami/kubectl
    entrypoint: [""]
  stage: deploy
  script:
    - kubectl apply -f ./test.yaml --kubeconfig=./kubeconfig.yaml

```

> kubeconfig.yaml由 cat ~/.kube/config得到

![image-20230608233725977](https://gitee.com/ferdinandaedth/ferdinand/raw/master/image-20230608233725977.png)

![image-20230608233755066](https://gitee.com/ferdinandaedth/ferdinand/raw/master/image-20230608233755066.png)