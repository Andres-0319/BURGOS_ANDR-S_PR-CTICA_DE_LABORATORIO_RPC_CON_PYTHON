<div align="center">

# Universidad Politécnica Salesiana

# Carrera de Computación

# Asignatura de Sistemas Distribuidos

</div>

**Integrantes:** Burgos Andrés, Morales Pool, Narváez Cristian

**Fecha:** 04 de noviembre de 2026

**Tema:** Práctica de Laboratorio RPC con Python.

**Objetivos**
- Comprender el concepto de invocación de métodos remotos (RMI/RPC) y la arquitectura cliente-servidor en entornos distribuidos.
- Dominar el uso del Name Server de Pyro4 para la localización dinámica de objetos remotos.
- Implementar la gestión del estado (stateful vs stateless) mediante políticas de instancia de Pyro4.
- Resolver problemas de concurrencia y tolerancia a fallos en comunicaciones distribuidas.

**Desarrollo de la actividad**

<div align="center">

**Actividades prácticas dirigidas (Dificultad Ascendente)**

</div>

<div align="center">

**Desarrollo del Nivel 1: Calculadora Remota Básica (Fundamentos de RPC)**

</div>

**Paso 1:**

**Paso 2:**

**Paso 3:**

**Paso 4:**

**Paso 5:**

<div align="center">

**Desarrollo del Nivel 2: Sistema de Notificaciones con Name Server**

</div>

**Paso 1:**

**Paso 2:**

**Paso 3:**

**Paso 4:**

**Paso 5:**

<div align="center">

**Desarrollo del Nivel 3: Banco Distribuido y Control de Estado (Stateful Services)**

</div>

**Paso 1:** Se lleva a cabo la configuración del entorno de trabajo del sistema distribuido, accediendo a la terminal del sistema operativo Ubuntu para preparar las dependencias correspondientes a través de la creación de los entornos virtuales aislados a través del comando "python3 -m venv venv" dentro de la carpeta correspondiente. Con el entorno virtual ya operativo y seguro frente a las restricciones del sistema, se instaló la biblioteca de comunicación remota Pyro4 empleando el gestor de paquetes "pip" por medio del comando "pip install Pyro4", con el objetivo de descargar e integrar de manera automática los módulos escenciales requeridos para la serialización y el transporte de datos distribuidos.

<img width="643" height="377" alt="c1" src="https://github.com/user-attachments/assets/a44f60d9-9176-4382-8bad-ac53c2a82af5" />

**Paso 2:** Una vez que el servidor se encuentre activo y operativo en la primera terminal, se procede a levantar el servicio central del banco en una segunda ventana de consola independiente. Para que se pueda garantizar la consistencia en el espacio de trabajo correspondiente, se navegó hacia el directorio raíz del proyecto para activar el entorno virtual a través del comando de activación correspondiente asegurándose que las librerías previamente instaladas estuvieran disponibles para el intérprete de Python. Luego de realizar este proceso, se ejecuta el script correspondiente al servidor bancario escribiendo en la terminal la instrucción "python servidor_nivel_3.py".

<img width="790" height="121" alt="c2" src="https://github.com/user-attachments/assets/ac5ede51-cd80-40d6-9f79-feed4e4305da" />

**Paso 3:** Con la infraestructura del servidor y el Name Server plenamente operativas, se desplegó el primer cliente del sistema abriendo una tercera terminal independiente para que se pueda validar el flujo interactivo de las transacciones correspondientes. Luego de entrar en el directorio del proyecto y activar el entorno virtual, se ejecuta el script del cliente a través del comando "python cliente_nivel_3.py" en la que se solicita el nombre del usuario para establecer de forma transparente la conexión remota con el servidor utilizando la directiva de búsqueda por nombre "PYRONAME:nivel_3".

<img width="820" height="662" alt="c3_cliente_1" src="https://github.com/user-attachments/assets/04f21cab-03bd-4b45-881a-ae9900ced9a7" />

**Paso 4:** Para que se pueda comprobar el cumplimiento de los requerimientos de concurrencia y aislamiento de sesiones del Nivel 3, se abrió una cuarta terminal independiente, con el objetivo de ejecutar una instancia simultánea del cliente bajo la identidad de un nuevo usuario. Se ejecuta nuevamente el proceso de navegación y activación del entorno virtual para poner en marcha el programa cliente a a través del comando "python cliente_nivel_3.py", para que pueda interactuar con el menú del banco, ingresando cantidades considerables.

<img width="1020" height="610" alt="c4_cliente_2" src="https://github.com/user-attachments/assets/8722fd40-76d2-4174-ada2-d37610318c4d" />

**Paso 5:** Luego de cumplir con la activación del entorno virtual y la ejecución del script del cliente, el tercer usuario procede a interactuar con el sistema realizando un depósito de 900.00 en su cuenta bancaria exclusiva, recibiendo un mensaje de confirmación inmediata del servidor con su respectivo saldo actualizado, consolidando de forma definitiva la demostración del Nivel 3 y evidenciando que el sistema distribuido es capaz de administrar múltiples sesiones concurrentes de manera totalmente aislada, segura y tolerante a interacciones simultáneas.

<img width="1009" height="608" alt="c5_cliente_3" src="https://github.com/user-attachments/assets/86fe3598-5375-4a80-ab8d-1bcc34f6ff23" />

<div align="center">

**Desarrollo del Nivel 4: Procesamiento Concurrente y Callback Asíncrono**

</div>

**Paso 1:**

**Paso 2:**

**Paso 3:**

**Paso 4:**

**Paso 5:**

<div align="center">

**Caso de Estudio Integrador: Sistema Distribuido de Subastas en Tiempo Real**

</div>

**Paso 1:**

**Paso 2:**

**Paso 3:**

**Paso 4:**

**Paso 5:**

<div align="center">

**Proyecto Avanzado: Autenticación Multifactor (MFA) con Bot de Telegram y Pyro4**

</div>

**Paso 1:**

**Paso 2:**

**Paso 3:**

**Paso 4:**

**Paso 5:**

**Conclusiones**

- **CONCLUSION 1**
- **CONCLUSION 2**
