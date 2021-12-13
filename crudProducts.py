import conn

conn = conn.conection()
class crud:
    def admin_products(self, data):
        try:
            # CREATE
            if data['action'] == 'create':
                sql = "INSERT INTO prt_producto (prt_id, prt_name, prov_id, prt_createdate, prt_expirationdate, cat_id, prt_cost, prt_photo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                id = conn.generate_id('products')
                return conn.sql_run(sql, (id ,data['name'], data['prov'], data['createdate'], data['expirationdate'], data['cat'], data['cost'], 'img/products/product'+str(id)+'.jpg'))
            # UPDATE
            elif data['action'] == 'update':
                sql = "UPDATE prt_producto SET prt_name = %s, prov_id = %s, prt_createdate = %s, prt_expirationdate = %s, cat_id = %s, prt_cost = %s, prt_photo = %s WHERE prt_id = %s"
                return conn.sql_run(sql, (data['name'], data['prov'], data['createdate'], data['expirationdate'], data['cat'], data['cost'], 'img/products/product'+str(data['id'])+'.jpg', data['id']))
            # DELETE
            elif data['action'] == 'delete':
                sql = "DELETE FROM prt_producto WHERE prt_id = %s"
                return conn.sql_run(sql, (data['id'],))
        except Exception as e:
            print(e)
            code = e.args[0]
            msg = e.args[1]
            return False, {'status':'error', 'msg':'Error al ejecutar la acción', 'code': [code, msg]}

    def search_to(self, match, id):
        try:
            sql = "SELECT prt_producto.prt_id, prt_producto.prt_name, prov_proveedor.prov_id, prov_proveedor.prov_name, prt_producto.prt_createdate, prt_producto.prt_expirationdate, cat_categoria.cat_id, cat_categoria.cat_name, prt_producto.prt_cost, prt_producto.prt_photo FROM prt_producto INNER JOIN cat_categoria ON prt_producto.cat_id = cat_categoria.cat_id INNER JOIN prov_proveedor ON prt_producto.prov_id = prov_proveedor.prov_id WHERE prt_producto.prt_id LIKE %s OR prt_producto.prt_name LIKE %s OR prov_proveedor.prov_id LIKE %s OR prt_producto.prt_createdate LIKE %s OR prt_producto.prt_expirationdate LIKE %s OR cat_categoria.cat_name LIKE %s OR cat_categoria.cat_id LIKE %s OR prov_proveedor.prov_name LIKE %s OR prt_producto.prt_cost LIKE %s ORDER BY prt_producto.prt_id LIMIT %s, %s"
            max_id = 20 - id
            if max_id < 0:
                max_id = 0
            return conn.sql_get(sql, (match, match, match, match, match, match, match, match, match, id, max_id))
        except Exception as e:
            code = e.args[0]
            msg = e.args[1]
            return False, {'status':'error', 'msg':'Error al ejecutar la acción', 'code': [code, msg]}

    def show_limits(self, id):
        try:
            sql = "SELECT prt_producto.prt_id, prt_producto.prt_name, prov_proveedor.prov_id, prov_proveedor.prov_name, prt_producto.prt_createdate, prt_producto.prt_expirationdate, cat_categoria.cat_id, cat_categoria.cat_name, prt_producto.prt_cost, prt_producto.prt_photo FROM prt_producto INNER JOIN cat_categoria ON prt_producto.cat_id = cat_categoria.cat_id INNER JOIN prov_proveedor ON prt_producto.prov_id = prov_proveedor.prov_id ORDER BY prt_producto.prt_id"
            return conn.sql_get(sql, (None))
        except Exception as e:
            code = e.args[0]
            msg = e.args[1]
            return False, {'status':'error', 'msg':'Error al ejecutar la acción', 'code': [code, msg]}