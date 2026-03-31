import sys
import math

# Cài đặt môi trường an toàn để dịch các hàm toán học
safe_math = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
safe_math['ln'] = math.log

def parse_input(val_str):
    try:
        return float(eval(val_str, {"__builtins__": None}, safe_math))
    except Exception:
        raise ValueError(f"Không thể đọc được giá trị: {val_str}")

def input_system():
    try:
        n = int(input("Nhập số lượng ẩn (n): "))
    except ValueError:
        print("Lỗi: Vui lòng nhập một số nguyên hợp lệ.")
        sys.exit()
        
    A = []
    B = []
    print(f"\nNhập ma trận mở rộng ({n} hàng, {n+1} cột).")
    print("Mẹo: Hãy đảm bảo ma trận có tính chéo trội để thuật toán hội tụ!")
    
    for i in range(n):
        while True:
            row_str = input(f"Nhập hàng thứ {i+1}: ").split()
            if len(row_str) != n + 1:
                print(f"Lỗi: Hàng này phải có đúng {n+1} phần tử. Vui lòng nhập lại!")
                continue
            
            try:
                row_vals = [parse_input(val) for val in row_str]
                A.append(row_vals[:-1]) # Lấy n phần tử đầu làm ma trận hệ số A
                B.append(row_vals[-1])  # Lấy phần tử cuối làm vector hằng số B
                break
            except ValueError as e:
                print(f"Lỗi: {e}. Vui lòng nhập lại hàng này.")
                
    return A, B, n

def gauss_seidel_method(A, B, n, tolerance=1e-6, max_iterations=100):
    # Kiểm tra phần tử trên đường chéo chính bằng 0
    for i in range(n):
        if A[i][i] == 0:
            print(f"Lỗi: Phần tử trên đường chéo chính A[{i+1}][{i+1}] bằng 0. Phương pháp lặp không thể thực hiện.")
            return None

    # Khởi tạo vector nghiệm ban đầu
    x = [0.0] * n
    
    for k in range(max_iterations):
        x_old = x.copy()
        
        for i in range(n):
            # Tính tổng A[i][j] * x[j]. 
            # Lưu ý: Lúc này mảng x đã chứa cả những giá trị MỚI NHẤT vừa được cập nhật.
            s = sum(A[i][j] * x[j] for j in range(n) if j != i)
            # Cập nhật trực tiếp vào mảng x
            x[i] = (B[i] - s) / A[i][i]
            
        # Kiểm tra điều kiện dừng
        max_diff = max(abs(x[i] - x_old[i]) for i in range(n))
        if max_diff < tolerance:
            print(f"\n-> Thuật toán hội tụ thành công sau {k+1} bước lặp.")
            return x
            
    print(f"\n-> Cảnh báo: Thuật toán không hội tụ sau {max_iterations} bước lặp. (Có thể do ma trận không chéo trội)")
    return x

if __name__ == "__main__":
    print("--- CHƯƠNG TRÌNH GIẢI HỆ PHƯƠNG TRÌNH BẰNG PHƯƠNG PHÁP GAUSS - SEIDEL ---")
    A, B, n = input_system()
    result = gauss_seidel_method(A, B, n)
    
    if result is not None:
        print("\n=> Nghiệm gần đúng của hệ phương trình là:")
        for i in range(n):
            print(f"x[{i+1}] = {result[i]:.12f}")