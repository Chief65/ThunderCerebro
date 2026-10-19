# 📖 nLogin (Proxy & Core Authentication)

- **Categoría**: Red / Autenticación de Proxy & Cuentas (Auth & Identity Management)
- **Servidor**: ThunderMC Network (Proxy Velocity / BungeeCord & Paper 1.21.11)
- **Desarrollador**: NickUC
- **Persistencia**: MariaDB / MySQL (`nlogin`, `nlogin_data`)
- **Documentación de Referencia**: [[wiki/sources/nlogin-official-docs|Documentación Oficial de nLogin]]

---

## 🎯 1. Propósito & Visión General
**nLogin** es el motor central de autenticación y protección de cuentas para la red de ThunderMC. Opera de forma coordinada entre el proxy de entrada y los servidores backend, gestionando el flujo de registro, inicio de sesión seguro, doble factor de autenticación (2FA vía Discord/Email) y prevención de ataques de fuerza bruta o multicuentas no autorizadas.

---

## 🔍 2. Auditoría de Cuentas: Consulta de IP por Nick

Para identificar la dirección IP asociada a un jugador registrado en nLogin existen dos vías oficiales y deterministas:

### 2.1 Vía Comandos (In-Game / Consola)
- **Comando principal**:
  ```text
  /nlogin verify <jugador>
  ```
  *Muestra la ficha técnica completa:* última IP de conexión (`last_ip`), fecha de creación de cuenta (`creation_date`), última sesión (`last_seen`), UUID asociado y estado 2FA.
  *(Requiere permiso `nlogin.command.nlogin.verify` o consola).*

- **Comando de correlación de multicuentas**:
  ```text
  /nlogin dupeip <jugador>
  ```
  Permite ingresar el nick y lista de forma inmediata todas las demás cuentas registradas que compartan la misma dirección IP.

### 2.2 Vía Base de Datos SQL (MariaDB / MySQL)
En la base de datos central de nLogin:
```sql
SELECT last_name, last_ip, last_seen, creation_date, unique_id 
FROM nlogin 
WHERE last_name = '<nick>';
```

---

## 🗑️ 3. Purga y Borrado de Cuentas Vinculadas a una IP

### 3.1 Análisis de Viabilidad Nativa
> [!IMPORTANT]
> **nLogin NO cuenta con un comando nativo del tipo `/nlogin deleteip <ip>`.**  
> Los comandos nativos `/nlogin delete` y `/nlogin unregister` están diseñados exclusivamente para recibir nombres de jugador (`<jugador>`), no direcciones IP.

### 3.2 Protocolo Operativo 1: Vía Comandos
1. **Identificar los nicks de la IP**:
   Ejecutar en la consola:
   ```text
   /nlogin dupeip <dirección_IP>
   ```
2. **Eliminar individualmente cada cuenta listada**:
   - Para borrado completo de cuenta:
     ```text
     /nlogin delete <nick>
     ```
   - Para desregistrar la clave preservando el perfil de UUID:
     ```text
     /nlogin unregister <nick>
     ```

### 3.3 Protocolo Operativo 2: Vía Base de Datos (Borrado Masivo por IP)
Si se requiere eliminar de forma atómica todas las cuentas asociadas a una IP específica:

1. **Auditoría previa (comprobación de cuentas afectadas)**:
   ```sql
   SELECT ai, last_name, unique_id, last_ip, last_seen 
   FROM nlogin 
   WHERE last_ip = '<IP_OBJETIVO>';
   ```
2. **Eliminación en cascada de metadatos y cuentas**:
   ```sql
   -- 1. Eliminar datos auxiliares en nlogin_data
   DELETE FROM nlogin_data 
   WHERE id IN (SELECT unique_id FROM nlogin WHERE last_ip = '<IP_OBJETIVO>');

   -- 2. Eliminar las cuentas de la tabla principal
   DELETE FROM nlogin 
   WHERE last_ip = '<IP_OBJETIVO>';
   ```
3. **Sincronización de memoria del plugin**:
   Ejecutar inmediatamente en la consola del proxy o servidor:
   ```text
   /nlogin reload
   ```

---

## ⚠️ 4. Red Teaming: Riesgos Fatales en Producción

1. **Colisión en CGNAT, Proxies Móviles y Redes Compartidas**:
   - En conexiones domésticas con CGNAT (típico en operadoras de fibra/móvil) o redes universitarias/escolares, decenas de usuarios legítimos pueden compartir una misma dirección IP pública.
   - *Modo de fallo:* Un borrado masivo por IP (`WHERE last_ip = '...'`) purgará cuentas de jugadores legítimos no relacionados con el infractor.
2. **Pérdida Irreversible de Datos por Ruptura de UUID (`/nlogin delete`)**:
   - La documentación oficial advierte: `🚨 Los datos UUID pueden perderse después de realizar esta operación`.
   - Si se usa `/nlogin delete` en lugar de `/nlogin unregister`, el mapeo de UUID en nLogin desaparece. Si el jugador vuelve a entrar, el servidor le generará un UUID diferente (en modo Offline), perdiendo sus parcelas en ProtectionStones, dinero en Vault, inventarios guardados y rango de LuckPerms.
3. **Inconsistencia de Sesiones en Caché Activa**:
   - Si se ejecuta un borrado directo en SQL mientras los usuarios están conectados, la memoria RAM del plugin mantiene las sesiones activas (`session.duration`). Los usuarios no serán expulsados de inmediato y al desconectarse intentarán sobreescribir la base de datos, corrompiendo registros.
   - *Mitigación obligatoria:* Expulsar a los jugadores (`kick <jugador>`) antes del borrado y ejecutar `/nlogin reload` inmediatamente después.
