# Kowa

**Kowa** is a multilingual, single-page web application built with Python and JavaScript technologies. It combines a Dash + Flask backend with a Tailwind CSS-powered frontend to deliver a fast, interactive, and responsive user experience.

---

## 📁 Project Structure

```
kowa/
├── src/                     # Main source code
├── package.json             # Node.js project config
├── package-lock.json        # Node.js dependency lock
├── requirements.txt         # Python dependencies
├── pyrightconfig.json       # Type checking config
├── tailwind.config.js       # Tailwind CSS configuration
├── .gitignore               # Ignored files
├── .gitattributes           # Git attributes
└── LICENSE                  # MIT License
```

---

## ⚙️ Installation

### Prerequisites

* Python 3.7+
* Node.js & npm

### Backend Setup

```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Setup

```bash
npm install
npx tailwindcss build -o output.css
```

---

## 🧰 Tech Stack

* **Dash**: Primary framework for building the app UI and interactivity.
* **Flask**: Extends the backend for flexibility and routing.
* **Tailwind CSS**: Utility-first CSS framework for styling.
* **Plotly/Dash Components**: Used to build reactive dashboards.

---

## 🧩 Features & Architecture

### 🧭 Routing

* Dynamic routes like `/signin`, `/signup`, `/spending`, etc.
* URL-based navigation managed through Dash callbacks.

### 🌐 Internationalization (i18n)

* Supports **English** and **Turkish** via a language dropdown.
* Language is managed via URL query params (e.g., `?lang=tr`).
* URL updates dynamically without page reloads.

### 🔐 Authentication UI

* Sign-in and Sign-up forms with consistent validation structure.
* UI styled with Tailwind, optimized for all screen sizes.

---

## 🧠 Smart Behaviors

* **Stateful Language Persistence**: Language choice is remembered across components using `dcc.Store`.
* **Smart URL Management**: All internal navigation respects the currently selected language.
* **Dynamic Dropdowns**: Filter elements adapt to user context (e.g., filtering by "image-type").

---

## 💡 UX & Design

* **Responsive**: Mobile-compatible design using Tailwind utility classes.
* **Branding Friendly**: Designed pages for user onboarding (login, signup).
* **User-Centric**: Focused on clarity and usability across languages and devices.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
