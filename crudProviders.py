import conn

conn = conn.conection()
class crud:
    def admin_provider(self, data):
        try:
            # CREATE
            if data['action'] == 'create':
                sql = "INSERT INTO prov_proveedor (prov_id, prov_name, prov_phone, prov_mail) VALUES (%s, %s, %s, %s)"
                id = conn.generate_id('providers')
                return conn.sql_run(sql, (id, data['name'], data['phone'], data['mail']))
            # UPDATE
            elif data['action'] == 'update':
                sql = "UPDATE prov_proveedor SET prov_name = %s, prov_phone = %s, prov_mail = %s WHERE prov_id = %s"
                return conn.sql_run(sql, (data['name'], data['phone'], data['mail'], data['id']))
            # DELETE
            elif data['action'] == 'delete':
                sql = "DELETE FROM prov_proveedor WHERE prov_id = %s"
                return conn.sql_run(sql, (data['id'],))
        except Exception as e:
            code = e.args[0]
            msg = e.args[1]
            return False, {'status':'error', 'msg':'Error al ejecutar la acción', 'code': [code, msg]}

    def search_to(self, match, id):
        sql = "SELECT prov_proveedor.prov_id, prov_proveedor.prov_name, prov_proveedor.prov_phone, prov_proveedor.prov_mail FROM prov_proveedor WHERE prov_proveedor.prov_name LIKE %s OR prov_proveedor.prov_phone LIKE %s OR prov_proveedor.prov_mail LIKE %s LIMIT %s, %s"
        max_id = 20 - id
        if max_id < 0:
            max_id = 0
        return conn.sql_get(sql, (match, match, match, id, max_id))

    def search_limit(self, id):
        sql = "SELECT prov_proveedor.prov_id, prov_proveedor.prov_name, prov_proveedor.prov_phone, prov_proveedor.prov_mail FROM prov_proveedor"
        return conn.sql_get(sql, (None))
