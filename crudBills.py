import conn

conn = conn.conection()
class crud:
    def admin_bill(self, data):
        try:
            # CREATE
            if data['action'] == 'create':
                sql = "INSERT INTO fac_factura (fac_id, ux_id, fac_date, fac_price) VALUES (%s, %s, %s, %s)"
                id = conn.generate_id('bill')
                conn.sql_run(sql, (id, data['user'], data['date'], data['total']))
                for product in data['products']:
                    sql = "INSERT INTO detfac_detallefactura (fac_id, prt_id, detfac_cantidad, detfac_subprice) VALUES (%s, %s, %s, %s)"
                    conn.sql_run(sql, (id, product['id'], product['cant'], product['subprice']))
                return True, {'status':'ok', 'msg':'Sentencia ejecutada correctamente'}

            # UPDATE
            elif data['action'] == 'update': # Update
                sql = "DELETE FROM detfac_detallefactura WHERE fac_id = %s"
                conn.sql_run(sql, (data['id'],))
                sql = "UPDATE fac_factura SET fac_date = %s, fac_price = %s WHERE fac_id = %s"
                conn.sql_run(sql, (data['date'], data['total'], data['id']))
                for product in data['products']:
                    sql = "INSERT INTO detfac_detallefactura (fac_id, prt_id, detfac_cantidad, detfac_subprice) VALUES (%s, %s, %s, %s)"
                    conn.sql_run(sql, (data['id'], product['id'], product['cant'], product['subprice']))
                return True, {'status':'ok', 'msg':'Sentencia ejecutada correctamente'}

            # DELETE
            elif data['action'] == 'delete':
                sql = "DELETE FROM detfac_detallefactura WHERE fac_id = %s"
                conn.sql_run(sql, (data['id'],))
                sql = "DELETE FROM fac_factura WHERE fac_id = %s"
                conn.sql_run(sql, (data['id'],))
                return True, {'status':'ok', 'msg':'Sentencia ejecutada correctamente'}

        except Exception as e:
            print(e)
            code = e.args[0]
            msg = e.args[1]
            return False, {'status':'error', 'msg':'Error al ejecutar la acción', 'code': [code, msg]}

    def search_to(self, match, id):
        try:
            sql = "SELECT fac_factura.fac_id, fac_factura.ux_id, fac_factura.fac_date, fac_factura.fac_price FROM fac_factura WHERE fac_factura.ux_id LIKE %s OR fac_factura.fac_id LIKE %s LIMIT %s, %s"
            max_id = 20 - id
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
            sql = "SELECT fac_factura.fac_id, fac_factura.ux_id, fac_factura.fac_date, fac_factura.fac_price, GROUP_CONCAT(prt_producto.prt_id) AS id_prd, GROUP_CONCAT(prt_producto.prt_name) AS prd_name, GROUP_CONCAT(detfac_detallefactura.detfac_cantidad) AS prd_cant, GROUP_CONCAT(detfac_detallefactura.detfac_subprice) AS subprice, ux_users.ux_name FROM fac_factura INNER JOIN detfac_detallefactura ON fac_factura.fac_id = detfac_detallefactura.fac_id INNER JOIN ux_users ON fac_factura.ux_id = ux_users.ux_id INNER JOIN prt_producto ON detfac_detallefactura.prt_id = prt_producto.prt_id GROUP BY fac_factura.fac_id"
            return conn.sql_get(sql, (None))
        except Exception as e:
            print(e)
            code = e.args[0]
            msg = e.args[1]
            return False, {'status':'error', 'msg':'Error al ejecutar la acción', 'code': [code, msg]}
