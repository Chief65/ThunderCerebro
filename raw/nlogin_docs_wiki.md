# Documentación en Bruto: nLogin (NickUC)
**Fuente Original**: https://docs.nickuc.com/ (Versiones EN y ES)
**Fecha de Ingesta**: 2026-10-15
**Autor/Desarrollador**: NickUC (nickuc.com)

---

## 1. Visión General
nLogin es un sistema de autenticación multi-plataforma enfocado en practicidad, seguridad y ergonomía para servidores y redes de Minecraft.
Soporta: Velocity, BungeeCord, Waterfall, Folia, Paper, Spigot, Mohist y derivados.
Compatibilidad AuthMe API mediante nLogin-AuthMeAPI.

---

## 2. Comandos Administrativos y de Jugador
- `/nlogin <comando> [argumentos]`: Comando raíz administrativo.
  - `/nlogin support`: Muestra canales de soporte.
  - `/nlogin version`: Versión instalada del plugin.
  - `/nlogin changepass <jugador> <nueva_contraseña>`: Cambia la clave de un jugador.
  - `/nlogin delete <jugador>`: Elimina por completo la cuenta de un jugador (¡atención: datos de UUID pueden perderse!).
  - `/nlogin dupeip <jugador/ip>`: Lista todas las cuentas vinculadas a la misma dirección IP.
  - `/nlogin forcelogin <jugador>`: Fuerza el inicio de sesión del jugador.
  - `/nlogin unregister <jugador>`: Elimina la contraseña de una cuenta sin purgar el registro de UUID.
  - `/nlogin verify <jugador>`: Inspecciona y lista la información técnica de una cuenta (IP, fecha registro, último acceso, etc.).
  - `/nlogin reload`: Recarga la configuración del plugin.
  - `/nlogin update`: Ajustes y control de actualizaciones.
  - `/nlogin spawn <acción> <tipo>`: Control de teletransporte y puntos de spawn de autenticación.
  - `/nlogin changeuuid <jugador> <nuevo_uuid>`: Modifica el UUID asignado a un jugador.
  - `/nlogin unban <jugador>`: Desbloquea un jugador.
  - `/nlogin converter <plugin>`: Migra datos de otros plugins (AuthMe, etc.).

- Comandos de Usuario:
  - `/register <contraseña> <repetir>`: Registra cuenta.
  - `/login <contraseña>`: Inicia sesión.
  - `/changepassword <actual> <nueva>`: Cambio de contraseña por parte del usuario.
  - `/unregister <contraseña>`: Autodesregistro (desactivado por defecto).
  - `/premium`: Marca cuenta como premium.
  - `/offline` / `/cracked`: Marca cuenta como no premium.
  - `/discord` / `/email`: Gestión de doble factor de autenticación (2FA).

---

## 3. Esquema de Base de Datos (MySQL / MariaDB / SQLite)
```yaml
database:
  type: MySQL # MariaDB, SQLite
  remote:
    hostname: "localhost:3306"
    database: "nLogin"
    username: "root"
    password: ""
  table:
    account:
      table-name: "nlogin"
      columns:
        ai: "ai"
        last-name: "last_name"
        unique-id: "unique_id"
        mojang-id: "mojang_id"
        bedrock-id: "bedrock_id"
        password: "password"
        premium: "premium"
        last-ip: "last_ip"
        last-seen: "last_seen"
        creation-date: "creation_date"
        email: "email"
        discord: "discord"
        settings: "settings"
    data:
      table-name: "nlogin_data"
      columns:
        id: "id"
        key: "key"
        value: "value"
```

---

## 4. Opciones Clave de Configuración
- `security.ip-limit.enable`: Control de límite de registros por IP (por defecto 3).
- `security.ip-limit.limit`: Número máximo de cuentas por dirección IP.
- `security.ip-limit.bypass.premium` / `bedrock`: Exclusiones para cuentas oficiales y Floodgate.
- `security.ip-limit.bypass.ips`: Lista blanca de IPs exentas (`127.0.0.1`, `localhost`).
- `security.disable-high-risk-commands: true`: Desactiva comandos de alto riesgo in-game para evitar secuestros de cuenta admin.
- `passwords.hashing.algorithm`: Algoritmos soportados: BCRYPT2A, BCRYPT2Y, PBKDF2, ARGON2ID, ARGON2I, ARGON2D, SHA256, SHA512.
- `premium.username-appender`: Diferenciación de jugadores offline vs premium agregando sufijos/prefijos automáticos.
- `premium.legacy.unique-id-type`: REAL, RANDOM, OFFLINE.
