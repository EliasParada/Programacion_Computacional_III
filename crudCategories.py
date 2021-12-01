import conn

conn = conn.conection()
class crud:
    def admin_categories(self, data):
        try:
            # CREATE
            if data['action'] == 'create':
                sql = "INSERT INTO cat_categoria (cat_id, cat_name, cat_description) VALUES (%s, %s, %s)"
                id = conn.generate_id('categories')
                return conn.sql_run(sql, (id, data['name'], data['description']))
            # UPDATE
            elif data['action'] == 'update': # Update
                sql = "UPDATE cat_categoria SET cat_name = %s, cat_description = %s WHERE cat_id = %s"
                return conn.sql_run(sql, (data['name'], data['description'], data['id']))
            # DELETE
            elif data['action'] == 'delete':
                sql = "DELETE FROM cat_categoria WHERE cat_id = %s"
                return conn.sql_run(sql, (data['id'],))
        except Exception as e:
            code = e.args[0]
            msg = e.args[1]
            return False, {'status':'error', 'msg':'Error al ejecutar la acción', 'code': [code, msg]}

    def search_to(self, match, id):
        sql = "SELECT cat_categoria.cat_id, cat_name, cat_categoria.cat_description FROM cat_categoria WHERE cat_name LIKE %s OR cat_categoria.cat_description LIKE %s LIMIT %s, %s"
        max_id = 20 - id
        if max_id < 0:
            max_id = 0
        return conn.sql_get(sql, (match, match, id, max_id))

    def search_limit(self, id):
        sql = "SELECT cat_categoria.cat_id, cat_name, cat_categoria.cat_description FROM cat_categoria LIMIT %s, %s"
        max_id = 20 - id
        if max_id < 0:
            max_id = 0
        return conn.sql_get(sql, (id, max_id))