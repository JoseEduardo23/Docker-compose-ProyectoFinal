# 📦 Aplicación Web Distribuida con Docker, Flask, MySQL y NGINX

Este proyecto implementa una infraestructura distribuida utilizando contenedores Docker. Incluye múltiples instancias de una aplicación web desarrollada en Flask, una base de datos MySQL configurada con replicación maestro-esclavo, y un balanceador de carga NGINX que distribuye el tráfico entre los servicios. Todo está orquestado mediante Docker Compose para facilitar su despliegue y administración.

```

## 📁 Estructura del Proyecto
├── app/ # Contenedor principal con la app Flask
├── app1/ # Réplica 1 de la app Flask
├── app2/ # Réplica 2 de la app Flask
├── app3/ # Réplica 3 de la app Flask
├── mysql/
│ ├── master.cnf # Configuración del servidor maestro
│ ├── slave1.cnf # Configuración esclavo 1
│ ├── slave2.cnf # Configuración esclavo 2
│ └── slave3.cnf # Configuración esclavo 3
├── nginx/
│ └── nginx.conf # Configuración de NGINX como balanceador
├── docker-compose.yml
```

## 1️⃣ Contenedores de la Aplicación Web

Se implementan cuatro contenedores (`app`, `app1`, `app2`, `app3`) que ejecutan la misma aplicación Flask de forma independiente. Estas instancias están conectadas a la misma base de datos y responden a las solicitudes del balanceador NGINX.

#### Funcionalidades principales:
- - **Inicio de sesión** para usuarios autenticados.
- - **Registro de productos**, incluyendo nombre, código, descripción, unidad y categoría.
- - **Validación de códigos duplicados** antes de guardar nuevos productos.
- - **Consulta en tiempo real** del inventario de productos registrados.

#### Justificación:
Contar con varias instancias web permite mejorar la disponibilidad, repartir la carga entre nodos y escalar el sistema horizontalmente. Cada instancia es autónoma pero comparte la lógica y la base de datos.

---

## 2️⃣ Configuración del Balanceador de Carga (NGINX)

El contenedor NGINX está configurado como **balanceador de carga** para redirigir las peticiones entrantes a las diferentes instancias Flask usando la directiva `upstream`.

#### Características de configuración:
- - **Balanceo por peso**, asignando mayor prioridad a `app` (peso 3), seguido de `app1` (peso 2) y `app2`, `app3` (peso 1 cada uno).
- - **Encabezados personalizados** como `X-Forwarded-For`, `Host` y `X-Real-IP` para mantener la trazabilidad.
- - **Timeouts definidos** para evitar bloqueos por latencia.

#### Objetivo:
Distribuir el tráfico de forma controlada y eficiente, aprovechando más los nodos más potentes o prioritarios, y asegurando disponibilidad incluso si una instancia falla.

---

## 3️⃣ Replicación de la Base de Datos (MySQL)

El sistema de base de datos está compuesto por un contenedor maestro (`maestro1`) y tres esclavos (`slave1`, `slave2`, `slave3`). Todos están conectados mediante una red virtual privada y configurados con archivos `.cnf`.

#### Configuración del maestro:
- - `server-id=1`
- - `log-bin=mysql-bin`
- - `binlog-do-db=db_inventario`

#### Configuración de cada esclavo:
- - `server-id` único por contenedor.
- - `relay-log` activado.
- - Replicación configurada desde el maestro mediante `CHANGE MASTER TO`.

#### Propósito:
La replicación permite que los esclavos mantengan una copia sincronizada de la base de datos principal, lo cual permite escalar operaciones de lectura y garantizar tolerancia a fallos.

---

## 4️⃣ Orquestación con Docker Compose

El archivo `docker-compose.yml` define y administra todos los servicios, incluyendo aplicaciones web, base de datos, balanceador y phpMyAdmin.

#### Elementos clave:
- - **Servicios separados** por roles: app web, base de datos, balanceador.
- - **Red privada `inventarioApp`** para comunicar los servicios.
- - **`depends_on`** para asegurar el orden de inicio.
- - **Variables de entorno** para conexiones entre servicios.

#### Ventajas:
Docker Compose permite levantar toda la infraestructura con un solo comando, simplificando pruebas, despliegues y mantenimiento.

---

## 5️⃣ Persistencia y Volúmenes

Se utilizan tanto volúmenes *bind* como *named volumes*.

#### Volúmenes utilizados:
- - `./mysql/master.cnf:/etc/mysql/conf.d/my.cnf` → configuración del maestro.
- - `./mysql/slave1.cnf:/etc/mysql/conf.d/zz-slave1.cnf` (y similares) → configuración de esclavos.
- - `maestro_data:/var/lib/mysql` → persistencia de datos reales del maestro.
- - `slave1_data:/var/lib/mysql` (y similares) → persistencia en los esclavos.

#### Objetivo:
Evitar pérdida de datos y permitir personalización de cada contenedor sin modificar las imágenes base.

---

## 6️⃣ Pruebas de Carga

Se realizaron pruebas con ApacheBench (`ab`) para simular múltiples usuarios concurrentes.

#### Comando de prueba:
```bash
ab -n 1000 -c 100 http://localhost/


## Presentacion Canva
https://www.canva.com/design/DAGue71cm_w/m3cVSuRDFPgsQXFAfzrJeg/edit?utm_content=DAGue71cm_w&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton
