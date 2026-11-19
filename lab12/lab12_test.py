import asyncio
from lab12 import run_pipeline


async def test_all_valid() -> None:
    data = [
        {"student": "Алия", "grade": 90},
        {"student": "Дамир", "grade": 60},
        {"student": "Руслан", "grade": 45},
    ]
    res = await run_pipeline(data, maxsize=3, workers_count=2)
    assert res["processed_count"] == 3
    assert res["errors_count"] == 0


async def test_empty_name() -> None:
    data = [
        {"student": "   ", "grade": 80},
        {"student": "Алия", "grade": 70},
    ]
    res = await run_pipeline(data, maxsize=2, workers_count=2)
    assert res["processed_count"] == 1
    assert res["errors_count"] == 1


async def test_out_of_range_grade() -> None:
    data = [
        {"student": "Алия", "grade": -5},
        {"student": "Дамир", "grade": 101},
        {"student": "Руслан", "grade": 88},
    ]
    res = await run_pipeline(data, maxsize=2, workers_count=2)
    assert res["processed_count"] == 1
    assert res["errors_count"] == 2


async def test_maxsize_one_backpressure() -> None:
    data = [{"student": f"Студент_{i}", "grade": 70 + i} for i in range(5)]
    res = await run_pipeline(data, maxsize=1, workers_count=2)
    assert res["processed_count"] == 5
    assert res["errors_count"] == 0


async def test_one_vs_two_consumers() -> None:
    data = [{"student": f"Студент_{i}", "grade": 75} for i in range(6)]
    res_one = await run_pipeline(data, maxsize=3, workers_count=1)
    res_two = await run_pipeline(data, maxsize=3, workers_count=2)
    assert res_one["processed_count"] == 6
    assert res_two["processed_count"] == 6
    assert res_two["elapsed"] < res_one["elapsed"]


async def test_exception_releases_join() -> None:
    data = [{"student": "", "grade": 50}]
    res = await asyncio.wait_for(
        run_pipeline(data, maxsize=2, workers_count=2),
        timeout=3.0,
    )
    assert res["errors_count"] == 1
    assert res["processed_count"] == 0


async def test_empty_input() -> None:
    res = await run_pipeline([], maxsize=2, workers_count=2)
    assert res["processed_count"] == 0
    assert res["errors_count"] == 0
    assert res["average"] == 0.0


async def run_all_tests() -> None:
    tests = [
        ("1. Все записи корректны", test_all_valid),
        ("2. Пустое имя", test_empty_name),
        ("3. Оценка вне диапазона 0..100", test_out_of_range_grade),
        ("4. Очередь maxsize=1 (обратное давление)", test_maxsize_one_backpressure),
        ("5. 1 vs 2 потребителя", test_one_vs_two_consumers),
        ("6. Исключение и завершение queue.join()", test_exception_releases_join),
        ("7. Пустой входной список", test_empty_input),
    ]
    for title, fn in tests:
        await fn()
        print(f"[OK] {title}")


if __name__ == "__main__":
    asyncio.run(run_all_tests())