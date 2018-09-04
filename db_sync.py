# this is a snarky comment
import ConfigParser
import os
import sys
import time
import glob

from dotenv import load_dotenv
dotenv_path = os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_path)

filestamp = time.strftime('%Y-%m-%d-%I:%M')

devs_db_user = os.getenv("devs_db_user")
devs_db_password = os.getenv("devs_db_password")
devs_db_host = os.getenv("devs_db_host")
devs_db = os.getenv("devs_db")
devs_db_file = "devs_db_"+filestamp+".gz"
devs_db_list = [devs_db_user, devs_db_password, devs_db_host, devs_db, devs_db_file]

sophs_uat_db_user = os.getenv("sophs_uat_db_user")
sophs_uat_db_password = os.getenv("sophs_uat_db_password")
sophs_uat_db_host = os.getenv("sophs_uat_db_host")
sophs_uat_db = os.getenv("sophs_uat_db")
sophs_uat_db_file = "sophs_uat_db_"+filestamp+".gz"
sophs_uat_db_list = [sophs_uat_db_user, sophs_uat_db_password, sophs_uat_db_host, sophs_uat_db, sophs_uat_db_file]

main_uat_db_user = os.getenv("main_uat_db_user")
main_uat_db_password = os.getenv("main_uat_db_password")
main_uat_db_host = os.getenv("main_uat_db_host")
main_uat_db = os.getenv("main_uat_db")
main_uat_db_file = "main_uat_db"+filestamp+".gz"
main_uat_db_list = [main_uat_db_user, main_uat_db_password, main_uat_db_host, main_uat_db, main_uat_db_file]


def get_dump(db):
    os.popen("mysqldump -u %s -p%s -h %s %s | gzip -c > %s 2>/dev/null" % (db[0], db[1], db[2], db[3], db[4]))
    return db[4]


def copy_over(db,source):
    os.popen("gunzip < %s |  mysql -u %s -p%s -h %s %s 2>/dev/null" % (source, db[0], db[1], db[2], db[3]))
    print "The database has been synced :)"


if __name__=="__main__":
    print ""
    print ""
    print "Welcome to Soph's Database Sycronisation Program"
    print ""
    print "Please select which option you wish to run:"
    print "1. Update Dev's Database from Soph's UAT Database"
    print "2. Update Soph's UAT Database from Main UAT Database"
    print "3. Update Main UAT Database from Soph's UAT Database"
    print "4. Delete all backup dumps"
    option_selected = input()
    if option_selected == 1:
        print "You selected option 1"
        source_db = get_dump(sophs_uat_db_list)
        get_dump(devs_db_list)
        copy_over(devs_db_list,source_db)
        os.remove(sophs_uat_db_list[4])
    elif option_selected == 2:
        print "You selected option 2"
        source_db = get_dump(main_uat_db_list)
        get_dump(sophs_uat_db_list)
        copy_over(sophs_uat_db_list,source_db)
        os.remove(main_uat_db_list[4])
    elif option_selected == 3:
        print "You selected option 3 - Are you sure you want to overwrite the main_uat database? yes=1 / no=0"
        overwrite_confirmed=input()
        if overwrite_confirmed == 1:
            source_db = get_dump(sophs_uat_db_list)
            get_dump(main_uat_db_list)
            copy_over(main_uat_db_list,source_db)
            os.remove(sophs_uat_db_list[4])
    elif option_selected == 4:
        print "You selected option 4 - Are you sure you want to delete all back up dumps? yes=1 / no=0"
        delete_confirmed = input()
        if delete_confirmed == 1:
            filelist=(glob.glob("devs*.gz"))
            for filename in filelist:
                os.remove(filename)
            filelist=(glob.glob("sophs*.gz"))
            for filename in filelist:
                os.remove(filename)
            filelist=(glob.glob("main*.gz"))
            for filename in filelist:
                os.remove(filename)
            print "All dump file have been deleted"
        else:
            print"All dump files are intact"