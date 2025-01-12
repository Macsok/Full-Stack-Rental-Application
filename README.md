# Full-Stack-Rental-Application
to be completed...

# Setting up Master-Slave database
Setting up a master-slave database replication involves configuring one database server (the master) to replicate its data to other database servers (in this case single slave). This setup is useful for load balancing, data redundancy, and backup purposes. Below are the steps to set up master-slave replication using Docker and Docker Compose.

# Instructions to enable and run master-slave replication on a virtual machine

1. **Install Docker and Docker Compose**:
- Follow the official Docker installation guide for your operating system: https://docs.docker.com/get-docker/
- Install Docker Compose: https://docs.docker.com/compose/install/

> [!TIP]
> The following commands will download the Docker Compose binary, make it executable, and verify the installation:
> 
> ```sh
> sudo curl -SL "https://github.com/docker/compose/releases/download/v2.32.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
> sudo chmod +755 /usr/local/bin/docker-compose
> docker-compose version
> ```

2. **Create a Docker Compose file**:
    - Create a `docker-compose.yml` file with the following content:
```yaml
services:
  mysql-master:
    image: mysql/mysql-server:8.0
    container_name: mysql-master
    command: --server-id=1 --log-bin=mysql-bin --binlog-format=row --early-plugin-load=keyring_file.so
    environment:
      MYSQL_ROOT_PASSWORD: root_pass
      MYSQL_DATABASE: car_rental_db
      MYSQL_USER: replication_user
      MYSQL_PASSWORD: user_pass
    ports:
      - "3306:3306"
    volumes:
      - ./data/mysql-master:/var/lib/mysql
      - ./keyring/master:/var/lib/mysql-keyring

  mysql-slave:
    image: mysql/mysql-server:8.0
    container_name: mysql-slave
    depends_on:
      - mysql-master
    command: --server-id=2 --log-bin=mysql-bin --binlog-format=row --early-plugin-load=keyring_file.so
    environment:
      MYSQL_ROOT_PASSWORD: root_pass
      MYSQL_DATABASE: car_rental_db
      MYSQL_USER: replication_user
      MYSQL_PASSWORD: user_pass
    ports:
      - "3307:3306"
    volumes:
      - ./data/mysql-slave:/var/lib/mysql
      - ./keyring/slave:/var/lib/mysql-keyring
```

3. **Start the Docker containers**:
   - Run the following command to start the containers:
    ```sh
    docker-compose up -d
    ```

4. **Configure the Master database**:
   - Access the master container:
    ```sh
    docker exec -it mysql-master mysql -u root -p
    ```
   - Run the following SQL commands to configure the master:
    ```sql
    CREATE USER 'app_user'@'%' IDENTIFIED BY 'app_pass';
    GRANT ALL PRIVILEGES ON car_rental_db.* TO 'app_user'@'%';
    FLUSH PRIVILEGES;
    ALTER USER 'replication_user'@'%' IDENTIFIED WITH 'mysql_native_password' BY 'replication_password';
    GRANT REPLICATION SLAVE ON *.* TO 'replication_user'@'%';
    FLUSH PRIVILEGES;
    SHOW MASTER STATUS;
    ```
   - Note the `File` and `Position` values from the `SHOW MASTER STATUS` output.

5. **Configure the Slave database**:
   - Access the slave container:
    ```sh
    docker exec -it mysql-slave mysql -u root -p
    ```
   - Run the following SQL commands to configure the slave:
    ```sql
    CHANGE MASTER TO
    MASTER_HOST='mysql-master',
    MASTER_USER='replication_user',
    MASTER_PASSWORD='replication_password',
    MASTER_LOG_FILE='mysql-bin.xxxxxx',
    MASTER_LOG_POS=xxxx;
    START SLAVE;
    ```

6. **Verify the replication**:
   - On the slave container, run:
    ```sql
    SHOW SLAVE STATUS\G;
    ```
   - Ensure that `Slave_IO_Running` and `Slave_SQL_Running` are both `Yes`.

7. **Create user to connect from other hosts**:
   - On the slave container in mysql, run:
   ```sql
   CREATE USER 'app_user'@'%' IDENTIFIED BY 'app_pass';
   GRANT ALL PRIVILEGES ON car_rental_db.* TO 'app_user'@'%';
   FLUSH PRIVILEGES;
   ```
   - Check users:
   ```sql
   SELECT user, host, plugin FROM mysql.user;
   ```

8. **Run auto backup creation**:
   - First create new directory:
   ```bash
   mkdir backups
   ```
   - Create new script named auto_backup.sh:
   ```bash
   #!/bin/bash

    perform_task() {
        docker exec mysql-master mysqldump -u root -proot_pass car_rental_db > backups/db_backup_$( date +"%Y_%m_%d_%H:%M:%S" ).sql
    }

    main() {
        while true; do
            perform_task
            sleep 60
        done
    }

    main &
   ```
   
   - Modify premission to make it executable and run:
   ```bash
   chmod +x auto_backup.sh
   ./auto_backup.sh
   ```

   - To kill the process use `ps` to find PID and then:
   ```bash
   kill [PID]
   ```

9. **Commands to verify end-to-end connection on host**:
  - Launch MySQL server on host:
  ```bash
  cd C:\Program Files\MySQL\MySQL Server 8.0\bin
  mysql.exe -h [virtual machine address] -P [VM port, ex. 3306] -u [username, ex. root, replication_user] -p
  ```

  - Show available databases:
  ```bash
  SHOW DATABASES;
  ```

  - Choose database:
  ```bash
  USE [database name];
  ```

  - Show database tables:
  ```bash
  SHOW TABLES;
  ```

# Running
Running fastAPI:
```bash
uvicorn API_main:app --reload
```

# SQL Injection
SQL Injection prevented (visit http://localhost:8000/docs# to see in better format). The bash command below is equivalent to typing `' or '1'='1` in brand parameter. 
```bash
curl -X 'GET' 'http://localhost:8000/api/v1/cars_vulnerable?brand=%27%20or%20%271%27%3D%271' -H 'accept: application/json'
```
This should return list of all the cars in the database.

# Modify Database
To create new encrypted column, run:
```sql
CREATE TABLE new_table (
  ...
) ENGINE=InnoDB ENCRYPTION='Y';
```
To check whether table is encrypted, run:
```sql
SELECT TABLE_SCHEMA, TABLE_NAME, CREATE_OPTIONS 
FROM INFORMATION_SCHEMA.TABLES;
```
You can specify one table by adding `WHERE TABLE_NAME = '[your_table]';`

# Side notes
Column encryption:
https://serverfault.com/questions/538715/whats-a-good-way-to-encrypt-a-mysql-database-and-is-it-worth-it

Table encryption:
https://datachild.net/data/enabling-data-at-rest-encryption-in-mysql

Master-slave replication:
https://dev.to/siddhantkcode/how-to-set-up-a-mysql-master-slave-replication-in-docker-4n0a

Master-slave docker automatization:
https://github.com/vbabak/docker-mysql-master-slave

SSL connection:
https://peterkellner.net/2023/08/02/Enforcing-SSL-Connections-in-MySql-Using-Docker/