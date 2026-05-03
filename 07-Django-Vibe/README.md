# 📌 **Gemini CLI – Primeros pasos**

---

## 🚀 1️⃣ Ejecutar (sin instalar)

```bash
npx @google/gemini-cli
```

👉 Se abre el modo interactivo

---

## 📦 2️⃣ Instalar (opcional)

```bash
npm install -g @google/gemini-cli
```

Luego:

```bash
gemini
```

---

## 🔐 3️⃣ Autenticación (2 formas)

### ✅ Opción 1 (RECOMENDADA para clase)

👉 Login con Google

```bash
gemini
```

✔ No necesitas API Key
✔ Tiene plan gratis (1000 requests/día)

---

### 🔑 Opción 2 (API Key)

Desde
Google AI Studio

```bash
export GEMINI_API_KEY="TU_API_KEY"
```

---

## 💻 4️⃣ Uso básico

```bash
gemini -p "¿Qué es JWT?"
```

---

## 📂 5️⃣ Usar en proyectos

```bash
gemini
```

Ejemplo dentro:

```
> Explica este proyecto
> Encuentra errores
> Mejora este código
```

---

## ⚡ 6️⃣ Ejemplos rápidos

👉 Analizar código

```bash
gemini -p "Explica este código" 
```

👉 Generar código

```bash
gemini -p "Crea login en Flask con JWT"
```

👉 Automatizar

```bash
gemini -p "Resume este log" --output-format json
```

---

## 🧠 7️⃣ Modo script

```bash
gemini -p "Explica este archivo" --output-format json
```

👉 Ideal para automatización

---

## 🔥 8️⃣ Cosas poderosas

* Lee archivos
* Ejecuta comandos
* Usa Google Search
* Puede integrarse con GitHub
* Soporta contexto grande (hasta 1M tokens)

---

## ⚠️ Importante

❌ No subas claves
❌ No mandes datos sensibles
