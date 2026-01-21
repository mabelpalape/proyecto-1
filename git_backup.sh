#!/bin/bash
# Script para respaldar el proyecto en GitHub
# Ejecuta este script desde el directorio del proyecto

echo "Inicializando repositorio Git..."
git init

echo "Configurando usuario Git..."
git config user.email "alumno@ejemplo.com"
git config user.name "Agente IA"

echo "Agregando archivos al staging area..."
git add .

echo "Creando commit inicial..."
git commit -m "Versión Inicial"

echo "Conectando con repositorio remoto..."
git remote add origin https://github.com/mabelpalape/proyecto-1.git || git remote set-url origin https://github.com/mabelpalape/proyecto-1.git

echo "Renombrando rama a main..."
git branch -M main

echo "Subiendo cambios a GitHub..."
git push -u origin main

echo "¡Listo! El proyecto ha sido respaldado en GitHub."
