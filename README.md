# Jira Exporter

**Jira Exporter** es una herramienta en Python que conecta con Jira Cloud, extrae issues y exporta sus datos a CSV incluyendo relaciones entre issues y validaciones personalizadas.

---

## 🚀 Instalación

1. Clona este repositorio:
   ```bash
   git clone https://tu-repo.git
   cd jira_exporter
   ```

2. Instala en modo editable:
   ```bash
   pip install -e .
   ```

---

## 🧾 Configuración

Crea un archivo `config.json` con el siguiente formato:

```json
{
  "jira_url": "https://tusitio.atlassian.net",
  "username": "tu.email@dominio.com",
  "api_token": "abc123apitoken",
  "jql": "project = DEMO ORDER BY created DESC",
  "fields": ["key", "summary", "status.name", "issuetype.name", "created"],
  "output_file": "issues.csv",
  "include_issue_links": true,
  "link_types": ["Blocks", "Parent Element Is"],
  "link_export_mode": "flattened",
  "relation_summary_file": "summary.csv",
  "relation_rules": [
    {
      "issue_type": "User Story",
      "status": "Open",
      "allowed_link_types": ["Parent Element Is"],
      "allowed_target_issue_types": ["Workpackage", "Release"]
    },
    {
      "issue_type": "User Story",
      "status": "Closed",
      "allowed_link_types": ["Parent Element Is"],
      "allowed_target_issue_types": ["Release"]
    }
  ]
}
```

---

## 📤 Ejecución

```bash
jira-export --config config.json
```

Esto generará:
- Un CSV con los issues (`issues.csv`)
- Un CSV de resumen por proyecto sobre relaciones (`summary_<fecha>.csv`)

---

## 📌 Requisitos

- Python >= 3.8
- Cuenta Jira Cloud con permisos de API

---

## 🛠 Módulos principales

- `config.py`: carga y validación
- `jira_client.py`: conexión a Jira
- `extractors.py`: extracción de campos y enlaces
- `validators.py`: evaluación de reglas
- `exporter.py`: salida CSV y resumen

---

## 📄 Licencia
MIT
