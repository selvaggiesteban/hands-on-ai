import subprocess
import os
import sys
import time
import shutil

# Configuración
ORCHESTRATOR_SCRIPT = "orchestrator.py"
TEST_PROJECT_DIR = os.path.join("project", "test")
TEST_PROJECT_ABS = os.path.abspath(TEST_PROJECT_DIR)

def setup_environment():
    """Prepara el entorno de prueba."""
    print(f"🛠️  Creando directorio de prueba: {TEST_PROJECT_DIR}")
    if os.path.exists(TEST_PROJECT_DIR):
        shutil.rmtree(TEST_PROJECT_DIR)
    os.makedirs(TEST_PROJECT_DIR, exist_ok=True)
    
    # Crear archivo plan.txt dummy para que /roadmap funcione
    plan_txt_path = os.path.join("project", "plan.txt")
    with open(plan_txt_path, "w", encoding="utf-8") as f:
        # Formato esperado por regex: hands-on-ai\project\test
        f.write(f"hands-on-ai\{TEST_PROJECT_DIR}")
    print(f"📄 Creado plan.txt temporal en: {plan_txt_path}")

def run_orchestrator_test():
    """Ejecuta el orquestador y simula interacción de usuario."""
    print(f"🚀 Iniciando Orchestrator bajo prueba...")
    
    # Comandos a simular (Secuencia de inputs)
    # 1. Cambiar root a la carpeta de prueba
    # 2. Ver ayuda
    # 3. Ver estado del sistema (Enhanced)
    # 4. Iniciar chat simple (Smoke test IA)
    # 5. Ejecutar tarea compleja (Landing Page)
    # 6. Salir
    
    # Secuencia maestra que dispara TODOS los comandos disponibles
    input_sequence = [
        "/root", TEST_PROJECT_DIR,       # 1. Root
        "/help",                         # 2. Ayuda
        "/status",                       # 3. Estado
        "/config", "",                   # 4. Config (abre y sale con Enter)
        "/sync",                         # 5. Sync
        "/roadmap",                      # 6. Roadmap
        "/publish",                      # 7. Publish
        "/compress",                     # 8. Compress
        "/templates", "",                # 9. Templates (abre y sale)
        "/init " + TEST_PROJECT_DIR,     # 10. Init
        "/print",                        # 11. Print
        "/chat Prueba de sistema",       # 12. Chat
        "/run Crear index.html",         # 13. Run (Enhanced)
        "/exit"                          # 14. Salida
    ]
    
    input_str = "\n".join(input_sequence) + "\n"
    
    # ... resto del código de ejecución ...
    
    process = subprocess.Popen(
        [sys.executable, ORCHESTRATOR_SCRIPT],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8', 
        cwd=os.getcwd(),
        env=os.environ.copy()
    )
    
    print("⏳ Ejecutando secuencia de comandos simulada...")
    stdout, stderr = process.communicate(input=input_str)
    
    return stdout, stderr, process.returncode

def analyze_results(output):
    """Analiza la salida para verificar mensajes de éxito."""
    print("\n📊 --- REPORTE DE VALIDACIÓN UX/UI ---")
    
    checks = [
        ("Cambio de Root", "Root cambiado a:", "✅"),
        ("Comando /help", "[ Comandos ]", "✅"),
        ("Comando /status", "ESTADO DEL SISTEMA", "✅"),
        ("Comando /config", "Inteligencia Artificial", "✅"), # "Configuración" tiene tilde, usamos esto
        ("Comando /sync", "Sync ejecutado", "✅"),
        ("Comando /roadmap", "ROADMAP COMPLETO", "✅"),
        ("Comando /publish", "Publicando proyecto", "✅"),
        ("Comando /compress", "Comprimiendo el proyecto", "✅"),
        ("Comando /templates", "Templates", "✅"),
        ("Comando /init", "Iniciando An", "✅"), # "Análisis" tiene tilde, "Iniciando An" es seguro
        ("Comando /print", "PLAN MAESTRO", "✅"),
        ("Comando /chat", "🤖", "✅"),
        ("Comando /run", "TAREA COMPLETADA", "✅"),
        ("Salida Exitosa", "pronto!", "✅")
    ]
    
    success_count = 0
    for name, signature, icon in checks:
        if signature in output:
            print(f"{icon} {name}: PASSED")
            success_count += 1
        else:
            print(f"❌ {name}: FAILED (No se encontró '{signature}')")
    
    # Check for run errors
    if "Error durante la ejecución" in output:
        print("❌ DETECTADO ERROR EN RUN: Se encontró mensaje de excepción en la salida.")

    print("-" * 40)
    if success_count == len(checks):
        print("🏆 RESULTADO FINAL: 100% ÉXITO. El pipeline opera correctamente.")
    else:
        print(f"⚠️ RESULTADO FINAL: {success_count}/{len(checks)} pruebas pasaron.")
        print("\n🔍 LOG COMPLETO (Debug):")
        print(output) # Imprimir TODO el log

if __name__ == "__main__":
    setup_environment()
    stdout, stderr, code = run_orchestrator_test()
    
    if stderr:
        print(f"\n⚠️ Errores detectados en stderr:\n{stderr}")
        
    analyze_results(stdout)
