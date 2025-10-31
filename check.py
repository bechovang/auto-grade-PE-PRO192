import os
import subprocess
import re
from pathlib import Path

class JavaTestRunner:
    def __init__(self, java_dir, test_dir):
        self.java_dir = Path(java_dir)
        self.test_dir = Path(test_dir)
        self.src_dir = self.java_dir / "src"
        
    def compile_java(self):
        """Biên dịch các file Java"""
        print("=== Biên dịch Java files ===")
        java_files = list(self.src_dir.glob("*.java"))
        
        if not java_files:
            print("Không tìm thấy file .java nào!")
            return False
            
        # Compile tất cả java files với UTF-8 encoding
        compile_cmd = ["javac", "-encoding", "UTF-8"] + [str(f) for f in java_files]
        
        try:
            result = subprocess.run(
                compile_cmd,
                capture_output=True,
                text=True,
                cwd=str(self.src_dir)
            )
            
            if result.returncode != 0:
                print(f"Lỗi biên dịch:\n{result.stderr}")
                return False
            else:
                print("✓ Biên dịch thành công!")
                return True
        except Exception as e:
            print(f"Lỗi khi biên dịch: {e}")
            return False
    
    def find_main_class(self):
        """Tìm class có phương thức main() - thử main, Main, và tìm tự động"""
        # Thử các tên phổ biến trước
        common_names = ["main", "Main"]
        for name in common_names:
            class_file = self.src_dir / f"{name}.class"
            if class_file.exists():
                print(f"✓ Tìm thấy class: {name}")
                return name
        
        # Nếu không có, tìm trong các file .java
        java_files = list(self.src_dir.glob("*.java"))
        
        for java_file in java_files:
            try:
                with open(java_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Tìm public static void main
                    if re.search(r'public\s+static\s+void\s+main\s*\(', content):
                        # Lấy tên class từ tên file
                        class_name = java_file.stem
                        print(f"✓ Tìm thấy main() trong file: {class_name}.java")
                        return class_name
            except:
                continue
        
        # Không tìm thấy - báo cáo chi tiết
        print("\n⚠️ KHÔNG TÌM THẤY MAIN CLASS!")
        self.report_available_files()
        
        return "main"  # Fallback to default
    
    def report_available_files(self):
        """Báo cáo tất cả file .java và .class có sẵn"""
        print("\n" + "="*60)
        print("📋 DANH SÁCH FILE TRONG THỦ MỤC:")
        print("="*60)
        
        # Tìm tất cả file .java
        java_files = list(self.src_dir.rglob("*.java"))
        if java_files:
            print(f"\n📄 File .java ({len(java_files)} file):")
            for f in sorted(java_files):
                rel_path = f.relative_to(self.src_dir)
                print(f"   - {rel_path}")
        else:
            print("\n📄 File .java: Không tìm thấy")
        
        # Tìm tất cả file .class
        class_files = list(self.src_dir.rglob("*.class"))
        if class_files:
            print(f"\n🔹 File .class ({len(class_files)} file):")
            for f in sorted(class_files):
                rel_path = f.relative_to(self.src_dir)
                # Lấy tên class (không có đường dẫn và extension)
                class_name = str(rel_path).replace('\\', '.').replace('/', '.')[:-6]
                print(f"   - {rel_path} → class: {class_name}")
        else:
            print("\n🔹 File .class: Không tìm thấy (cần biên dịch)")
        
        print("\n💡 GỢI Ý:")
        print("   1. Kiểm tra xem có file .class nào sau khi compile")
        print("   2. Đảm bảo có file chứa 'public static void main(String[] args)'")
        print("   3. Tên class phải khớp với tên file .java")
        print("="*60 + "\n")
    
    def _try_run_java(self, class_name, input_data):
        """Thử chạy Java với tên class cụ thể"""
        try:
            result = subprocess.run(
                ["java", class_name],
                input=input_data,
                capture_output=True,
                text=True,
                cwd=str(self.src_dir),
                timeout=10
            )
            
            # Chỉ lấy phần sau chữ "OUTPUT:"
            stdout = result.stdout
            if "OUTPUT:" in stdout:
                # Lấy phần sau "OUTPUT:" và loại bỏ phần BUILD SUCCESSFUL
                output_part = stdout.split("OUTPUT:")[1]
                # Loại bỏ phần BUILD SUCCESSFUL nếu có
                if "BUILD SUCCESSFUL" in output_part:
                    output_part = output_part.split("BUILD SUCCESSFUL")[0]
                stdout = output_part.strip()
            
            return stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            return "", "TIMEOUT", -1
        except Exception as e:
            return "", str(e), -1
    
    def run_java_with_input(self, input_data):
        """Chạy main.java với input và trả về output"""
        try:
            # Tự động tìm class có main method
            main_class = self.find_main_class()
            
            # Thử chạy với tên tìm được
            result = self._try_run_java(main_class, input_data)
            if result[2] == 0:  # returncode == 0 nghĩa là thành công
                return result
            
            # Nếu fail, thử các tên phổ biến khác
            for fallback_name in ["main", "Main"]:
                if fallback_name != main_class:
                    result = self._try_run_java(fallback_name, input_data)
                    if result[2] == 0:
                        return result
            
            # Trả về kết quả cuối cùng (có thể là lỗi)
            return result
        except Exception as e:
            return "", str(e), -1
    
    def parse_test_case(self, tc_file):
        """Parse file test case để lấy INPUT, OUTPUT và các config"""
        with open(tc_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse INPUT
        input_match = re.search(r'INPUT:\s*\n(.*?)\nOUTPUT:', content, re.DOTALL)
        input_data = input_match.group(1).strip() if input_match else ""
        
        # Parse OUTPUT
        output_match = re.search(r'OUTPUT:\s*\n(.*?)\n(?:REMOVE_SPACES|CASE_SENSITIVE|MARK|$)', content, re.DOTALL)
        expected_output = output_match.group(1).strip() if output_match else ""
        
        # Parse configs
        remove_spaces = re.search(r'REMOVE_SPACES:\s*\n(YES|NO)', content)
        remove_spaces = remove_spaces.group(1) == "YES" if remove_spaces else False
        
        case_sensitive = re.search(r'CASE_SENSITIVE:\s*\n(YES|NO)', content)
        case_sensitive = case_sensitive.group(1) == "YES" if case_sensitive else True
        
        mark = re.search(r'MARK:\s*\n([\d.]+)', content)
        mark = float(mark.group(1)) if mark else 0.0
        
        return {
            'input': input_data,
            'expected_output': expected_output,
            'remove_spaces': remove_spaces,
            'case_sensitive': case_sensitive,
            'mark': mark
        }
    
    def normalize_output(self, text, remove_spaces=False, case_sensitive=True):
        """Chuẩn hóa output theo config"""
        result = text.strip()
        
        if remove_spaces:
            result = re.sub(r'\s+', '', result)
        
        if not case_sensitive:
            result = result.lower()
        
        return result
    
    def compare_outputs(self, actual, expected, remove_spaces=False, case_sensitive=True):
        """So sánh output thực tế với expected"""
        actual_normalized = self.normalize_output(actual, remove_spaces, case_sensitive)
        expected_normalized = self.normalize_output(expected, remove_spaces, case_sensitive)
        
        return actual_normalized == expected_normalized
    
    def run_all_tests(self):
        """Chạy tất cả test cases"""
        # Biên dịch trước
        if not self.compile_java():
            return
        
        print("\n" + "="*60)
        print("BẮT ĐẦU CHẠY TEST CASES")
        print("="*60 + "\n")
        
        # Lấy tất cả test case files
        test_files = sorted(self.test_dir.glob("tc*.txt"))
        
        if not test_files:
            print("Không tìm thấy test case nào!")
            return
        
        total_mark = 0
        earned_mark = 0
        results = []
        
        for tc_file in test_files:
            tc_name = tc_file.stem
            print(f"--- {tc_name.upper()} ---")
            
            # Parse test case
            tc_data = self.parse_test_case(tc_file)
            
            print(f"Input: {tc_data['input'][:50]}..." if len(tc_data['input']) > 50 else f"Input: {tc_data['input']}")
            print(f"Expected: {tc_data['expected_output'][:50]}..." if len(tc_data['expected_output']) > 50 else f"Expected: {tc_data['expected_output']}")
            
            # Chạy Java program
            stdout, stderr, returncode = self.run_java_with_input(tc_data['input'])
            
            if returncode != 0:
                print(f"✗ LỖI: {stderr}")
                
                # Nếu lỗi "Could not find or load main class", báo cáo chi tiết
                if "Could not find or load main class" in stderr:
                    print("\n⚠️ Không thể tìm thấy hoặc load main class!")
                    self.report_available_files()
                
                print(f"Điểm: 0/{tc_data['mark']}\n")
                results.append((tc_name, False, tc_data['mark'], 0))
                total_mark += tc_data['mark']
                continue
            
            print(f"Actual: {stdout[:50]}..." if len(stdout) > 50 else f"Actual: {stdout}")
            
            # So sánh kết quả
            passed = self.compare_outputs(
                stdout,
                tc_data['expected_output'],
                tc_data['remove_spaces'],
                tc_data['case_sensitive']
            )
            
            if passed:
                print(f"✓ PASS")
                print(f"Điểm: {tc_data['mark']}/{tc_data['mark']}\n")
                results.append((tc_name, True, tc_data['mark'], tc_data['mark']))
                earned_mark += tc_data['mark']
            else:
                print(f"✗ FAIL")
                print(f"Điểm: 0/{tc_data['mark']}\n")
                results.append((tc_name, False, tc_data['mark'], 0))
            
            total_mark += tc_data['mark']
        
        # Tổng kết
        print("="*60)
        print("TỔNG KẾT")
        print("="*60)
        for tc_name, passed, max_mark, earned in results:
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"{tc_name}: {status} - {earned}/{max_mark} điểm")
        
        print(f"\nTổng điểm: {earned_mark}/{total_mark}")
        print(f"Tỷ lệ: {earned_mark/total_mark*100:.1f}%")
        print("="*60)

def main():
    # Cấu hình đường dẫn
    current_dir = Path.cwd()
    java_dir = current_dir / "given"
    test_dir = current_dir / "TestCases"
    
    # Kiểm tra thư mục tồn tại
    if not java_dir.exists():
        print(f"Không tìm thấy thư mục: {java_dir}")
        return
    
    if not test_dir.exists():
        print(f"Không tìm thấy thư mục: {test_dir}")
        return
    
    # Chạy test
    runner = JavaTestRunner(java_dir, test_dir)
    runner.run_all_tests()

if __name__ == "__main__":
    main()