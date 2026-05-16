#!/bin/bash
set -e

mariadb -u root -p"$MARIADB_ROOT_PASSWORD" <<-INIT_SCRIPT
  CREATE DATABASE IF NOT EXISTS metrics_monitor_db;
  CREATE USER IF NOT EXISTS 'dbusr'@'%' IDENTIFIED BY 'W4lFRuS0wosPePhL6Otr';
  GRANT ALL PRIVILEGES ON metrics_monitor_db.* TO 'dbusr'@'%';
  FLUSH PRIVILEGES;
INIT_SCRIPT