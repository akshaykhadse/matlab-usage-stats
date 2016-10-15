import MySQLdb


def pop_ldap(ip):
    db = MySQLdb.connect("10.200.18.6", "matlabuser", "matlabsql", "MATLAB")
    cursor = db.cursor()
    sql = "SELECT USERID FROM MATLAB_ACTIVE WHERE IP = '" + str(ip) + "' ORDER BY START_TIME_UNIX desc"
    print sql
#list1 = []
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) != 0:
            return results[0][0]
        else:
	    print "No entry in ACTIVE"
            sql = "SELECT USERID FROM MATLAB_ARCHIVE WHERE IP = '" + str(ip) +"' ORDER BY STOP_TIME_UNIX desc"
            print sql
            cursor.execute(sql)
            results = cursor.fetchall()
            return results[0][0]
    except:
        db.rollback()

