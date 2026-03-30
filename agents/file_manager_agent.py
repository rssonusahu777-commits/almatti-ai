import os
import shutil
from datetime import datetime


class FileManagerAgent:
    """Scans /output and organizes all generated files into typed subfolders."""

    OUTPUT_ROOT = "output"

    CATEGORY_MAP = {
        "websites": [".html", ".htm"],
        "presentations": [".pptx", ".ppt", ".md"],
        "communications": [".txt", ".eml"],
        "images": [".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"],
        "data": [".json", ".csv", ".xml", ".yaml", ".yml"],
        "misc": [],
    }

    def run(self, task: str) -> dict:
        files_found = []
        files_organized = []

        for dirpath, _, filenames in os.walk(self.OUTPUT_ROOT):
            for fname in filenames:
                full_path = os.path.join(dirpath, fname)
                ext = os.path.splitext(fname)[1].lower()
                target_folder = self._categorize(ext)
                target_dir = os.path.join(self.OUTPUT_ROOT, target_folder)
                os.makedirs(target_dir, exist_ok=True)
                dest = os.path.join(target_dir, fname)

                files_found.append(full_path)

                if full_path != dest:
                    try:
                        shutil.copy2(full_path, dest)
                        files_organized.append({"from": full_path, "to": dest})
                    except Exception:
                        pass  # File may already be in right place

        file_tree = self._build_tree()

        return {
            "status": "success",
            "agent": "File Manager Agent",
            "total_files_found": len(files_found),
            "files_organized": len(files_organized),
            "file_tree": file_tree,
            "message": f"Organized {len(files_found)} files across {len(self.CATEGORY_MAP)} categories.",
        }

    def _categorize(self, ext: str) -> str:
        for category, extensions in self.CATEGORY_MAP.items():
            if ext in extensions:
                return category
        return "misc"

    def _build_tree(self) -> list:
        tree = []
        if not os.path.exists(self.OUTPUT_ROOT):
            return tree
        for dirpath, dirnames, filenames in os.walk(self.OUTPUT_ROOT):
            level = dirpath.replace(self.OUTPUT_ROOT, "").count(os.sep)
            indent = "  " * level
            folder_name = os.path.basename(dirpath)
            tree.append(f"{indent}📁 {folder_name}/")
            sub_indent = "  " * (level + 1)
            for fname in filenames:
                fpath = os.path.join(dirpath, fname)
                size = os.path.getsize(fpath)
                tree.append(f"{sub_indent}📄 {fname} ({self._human_size(size)})")
        return tree

    def _human_size(self, size: int) -> str:
        for unit in ["B", "KB", "MB"]:
            if size < 1024:
                return f"{size:.0f} {unit}"
            size /= 1024
        return f"{size:.1f} GB"
