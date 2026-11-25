# Copyright (c) 2026 Dev LumiaG5. All rights reserved.
# Licensed under the MIT License.

import os
import sys

# Garante suporte seguro a UTF-8 no console Windows sem falhas de cp1252
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import re
import time
import shutil
import hashlib
import tempfile
import urllib.request
import urllib.error
import json
from pathlib import Path
from typing import Optional, Tuple, Dict, Any, List

from config import config
from language_manager import language_manager

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
VERSION_FILE = SCRIPT_DIR / "version.json"

def parse_semver(tag: str) -> Tuple[int, int, int]:
    """Extrai versão semver (major, minor, patch) de uma tag como 'v2.5.1' ou '2.5.1'."""
    match = re.search(r"(\d+)\.(\d+)(?:\.(\d+))?", tag)
    if match:
        major = int(match.group(1))
        minor = int(match.group(2))
        patch = int(match.group(3)) if match.group(3) is not None else 0
        return (major, minor, patch)
    return (0, 0, 0)

def is_newer_version(remote_tag: str, current_version: str) -> bool:
    """Retorna True se a versão remota for estritamente superior à versão atual do Local Server."""
    remote_ver = parse_semver(remote_tag)
    current_ver = parse_semver(current_version)
    return remote_ver > current_ver

def compute_file_hash(path: Path) -> str:
    """Calcula o hash SHA-256 de um arquivo para comparação de integridade."""
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return ""

def update_local_version_file(version_tag: str):
    """Atualiza version.json local com a versão instalada para persistência."""
    try:
        clean_ver = re.sub(r'^[^\d]*', '', version_tag).strip()
        data = {
            "version": clean_ver if clean_ver else "2.5.1",
            "tag": version_tag,
            "name": "Antigravity Mobile - Local Server",
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(VERSION_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass

def ensure_config_version(target_version_tag: str):
    """Garante que config.py contenha a versão atualizada e nunca regrida."""
    try:
        clean_ver = re.sub(r'^[^\d]*', '', target_version_tag).strip()
        if not clean_ver:
            clean_ver = "2.5.1"
        config_path = SCRIPT_DIR / "config.py"
        if config_path.exists():
            text = config_path.read_text(encoding="utf-8")
            if "VERSION: str = get_installed_version()" not in text:
                text = re.sub(r'VERSION:\s*str\s*=\s*["\'][^"\']+["\']', f'VERSION: str = "{clean_ver}"', text)
                config_path.write_text(text, encoding="utf-8")
    except Exception:
        pass

def fetch_latest_release(repo: str, timeout: float = 6.0) -> Optional[Dict[str, Any]]:
    """Consulta a API pública do GitHub para obter a release mais recente do repositório."""
    url = f"https://api.github.com/repos/{repo}/releases"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": f"Antigravity-Local-Server/{config.VERSION}",
            "Accept": "application/vnd.github.v3+json"
        }
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        if response.status == 200:
            releases = json.loads(response.read().decode("utf-8"))
            if isinstance(releases, list) and releases:
                for rel in releases:
                    if not rel.get("draft", False):
                        return rel
    return None

def find_server_asset(release: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Localiza o pacote do Local Server (.7z ou .zip) no release, ignorando APKs do Android."""
    assets = release.get("assets", [])
    
    # 1. Prioridade: arquivo .7z ou .zip que contenha 'server', 'desktop' ou 'bridge'
    for asset in assets:
        name = asset.get("name", "").lower()
        if (name.endswith(".7z") or name.endswith(".zip")) and any(k in name for k in ("server", "desktop", "bridge")):
            return asset
            
    # 2. Arquivo .7z ou .zip que NÃO contenha 'apk' ou 'android'
    for asset in assets:
        name = asset.get("name", "").lower()
        if (name.endswith(".7z") or name.endswith(".zip")) and not any(k in name for k in ("apk", "android")):
            return asset
            
    return None

def download_with_progress(download_url: str, dest_path: Path, prompt_label: str = "Baixando") -> bool:
    """Baixa um arquivo exibindo barra de progresso gráfica com porcentagem e velocidade no terminal."""
    try:
        req = urllib.request.Request(
            download_url,
            headers={"User-Agent": f"Antigravity-Local-Server/{config.VERSION}"}
        )
        with urllib.request.urlopen(req, timeout=30.0) as response:
            total_size = int(response.headers.get("Content-Length", 0))
            downloaded = 0
            chunk_size = 65536
            start_time = time.time()
            
            with open(dest_path, "wb") as f:
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    elapsed = max(0.001, time.time() - start_time)
                    speed_mb = (downloaded / elapsed) / (1024 * 1024)
                    down_mb = downloaded / (1024 * 1024)
                    
                    if total_size > 0:
                        pct = min(100, int((downloaded / total_size) * 100))
                        total_mb = total_size / (1024 * 1024)
                        bar_len = 26
                        filled = int(bar_len * pct / 100)
                        bar = "=" * max(0, filled - 1) + (">" if filled > 0 else "")
                        bar = bar.ljust(bar_len, " ")
                        sys.stdout.write(f"\r  [{bar}] {pct:3d}% ({down_mb:.1f} / {total_mb:.1f} MB) [{speed_mb:.1f} MB/s] ")
                    else:
                        sys.stdout.write(f"\r  [====>                     ] ({down_mb:.1f} MB) [{speed_mb:.1f} MB/s] ")
                    sys.stdout.flush()
                    
            sys.stdout.write("\n")
            sys.stdout.flush()
            return True
    except Exception as e:
        sys.stdout.write("\n")
        print(f" [!] Erro no download: {e}", flush=True)
        return False

def extract_archive(archive_path: Path, extract_dir: Path) -> bool:
    """Descompacta pacote .7z ou .zip para um diretório temporário."""
    archive_name = archive_path.name.lower()
    extract_dir.mkdir(parents=True, exist_ok=True)
    
    if archive_name.endswith(".7z"):
        try:
            import py7zr
            with py7zr.SevenZipFile(archive_path, mode="r") as z:
                z.extractall(path=extract_dir)
            return True
        except Exception as e:
            print(f" [!] Erro ao descompactar .7z: {e}", flush=True)
            return False
    elif archive_name.endswith(".zip"):
        try:
            import zipfile
            with zipfile.ZipFile(archive_path, "r") as z:
                z.extractall(path=extract_dir)
            return True
        except Exception as e:
            print(f" [!] Erro ao descompactar .zip: {e}", flush=True)
            return False
    else:
        print(f" [!] Formato de arquivo desconhecido: {archive_path.name}", flush=True)
        return False

def get_file_mappings(extract_dir: Path) -> List[Tuple[Path, Path]]:
    """Mapeia cada arquivo extraído para seu destino correspondente na instalação local."""
    mappings: List[Tuple[Path, Path]] = []
    
    sub_bridge = extract_dir / "desktop-bridge"
    if sub_bridge.is_dir():
        # Caso A: pacote com pasta desktop-bridge
        for root, dirs, files in os.walk(sub_bridge):
            dirs[:] = [d for d in dirs if d not in ("__pycache__", ".git", ".idea", ".vscode")]
            rel = Path(root).relative_to(sub_bridge)
            for f in files:
                if f.endswith(".pyc") or f == "user_language.json":
                    continue
                mappings.append((Path(root) / f, SCRIPT_DIR / rel / f))
                
        # Arquivos da raiz do pacote (ex: CHANGELOG, README)
        for item in extract_dir.iterdir():
            if item.name != "desktop-bridge" and item.is_file():
                mappings.append((item, PROJECT_DIR / item.name))
        return mappings

    # Caso B: pacote direto com run.py ou server.py
    if (extract_dir / "run.py").exists() or (extract_dir / "server.py").exists():
        for root, dirs, files in os.walk(extract_dir):
            dirs[:] = [d for d in dirs if d not in ("__pycache__", ".git", ".idea", ".vscode")]
            rel = Path(root).relative_to(extract_dir)
            for f in files:
                if f.endswith(".pyc") or f == "user_language.json":
                    continue
                mappings.append((Path(root) / f, SCRIPT_DIR / rel / f))
        return mappings

    # Caso C: subpasta do zipball (<repo>-<commit>)
    for sub in extract_dir.iterdir():
        if sub.is_dir():
            if (sub / "desktop-bridge").is_dir():
                return get_file_mappings(sub)
            elif (sub / "run.py").exists():
                return get_file_mappings(sub)

    return mappings

def analyze_extracted_files(extract_dir: Path) -> Tuple[bool, int, int]:
    """Analisa todos os arquivos extraídos e compara com os arquivos locais via tamanho e hash SHA-256.
    
    Retorna:
        (has_changes, changed_count, total_count)
    """
    mappings = get_file_mappings(extract_dir)
    total_count = len(mappings)
    changed_count = 0
    
    for src_file, dst_file in mappings:
        if not dst_file.exists():
            changed_count += 1
            continue
        # Se os tamanhos forem diferentes, houve modificação
        if dst_file.stat().st_size != src_file.stat().st_size:
            changed_count += 1
            continue
        # Se os hashes diferirem, houve modificação
        if compute_file_hash(dst_file) != compute_file_hash(src_file):
            changed_count += 1
            continue
            
    has_changes = (changed_count > 0)
    return (has_changes, changed_count, total_count)

def apply_extracted_files(extract_dir: Path, remote_tag: str = "") -> bool:
    """Aplica os arquivos extraídos na instalação local, atualizando arquivos e gravando version.json."""
    try:
        mappings = get_file_mappings(extract_dir)
        for src_file, dst_file in mappings:
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            try:
                shutil.copy2(src_file, dst_file)
            except Exception:
                time.sleep(0.08)
                try:
                    shutil.copy2(src_file, dst_file)
                except Exception:
                    pass
                    
        # Persiste a versão no version.json e em config.py para nunca regredir versão
        if remote_tag:
            update_local_version_file(remote_tag)
            ensure_config_version(remote_tag)
            
        return True
    except Exception as e:
        print(f" [!] Erro ao aplicar atualização: {e}", flush=True)
        return False

def check_and_update_local_server(force_check: bool = False) -> bool:
    """Verifica e atualiza o Local Server via GitHub. Realiza 2 tentativas automáticas caso haja falha de conexão.
    
    Analisa todos os arquivos para garantir que não haja downloads repetidos se os arquivos locais
    já estiverem 100% atualizados.
    
    Retorna:
        True: uma atualização com alterações reais foi instalada (o processo deve ser reiniciado).
        False: nenhuma atualização necessária ou arquivos já idênticos (continuar fluxo normal).
    """
    t = language_manager.get_dict()
    current_ver = config.VERSION
    repo = config.GITHUB_REPO
    
    print("\n" + "-" * 68, flush=True)
    print(f" [*] {t.get('updater_checking', 'Verificando atualizações do Local Server no GitHub...')}", flush=True)
    print(f"     {t.get('terminal_version', 'Versão do Servidor')}: v{current_ver}", flush=True)
    print("-" * 68, flush=True)
    
    max_attempts = 2
    release = None
    
    for attempt in range(1, max_attempts + 1):
        try:
            release = fetch_latest_release(repo)
            if release:
                break
        except Exception:
            if attempt < max_attempts:
                retry_msg = t.get(
                    "updater_retry",
                    "Falha na tentativa {attempt}. Tentando novamente em instantes ({attempt}/{total})..."
                ).format(attempt=attempt, total=max_attempts)
                print(f" [!] {retry_msg}", flush=True)
                time.sleep(1.2)
                
    if not release:
        fail_msg = t.get(
            "updater_failed",
            "Não foi possível verificar atualizações no momento (sem conexão com GitHub). Continuando inicialização..."
        )
        print(f" [!] {fail_msg}\n", flush=True)
        return False
        
    remote_tag = release.get("tag_name", "")
    
    # 1. Verificação prévia de semver: se a versão remota não for mais nova, dispensa download
    if not force_check and not is_newer_version(remote_tag, current_ver):
        up_to_date_msg = t.get(
            "updater_up_to_date",
            "Local Server já está na versão mais recente ({version})!"
        ).format(version=current_ver)
        print(f" [OK] {up_to_date_msg}\n", flush=True)
        return False
        
    found_msg = t.get(
        "updater_found",
        "Nova versão encontrada: {new_version} (versão atual: {current_version})"
    ).format(new_version=remote_tag, current_version=current_ver)
    print(f"\n [*] {found_msg}", flush=True)
    
    # 2. Localiza asset do Local Server (.7z ou .zip)
    asset = find_server_asset(release)
    download_url = None
    asset_name = ""
    
    if asset:
        download_url = asset.get("browser_download_url")
        asset_name = asset.get("name", "update.7z")
    else:
        zipball = release.get("zipball_url")
        if zipball:
            download_url = zipball
            asset_name = f"release_{remote_tag}.zip"
            
    if not download_url:
        no_asset_msg = t.get(
            "updater_no_asset",
            "Nova versão {new_version} encontrada, mas nenhum arquivo de pacote do Local Server foi disponibilizado no release."
        ).format(new_version=remote_tag)
        print(f" [!] {no_asset_msg}\n", flush=True)
        return False
        
    # 3. Baixa e descompacta para análise minuciosa de arquivos
    temp_dir = Path(tempfile.mkdtemp(prefix="antigravity_update_"))
    try:
        archive_path = temp_dir / asset_name
        down_title = t.get("updater_downloading", "Baixando atualização do Local Server...")
        print(f" [*] {down_title} ({asset_name})", flush=True)
        
        success = download_with_progress(download_url, archive_path, prompt_label=down_title)
        if not success or not archive_path.exists() or archive_path.stat().st_size == 0:
            print(" [!] Falha ao baixar o pacote de atualização.\n", flush=True)
            return False
            
        ext_title = t.get("updater_extracting", "Extraindo e analisando arquivos do servidor...")
        print(f" [*] {ext_title}", flush=True)
        
        extract_dir = temp_dir / "extracted"
        if not extract_archive(archive_path, extract_dir):
            print(" [!] Falha na descompactação dos arquivos de atualização.\n", flush=True)
            return False
            
        # 4. ANÁLISE DE ARQUIVOS: compara arquivos locais vs arquivos baixados
        has_changes, changed_count, total_count = analyze_extracted_files(extract_dir)
        
        if not has_changes:
            # Todos os arquivos locais já estão idênticos e atualizados!
            identical_msg = t.get(
                "updater_files_identical",
                "Todos os arquivos locais já estão atualizados e idênticos aos do GitHub!"
            )
            print(f" [OK] {identical_msg}\n", flush=True)
            return False
            
        # 5. Aplica as alterações reais encontradas
        if not apply_extracted_files(extract_dir, remote_tag=remote_tag):
            print(" [!] Falha ao substituir os arquivos da versão atual.\n", flush=True)
            return False
            
        # 6. Sucesso! Notifica que arquivos foram atualizados e solicita reiniciar
        success_title = t.get("updater_success_title", "ATUALIZAÇÃO DO SERVIDOR CONCLUÍDA COM SUCESSO!")
        restart_prompt = t.get(
            "updater_restart_prompt",
            "Os arquivos do Local Server foram atualizados para a versão {version}.\n Por favor, feche esta janela do terminal e abra-a novamente para carregar as alterações."
        ).format(version=remote_tag)
        enter_prompt = t.get("updater_press_enter", "Pressione Enter para encerrar este terminal...")
        
        print("\n" + "=" * 68, flush=True)
        print(f"        [*] ANTIGRAVITY MOBILE - {success_title}", flush=True)
        print("=" * 68, flush=True)
        print(f" [*] {changed_count} de {total_count} arquivos atualizados.")
        print(f"\n {restart_prompt}\n", flush=True)
        print("=" * 68 + "\n", flush=True)
        
        is_interactive = bool(sys.stdin and hasattr(sys.stdin, "isatty") and sys.stdin.isatty())
        if is_interactive:
            try:
                input(f" {enter_prompt} ")
            except Exception:
                pass
                
        return True
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
