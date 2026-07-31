from pathlib import Path


class LanguageDetector:
    """
    Groups repository files by language/type.
    """

    PYTHON_EXTENSIONS = {".py"}

    JAVA_EXTENSIONS = {".java"}

    CONFIG_FILES = {
        ".yaml",
        ".yml",
        ".json",
        ".toml",
        ".ini",
        ".conf",
    }

    SPECIAL_CONFIG_FILES = {
        "Dockerfile",
        "docker-compose.yml",
    }

    def detect_languages(
        self,
        files: list[Path],
    ) -> dict[str, list[Path]]:

        grouped_files = {
            "python": [],
            "java": [],
            "config": [],
        }

        for file in files:

            if file.suffix in self.PYTHON_EXTENSIONS:
                grouped_files["python"].append(file)

            elif file.suffix in self.JAVA_EXTENSIONS:
                grouped_files["java"].append(file)

            elif (
                file.suffix in self.CONFIG_FILES
                or file.name in self.SPECIAL_CONFIG_FILES
            ):
                grouped_files["config"].append(file)

        return grouped_files