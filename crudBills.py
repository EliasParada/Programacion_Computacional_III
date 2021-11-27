import conn

conn = conn.conection()
class crud:
    # Crud para las facturas, que contiene dos tablas:
    # fac_factura:
    #   fac_id: id de la factura, ux_id: id del usuario que realiza la factura, fac_date: fecha de la factura, fac_price: total de la factura
    # detfac_detallefactura:
    #   fac_id: id de la factura, prt_id: id del producto, detfac_cantidad: cantidad del producto, detfac_subprice: precio del producto
    def admin_bill(self, data):
        try:
            # CREATE
            if data['action'] == 'create':
                sql = "INSERT INTO fac_factura (fac_id, ux_id, fac_date, fac_price) VALUES (%s, %s, %s, %s)"
                id = conn.generate_id('bill')
                return conn.sql_run(sql, (id, data['idusuario'], data['date'], data['price']))
            # UPDATE
            elif data['action'] == 'update': # Update
                sql = "UPDATE fac_factura SET ux_id = %s, fac_date = %s, fac_price = %s WHERE fac_id = %s"
                return conn.sql_run(sql, (data['idusuario'], data['date'], data['price'], data['id']))
            # DELETE
            elif data['action'] == 'delete':
                sql = "DELETE FROM fac_factura WHERE fac_id = %s"
                return conn.sql_run(sql, (data['id'],))
        except Exception as e:
            code = e.args[0]
            msg = e.args[1]
            return False, {'status':'error', 'msg':'Error al ejecutar la acción', 'code': [code, msg]}

    def search_to(self, match, id):
        sql = "SELECT fac_factura.fac_id, fac_factura.ux_id, fac_factura.fac_date, fac_factura.fac_price FROM fac_factura WHERE fac_factura.ux_id LIKE %s OR fac_factura.fac_id LIKE %s LIMIT %s, %s"
        max_id = id-20
        if max_id < 0:
            max_id = 0
        return conn.sql_get(sql, (match, match, id, max_id))

    def search_limit(self, id):
        sql = "SELECT fac_factura.fac_id, fac_factura.ux_id, fac_factura.fac_date, fac_factura.fac_price FROM fac_factura LIMIT %s, %s"
        max_id = id-20
        if max_id < 0:
            max_id = 0
        return conn.sql_get(sql, (id, max_id))