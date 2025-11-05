import subprocess
import re
from pathlib import Path


class PETestRunner:
    def __init__(self, base_dir: Path) -> None:
        self.base_dir = Path(base_dir)
        self.test_file = self.base_dir / "tests.txt"

    def parse_tests(self) -> dict:
        """Parse file tests.txt để lấy thông tin test cho 4 bài (Q1..Q4)."""
        if not self.test_file.exists():
            print(f"⚠️  Không tìm thấy file: {self.test_file}")
            return {}

        content = self.test_file.read_text(encoding="utf-8")
        tests: dict[int, list[dict]] = {}

        # Parse từng bài (Q1, Q2, Q3, Q4)
        for q_num in range(1, 5):
            pattern = rf"===\s*Q{q_num}\s*===\s*\n(.*?)(?=(?:===\s*Q\d\s*===)|$)"
            match = re.search(pattern, content, re.DOTALL)
            if not match:
                continue

            q_content = match.group(1)

            # Parse từng test case trong bài
            tc_pattern = (
                r"---\s*TC(\d+)\s*---\s*\n"
                r"INPUT:\s*\n(.*?)\n"
                r"OUTPUT:\s*\n(.*?)\n"
                r"REMOVE_SPACES:\s*\n(YES|NO)\s*\n"
                r"CASE_SENSITIVE:\s*\n(YES|NO)\s*\n"
                r"MARK:\s*\n([\d.]+)"
            )

            test_cases: list[dict] = []
            for tc_match in re.finditer(tc_pattern, q_content, re.DOTALL):
                test_cases.append(
                    {
                        "tc_num": int(tc_match.group(1)),
                        "input": tc_match.group(2).strip(),
                        "expected_output": tc_match.group(3).strip(),
                        "remove_spaces": tc_match.group(4) == "YES",
                        "case_sensitive": tc_match.group(5) == "YES",
                        "mark": float(tc_match.group(6)),
                    }
                )

            if test_cases:
                tests[q_num] = test_cases

        return tests

    def find_jar_file(self, question_dir: Path) -> Path | None:
        """Tìm file .jar trong thư mục run/ của từng câu hỏi."""
        run_dir = question_dir / "run"
        if not run_dir.exists():
            return None

        jar_files = list(run_dir.glob("*.jar"))
        if not jar_files:
            return None

        # Ưu tiên tên file có 'dist'
        for jar in jar_files:
            if "dist" in jar.name.lower():
                return jar

        # Nếu không có, lấy file đầu tiên
        return jar_files[0]

    def run_jar_with_input(self, jar_file: Path, input_data: str) -> tuple[str, str, int]:
        """Chạy file .jar với input (timeout 10s)."""
        try:
            result = subprocess.run(
                ["java", "-jar", str(jar_file)],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=10,
                cwd=str(jar_file.parent),
            )

            stdout = result.stdout

            # Nếu output có từ khóa OUTPUT:, chỉ lấy phần sau đó
            if "OUTPUT:" in stdout:
                output_part = stdout.split("OUTPUT:", 1)[1]
                if "BUILD SUCCESSFUL" in output_part:
                    output_part = output_part.split("BUILD SUCCESSFUL", 1)[0]
                stdout = output_part.strip()

            return stdout, result.stderr, result.returncode

        except subprocess.TimeoutExpired:
            return "", "⏱️  TIMEOUT - Chương trình chạy quá 10 giây", -1
        except Exception as exc:  # noqa: BLE001
            return "", f"❌ Lỗi: {str(exc)}", -1

    def normalize_output(self, text: str, remove_spaces: bool = False, case_sensitive: bool = True) -> str:
        """Chuẩn hóa output theo config so sánh."""
        result = text.strip()
        if remove_spaces:
            result = re.sub(r"\s+", "", result)
        if not case_sensitive:
            result = result.lower()
        return result

    def compare_outputs(
        self,
        actual: str,
        expected: str,
        remove_spaces: bool = False,
        case_sensitive: bool = True,
    ) -> bool:
        """So sánh output thực tế và mong đợi theo cấu hình."""
        actual_norm = self.normalize_output(actual, remove_spaces, case_sensitive)
        expected_norm = self.normalize_output(expected, remove_spaces, case_sensitive)
        return actual_norm == expected_norm

    def run_question(self, q_num: int, test_cases: list[dict]) -> dict | None:
        """Chạy test cho 1 câu hỏi (folder 1..4)."""
        print(f"\n{'=' * 70}")
        print(f"🔷 QUESTION {q_num}")
        print(f"{'=' * 70}")

        question_dir = self.base_dir / str(q_num)
        if not question_dir.exists():
            print(f"⚠️  Không tìm thấy folder: {question_dir}")
            return None

        jar_file = self.find_jar_file(question_dir)
        if not jar_file:
            print(f"⚠️  Không tìm thấy file .jar trong {question_dir / 'run'}")
            return None

        print(f"📦 Sử dụng: {jar_file.name}\n")

        total_mark = 0.0
        earned_mark = 0.0
        results: list[dict] = []

        for tc in test_cases:
            tc_num = tc["tc_num"]
            print(f"┌─ Test Case {tc_num} ─────────────────────────────────────")

            input_display = (tc["input"][:80] + "...") if len(tc["input"]) > 80 else tc["input"]
            print(f"│ 📥 Input:    {input_display}")

            expected_display = (
                tc["expected_output"][:80] + "..." if len(tc["expected_output"]) > 80 else tc["expected_output"]
            )
            print(f"│ 📋 Expected: {expected_display}")

            stdout, stderr, returncode = self.run_jar_with_input(jar_file, tc["input"])

            if returncode != 0:
                print(f"│ ❌ ERROR: {stderr[:100]}")
                print(f"│ 💯 Score: 0/{tc['mark']}")
                print(f"└{'─' * 65}\n")
                results.append(
                    {
                        "tc_num": tc_num,
                        "passed": False,
                        "max_mark": tc["mark"],
                        "earned": 0.0,
                    }
                )
                total_mark += tc["mark"]
                continue

            actual_display = stdout[:80] + "..." if len(stdout) > 80 else stdout
            print(f"│ 📤 Actual:   {actual_display}")

            passed = self.compare_outputs(
                stdout, tc["expected_output"], tc["remove_spaces"], tc["case_sensitive"]
            )

            if passed:
                print("│ ✅ PASS")
                print(f"│ 💯 Score: {tc['mark']}/{tc['mark']}")
                earned_mark += tc["mark"]
                results.append(
                    {
                        "tc_num": tc_num,
                        "passed": True,
                        "max_mark": tc["mark"],
                        "earned": tc["mark"],
                    }
                )
            else:
                print("│ ❌ FAIL")
                print(f"│ 💯 Score: 0/{tc['mark']}")
                results.append(
                    {
                        "tc_num": tc_num,
                        "passed": False,
                        "max_mark": tc["mark"],
                        "earned": 0.0,
                    }
                )

            print(f"└{'─' * 65}\n")
            total_mark += tc["mark"]

        return {
            "question": q_num,
            "total_mark": total_mark,
            "earned_mark": earned_mark,
            "results": results,
        }

    def run_all_tests(self) -> None:
        """Chạy tất cả test cho 4 câu hỏi."""
        print("\n" + "=" * 70)
        print("🎯 PE TEST RUNNER - BẮT ĐẦU CHẤM BÀI")
        print("=" * 70)

        all_tests = self.parse_tests()
        if not all_tests:
            print("⚠️  Không tìm thấy test case nào trong tests.txt")
            return

        all_results: list[dict] = []
        for q_num in range(1, 5):
            if q_num in all_tests:
                result = self.run_question(q_num, all_tests[q_num])
                if result:
                    all_results.append(result)
            else:
                print(f"\n⚠️  Không có test case cho Question {q_num}")

        self.print_summary(all_results)

    def print_summary(self, all_results: list[dict]) -> None:
        """In tổng kết điểm cuối cùng."""
        print("\n" + "=" * 70)
        print("📊 TỔNG KẾT ĐIỂM")
        print("=" * 70)

        total_earned = 0.0
        total_max = 0.0

        for result in all_results:
            q_num = result["question"]
            earned = result["earned_mark"]
            max_mark = result["total_mark"]
            percentage = (earned / max_mark * 100) if max_mark > 0 else 0.0

            total_earned += earned
            total_max += max_mark

            status = "✅" if earned == max_mark else ("❌" if earned == 0 else "⚠️")
            print(f"{status} Question {q_num}: {earned:.1f}/{max_mark:.1f} ({percentage:.1f}%)")

            for tc_result in result["results"]:
                tc_status = "✅" if tc_result["passed"] else "❌"
                print(
                    f"   {tc_status} TC{tc_result['tc_num']}: {tc_result['earned']:.1f}/{tc_result['max_mark']:.1f}"
                )

        print("─" * 70)

        final_percentage = (total_earned / total_max * 100) if total_max > 0 else 0.0
        print(f"🏆 TỔNG ĐIỂM: {total_earned:.1f}/{total_max:.1f} ({final_percentage:.1f}%)")

        if final_percentage >= 90:
            grade = "🌟 XUẤT SẮC"
        elif final_percentage >= 70:
            grade = "👍 KHÁ"
        elif final_percentage >= 50:
            grade = "📝 TRUNG BÌNH"
        else:
            grade = "📉 CẦN CỐ GẮNG"

        print(f"📈 Đánh giá: {grade}")
        print("=" * 70)


def main() -> None:
    current_dir = Path.cwd()
    print(f"📁 Working directory: {current_dir}")

    missing: list[str] = []
    for i in range(1, 5):
        if not (current_dir / str(i)).exists():
            missing.append(f"Folder {i}")

    if not (current_dir / "tests.txt").exists():
        missing.append("tests.txt")

    if missing:
        print(f"\n⚠️  Thiếu: {', '.join(missing)}")
        print("\n📋 Cấu trúc thư mục cần có:")
        print("├── 1/")
        print("│   ├── src/  (code Java)")
        print("│   └── run/  (file .jar)")
        print("├── 2/")
        print("│   ├── src/")
        print("│   └── run/")
        print("├── 3/")
        print("│   ├── src/")
        print("│   └── run/")
        print("├── 4/")
        print("│   ├── src/")
        print("│   └── run/")
        print("└── tests.txt")
        return

    runner = PETestRunner(current_dir)
    runner.run_all_tests()


if __name__ == "__main__":
    main()


