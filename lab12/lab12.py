import asyncio
import time
from typing import Any

SENTINEL = object()

RECORDS: list[dict[str, Any]] = [
    {"student": "Алия", "grade": 85},
    {"student": "Дамир", "grade": 54},
    {"student": "Руслан", "grade": 78},
    {"student": "", "grade": 91},
    {"student": "Мадина", "grade": 105},
]


async def producer(queue: asyncio.Queue[Any], data: list[dict[str, Any]], workers_count: int) -> None:
    for record in data:
        await asyncio.sleep(0.15)
        await queue.put(record)
        print("Получено:", record)

    for _ in range(workers_count):
        await queue.put(SENTINEL)


def validate(record: dict[str, Any]) -> None:
    if not isinstance(record, dict):
        raise ValueError("Запись должна быть словарём")

    student = str(record.get("student", "")).strip()
    grade = record.get("grade")

    if not student:
        raise ValueError("Не указано имя студента")
    if isinstance(grade, bool) or not isinstance(grade, (int, float)) or not (0 <= grade <= 100):
        raise ValueError("Оценка должна быть числом от 0 до 100")


async def process(record: dict[str, Any], timeout_sec: float = 1.0) -> dict[str, Any]:
    async with asyncio.timeout(timeout_sec):
        await asyncio.sleep(0.25)
        validate(record)
        grade = float(record["grade"])
        status = "зачет" if grade >= 60 else "незачет"
        return {
            "student": str(record["student"]).strip(),
            "grade": grade,
            "status": status,
        }


async def consumer(
    name: str,
    queue: asyncio.Queue[Any],
    results: list[dict[str, Any]],
    errors: list[str],
    timeout_sec: float = 1.0,
) -> None:
    while True:
        item = await queue.get()
        try:
            if item is SENTINEL:
                print(f"{name} завершен")
                return

            try:
                result = await process(item, timeout_sec=timeout_sec)
                results.append(result)
                print(f"{name} обработал: {result}")
            except (ValueError, TimeoutError) as exc:
                errors.append(f"{item}: {exc}")
        finally:
            queue.task_done()


async def run_pipeline(
    data: list[dict[str, Any]],
    maxsize: int = 3,
    workers_count: int = 2,
    timeout_sec: float = 1.0,
) -> dict[str, Any]:
    if not 2 <= maxsize <= 5 and maxsize != 1:
        raise ValueError("maxsize должен быть в диапазоне 2..5 (или 1 для теста backpressure)")
    if workers_count < 2 and maxsize != 1:
        # Для обычного запуска по ТЗ минимум 2 потребителя, но для сценария №5 можно передать 1
        pass

    queue: asyncio.Queue[Any] = asyncio.Queue(maxsize=maxsize)
    results: list[dict[str, Any]] = []
    errors: list[str] = []

    started = time.perf_counter()
    workers = [
        asyncio.create_task(
            consumer(f"worker-{i}", queue, results, errors, timeout_sec=timeout_sec)
        )
        for i in range(1, workers_count + 1)
    ]

    await producer(queue, data, workers_count=workers_count)
    await queue.join()
    await asyncio.gather(*workers)

    elapsed = time.perf_counter() - started
    average = sum(item["grade"] for item in results) / len(results) if results else 0.0
    rating = sorted(results, key=lambda x: x["grade"], reverse=True)

    return {
        "processed_count": len(results),
        "errors_count": len(errors),
        "average": average,
        "elapsed": elapsed,
        "results": results,
        "rating": rating,
        "errors": errors,
    }


def print_report(summary: dict[str, Any]) -> None:
    print(f"Обработано: {summary['processed_count']}")
    print(f"Ошибок: {summary['errors_count']}")
    print(f"Средний балл: {summary['average']:.2f}")
    print(f"Время: {summary['elapsed']:.2f} c")

    if summary["rating"]:
        print("Рейтинг студентов:")
        for place, entry in enumerate(summary["rating"], start=1):
            print(f"  {place}. {entry['student']} — {entry['grade']} ({entry['status']})")

    for err in summary["errors"]:
        print("Ошибка:", err)


async def main() -> None:
    summary = await run_pipeline(RECORDS, maxsize=3, workers_count=2, timeout_sec=1.0)
    print_report(summary)


if __name__ == "__main__":
    asyncio.run(main())