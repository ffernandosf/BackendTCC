#!/usr/bin/env python
"""
Executar testes com visualização melhorada
"""
import subprocess
import sys
from datetime import datetime

def main():
    print("=" * 80)
    print("🔋 SISTEMA DE GESTAO DE ENERGIA ELETRICA - TESTES")
    print("=" * 80)
    print(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("🐍 Django + Django REST Framework")
    print("=" * 80)
    
    print("\n🚀 Executando testes...")
    print("=" * 80)
    
    # Executar testes com verbosity 2 para ver cada teste
    result = subprocess.run([
        sys.executable, 'manage.py', 'test', '--verbosity=2'
    ])
    
    print("\n" + "=" * 80)
    if result.returncode == 0:
        print("✅ TODOS OS TESTES PASSARAM!")
        print("🎉 Sistema funcionando perfeitamente!")
    else:
        print("❌ ALGUNS TESTES FALHARAM!")
        print("⚠️  Verifique os erros acima")
    print("=" * 80)
    
    return result.returncode

if __name__ == '__main__':
    sys.exit(main())