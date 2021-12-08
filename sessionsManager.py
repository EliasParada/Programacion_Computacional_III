import conn
import datetime
import random

conn = conn.conection()
class manager:
    def newSession(self, userData):
        try:
            print(userData)
            token = self.generateToken()
            print(token)
            sql = "SELECT * FROM sessions WHERE id_ses = %s AND sess_status = '1'"
            val = (token,)
            validToken = conn.sql_get(sql, val)
            print('VALIDAR',validToken)
            if len(validToken[0]) < 1:
                sql = ("INSERT INTO sessions (id_ses, ux_id, enter_date, pms_ux, sess_status) VALUES (%s, %s, %s, %s, %s)")
                val = (token, userData['ux_id'], datetime.datetime.now(), userData['pms_ux'], 1)
                conn.sql_run(sql, val)
                return token
            else:
                return self.newSession(userData)
        except:
            return False

    def closeSession(self, token):
        try:
            sql = ("UPDATE sessions SET sess_status = '0', exit_date = %s WHERE id_ses = %s")
            val = (datetime.datetime.now(), token)
            conn.sql_run(sql, val)
            return True
        except:
            return False

    def isLogged(self, token):
        try:
            sql = ("SELECT * FROM sessions WHERE id_ses = %s AND sess_status = 1")
            val = (token,)
            result = conn.sql_get(sql, val)
            print(len(result[0]) == 1)
            if len(result[0]) == 1:
                return True
            else:
                return False
        except:
            return False

    def isAdmin(self, token):
        try:
            sql = ("SELECT * FROM sessions WHERE id_ses = %s AND sess_status = 1 AND pms_ux = 1")
            val = (token,)
            result = conn.sql_get(sql, val)
            if len(result[0]) == 1:
                return True
            else:
                return False
        except:
            return False

    def generateToken(self):
        token = ''
        for i in range(16):
            token += random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        return token