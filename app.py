import streamlit as st

st.set_page_config(page_title="CV Builder - Input Data", layout="wide")
st.title("📝 Input Data CV")

# 1. Inisialisasi Session State untuk Data Dinamis
if "pengalaman" not in st.session_state:
    st.session_state.pengalaman = [{"perusahaan": "", "posisi": "", "periode": "", "deskripsi": ""}]

if "pendidikan" not in st.session_state:
    st.session_state.pendidikan = [{"institusi": "", "jurusan": "", "tahun": "", "nilai": ""}]

# 2. Pengelompokan Menggunakan Tabs
tab_profil, tab_exp, tab_edu, tab_skill = st.tabs([
    "👤 Profil Utama", 
    "💼 Pengalaman Kerja", 
    "🎓 Pendidikan", 
    "⚡ Skill & Lainnya"
])

# --- TAB 1: PROFIL UTAMA ---
with tab_profil:
    st.subheader("Informasi Kontak & Ringkasan")
    col1, col2 = st.columns(2)
    with col1:
        nama = st.text_input("Nama Lengkap", placeholder="Contoh: Budi Santoso")
        email = st.text_input("Email", placeholder="budi@email.com")
        telepon = st.text_input("Nomor Telepon", placeholder="+62 812 3456 7890")
    with col2:
        posisi_target = st.text_input("Posisi/Title Dilamar", placeholder="Contoh: Frontend Developer")
        lokasi = st.text_input("Domisili", placeholder="Jakarta, Indonesia")
        linkedin = st.text_input("URL LinkedIn / Portofolio", placeholder="linkedin.com/in/budi")

    ringkasan = st.text_area(
        "Ringkasan Profesional", 
        placeholder="Tuliskan 3-4 kalimat yang merangkum pengalaman dan nilai jual utama Anda...",
        height=120
    )

# --- TAB 2: PENGALAMAN KERJA (DINAMIS) ---
with tab_exp:
    st.subheader("Riwayat Pengalaman Kerja")
    
    for i, exp in enumerate(st.session_state.pengalaman):
        title_label = f"Pengalaman #{i+1}: {exp['posisi']}" if exp['posisi'] else f"Pengalaman #{i+1}"
        with st.expander(title_label, expanded=True):
            c1, c2 = st.columns(2)
            exp["perusahaan"] = c1.text_input(f"Nama Perusahaan", value=exp["perusahaan"], key=f"corp_{i}")
            exp["posisi"] = c2.text_input(f"Jabatan / Posisi", value=exp["posisi"], key=f"pos_{i}")
            exp["periode"] = st.text_input(f"Periode (Contoh: Jan 2022 - Present)", value=exp["periode"], key=f"per_{i}")
            exp["deskripsi"] = st.text_area(
                f"Pencapaian & Tugas (Gunakan bullet point)", 
                value=exp["deskripsi"], 
                key=f"desc_{i}",
                help="Gunakan tanda strip (-) di awal baris untuk membuat list."
            )

    c_add, c_del = st.columns([1, 5])
    if c_add.button("➕ Tambah Pengalaman"):
        st.session_state.pengalaman.append({"perusahaan": "", "posisi": "", "periode": "", "deskripsi": ""})
        st.rerun()

# --- TAB 3: PENDIDIKAN (DINAMIS) ---
with tab_edu:
    st.subheader("Riwayat Pendidikan")
    
    for j, edu in enumerate(st.session_state.pendidikan):
        with st.expander(f"Pendidikan #{j+1}", expanded=True):
            e1, e2 = st.columns(2)
            edu["institusi"] = e1.text_input("Nama Sekolah / Universitas", value=edu["institusi"], key=f"inst_{j}")
            edu["jurusan"] = e2.text_input("Jurusan / Program Studi", value=edu["jurusan"], key=f"jur_{j}")
            edu["tahun"] = e1.text_input("Tahun Lulus", value=edu["tahun"], key=f"thn_{j}")
            edu["nilai"] = e2.text_input("IPK / Nilai (Opsional)", value=edu["nilai"], key=f"nil_{j}")

    if st.button("➕ Tambah Pendidikan"):
        st.session_state.pendidikan.append({"institusi": "", "jurusan": "", "tahun": "", "nilai": ""})
        st.rerun()

# --- TAB 4: SKILL & LAINNYA ---
with tab_skill:
    st.subheader("Keahlian & Informasi Tambahan")
    skills = st.text_area("Hard Skills (Pisahkan dengan koma)", placeholder="Python, SQL, HTML/CSS, Git")
    soft_skills = st.text_area("Soft Skills (Pisahkan dengan koma)", placeholder="Problem Solving, Teamwork, Communication")
    bahasa = st.text_input("Bahasa yang Dikuasai", placeholder="Indonesia (Native), Inggris (Professional Working)")
