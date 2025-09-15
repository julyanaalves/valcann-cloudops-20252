from __future__ import annotations

import argparse
import os
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Tuple, Dict

DEFAULT_SOURCE = Path(os.environ.get("BACKUP_SOURCE", "/home/valcann/backupsFrom"))
DEFAULT_DEST = Path(os.environ.get("BACKUP_DEST", "/home/valcann/backupsTo"))
DEFAULT_LOG_DIR = Path(os.environ.get("BACKUP_LOGDIR", "/home/valcann/"))
DEFAULT_DAYS = int(os.environ.get("BACKUP_DAYS", "3"))

# Nomes de log
FROM_LOG_NAME = "backupsFrom.log"
TO_LOG_NAME = "backupsTo.log"

# Formato de data/hora nos logs
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Gerencia backups conforme política de retenção.")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE, help="Diretório origem dos arquivos (backupsFrom)")
    parser.add_argument("--dest", type=Path, default=DEFAULT_DEST, help="Diretório destino para cópia (backupsTo)")
    parser.add_argument("--log-dir", type=Path, default=DEFAULT_LOG_DIR, help="Diretório onde ficam os logs")
    parser.add_argument("--days", type=int, default=DEFAULT_DAYS, help="Quantidade de dias limite (<= mantém, > remove)")
    parser.add_argument("--time-field", choices=["ctime", "mtime"], default="ctime", help="Campo de tempo usado para critério de idade")
    parser.add_argument("--dry-run", action="store_true", help="Simula sem remover/copiar arquivos")
    parser.add_argument("--append-logs", action="store_true", help="Acrescenta aos logs em vez de sobrescrever")
    return parser.parse_args()


def ensure_dirs(*paths: Path) -> None:
    for p in paths:
        p.mkdir(parents=True, exist_ok=True)


def collect_file_info(path: Path) -> Dict[str, str]:
    st = path.stat()
    creation_time = datetime.fromtimestamp(st.st_ctime)
    mod_time = datetime.fromtimestamp(st.st_mtime)
    return {
        "path": str(path),
        "name": path.name,
        "size": str(st.st_size),
        "ctime": creation_time.strftime(TIME_FORMAT),
        "mtime": mod_time.strftime(TIME_FORMAT),
        "st_ctime": st.st_ctime,
        "st_mtime": st.st_mtime,
    }


def list_files(directory: Path) -> List[Path]:
    files: List[Path] = []
    for entry in os.scandir(directory):
        if entry.is_file():
            files.append(Path(entry.path))
    return files


def format_listing_line(info: Dict[str, str]) -> str:
    return (f"Nome: {info['path']}, Tamanho: {info['size']} bytes, "
            f"Criação: {info['ctime']}, Modificação: {info['mtime']}")


def write_listing_log(files: List[Path], log_path: Path, mode: str) -> None:
    now_str = datetime.now().strftime(TIME_FORMAT)
    with log_path.open(mode, encoding="utf-8") as f:
        f.write(f"Log de arquivos em {log_path.parent} gerado em {now_str}\n\n")
        count = 0
        for file in files:
            try:
                info = collect_file_info(file)
                f.write(format_listing_line(info) + "\n")
                count += 1
            except Exception as e:  # pragma: no cover (falhas raras de FS)
                f.write(f"ERRO lendo '{file}': {e}\n")
        f.write(f"\nTotal listado: {count}\n")


def classify_files(files: List[Path], days: int, time_field: str) -> Tuple[List[Path], List[Path]]:
    threshold = datetime.now() - timedelta(days=days)
    recent: List[Path] = []
    old: List[Path] = []
    for f in files:
        try:
            st = f.stat()
            ref_ts = st.st_ctime if time_field == "ctime" else st.st_mtime
            file_time = datetime.fromtimestamp(ref_ts)
            if file_time < threshold:
                old.append(f)
            else:
                recent.append(f)
        except Exception:
            recent.append(f)
    return recent, old


def remove_files(files: List[Path], dry_run: bool) -> Tuple[int, List[str]]:
    removed = 0
    errors: List[str] = []
    for f in files:
        try:
            if dry_run:
                continue
            f.unlink(missing_ok=True)
            removed += 1
        except Exception as e:
            errors.append(f"Erro removendo {f}: {e}")
    return removed, errors


def copy_files(files: List[Path], dest: Path, dry_run: bool) -> Tuple[int, List[Dict[str, str]], List[str]]:
    copied_infos: List[Dict[str, str]] = []
    errors: List[str] = []
    copied = 0
    for f in files:
        try:
            if not dry_run:
                shutil.copy2(f, dest)
            info = collect_file_info(f)
            copied_infos.append(info)
            copied += 1
        except Exception as e:
            errors.append(f"Erro copiando {f}: {e}")
    return copied, copied_infos, errors


def write_copy_log(dest_log: Path, mode: str, copied_infos: List[Dict[str, str]], summary: Dict[str, int], dry_run: bool) -> None:
    now_str = datetime.now().strftime(TIME_FORMAT)
    with dest_log.open(mode, encoding="utf-8") as f:
        f.write(f"Log de cópia gerado em {now_str}\n\n")
        if not copied_infos:
            f.write("Nenhum arquivo recente para copiar.\n")
        else:
            for info in copied_infos:
                f.write("Copiado: " + format_listing_line(info) + (" (dry-run)" if dry_run else "") + "\n")
        f.write("\nResumo:\n")
        for k, v in summary.items():
            f.write(f"{k}: {v}\n")


def manage_backups(source: Path, dest: Path, log_dir: Path, days: int, time_field: str, dry_run: bool, append_logs: bool) -> int:
    if source.resolve() == dest.resolve():
        print("ERRO: Diretório de origem e destino são o mesmo.")
        return 2

    ensure_dirs(source, dest, log_dir)

    from_log = log_dir / FROM_LOG_NAME
    to_log = log_dir / TO_LOG_NAME
    file_mode = "a" if append_logs else "w"

    print(f"Iniciando gerenciamento. SOURCE={source} DEST={dest} DIAS={days} TIME_FIELD={time_field} DRY_RUN={dry_run}")

    # 1 & 2: Listar + log
    try:
        files = list_files(source)
        write_listing_log(files, from_log, file_mode)
        print(f"Log de listagem salvo em {from_log}")
    except Exception as e:
        print(f"Falha ao listar: {e}")
        return 1

    # Classificar
    recent, old = classify_files(files, days, time_field)

    # Remover antigos
    removed_count, remove_errors = remove_files(old, dry_run)
    for err in remove_errors:
        print(err)

    # Copiar recentes
    copied_count, copied_infos, copy_errors = copy_files(recent, dest, dry_run)
    for err in copy_errors:
        print(err)

    summary = {
        "Arquivos_listados": len(files),
        "Antigos_para_remover": len(old),
        "Removidos": removed_count,
        "Recentes_para_copiar": len(recent),
        "Copiados": copied_count,
        "Dry_run": 1 if dry_run else 0,
        "Erros_remocao": len(remove_errors),
        "Erros_copia": len(copy_errors),
    }

    # Log de cópia (5)
    write_copy_log(to_log, file_mode, copied_infos, summary, dry_run)
    print(f"Log de cópia salvo em {to_log}")

    if remove_errors or copy_errors:
        print("Concluído com avisos/erros.")
        return 3

    print("Processo finalizado com sucesso!")
    return 0


def main() -> None:
    args = parse_args()
    exit_code = manage_backups(
        source=args.source,
        dest=args.dest,
        log_dir=args.log_dir,
        days=args.days,
        time_field=args.time_field,
        dry_run=args.dry_run,
        append_logs=args.append_logs,
    )
    sys.exit(exit_code)


if __name__ == "__main__":
    main()