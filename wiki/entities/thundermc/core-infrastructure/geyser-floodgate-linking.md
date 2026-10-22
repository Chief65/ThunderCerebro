# 🌉 Vinculación de Cuentas Java & Bedrock en Redes Cracked (Geyser + Floodgate + nLogin)

- **Categoría**: Infraestructura Proxy / Autenticación Híbrida & Crossplay
- **Servidor**: ThunderMC Network (Velocity Proxy `5db0bd79` & Paper 1.21.11)
- **Componentes**: Geyser-Velocity, Floodgate-Velocity, nLogin (Proxy & Paper)
- **Fecha de Auditoría**: 2026-10-21
- **Estado de Implementación**: Diagnosticado y Diseñado (Pendiente de despliegue)

---

## 🎯 1. Problema & Objetivo Técnico

Permitir que un jugador de la red (ejemplo: `Dragonmil65`) pueda alternar libremente su juego entre la versión de **Minecraft Java Edition** (PC) y **Minecraft Bedrock Edition** (Móvil / Consola) manteniendo:
1. El mismo inventario, nivel y estadísticas de supervivencia.
2. La misma contraseña de **nLogin**.
3. El mismo rango y permisos en **LuckPerms**.
4. La misma identidad en la base de datos sin colisiones ni suplantación.

> [!IMPORTANT]
> **Modo Concurrente Imposible**: Por diseño del protocolo de Minecraft y el gestor de sesiones de nLogin/Velocity, un jugador **NUNCA** puede estar conectado simultáneamente en ambas plataformas bajo la misma cuenta. Si intenta abrir ambas a la vez, el proxy expulsará a una de las sesiones con `"You logged in from another location"`.

---

## 🔍 2. Auditoría Técnica del Proxy Velocity (Estado Previo)

Durante la auditoría del split Proxy (`5db0bd79` en `MIA-251006.bloom.host`), se detectaron 3 bloqueos críticos que impiden la vinculación:

### 2.1 Inconsistencia en `Geyser-Velocity/config.yml`
* **Configuración observada**: `auth-type: online` (Línea 84).
* **Fallo**: Con `online-mode = false` en `velocity.toml`, Geyser intentaba forzar autenticación contra servidores oficiales de Microsoft/Mojang para Bedrock, bloqueando o desincronizando a jugadores No-Premium.
* **Corrección**: Requiere `auth-type: floodgate`.

### 2.2 Incompatibilidad de Global Linking en Red Cracked (`floodgate/config.yml`)
* **Configuración observada**: `enable-global-linking: true` y `enable-own-linking: false`.
* **Fallo**: El enlace global (`link.geysermc.org`) exige que la cuenta de Java sea Premium oficial validada por Mojang. En un servidor No-Premium, las cuentas de Java tienen UUIDs v3 (offline) y carecen de token de Microsoft. El servidor central de Geyser rechaza o no puede asociar cuentas offline.
* **Corrección**: Requiere `enable-own-linking: true` y `enable-global-linking: false`.

### 2.3 Ausencia del Driver de Base de Datos de Floodgate
* **Estado en disco**: En `plugins/floodgate/` solo existían `config.yml` y `key.pem`.
* **Riesgo Fatal**: Activar `enable-own-linking: true` sin el archivo `.jar` de extensión de base de datos provoca el crasheo inmediato de Floodgate al iniciar.

---

## 🛠️ 3. Plan de Despliegue e Implementación

### Paso 1: Descargar e Instalar la Extensión de Base de Datos
1. Descargar el archivo oficial **`floodgate-sqlite-database.jar`** de las builds oficiales de GeyserMC / Floodgate.
2. Subir el archivo vía SFTP a la ruta del Proxy:
   ```text
   plugins/floodgate/floodgate-sqlite-database.jar
   ```

### Paso 2: Configurar `plugins/floodgate/config.yml`
Modificar la sección `player-link` con los siguientes parámetros:
```yaml
player-link:
  enabled: true
  require-link: false
  enable-own-linking: true
  allowed: true
  link-code-timeout: 300
  type: sqlite
  enable-global-linking: false
```

### Paso 3: Configurar `plugins/Geyser-Velocity/config.yml`
Asegurar que la autenticación de Geyser delega en Floodgate:
```yaml
java:
  auth-type: floodgate
```

### Paso 4: Permisos en LuckPerms (Velocity)
Otorgar permiso a los usuarios para generar y validar códigos de vinculación:
```text
/lp group default permission set floodgate.command.linkaccount true
```

---

## 🔄 4. Flujo de Usuario para Vincularse

1. El jugador inicia sesión desde su cliente de **Java** (`Dragonmil65`) y pasa el login de nLogin.
2. Ejecuta en el chat:
   ```text
   /linkaccount <Gamertag_Xbox_De_Bedrock>
   ```
   *El servidor le devuelve un código numérico temporal de 4 dígitos (ejemplo: `7392`).*
3. El jugador entra al servidor desde **Bedrock** (con su Gamertag de Xbox) y escribe:
   ```text
   /linkaccount <Dragonmil65> 7392
   ```
4. Floodgate almacena la correspondencia en `floodgate/linking.db` (SQLite).
5. A partir de la siguiente conexión, al entrar desde Bedrock:
   - Floodgate omite el prefijo `.` en el nombre.
   - Le asigna el UUID offline de Java (`OfflinePlayer:Dragonmil65`).
   - Comparte exactamente el mismo inventario, nivel y permisos.
   - nLogin solicita la misma contraseña que el usuario registró en Java.

---

## ⚠️ 5. Matriz de Riesgos Fatales (Red Teaming)

| Riesgo Fatal | Causa Raíz | Impacto Operativo | Medida de Mitigación |
|---|---|---|---|
| **Suplantación de Cuenta (Account Stealing)** | Remover el prefijo `.` de Bedrock sin linking obligatorio manteniendo `autologin.bedrock.skip-register: true` en nLogin. | Un jugador de Bedrock se pone el Gamertag de un Admin/VIP y entra sin contraseña. | **PROHIBIDO** poner `username-prefix: ""` en Floodgate de forma global. El prefijo `.` debe mantenerse para todos los usuarios NO vinculados. |
| **Crash en Arranque de Floodgate** | Activar `enable-own-linking: true` sin haber subido `floodgate-sqlite-database.jar`. | Floodgate lanza una `ClassNotFoundException` / error fatal y deshabilita el soporte de Bedrock. | Subir primero el `.jar` a `plugins/floodgate/` antes de activar la directiva en `config.yml`. |
| **Bloqueo a Nuevos Jugadores Bedrock** | Configurar accidentalmente `require-link: true`. | Cualquier usuario que entre por primera vez desde móvil/consola es expulsado al no estar vinculado. | Mantener estrictamente `require-link: false`. |
