from pathlib import Path
import shutil

BASE_DIR = Path(__file__).parent
PEOPLE_FILE = BASE_DIR / "people.json"
CLEAN_FILE = BASE_DIR / "people_clean.json"
BACKUP_FILE = BASE_DIR / "people_backup.json"


def main():
    if not PEOPLE_FILE.exists():
        print("错误：people.json 不存在，无法备份")
        return

    if not CLEAN_FILE.exists():
        print("错误：people_clean.json 不存在，无法替换")
        return

    shutil.copy(PEOPLE_FILE, BACKUP_FILE)
    print("已备份原始文件到 people_backup.json")

    shutil.copy(CLEAN_FILE, PEOPLE_FILE)
    print("已用 people_clean.json 替换 people.json")


if __name__ == "__main__":
    main()