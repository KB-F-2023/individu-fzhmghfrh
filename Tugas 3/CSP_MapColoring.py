# Membuat fungsi recursive untuk melakukan Backtracking
def backtracking_search(assignment, csp):
    # Memeriksa apakah semua variabel sudah di-assign
    if len(assignment) == len(csp.states):
        return assignment

    # Memilih variabel yang belum di-assign
    var = select_unassigned_variable(assignment, csp)

    # Memilih nilai dari color variabel
    for value in order_color_values(var, assignment, csp):
        # Mengecek apakah nilai yang di-assign memenuhi constraint
        if is_consistent(var, value, assignment, csp):
            # Jika memenuhi constraint, maka di-assign
            assignment[var] = value
            # Memeriksa apakah solusi ditemukan dengan mengambil nilai dari variabel berikutnya
            result = backtracking_search(assignment, csp)
            # Jika solusi ditemukan, maka solusi dikembalikan
            if result is not None:
                return result
            # Jika solusi tidak ditemukan, maka nilai yang di-assign dihapus dan mencoba nilai dari color yang lain
            del assignment[var]

    # Jika solusi tidak ditemukan, kembali ke node parent
    return None


# Fungsi untuk memilih variabel yang belum di-assign
def select_unassigned_variable(assignment, csp):
    for var in csp.states:
        if var not in assignment:
            return var


# Fungsi untuk memilih nilai dari color variabel
def order_color_values(var, assignment, csp):
    return csp.colors[var]


# Fungsi untuk memeriksa apakah nilai yang di-assign memenuhi constraint
def is_consistent(var, value, assignment, csp):
    # Mengecek constraint dengan variabel tetangga
    for neighbor in csp.neighbors[var]:
        if neighbor in assignment and assignment[neighbor] == value:
            return False
    return True


# Class CSP untuk Map Coloring
class MapColoringCSP:
    def __init__(self, states, colors, neighbors):
        self.states = states
        self.colors = colors
        self.neighbors = neighbors


# Inisialisasi Map Coloring
states = ["WA", "NT", "Q", "NSW", "V", "SA", "T"]
colors = {
    "WA": ["red", "green", "blue"],
    "NT": ["red", "green", "blue"],
    "Q": ["red", "green"],
    "NSW": ["red", "green", "blue"],
    "V": ["red", "green", "blue"],
    "SA": ["red", "green", "blue"],
    "T": ["red", "green"],
}
neighbors = {
    "WA": ["NT", "SA"],
    "NT": ["WA", "SA", "Q"],
    "Q": ["NT", "SA", "NSW"],
    "NSW": ["Q", "SA", "V"],
    "V": ["NSW", "SA"],
    "SA": ["WA", "NT", "Q", "NSW", "V", "T"],
    "T": ["SA"],
}

# Inisialisasi CSP
csp = MapColoringCSP(states, colors, neighbors)

# Solusi Map Coloring menggunakan Backtracking
solution = backtracking_search({}, csp)

# Cetak hasil solusi
print(solution)
