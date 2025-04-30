# Авторы

- Полякова Дарья К3342
- Жижилева Арина К3342

# Лабораторная работа №1: k8s

Задачи:
1. развернуть minicube 
2. создать docker образ вашего приложения;
3. создать deployment;
4. установить кол-во подов на 3
5. добавьте Metrics Server (kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml).
6. настройте Horizontal Pod Autoscaler (HPA), чтобы масштабировать поды при увеличении нагрузки (kubectl autoscale deployment my-app --cpu-percent=50 --min=2 --max=5).
7. настройте Prometheus и Grafana через (helm install prometheus prometheus-community/kube-prometheus-stack). Настройте дашборды в Grafana для мониторинга нагрузки (хотя бы один)


## Установка бинарного файла kubectl с помощью curl в Linux
Загрузили последнюю версию с помощью команды:
```
curl -LO https://dl.k8s.io/release/`curl -LS https://dl.k8s.io/release/stable.txt`/bin/linux/amd64/kubectl
```

Сделали бинарный файл kubectl исполняемым:
```
chmod +x ./kubectl
```

Переместили бинарный файл в директорию из переменной окружения PATH:
```
sudo mv ./kubectl /usr/local/bin/kubectl
```

## Minikube

Установили minikube с помощью инструкции https://minikube.sigs.k8s.io/docs/start/?arch=%2Fwindows%2Fx86-64%2Fstable%2F.exe+download
```
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

sudo chmod +x /usr/local/bin/minikube
```
Запускаем docker desktop
Запускаем minikube 
```
minikube start --driver=docker --cpus=2 --memory=4096
```
в новом терминале запускаем minikube dashboard. Команда dashboard активирует дополнение dashboard и открывает прокси в веб-браузере по умолчанию. В этой панели можно создавать такие Kubernetes-ресурсы, как Deployment и Service.

## Docker образ

Создаем dockerfile

Собираем образ:
```
eval $(minikube docker-env)
docker build -t pris-proj:1.0 .
```
Создаем файл deployment.yaml, service.yaml, app.js

Применяем конфигурацию:
```
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

## Установка Metrics Server
```
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```
Проверяем работу:
```
kubectl top pods
```

## Настройка Horizontal Pod Autoscaler (HPA)
```
kubectl autoscale deployment my-app --cpu-percent=50 --min=2 --max=5
```
Проверяем HPA:
```
kubectl get hpa
```
## Установка Prometheus и Grafana с помощью Helm

Сначала установите Helm, если он еще не установлен:
```
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```
Добавьте репозиторий и установите:
```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack
```

Нужно подождать несколько минут, пока grafana настраивается.

Откройте доступ к Grafana:
```
kubectl port-forward service/prometheus-grafana 3000:80
```

Откройте Grafana в браузере: http://localhost:3000

Создаем дашборд, в queries вставляем, смотрим нагрузку
```
sum(rate(container_cpu_usage_seconds_total{namespace="default", pod=~"pris-proj-.+"}[1m])) by (pod)
```
Если визуализация не показательная можем создать тестовую нагрузку
```
kubectl run load-generator --image=busybox --restart=Never -- /bin/sh -c "while true; do wget -q -O- http://pris-proj; done"
```
потом меняем на
```
 kube_deployment_status_replicas{deployment="my-node-app"}
```
смотрим количество подов.

# Лабораторная работа №2: Разработка микросервисной архитектуры с GraphQL

## Описание

Учебный проект, демонстрирующий микросервисную архитектуру с использованием GraphQL и Apollo Gateway.  
Приложение состоит из трёх микросервисов: Пользователи, Товары и Заказы. Все взаимодействия происходят через GraphQL API.

## Как запустить

1. Убедитесь, что установлены:

- Python 3.10+
- PostgreSQL
- MongoDB
- Node.js + npm

2. Создайте базы данных:

- `users_db` (PostgreSQL)
- `products_db` (PostgreSQL)
- `orders_db` создастся автоматически в MongoDB при первом запросе

3. Установите зависимости Python для каждого микросервиса:
```
pip install fastapi uvicorn strawberry-graphql[fastapi] sqlalchemy psycopg2 pymongo motor
```
4. Установите зависимости Node.js в папке gateway:
```
cd gateway
npm install
```
5. Запустите микросервисы (в отдельных терминалах):
```
cd users_service
uvicorn main:app --port 8001

cd products_service
uvicorn main:app --port 8002

cd orders_service
uvicorn main:app --port 8003
```
6. Запустите GraphQL Gateway:
```
cd gateway
node index.js
```
7. Откройте браузер:
```
http://localhost:4000
```

## Функциональность

- Получение списка пользователей, товаров и заказов
- Создание новых пользователей, товаров и заказов
- Обновление записей (пользователей, товаров, заказов)
- Удаление записей
- Объединение всех микросервисов в один GraphQL API через Apollo Gateway

## Используемые библиотеки

Python микросервисы:
- FastAPI
- Strawberry GraphQL
- SQLAlchemy
- psycopg2
- Motor (для MongoDB)

GraphQL Gateway:
- Apollo Server
- Apollo Gateway
- GraphQL (Node.js)

# Лабораторная работа №3: Работа с Big Data

## Описание

Веб-приложение на Flask, позволяющее загружать большие данные (CSV), обучать простую ML-модель и визуализировать результаты.

## Как запустить

1. Клонируй репозиторий:
```
git clone https://github.com/ИМЯ_ПОЛЬЗОВАТЕЛЯ/big-data-lab.git
cd big-data-lab
```
2. Установи зависимости:
```
pip install -r requirements.txt
```
3. Запусти Flask-приложение:
```
python app.py
```
4. Перейди в браузер:
```
http://127.0.0.1:5000/
```

## Функциональность

- Загрузка CSV-файлов
- Предпросмотр таблицы
- Выбор признаков X и Y
- Обучение модели (линейная регрессия)
- Построение графиков
- Корреляционная матрица

## Используемые библиотеки

- Flask
- Pandas
- Matplotlib
- Seaborn
- Scikit-learn

