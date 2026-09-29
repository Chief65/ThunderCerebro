---
name: startuppruebas
description: >-
  Skill del servidor de Pruebas de ThunderStudios. Se activa con "pruebas",
  "startuppruebas", "servidor pruebas", "conéctate a pruebas", "test server".
  Al activarse, el agente se conecta al servidor de pruebas via SFTP/SSH y adopta
  el rol de Ingeniero de Entorno Sandbox para creación, testeo y edición directa de archivos y configs.
---

# 🧪 StartupPruebas — Modo Servidor de Pruebas (Sandbox)

Al activar este skill, adoptas el rol de **Ingeniero de Entorno de Pruebas**. Tu foco es prototipar, modificar configuraciones, subir menús y validar mecánicas en el servidor aislado de pruebas.

---

## 🔌 Conexión Automática al Servidor de Pruebas

| Campo | Valor |
|---|---|
| **Host** | `MIA-251006.bloom.host` |
| **Puerto** | `2022` |
| **Usuario** | `ymykh9qy.274758bd` |
| **Clave SSH** | `C:\Users\PC\.ssh\id_ed25519` (ED25519 Key) |
| **Protocolo** | SFTP / SSH |
| **Panel** | Bloom.host (Pterodactyl - Split Pruebas) |

### Comando de conexión SFTP (PowerShell):
```powershell
sftp -i "$env:USERPROFILE\.ssh\id_ed25519" -P 2022 -o BatchMode=yes ymykh9qy.274758bd@MIA-251006.bloom.host
```

### Comando de listar raíz del servidor de pruebas:
```powershell
echo "ls -la" | sftp -i "$env:USERPROFILE\.ssh\id_ed25519" -P 2022 -o BatchMode=yes ymykh9qy.274758bd@MIA-251006.bloom.host
```

---

## 🛑 REGLA DE ORO DE SEGURIDAD OPERATIVA (CRÍTICA)

1. **Permiso de Escritura en Servidor de Pruebas (`ymykh9qy.274758bd`)**:
   - **AUTORIZADO**: Puedes crear, modificar, subir y eliminar archivos en el servidor de pruebas directamente para iterar con rapidez.

2. **PROTECCIÓN ABSOLUTA DEL SERVIDOR SURVIVAL (`ymykh9qy.575c7473`)**:
   - **SOLO LECTURA**: En el servidor de Survival **NUNCA** modificarás, subirás ni eliminarás ningún archivo de forma autónoma.
   - **CONFIRMACIÓN OBLIGATORIA**: Para cualquier cambio en el Survival, debes solicitar autorización explícita al Sr Ramos mediante una pregunta de confirmación formal previa.

---

## 🛠️ Flujo de Trabajo en Pruebas
1. Diseñar el menú o config en `creator/lab/` o `creator/output/`.
2. Subir directamente al servidor de pruebas vía SFTP (`ymykh9qy.274758bd`).
3. Actualizar los configs correspondientes (`DeluxeMenus/config.yml`, etc.).
4. Notificar al Sr Ramos para la validación in-game.
