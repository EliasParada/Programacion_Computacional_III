import mysql.connector

class conection:
    def __init__(self):
        self.conn = mysql.connector.connect(host="localhost", user="root", port="3307", passwd="", database="fast_store")
        if self.conn.is_connected():
            print("\033[4;1;37;42m Conectado a la base de datos \033[0;m")
        else:
            print("\033[4;1;37;41m No se pudo conectar a la base de datos \033[0;m")

    def sql_run(self, sql, data):
        try:
            print('\033[4;1;37;42m Ejecutando sentencia SQL \033[0;m')
            print('\033[4;1;37;42m Sentencia: ' + sql + '\033[0;m')
            print('\033[4;1;37;42m Datos: ' + str(data) + '\033[0;m')
            cursor = self.conn.cursor()
            cursor.execute(sql, data)
            self.conn.commit()
            return True, {'status':'ok', 'msg':'Sentencia ejecutada correctamente'}
        except Exception as e:
            code = e.args[0]
            msg = e.args[1]
            return False, {'status':'ok', 'msg':'Error al ejecutar la sentencia SQL', 'code': [code, msg]}

    def sql_get(self, sql, data):
        try:
            print('\033[4;1;37;42m Ejecutando sentencia SQL \033[0;m')
            print('\033[4;1;37;42m Sentencia: ' + sql + '\033[0;m')
            print('\033[4;1;37;42m Datos: ' + str(data) + '\033[0;m')
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(sql, data)
            result = cursor.fetchall()
            return result, {'status':'ok', 'msg':'Sentencia ejecutada correctamente'}
        except Exception as e:
            code = e.args[0]
            msg = e.args[1]
            return False, {'status':'error', 'msg':'Error al ejecutar la sentencia SQL', 'code': [code, msg]}

    def generate_id(self, table):
        if table == 'users':
            sql = "SELECT MAX(ux_id) AS id FROM ux_users"
        elif table == 'products':
            sql = "SELECT MAX(prt_id) AS id FROM prt_producto"
        elif table == 'categories':
            sql = "SELECT MAX(cat_id) AS id FROM cat_categoria"
        elif table == 'providers':
            sql = "SELECT MAX(prov_id) AS id FROM prov_proveedor"
        elif table == 'features':
            sql = "SELECT MAX(pms_id) AS id FROM pms_permissions"
        elif table == 'bill':
            sql = "SELECT MAX(fac_id) AS id FROM fac_factura"
        elif table == 'carts':
            sql = "SELECT MAX(car_id) AS id FROM car_carrito"
        result = self.sql_get(sql, None)
        print(f'\033[4;1;37;42m Generando ID para: {table} \033[0;m', result[0][0]['id'])
        if result[1]['status'] == 'ok':
            if result[0][0]['id'] is None:
                print('\033[4;1;37;42m ID generado: \033[0;m', 1)
                return 1
            else:
                print('\033[4;1;37;42m ID generado: \033[0;m', result[0][0]['id'] + 1)
                return result[0][0]['id'] + 1
        else:
            return False