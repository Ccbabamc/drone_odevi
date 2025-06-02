"""
Drone Filo Optimizasyonu projesini başlatan wrapper script
"""

import sys
from pathlib import Path

# src dizinini Python path'ine ekle
src_path = Path(__file__).parent / 'src'
sys.path.append(str(src_path))

from src.main import main

if __name__ == '__main__':
    main()