import argparse
import shutil
from pathlib import Path
from typing import Dict, List

# Маппинг категорий и расширений
FILE_CATEGORIES: Dict[str, List[str]] = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".bmp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".csv", ".pptx", ".md"],
    "Archives": [".zip", ".tar", ".gz", ".rar", ".7z"],
    "Audio": [".mp3", ".wav", ".flac", ".aac"],
    "Video": [".mp4", ".mkv", ".avi", ".mov"],
    "Code": [".py", ".js", ".html", ".css", ".json", ".sql", ".cpp"],
}


def get_category(file_extension: str) -> str:
    """Определяет категорию файла по его расширению."""
    ext = file_extension.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return "Others"


def organize_directory(target_dir: Path, dry_run: bool = False) -> None:
    """Сортирует файлы в целевой директории по папкам-категориям."""
    if not target_dir.exists() or not target_dir.is_dir():
        print(f"Ошибка: Путь '{target_dir}' не существует или не является директорией.")
        return

    moved_count = 0

    for item in target_dir.iterdir():
        # Игнорируем директории и скрытые файлы
        if item.is_dir() or item.name.startswith("."):
            continue

        category = get_category(item.suffix)
        category_dir = target_dir / category

        destination = category_dir / item.name

        # Избегаем коллизий имен, если файл с таким именем уже есть
        counter = 1
        while destination.exists():
            destination = category_dir / f"{item.stem}_{counter}{item.suffix}"
            counter += 1

        if dry_run:
            print(f"[DRY-RUN] Перемещение: {item.name} -> {category}/{destination.name}")
        else:
            category_dir.mkdir(exist_ok=True)
            shutil.move(str(item), str(destination))
            print(f"Перемещен: {item.name} -> {category}/{destination.name}")

        moved_count += 1

    status = "Предварительный просмотр завершен" if dry_run else "Сортировка завершена"
    print(f"\n{status}. Всего обработано файлов: {moved_count}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Утилита для автоматической сортировки файлов по категориям."
    )
    parser.add_argument(
        "path",
        type=str,
        nargs="?",
        default=".",
        help="Путь к директории для сортировки (по умолчанию: текущая папка)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Показать, что будет сделано, без реального перемещения файлов",
    )

    args = parser.parse_args()
    target_path = Path(args.path).resolve()

    print(f"Обработка директории: {target_path}\n" + "-" * 40)
    organize_directory(target_path, dry_run=args.dry_run)


if __name__ == "__main__":
    main()