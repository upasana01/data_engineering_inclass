# this program loads Census ACS data using basic, slow INSERTs
# run it with -h to see the command line options

import time
import psycopg2
import argparse
import re
import csv

DBname = "postgres"
DBuser = "postgres"
DBpwd = "BadPassword"
TableName = "CensusData"
Datafile = "filedoesnotexist"  # name of the data file to be loaded
CreateDB = False  # indicates whether the DB table should be (re)-created


def initialize():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--datafile", required=True)
    parser.add_argument("-c", "--createtable", action="store_true")
    args = parser.parse_args()

    global Datafile
    Datafile = args.datafile
    global CreateDB
    CreateDB = args.createtable


# connect to the database
def dbconnect():
    connection = psycopg2.connect(
        host="localhost",
        database=DBname,
        user=DBuser,
        password=DBpwd,
    )

    return connection


def createTable(conn):
    with conn.cursor() as cursor:
        cursor.execute(
            f"""
			DROP TABLE IF EXISTS {TableName};
			CREATE TABLE {TableName} (
				CensusTract         NUMERIC,
				State               TEXT,
				County              TEXT,
				TotalPop            INTEGER,
				Men                 INTEGER,
				Women               INTEGER,
				Hispanic            DECIMAL,
				White               DECIMAL,
				Black               DECIMAL,
				Native              DECIMAL,
				Asian               DECIMAL,
				Pacific             DECIMAL,
				Citizen             DECIMAL,
				Income              DECIMAL,
				IncomeErr           DECIMAL,
				IncomePerCap        DECIMAL,
				IncomePerCapErr     DECIMAL,
				Poverty             DECIMAL,
				ChildPoverty        DECIMAL,
				Professional        DECIMAL,
				Service             DECIMAL,
				Office              DECIMAL,
				Construction        DECIMAL,
				Production          DECIMAL,
				Drive               DECIMAL,
				Carpool             DECIMAL,
				Transit             DECIMAL,
				Walk                DECIMAL,
				OtherTransp         DECIMAL,
				WorkAtHome          DECIMAL,
				MeanCommute         DECIMAL,
				Employed            INTEGER,
				PrivateWork         DECIMAL,
				PublicWork          DECIMAL,
				SelfEmployed        DECIMAL,
				FamilyWork          DECIMAL,
				Unemployment        DECIMAL
			);	
		"""
        )

        print(f"Created {TableName}")
    conn.cursor().execute(
        f""" ALTER TABLE {TableName} ADD PRIMARY KEY (CensusTract);
			CREATE INDEX idx_{TableName}_State ON {TableName}(State); """
    )


def load(conn, datafile):
    with conn.cursor() as cursor:
        start = time.perf_counter()

        with open(datafile, "r") as f:
            cursor.copy_expert(f"COPY {TableName} FROM STDIN WITH CSV HEADER", f)

        elapsed = time.perf_counter() - start
        print(f"Finished Loading. Elapsed Time: {elapsed:0.4} seconds")


def main():
    initialize()
    conn = dbconnect()

    if CreateDB:
        createTable(conn)

    load(conn, Datafile)


if __name__ == "__main__":
    main()
