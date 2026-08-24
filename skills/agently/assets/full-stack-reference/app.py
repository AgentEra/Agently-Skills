"""最小组合入口：加载配置、启动 Flow、输出业务结果。"""

import asyncio
from pathlib import Path

from agently import Agently

from workflows.main_flow import run_analysis


ROOT = Path(__file__).resolve().parent
DEFAULT_QUESTION = "比较 2024 和 2025 年净营收"


async def main() -> None:
    Agently.load_settings(
        "yaml_file",
        str(ROOT / "SETTINGS.yaml"),
        auto_load_env=True,
    )
    question = input(f"经营问题（回车使用示例）：\n{DEFAULT_QUESTION}\n> ").strip()
    run = await run_analysis(
        question or DEFAULT_QUESTION,
        task_id="business-analysis-demo",
        metrics_path=ROOT / "resources/metrics.json",
        output_directory=ROOT / "outputs/latest",
    )
    print(run["final_answer"]["answer"])


if __name__ == "__main__":
    asyncio.run(main())
