# Desglose de Fuente: Documentación Oficial de nLogin (NickUC)

**Fuente**: `https://docs.nickuc.com/` (NickUC Official Documentation)  
**Tipo**: Documentación Técnica / Sistema de Autenticación de Red y Proxy Minecraft  
**Materia**: Arquitectura de login, persistencia en MariaDB/MySQL, gestión de cuentas por IP, comandos administrativos y seguridad.

---

## 1. Arquitectura del Sistema & Multi-Plataforma

nLogin está diseñado para operar tanto en arquitecturas de servidor único (Paper, Spigot, Folia) como en entornos distribuidos mediante proxies (Velocity, BungeeCord, Waterfall):

- **Modo Proxy**: El proxy intercepta el handshake inicial, gestiona la verificación preliminar y envía al usuario al servidor de autenticación/lobby (`backend.auth-servers`).
- **Modo Backend/Spigot**: Gestiona la interacción in-game, bloqueo de movimiento (`limbo.block-player-walk`), ocultación de inventario (`limbo.inventory.hide-inventory`) y efectos de ceguera pre-login.
- **Capa de Compatibilidad**: Proporciona soporte para plugins de terceros que invocan la API de AuthMe mediante el wrapper `nLogin-AuthMeAPI`.

---

## 2. Esquema de Datos y Persistencia Relacional

nLogin desacopla la información de la cuenta en dos tablas principales (personalizables en `config.yml`):

### 2.1 Tabla de Cuentas (`nlogin`)
| Columna | Tipo / Propósito | Descripción |
|---|---|---|
| `ai` | Integer / Auto-Increment | Identificador numérico interno de la cuenta. |
| `last_name` | Varchar | Nombre de usuario (nick) actual registrado. |
| `unique_id` | UUID (String) | UUID asignado al jugador (REAL, RANDOM u OFFLINE). |
| `mojang_id` | UUID (String) | UUID oficial de Mojang si la cuenta es Premium. |
| `bedrock_id` | String | Identificador derivado de Floodgate/Geyser (XUID). |
| `password` | Hash String | Contraseña cifrada (BCRYPT2A, ARGON2ID, PBKDF2, etc.). |
| `premium` | Boolean / Tinyint | Bandera indicativa de cuenta Premium verificada. |
| `last_ip` | Varchar / IP | Última dirección IP con la que el usuario autenticó. |
| `last_seen` | Timestamp / Long | Fecha y hora del último acceso exitoso. |
| `creation_date` | Timestamp / Long | Fecha y hora en la que la cuenta fue registrada. |
| `email` | String | Correo electrónico asociado para 2FA o recuperación. |
| `discord` | String | ID de Discord vinculado para autenticación en dos pasos. |
| `settings` | String / JSON | Preferencias y metadatos de configuración del usuario. |

### 2.2 Tabla Auxiliar de Datos (`nlogin_data`)
| Columna | Tipo / Propósito | Descripción |
|---|---|---|
| `id` | String / UUID | Identificador foráneo vinculado al `unique_id` del jugador. |
| `key` | Varchar | Clave del atributo o metadato almacenado. |
| `value` | Text / String | Valor persistido correspondiente. |

---

## 3. Comandos Administrativos de Auditoría e Identidad

| Comando | Argumentos | Permiso | Descripción Operativa |
|---|---|---|---|
| `/nlogin verify` | `<jugador>` | `nlogin.command.nlogin.verify` | Inspecciona la ficha completa de un jugador: última IP registrada (`last_ip`), fecha de registro, último inicio de sesión y estado 2FA. |
| `/nlogin dupeip` | `<jugador/ip>` | `nlogin.admin` | Rastrea y lista todas las cuentas que comparten la misma dirección IP. Acepta tanto un nick como una IP directa. |
| `/nlogin delete` | `<jugador>` | `nlogin.command.nlogin.delete` | **Purga total**: Elimina la cuenta y sus registros. *Peligro fatal: puede romper el mapeo de UUID persistido.* |
| `/nlogin unregister` | `<jugador>` | `nlogin.command.nlogin.unregister` | **Reinicio de credenciales**: Elimina únicamente la contraseña registrada, permitiendo un nuevo registro sin alterar UUIDs. |
| `/nlogin changepass` | `<jugador> <password>`| `nlogin.command.nlogin.changepass` | Sobrescribe de forma administrativa la contraseña del usuario. |
| `/nlogin changeuuid` | `<jugador> <nuevo_uuid>`| `nlogin.command.nlogin.changeuuid` | Modifica manualmente el identificador UUID vinculado al nick. |
| `/nlogin forcelogin`| `<jugador>` | `nlogin.admin` | Autentica a la fuerza a un jugador sin requerir contraseña. |
| `/nlogin reload` | Ninguno | `nlogin.admin` | Recarga las configuraciones del plugin y sincroniza cachés. |

---

## 4. Políticas de Seguridad y Control por IP

En la sección `security.ip-limit`:
- `security.ip-limit.enable: true`: Habilita el control estricto de multicuentas por dirección IP.
- `security.ip-limit.limit: <número>`: Establece el umbral máximo de cuentas registradas toleradas por cada IP (típicamente 2 o 3 en entornos de producción).
- `security.ip-limit.bypass`: Permite excluir cuentas con autenticación oficial de Mojang (`premium: true`), cuentas Bedrock verificadas (`bedrock: true`) o rangos de loopback local (`127.0.0.1`, `localhost`).
- `security.disable-high-risk-commands: true`: Bloquea la ejecución in-game de comandos críticos (`/nlogin delete`, etc.) obligando a que se ejecuten desde la consola del servidor o proxy para mitigar ataques por compromiso de rangos OP.
