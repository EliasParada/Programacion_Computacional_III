import conn

conn = conn.conection()
class crud:
    def admin_users(self, data):
        try:
            # CREATE
            if data['action'] == 'create':
                sql = "INSERT INTO ux_users (ux_id, ux_dui, ux_name, ux_nick, ux_phone, ux_mail, ux_pass, ux_DBirth, ux_urlphoto, pms_ux) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                id = conn.generate_id('users')
                return conn.sql_run(sql, (id, data['dui'], data['name'], data['nick'], data['phone'], data['mail'], data['pass'], data['dbirth'], 'img/users/profile'+str(id)+'.jpg', data['permiss'])), id
            # UPDATE
            elif data['action'] == 'update':
                sql = "UPDATE ux_users SET ux_dui = %s, ux_name = %s, ux_nick = %s, ux_phone = %s, ux_mail = %s, ux_pass = %s, ux_DBirth = %s, ux_urlphoto = %s, pms_ux = %s WHERE ux_id = %s"
                return conn.sql_run(sql, (data['dui'], data['name'], data['nick'], data['phone'], data['mail'], data['pass'], data['dbirth'], 'img/users/profile'+str(data['id'])+'.jpg', data['permiss'], data['id']))
            # DELETE
            elif data['action'] == 'delete':
                sql = "DELETE FROM ux_users WHERE ux_id = %s"
                return conn.sql_run(sql, (data['id'],))
        except Exception as e:
            code = e.args[0]
            msg = e.args[1]
            return False, {'status':'error', 'msg':'Error al ejecutar la acción', 'code': [code, msg]}

    def search_to(self, match, id):
        try:
            sql = "SELECT ux_users.ux_id, ux_users.ux_dui, ux_users.ux_name, ux_users.ux_nick, ux_users.ux_phone, ux_users.ux_mail, ux_users.ux_pass, ux_users.ux_DBirth, ux_users.ux_urlphoto, ux_users.pms_ux, pms_permissions.pms_type FROM ux_users INNER JOIN pms_permissions ON ux_users.pms_ux = pms_permissions.pms_id WHERE ux_users.ux_id LIKE %s OR ux_users.ux_dui LIKE %s ux_users.ux_name LIKE %s OR ux_users.ux_nick LIKE %s OR ux_users.ux_phone LIKE %s OR ux_users.ux_mail LIKE %s OR ux_users.ux_pass LIKE %s OR ux_users.ux_DBirth LIKE %s LIMIT %s, %s"
            max_id = 20 - id
            if max_id < 0:
                max_id = 0
            return conn.sql_get(sql, (match, match, match, match, match, match, match, match, id, max_id))
        except Exception as e:
            code = e.args[0]
            msg = e.args[1]
            return False, {'status':'error', 'msg':'Error al ejecutar la acción', 'code': [code, msg]}

    def show_limit(self, id):
        try:
            sql = "SELECT ux_users.ux_id, ux_users.ux_dui, ux_users.ux_name, ux_users.ux_nick, ux_users.ux_phone, ux_users.ux_mail, ux_users.ux_pass, ux_users.ux_DBirth, ux_users.ux_urlphoto, ux_users.pms_ux, pms_permissions.pms_type FROM ux_users INNER JOIN pms_permissions ON ux_users.pms_ux = pms_permissions.pms_id LIMIT %s, %s"
            max_id = 20 - id
            if max_id < 0:
                max_id = 0
            return conn.sql_get(sql, (id, max_id))
        except Exception as e:
            print(e)
            code = e.args[0]
            msg = e.args[1]
            return False, {'status':'error', 'msg':'Error al ejecutar la acción', 'code': [code, msg]}