import sys
import sympy as sp

def input_sympy_matrix():
    try:
        n = int(input("Nhập số lượng ẩn (n): "))
    except ValueError:
        print("Lỗi: Vui lòng nhập một số nguyên hợp lệ.")
        sys.exit()
        
    a = []
    print(f"\nNhập ma trận mở rộng ({n} hàng, {n+1} cột).")
    print("Mẹo: Hỗ trợ phân số (1/3), căn (sqrt(2)), hằng số (pi, E), logarit (ln(3))...")
    
    e_normal = sp.Symbol('e')
    local_dict = {'ln': sp.log, 'E': e_normal, 'e': e_normal}
    
    for i in range(n):
        while True:
            row_str = input(f"Nhập hàng thứ {i+1}: ").split()
            if len(row_str) != n + 1:
                print(f"Lỗi: Hàng này phải có đúng {n+1} phần tử. Vui lòng nhập lại!")
                continue
            
            try:
                row = [sp.sympify(val, locals=local_dict) for val in row_str]
                a.append(row)
                break
            except Exception:
                print(f"Lỗi đọc dữ liệu: Không hiểu được giá trị bạn nhập. Vui lòng nhập lại.")
                
    return a, n, e_normal

if __name__ == "__main__":
    print("--- CHƯƠNG TRÌNH GIẢI HỆ PT BẰNG GAUSS - JORDAN (SYMPY) ---")
    a, n, e_normal = input_sympy_matrix()
    
    symbols = sp.symbols(f'x1:{n+1}')
    A_aug = sp.Matrix(a)
    
    print("\n[1] Ma trận mở rộng ban đầu:")
    sp.pprint(A_aug)
    
    # RREF: Đưa về dạng bậc thang rút gọn (Gauss-Jordan)
    A_rref, pivots = A_aug.rref()
    print("\n[2] Ma trận sau khi khử Gauss - Jordan (Dạng bậc thang rút gọn):")
    sp.pprint(A_rref)
    
    solution = sp.linsolve(A_aug, symbols)
    
    print("\n[3] KẾT LUẬN:")
    if solution == sp.EmptySet:
        print("=> Hệ phương trình VÔ NGHIỆM.")
    else:
        print("=> Bộ nghiệm của hệ là:")
        sol_list = list(solution)[0]
        
        for i in range(n):
            approx_str = ""
            try:
                # Tính giá trị xấp xỉ
                val_approx = float(sol_list[i].subs(e_normal, sp.E).evalf())
                approx_str = f"    ≈ {val_approx:.12f}"
            except TypeError:
                pass # Bỏ qua nếu là ẩn tự do (hệ có vô số nghiệm)

            # Ép biểu thức về dạng tuyến tính 1D (sstr) để đồng nhất định dạng phân số
            eq_str = f"x{i+1} = {sp.sstr(sol_list[i])}"
            
            # In thẳng ra màn hình
            print(f"{eq_str}{approx_str}\n")