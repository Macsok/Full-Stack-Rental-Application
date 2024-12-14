# Full-Stack-Rental-Application
to be completed...

# Setting up Master-Slave database
Setting up a master-slave database replication involves configuring one database server (the master) to replicate its data to other database servers (in this case single slave). This setup is useful for load balancing, data redundancy, and backup purposes. Below are the steps to set up master-slave replication using Docker and Docker Compose.

## Instructions to enable and run master-slave replication on a virtual machine

1. **Install Docker and Docker Compose**:
- Follow the official Docker installation guide for your operating system: https://docs.docker.com/get-docker/
- Install Docker Compose: https://docs.docker.com/compose/install/

> [!TIP]
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
        image: mysql:8.0
        container_name: mysql-master
        command: --server-id=1 --log-bin=mysql-bin --binlog-format=row
        environment:
        MYSQL_ROOT_PASSWORD: root_pass
        MYSQL_DATABASE: car_rental_db
        MYSQL_USER: replication_user
        MYSQL_PASSWORD: user_pass
        ports:
        - "3306:3306"

    mysql-slave:
        image: mysql:8.0
        container_name: mysql-slave
        depends_on:
        - mysql-master
        command: --server-id=2 --log-bin=mysql-bin --binlog-format=row
        environment:
        MYSQL_ROOT_PASSWORD: root_pass
        MYSQL_DATABASE: car_rental_db
        MYSQL_USER: replication_user
        MYSQL_PASSWORD: user_pass
        ports:
        - "3307:3306"
    ```

3. **Start the Docker containers**:
   - Run the following command to start the containers:
     ```sh
     docker-compose up -d
     ```

4. **Configure the Master database**:
   - Access the master container:
    ```sh
    docker exec -it master mysql -u root -p root_pass
    ```
   - Run the following SQL commands to configure the master:
    ```sql
    ALTER USER 'replication_user'@'%' IDENTIFIED WITH 'mysql_native_password' BY 'replication_password';
    GRANT REPLICATION SLAVE ON *.* TO 'replication_user'@'%';
    FLUSH PRIVILEGES;
    SHOW MASTER STATUS;
    ```
   - Note the `File` and `Position` values from the `SHOW MASTER STATUS` output.

5. **Configure the Slave database**:
   - Access the slave container:
    ```sh
    docker exec -it slave mysql -u root -p root_pass
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

# Read more
- https://dev.to/siddhantkcode/how-to-set-up-a-mysql-master-slave-replication-in-docker-4n0a