import conn

conn = conn.conection()
class crud:
    def admin_carts(self, data):
        try:
            print(data)
            # CREATE
            if data['action'] == 'create':
                sql = "INSERT INTO car_carrito (car_id, ux_id) VALUES (%s, %s)"
                id = conn.generate_id('carts')
                return conn.sql_run(sql, (id, data['id']))
            # UPDATE
            elif data['action'] == 'update': # Update
                sql = "INSERT INTO detcar_detallecarrito (car_id, prt_id, detcar_cantidad) VALUES (%s, %s, %s)"
                for i in data['products']:
                    print(i)
                    conn.sql_run(sql, (data['id'], i['idPrd'], i['quantity']))
                return True
            # DELETE
            elif data['action'] == 'delete':
                sql = "DELETE FROM detcar_detallecarrito WHERE detcar_detallecarrito.car_id = %s"
                return conn.sql_run(sql, (data['id'],))
                
        except Exception as e:
            print(e)
            code = e.args[0]
            msg = e.args[1]
            return False, {'status':'error', 'msg':'Error al ejecutar la acción', 'code': [code, msg]}

    def search_to(self, match, id):
        try:
            sql = "SELECT car_carrito.car_id, car_carrito.car_idusuario, car_carrito.car_idux FROM car_carrito WHERE car_carrito.car_idusuario LIKE %s OR car_carrito.car_idux LIKE %s LIMIT %s, %s"
            max_id = id-20
            if max_id < 0:
                max_id = 0
            return conn.sql_get(sql, (match, match, id, max_id))
        except Exception as e:
            print(e)
            code = e.args[0]
            msg = e.args[1]
            return False, {'status':'error', 'msg':'Error al ejecutar la acción', 'code': [code, msg]}

    def search_limit(self, id):
        try:
            sql = f"SELECT car_carrito.car_id, car_carrito.ux_id, detcar_detallecarrito.detcar_cantidad, prt_producto.prt_id, prt_producto.prt_name, prt_producto.prt_cost, prt_producto.prt_photo, ux_users.ux_name FROM car_carrito INNER JOIN detcar_detallecarrito ON car_carrito.car_id = detcar_detallecarrito.car_id INNER JOIN prt_producto ON detcar_detallecarrito.prt_id = prt_producto.prt_id INNER JOIN ux_users ON car_carrito.ux_id = ux_users.ux_id WHERE ux_users.ux_id = {id}"
            return conn.sql_get(sql, (None))
        except Exception as e:
            print(e)
            code = e.args[0]
            msg = e.args[1]
            return False, {'status':'error', 'msg':'Error al ejecutar la acción', 'code': [code, msg]}

    def get_cart(self, id):
        try:
            sql = "SELECT car_carrito.car_id, car_carrito.ux_id FROM car_carrito WHERE car_carrito.ux_id = %s"
            return conn.sql_get(sql, (id,))
        except Exception as e:
            print(e)
            code = e.args[0]
            msg = e.args[1]
            return False, {'status':'error', 'msg':'Error al ejecutar la acción', 'code': [code, msg]}