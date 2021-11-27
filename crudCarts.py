import conn

conn = conn.conection()
class crud:
    def admin_carts(self, data):
        try:
            # CREATE
            if data['action'] == 'create':
                sql = "INSERT INTO car_carrito (car_id, car_idusuario, car_idux) VALUES (%s, %s, %s)"
                id = conn.generate_id('carts')
                return conn.sql_run(sql, (id, data['idusuario'], data['idux']))
            # UPDATE
            elif data['action'] == 'update': # Update
                sql = "UPDATE car_carrito SET car_idusuario = %s, car_idux = %s WHERE car_id = %s"
                return conn.sql_run(sql, (data['idusuario'], data['idux'], data['id']))
            # DELETE
            elif data['action'] == 'delete':
                sql = "DELETE FROM car_carrito WHERE car_id = %s"
                return conn.sql_run(sql, (data['id'],))
        except Exception as e:
            code = e.args[0]
            msg = e.args[1]
            return False, {'status':'error', 'msg':'Error al ejecutar la acción', 'code': [code, msg]}

    def search_to(self, match, id):
        sql = "SELECT car_carrito.car_id, car_carrito.car_idusuario, car_carrito.car_idux FROM car_carrito WHERE car_carrito.car_idusuario LIKE %s OR car_carrito.car_idux LIKE %s LIMIT %s, %s"
        max_id = id-20
        if max_id < 0:
            max_id = 0
        return conn.sql_get(sql, (match, match, id, max_id))

    def search_limit(self, id):
        sql = "SELECT car_carrito.car_id, car_carrito.car_idusuario, car_carrito.car_idux FROM car_carrito LIMIT %s, %s"
        max_id = id-20
        if max_id < 0:
            max_id = 0
        return conn.sql_get(sql, (id, max_id))