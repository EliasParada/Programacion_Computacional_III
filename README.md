# Parcial II

## *Generalidades*

#### Integrantes:

*Integrantes* | *Código*
-|-
Carlos Manuel Ábrego Martínez|USIS044220
William Alexander Amaya García|USIS032120
José Daniel Mejía Jovel|USIS010420
Elías Mauricio Parada Lozano|USIS030320

#### Indicaciones:

> - Realizar una inteligencia artificial que convierta de grados celsius a fahrenheits, tal cueal se ha realizado en las practicas.
> - Realizar una página web que disponga de un campo necesario para ingresar los grados celsius y un contenedor para la respuesta en fahrenheits.
> - Hacer una petición AJAX que permita enviar el dato de la página web a un servidor local, el cual llamará a la AI para realizar la conversión, y retornar el valor.

## *Código*

###### :warning: **El código que se utilizo para la AI no se mostrará, puesto que se realizó en las clases prácticas.**

- El primer paso que realizamos fue la creación de la clase, la cual hicimos tal cual en la clase:

```Python
class basicServer(BaseHTTPRequestHandler):
```
- Ahora realizamos el metodo GET:
```Python
  def do_GET(self):
        print("GET")
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write('Server initialiced in 3004 port'.encode())
```
- Para finalizar agregar el metodo POST:
```Python
  def do_POST(self):
        print('POST')
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        data = data.decode()
        data = parse.unquote(data)
        data = float(data)

        predict = model.predict([data])
        print('La predicción fue:', predict)
        predict = str(predict[0][0])

        message = str(data) + ' C° son ' + predict + ' F°.'
        
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(message.encode())
```
- Hay que revisar el metodo POST pro partes
  - Primero se conseguen los datos.
  - Despues se decodifican los datos.
  - Luego se convierten los datos en decimales.
  - Y ahora se realiza la predicción.
  - Una vez obtenida la predicción la imprimimos en al terminal.
  - Ahora se crea una variable, que será el mensaje que se enviara.
  - Se envia una respuesta 200 al servidor.
  - Y finalmente se permite el acceso y control de cualquier origen y se envia el mensaje.

- Inicializar el servidor en el puerto 3004:
```Python
print('Initialized server')
server = HTTPServer(('localhost', 3004), basicServer)
server.serve_forever()
```
Una vez se ha realizado el servidor y la AI nos dirigimos a la página web, al documento index.html, en la que hacemos uso de la etiqueta `<form>`, en esta agregamos un `<input type="number">` y un `<input type="submit">` para los datos de ingreso y su envio, y fuera del formulario agregamos un `<div>` que contiene un `<span>`, el cual contendrá la respuesta que enviará nuestro servidor.

```HTML
<form action="POST" class="input active" id="input">
        <h2>Ingresa la cantidad en celcius</h2>
        <input type="number" placeholder="Ejemplo: 120.50"><br>
        <input type="submit" value="Convertir">
</form>
        
<div class="output" id="output">
        <span id="result">Convierte grados celcius a fahrenheits </span>
</div>
```
Ahora que creamos nuestro formulario es hora de agregar funcionalidad:
- Primero agregramos JQUERY y creamos una etiqueta `<script>` en la que ingresaremos nuestro código JS:
```HTML
<script src="https://code.jquery.com/jquery-3.6.0.js" integrity="sha256-H+K7U5CnXl1h5ywQfKtSj8PCmoN9aaq30gDh27Xc0jk=" crossorigin="anonymous"></script>
<script>
...
</script>
```
- Ahora agregamos la funcion que detecta cuando la página esta cargada, y dentro de ella, agregamos una variable que leerá todos los inputs en la página.
```JS
$(document).ready(e => {
        let inputs = $('input');
});
```
- Agregamos un evento `onsubmit` para el input numero 0, que corresponde al input de tipo númerico y un evento `onclick` para el input tipo submit, que es el 1, y creamos una variable calc que será la encargada de hacer la petición al servidor:
```JS
$(document).ready(e => {
        let inputs = $('input');
});
inputs[0].onsubmit = e => {
        console.log(inputs[0].value);
        calc(inputs[0].value);
};
inputs[1].onclick = e => {
        e.preventDefault();
        console.log(inputs[0].value);
        calc(inputs[0].value);
};
let calc = val => {
...
};
```
- Finalmente agregamos la petición, y dentro de ella haremos que cuando se ejecute al elemento con el id `result` adquiera el texto de la respuesta:
```JS
$.post("http://localhost:3004", val, response => {
        $('#result').text(response);
});
```
- Y luego de esto nuestra página debería funcionar con nuestro servidor.
