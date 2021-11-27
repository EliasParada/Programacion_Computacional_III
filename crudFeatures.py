import conn

conn = conn.conection()
class crud:
    def admin_permissions(self, data):
        try:
            # CREATE
            if data['action'] == 'create':
                sql = "INSERT INTO pms_permissions (pms_id, pms_type) VALUES (%s, %s)"
                id = conn.generate_id('features')
                return self.sql_run(sql, (id, data['type']))
            # UPDATE
            elif data['action'] == 'update':
                sql = "UPDATE pms_permissions SET pms_type = %s WHERE pms_id = %s"
                return self.sql_run(sql, (data['id'], data['type']))
            # DELETE
            elif data['action'] == 'delete':
                sql = "DELETE FROM pms_permissions WHERE pms_id = %s"
                return self.sql_run(sql, (data['id'],))
        except Exception as e:
            code = e.args[0]
            msg = e.args[1]
            return False, {'status':'error', 'msg':'Error al ejecutar la acción', 'code': [code, msg]}

    def search_to(self, match, id):
        sql = "SELECT pms_permissions.pms_id, pms_permissions.pms_type FROM pms_permissions WHERE pms_permissions.pms_id = %s OR pms_permissions.pms_type = %s LIMIT %s, %s"
        max_id = id-20
        if max_id < 0:
            max_id = 0
        return self.sql_run(sql, (match, match, id, max_id))

    def search_limit(self, id):
        sql = "SELECT pms_permissions.pms_id, pms_permissions.pms_type FROM pms_permissions LIMIT %s, %s"
        max_id = id-20
        if max_id < 0:
            max_id = 0
        return self.sql_run(sql, (id, max_id))
        