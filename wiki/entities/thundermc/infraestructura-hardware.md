# 🖥️ Especificación de Infraestructura & Hardware — Red ThunderMC

Documento maestro de especificaciones de hardware, asignación de recursos y topología de splits en Bloom.host.

---

## ⚡ 1. Hardware y Plan del Servidor
- **Proveedor**: Bloom.host (Panel Pterodactyl)
- **Plan**: Performance+ ( USD/mes)
- **Procesador (CPU)**: AMD Ryzen 9 9950X (5 Logical Cores dedicados de alto rendimiento IPC)
- **Memoria RAM Total**: 20 GB (20,480 MB) DDR5
- **Almacenamiento**: 375 GB NVMe SSD Storage
- **Capacidad de Splits**: Hasta 6 sub-servidores independientes

---

- **Parte de**: [[wiki/entities/thundermc/ecosistema-plugins|Ecosistema Plugins]] | [[wiki/synthesis/thundermc-master-synthesis|SÃ­ntesis Maestra]]
## 🌐 2. Topología y Distribución Actual de Splits (RAM / Disco)

| Servidor / Split | ID Pterodactyl | Tipo | RAM Asignada | Almacenamiento NVMe | IP : Puerto | Función en la Network |
|---|---|---|---|---|---|---|
| **Proxy (Main)** | 5db0bd79 | Velocity / Paper Proxy | 1,824 MB (1.8 GB) | 10,000 MB (10 GB) | 161.129.180.125:25565 | Entrada principal, enrutamiento, compresión y firewall |
| **Auth** | 2147fa66 | Java - Paper | 1,024 MB (1.0 GB) | 5,000 MB (5 GB) | 161.129.180.125:25564 | Servidor de login/registro (aislado de ataques) |
| **Lobby** | 64d5226d | Java - Paper | 1,024 MB (1.0 GB) | 5,000 MB (5 GB) | 161.129.180.125:25567 | Hub principal de selección de modalidades |
| **Pruebas (Ommited)** | 274758bd | Java - Paper | 1,028 MB (1.0 GB) | 5,000 MB (5 GB) | 161.129.180.125:25566 | Entorno sandbox para testeo de configs y plugins |
| **Survival** | 575c7473 | Java - Paper 1.21.11 | 15,100 MB (15.1 GB) | 350,000 MB (350 GB) | 161.129.180.125:25563 | Servidor principal Survival RPG, mundos, minas y mazmorras |

- **Total RAM Asignada**: 20,000 MB / 20,480 MB (Quedan 480 MB libres de margen de seguridad para evitar OOM a nivel de host).
- **Total Almacenamiento**: 375,000 MB (375 GB NVMe).

---

## Referencias Cruzadas
- [[wiki/synthesis/thundermc-master-synthesis|SÃ­ntesis Maestra ThunderMC]]
- [[wiki/synthesis/optimizacion-granjas-survival|OptimizaciÃ³n Granjas Survival]]
- [[wiki/entities/thundermc/core-infrastructure/plan|Plan]]
- [[wiki/entities/thundermc/ecosistema-plugins|Ecosistema Plugins]]
