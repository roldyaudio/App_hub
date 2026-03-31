# App Hub Launcher

App Hub Launcher es una aplicación de escritorio en **Python + CustomTkinter** para centralizar utilidades de audio y herramientas relacionadas con Reaper.

Desde una interfaz simple por pestañas, permite:

- Descargar/clonar repositorios configurados.
- Actualizar automáticamente repositorios ya instalados.
- Lanzar la app principal de cada herramienta (cuando corresponde).
- Mantener dependencias sincronizadas a partir de `requirements.txt`.

## Características

- Interfaz gráfica con tres secciones:
  - **Audio**
  - **Reaper Tools**
  - **Download**
- Gestión de repositorios vía Git (`clone` / `pull`).
- Ejecución asíncrona para descargas/actualizaciones iniciadas desde botones.
- Autoactualización del propio hub al iniciar (según configuración en `repos.json`).

## Estructura del proyecto

- `main.py`: UI principal y lógica de botones/pestañas.
- `repo_manager.py`: funciones para clonar, actualizar y ejecutar apps de los repos.
- `lib_installer.py`: verificación de `pip` e instalación de dependencias.
- `repos.json`: configuración de repositorios y ruta de descarga.
- `requirements.txt`: dependencias del launcher.
- `resources/`: iconos e imágenes usadas por la interfaz.

## Requisitos

- Python 3.10+ recomendado.
- Git instalado y disponible en PATH.
- Sistema orientado a Windows (el proyecto usa rutas como `C:/Apps`).

## Instalación

1. Clona este repositorio:

   ```bash
   git clone https://github.com/roldyaudio/App_hub.git
   cd App_hub
   ```

2. Crea y activa un entorno virtual (opcional pero recomendado):

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Instala dependencias:

   ```bash
   pip install -r requirements.txt
   ```

## Configuración

Edita `repos.json` para definir:

- `download_path`: carpeta base donde se clonan los repositorios.
- `repos`: lista de herramientas (nombre visible + URL del repo).

Ejemplo:

```json
{
  "download_path": "C:/Apps",
  "repos": [
    {
      "name": "App Hub",
      "repo_url": "https://github.com/roldyaudio/App_hub.git"
    }
  ]
}
```

## Uso

Ejecuta el launcher:

```bash
python main.py
```

Al iniciar, el hub intenta sincronizar dependencias y actualizar su propio repositorio (si está configurado en `repos.json`).

Luego puedes pulsar cada botón para clonar/actualizar y abrir las herramientas asociadas.

## Notas importantes

- El proyecto escanea directorios para instalar cualquier `requirements.txt` encontrado bajo la ruta base configurada.
- Si cambias `download_path`, asegúrate de que exista y tenga permisos de escritura.
- Para ejecutar apps externas, se espera que cada repo tenga un `main.py` en su raíz.

## Licencia

No se especifica una licencia en este repositorio.
