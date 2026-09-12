"""沙盒脚本只处理输入和输出，不自行获取权限或启动运行时。"""

import json
import sys
from typing import Any


def calculate(payload: dict[str, Any]) -> dict[str, float]:
    previous = float(payload["previous"])
    current = float(payload["current"])
    if previous == 0:
        raise ValueError("previous must not be zero")
    return {
        "change": round(current - previous, 6),
        "growth_rate": round((current - previous) / previous, 6),
    }


def main() -> None:
    payload = json.loads(sys.stdin.read())
    print(json.dumps(calculate(payload), ensure_ascii=False))


if __name__ == "__main__":
    main()
