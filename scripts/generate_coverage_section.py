import re

from datetime import datetime

import defusedxml.ElementTree as ET


def get_coverage(xml_path: str = "coverage.xml") -> float:
    tree = ET.parse(xml_path)
    root = tree.getroot()
    return round(float(root.attrib["line-rate"]) * 100, 2)


def get_date(xml_path: str = "coverage.xml") -> str:
    tree = ET.parse(xml_path)
    root = tree.getroot()
    timestamp = root.attrib["timestamp"]
    data_str = datetime.fromtimestamp(int(timestamp) / 1000).strftime("%Y-%m-%d %H:%M:%S")
    return data_str


def generate_progress_bar(percent: float, length: int = 30):
    filled = int(length * percent / 100)
    bar = "█" * filled + "░" * (length - filled)
    return f"{bar}  {percent}%"


def update_readme(coverage: float, update_date: str, readme_path: int = "README.md"):
    start_tag = "<!-- coverage:start -->"
    end_tag = "<!-- coverage:end -->"

    progress_bar = generate_progress_bar(coverage)
    coverage_md = f"""{start_tag}
## 📊 Code Coverage
{progress_bar}<br>
Updated at: {update_date}
{end_tag}"""

    with open(readme_path, encoding="utf-8") as f:
        content = f.read()

    if start_tag in content and end_tag in content:
        content = re.sub(f"{start_tag}.*?{end_tag}", coverage_md, content, flags=re.DOTALL)
    else:
        content += "\n\n" + coverage_md

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    coverage = get_coverage()
    udpate_date = get_date()
    update_readme(coverage, udpate_date)
