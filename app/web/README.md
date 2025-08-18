# Proyecto de Landing Page

Este repositorio contiene el código para una landing page desarrollada con React y Vite. El proyecto incluye una estructura organizada de archivos y carpetas para facilitar el desarrollo y mantenimiento.

## Tabla de Contenidos

1. Instalación
2. Estructura de Archivos
3. Uso
4. Configuraciones
5. Dependencias
6. Licencia

## Instalación

Sigue estos pasos para clonar y ejecutar el proyecto localmente:

1. Clona el repositorio:

    ```bash
    git clone https://github.com/tuusuario/landing-page.git
    ```

2. Navega al directorio del proyecto:

    ```bash
    cd landing-page
    ```

3. Instala las dependencias:

    ```bash
    npm install
    ```

4. Inicia el servidor de desarrollo:

    ```bash
    npm run dev
    ```

El proyecto estará disponible en `http://localhost:3000`.

## Estructura de Archivos

```bash
├── frontend/
│   ├── public/
│   │   └── vite.svg
│   ├── src/
│   │   ├── assets/
│   │   │   ├── profile-pictures/
│   │   │   ├── code.jpg
│   │   │   ├── logo.png
│   │   │   ├── vanguard-logo.png
│   │   │   ├── video1.mp4
│   │   │   └── video2.mp4
│   │   ├── components/
│   │   │   ├── FeatureSection.jsx
│   │   │   ├── Footer.jsx
│   │   │   ├── HeroSection.jsx
│   │   │   ├── NavBar.jsx
│   │   │   ├── Pricing.jsx
│   │   │   └── Workflow.jsx
│   │   ├── constants/
│   │   │   └── index.jsx
│   │   ├── pages/
│   │   │   └── App.jsx
│   │   ├── index.css
│   │   ├── main.jsx
│   │   └── eslint.cjs
│   ├── .gitignore
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   └── vite.config.js
├── .env
└── README.md
```

### Descripción de Carpetas y Archivos
- **frontend/**: Directorio principal que contiene todo el código de la aplicación.
  - **public/**: Archivos estáticos públicos.
  - **src/**: Contiene el código fuente.
    - **assets/**: Recursos como imágenes y videos.
    - **components/**: Componentes reutilizables de React.
    - **constants/**: Constantes y configuraciones globales.
    - **pages/**: Páginas principales de la aplicación.
    - **index.css**: Estilos globales.
    - **main.jsx**: Punto de entrada de la aplicación.
    - **eslint.cjs**: Configuración de ESLint para el código.
- **.gitignore**: Ignora archivos y carpetas que no se deben incluir en el repositorio.
- **index.html**: Archivo HTML principal.
- **package-lock.json**: Archivo de bloqueo de dependencias.
- **package.json**: Archivo de configuración de npm y lista de dependencias.
- **postcss.config.js**: Configuración de PostCSS.
- **tailwind.config.js**: Configuración de Tailwind CSS.
- **vite.config.js**: Configuración de Vite.
- **.env**: Variables de entorno.

### Uso
Puedes utilizar este proyecto como base para desarrollar tu landing page. Los componentes son modulares y pueden ser reutilizados y personalizados según tus necesidades.

### Configuraciones
- **Vite**: Herramienta rápida de desarrollo para proyectos de frontend.
- **Tailwind CSS**: Framework de CSS para estilos rápidos y reutilizables.
- **ESLint**: Herramienta para asegurar la calidad del código.

### Dependencias
Las principales dependencias de este proyecto incluyen:

- **react**: Librería de JavaScript para construir interfaces de usuario.
- **vite**: Herramienta de construcción para proyectos frontend.
- **tailwindcss**: Framework de utilidades CSS.

Consulta el archivo `package.json` para ver todas las dependencias.

### Licencia
Este proyecto está licenciado bajo la **MIT License**.
