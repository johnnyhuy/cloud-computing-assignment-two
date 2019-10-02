#!/bin/bash

# This is a quick script to seed the database
# Run on only on a clean database or a newly created MySQL database server
# Prerequisites: mysqldump and bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
usage() { echo "Usage: $0 [-d <database>] [-u <username>] [-p <password>] [-h <host>]" 1>&2; exit 1; }

while getopts ":d:u:p:h:" o; do
    case "${o}" in
        d)
            database=${OPTARG}
            ;;
        u)
            username=${OPTARG}
            ;;
        p)
            password=${OPTARG}
            ;;
        h)
            host=${OPTARG}
            ;;
        *)
            usage
            ;;
    esac
done

if [ -z "${username}" ] || [ -z "${password}" ]; then
    usage
    exit 1
fi

mysql -u ${username} --password=${password} -h ${host} < ${DIR}/000_create_database.sql
mysql -u ${username} --password=${password} -h ${host} -D ${database} < ${DIR}/001_dump.sql
