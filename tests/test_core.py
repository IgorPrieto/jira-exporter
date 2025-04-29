[project]
name = "jira-exporter"
version = "0.1.0"
description = "Exportador de issues Jira a CSV con análisis de relaciones"
authors = [
  { name="Equipo de Ingeniería", email="ingenieria@example.com" }
]
readme = "README.md"
requires-python = ">=3.8"
dependencies = [
  "requests",
  "pytest"
]

[project.scripts]
jira-export = "jira_exporter.__main__:main"

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[tool.pytest.ini_options]
minversion = "6.0"
addopts = "-ra -q"
testpaths = [
  "tests",
  "."
]
