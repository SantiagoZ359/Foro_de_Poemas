# Programacion

En este proyecto la idea es crear una foro de poemas para un grupo selecto de escritores, pero que tambien sea visible para x usuarios, pero solo los poetas o usuarios registrados tengan permisos para subir poemas, comentarlos y ponerles una calificacion.

Lo primero que hicimos fue crear el entorno virtual con flask que es un microframework (es un marco de aplicaciones web mas minimalista, que se enfoca mas en el manejo de solicitudes http) escrito en py para crear una aplicacion web rapidamente y con un minimo numero de lineas

Despues procedimos a crear la api rest con cURL, que consiste en una bliblioteca y un interprete de comandos orientado a la trasferencia de archivos

Despues creamos la base de datos, eligimos una base de tipo sql por su facil uso con py y porque solo vamos a almacenar datos en formato plano(nada de contenido digital). Lo que hicimos fue crear las relaciones entre tablas.

Siguiendo con el backend implementamos los metodos de autentificacion (login) hay un register pero lo deje comentado porque no lo usamos en este proyecto, protegimos las rutas mediante JWT (que es json web token que se almacena en las cookies, que es principalmente para los usuarios registrados Token JWT = Es una cadena de texto que esta codificada en Base64, la cual tiene 3 partes, la cabecera (donde se indica el algoritmo y el tipo de token), el payload (datos de usuario y privilegios) y el cuerpo del mensaje que es la firma (nos permite verificar si el token es válido). Tienen un ciclo de vida en este caso son 3600 seg.

Despues definimos el envio de mail que fue con la libreria email sending de flask, que le llega un correo al poeta cuando su poema recibio un comentario y cuando es registrado

Despues comenzamos con el frontend que fue disenhando los bocetos, despues Procedemos a volcar nuestras maquetas a codigo, realizando nuestros primero HTML TEMPLATES y codeando algunos estilos adicionales en CSS. Ya que hicimos uso de Bootstrap para la creacion de las mismas, teniendo como ejemplo guia de codigo algunas navbars, tablas, formularios, etc, que aparecian en su pagina web. 

Despues enrutamos el servidor flask Con la ayuda de librerias como redirect, render_templates, url_for, etc, que son propias de Flask, comenzamos con el enrutamiento de nuestra pagina. Pudiendo realizar los primeros desplazamientos entre los diferentes templates con los botones que habiamos creado en los mismos. 

Para renderizar los templates usamos Jinja2 es un motor de renderizado de Flask el cual lo implementamos para no tener tanto código repetido en nuestros templates. Lo que hicimos fue crear un 'base.html' el cual, como su nombre lo indica, tiene todas las partes que se repetirian en todos los templates como navbars, menus, footer, etc. Nos ayuda a poder integrar todo esto en los demas templates sin tener que repetir esto en cada uno de ellos. 

Por ultimo las requests y proteccion de las vistas Por último lo que hicimos fue terminar de enlazar nuestro servidor Backend con el servidor Frontend a través de Requests a la base de datos. Lo que hacemos es tomar todas las peticiones que realiza el usuario a traves de la página, enviarlas a al Backend en forma de consulta y este a su vez, tambien devolver una respuesta con consultas. Y por supuesto, protegimos todas las vistas para que los usuarios que no estuvieran logueados no puedan acceder a rutas en donde sea necesario el token.

Algunos Requerimientos usados:

Que programas se usa:

    Backend
    cURL es un proyecto de software consistente en una biblioteca y un intérprete de comandos orientado a la transferencia de archivos
    Flask: es un microframework escrito en Python que permite crear aplicaciones web rápidamente y con un mínimo número de líneas de código.
    Un ORM es un modelo de programación que permite mapear las estructuras de una base de datos relacional (SQL Server, Oracle, MySQL, etc.), en adelante RDBMS (Relational Database Management System), sobre una estructura lógica de entidades con el objeto de simplificar y acelerar el desarrollo de nuestras aplicaciones.
    JWT = es un estandar que esta dentro de los RFC. Basicamente es un mecanismo de proteccion, el cual garantiza que la comunicacion entre el frontend y el backend va a ser segura y no se revelará la información dentro de esa comunicación. Codificados en objetos de tipo JSON.
    Token JWT = Es una cadena de texto que esta codificada en Base64, la cual tiene 3 partes, la cabecera (donde se indica el algoritmo y el tipo de token), el payload (datos de usuario y privilegios) y el cuerpo del mensaje que es la firma (nos permite verificar si el token es válido). Tienen un ciclo de vida.
    MySQLAlchemy: Manejo de base de datos mediante ORM.
    Werkzeug: Encriptado de la contraseña. Backend.
    Flask-JWT-Extended: Manejo de JSON Web Token


    Frontend
    Jinja2: Motor de plantilla web, para el lenguaje de programación Python.
    Insomnia: Insomnia es un cliente REST multiplataforma, con una interfaz clara y sencilla. Nos permite crear variables para poder utilizarlas en diferentes consultas.
    PyJWT: Manejo de JSON Web Token.
    Requests: requests es una librería Python que facilita enormemente el trabajo con peticiones HTTP.
    HTTP Request: La petición o HTTP request es el mensaje que se envía desde el cliente al servidor para solicitar un resource. GET POST

