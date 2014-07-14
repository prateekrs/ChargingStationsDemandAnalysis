import os, sys
import MySQLdb


class Database:
    # host="research.czxveiixjbkr.us-east-1.rds.amazonaws.com"
    # user="user"
    # password="tw33ter12"
    # db="twitterresearch"

    host='localhost'
    user='root'
    password='yourpassword'
    db='solar_marketing'

    def __init__(self):
        self.connection = MySQLdb.connect(self.host, self.user, self.password, self.db)
        self.cursor = self.connection.cursor()

    def query(self, query):
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()

        except Exception as e:
            print sys.exc_info()
            print "broken"


def query(county_name):
    db = Database()
    print('Starting queries')

    if county_name == 'San Francisco':
        query = """SELECT us_solar_installations.col_installer_clean, addresses.latitude, addresses.longitude, us_solar_installations.col_date, addresses.property_area_sqft, addresses.property_class_code, addresses.year_built, addresses.assessed_land_value, addresses.assessed_personal_prop_value, addresses.property_area_sqft
                        FROM addresses LEFT JOIN us_solar_installations ON  addresses.col_app_num_original_fkey = us_solar_installations.col_app_num_original 
                        WHERE addresses.city = %s"""
    else:
        query = """SELECT us_solar_installations.col_installer_clean, addresses.latitude, addresses.longitude, us_solar_installations.col_date, addresses.property_area_sqft, addresses.property_class_code, addresses.year_built, addresses.assessed_land_value, addresses.assessed_personal_prop_value, addresses.property_area_sqft
                        FROM addresses LEFT JOIN us_solar_installations ON  addresses.col_app_num_original_fkey = us_solar_installations.col_app_num_original 
                        WHERE addresses.county = %s"""

    args = ["{this_name}".format(this_name=county_name)] 
    
    db.cursor.execute(query, args)
    return db.cursor.fetchall()