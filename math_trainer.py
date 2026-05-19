
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
import random
import re
from dataclasses import dataclass
from fractions import Fraction
from typing import Callable, Dict, List


@dataclass
class Task:
    topic: str
    prompt: str
    answer: Fraction
    answer_note: str


def format_fraction(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def parse_answer(raw: str) -> Fraction | None:
    s = raw.strip().replace(",", ".")
    if not s:
        return None
    if re.fullmatch(r"-?\d+\/-?\d+", s):
        n, d = s.split("/")
        if int(d) == 0:
            return None
        return Fraction(int(n), int(d))
    if re.fullmatch(r"-?\d+", s):
        return Fraction(int(s), 1)
    if re.fullmatch(r"-?\d+\.\d+", s):
        parts = s.split(".")
        sign = -1 if s.startswith("-") else 1
        left = abs(int(parts[0]))
        right = int(parts[1])
        den = 10 ** len(parts[1])
        num = left * den + right
        return Fraction(sign * num, den)
    return None


def gen_sequence() -> Task:
    # a_n = n(n+1)
    n0 = random.randint(1, 6)
    shown = [k * (k + 1) for k in range(n0, n0 + 6)]
    ask_n = n0 + 6
    answer = Fraction(ask_n * (ask_n + 1), 1)
    prompt = (
        "Продолжите закономерность: "
        + ", ".join(str(x) for x in shown)
        + ". Чему равен следующий член?"
    )
    return Task("последовательности", prompt, answer, "целое число")


def gen_ratio_perimeter() -> Task:
    a, b, c = random.sample(range(2, 8), 3)
    ratio_sum = a + b + c
    k = random.randint(4, 18)
    perimeter = ratio_sum * k
    answer = Fraction(max(a, b, c) * k, 1)
    prompt = (
        f"Периметр треугольника равен {perimeter}, а стороны относятся как "
        f"{a}:{b}:{c}. Найдите наибольшую сторону."
    )
    return Task("отношения и пропорции", prompt, answer, "целое число")


def gen_alloy() -> Task:
    percent = random.choice([20, 25, 30, 40, 45, 60, 75])
    target = random.choice([18, 24, 30, 36, 45, 54, 72])
    mass = Fraction(target * 100, percent)
    prompt = (
        f"Сплав содержит {percent}% меди. Сколько килограммов сплава нужно взять, "
        f"чтобы меди было {target} кг?"
    )
    return Task("проценты", prompt, mass, "число (можно дробь)")


def gen_candies_crt() -> Task:
    # N = 7f + 4 = 9f - 24 -> f = 14, N = 102. Randomized variant.
    a = random.choice([5, 6, 7, 8])
    b = a + random.choice([1, 2, 3])
    f = random.randint(6, 24)
    n = a * f + random.randint(1, a - 1)
    rem = n - a * f
    shortage = b * f - n
    prompt = (
        f"Если ученик даст каждому другу по {a} конфет, останется {rem} конфет. "
        f"Если по {b} конфет, не хватит {shortage} конфет. Сколько у ученика друзей?"
    )
    return Task("текстовые задачи", prompt, Fraction(f, 1), "целое число")


def gen_linear_pair() -> Task:
    x = random.randint(8, 80)
    d = random.randint(2, 10)
    y = x + d
    k1 = random.randint(2, 7)
    k2 = random.randint(2, 9)
    # enforce x/k1 = y/k2
    lcm = k1 * k2 // math.gcd(k1, k2)
    m = random.randint(2, 10)
    x = lcm // k1 * m
    y = lcm // k2 * m
    d = y - x
    prompt = (
        f"Второе число на {d} больше первого. Частное от деления первого на {k1} "
        f"равно частному от деления второго на {k2}. Найдите первое число."
    )
    return Task("уравнения", prompt, Fraction(x, 1), "целое число")


def gen_clock_angle() -> Task:
    hour = random.randint(1, 11)
    minute = random.choice([5, 10, 15, 20, 24, 30, 36, 40, 45, 50, 55])
    minute_angle = 6 * minute
    hour_angle = 30 * hour + 0.5 * minute
    diff = abs(minute_angle - hour_angle)
    ans = min(diff, 360 - diff)
    answer = Fraction(int(ans * 2), 2)
    prompt = (
        f"Какой угол (в градусах) образуют минутная и часовая стрелки в "
        f"{hour:02d}:{minute:02d}? (Ответ от 0 до 180)"
    )
    return Task("геометрия/часы", prompt, answer, "число (можно .5)")


def gen_field() -> Task:
    # day1 p%, day2 q% of remainder, day3 rest = R
    p = random.choice([20, 25, 30, 35, 40])
    q = random.choice([25, 33, 40, 50, 60])
    whole = random.choice([60, 72, 80, 90, 96, 108, 120, 144])
    remaining_after_two = Fraction(whole * (100 - p) * (100 - q), 10000)
    rest = remaining_after_two
    if rest.denominator != 1:
        whole *= rest.denominator
        remaining_after_two = Fraction(whole * (100 - p) * (100 - q), 10000)
    answer = Fraction(whole, 1)
    prompt = (
        f"За первый день вспахали {p}% поля, за второй день {q}% от остатка, "
        f"за третий день — остальные {remaining_after_two.numerator} га. "
        f"Найдите площадь поля."
    )
    return Task("проценты", prompt, answer, "целое число")


def validate_task(task: Task) -> bool:
    # Базовый фильтр качества: никакой неопределенности и ответ в разумном диапазоне.
    if not task.prompt.strip() or "?" not in task.prompt:
        return False
    if task.answer.denominator == 0:
        return False
    if abs(task.answer) > 10**6:
        return False
    return True


GENERATORS: List[Callable[[], Task]] = [
    gen_sequence,
    gen_ratio_perimeter,
    gen_alloy,
    gen_candies_crt,
    gen_linear_pair,
    gen_clock_angle,
    gen_field,
]


def next_valid_task() -> Task:
    for _ in range(100):
        task = random.choice(GENERATORS)()
        if validate_task(task):
            return task
    raise RuntimeError("Не удалось сгенерировать корректную задачу")


def run_session(count: int) -> None:
    stats: Dict[str, Dict[str, int]] = {}
    for i in range(1, count + 1):
        task = next_valid_task()
        topic_stat = stats.setdefault(task.topic, {"ok": 0, "all": 0})
        topic_stat["all"] += 1

        print(f"\nЗадача {i}/{count} [{task.topic}]")
        print(task.prompt)
        print(f"Формат ответа: {task.answer_note}")

        raw = input("Ваш ответ: ")
        user = parse_answer(raw)
        if user is None:
            print(f"Неверный формат. Правильный ответ: {format_fraction(task.answer)}")
            continue

        if user == task.answer:
            topic_stat["ok"] += 1
            print("Верно")
        else:
            print(f"Неверно. Правильный ответ: {format_fraction(task.answer)}")

    total_ok = sum(v["ok"] for v in stats.values())
    total_all = sum(v["all"] for v in stats.values())
    print("\nИтог:")
    print(f"Правильно: {total_ok}/{total_all}")
    for topic, v in sorted(stats.items()):
        print(f"- {topic}: {v['ok']}/{v['all']}")


def run_infinite() -> None:
    i = 1
    ok = 0
    while True:
        task = next_valid_task()
        print(f"\nЗадача #{i} [{task.topic}]")
        print(task.prompt)
        print(f"Формат ответа: {task.answer_note}")
        raw = input("Ваш ответ (или 'q' для выхода): ").strip().lower()
        if raw in {"q", "quit", "exit"}:
            break
        user = parse_answer(raw)
        if user is not None and user == task.answer:
            ok += 1
            print("Верно")
        else:
            print(f"Неверно. Правильный ответ: {format_fraction(task.answer)}")
        i += 1

    print(f"\nРезультат: {ok} правильных из {i - 1}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Тренажер открытых задач по математике для поступления в 7 класс"
    )
    parser.add_argument("--count", type=int, default=10, help="Количество задач в сессии")
    parser.add_argument("--infinite", action="store_true", help="Бесконечный режим")
    parser.add_argument("--seed", type=int, help="Фиксация random seed")
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    if args.infinite:
        run_infinite()
    else:
        run_session(args.count)


if __name__ == "__main__":
    main()
