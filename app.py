import streamlit as st

st.set_page_config(page_title="CV Builder - Full Data Input", layout="wide")
st.title("📝 Form Pengisian Data CV Profesional")

# 1. Inisialisasi Session State untuk Data Dinamis
if "pengalaman" not in st.session_state:
    st.session_state.pengalaman = [{"perusahaan": "", "posisi": "", "periode": "", "deskripsi": ""}]

if "pendidikan" not in st.session_state:
    st.session_state.pendidikan = [{"institusi": "", "jurusan": "", "tahun": "", "nilai": ""}]

if "proyek" not in st.session_state:
    st.session_state.proyek = [{"nama": "", "peran": "", "tools": "", "link": "", "deskripsi": ""}]

if "sertifikasi" not in st.session_state:
    st.session_state.sertifikasi = [{"nama": "", "penerbit": "", "tahun": "", "link": ""}]

if "organisasi" not in st.session_state:
    st.session_state.organisasi = [{"nama_org": "", "peran": "", "periode": "", "deskripsi": ""}]


# 2. Pengelompokan Menggunakan 5 Tab Utama
tab_profil, tab_exp, tab_edu, tab_proj_cert, tab_skill_org = st.tabs([
    "👤 Profil & Kontak", 
    "💼 Pengalaman Kerja", 
    "🎓 Pendidikan", 
    "🚀 Proyek & Sertifikasi",
    "⚡ Skill & Organisasi"
])

# --- TAB 1: PROFIL & KONTAK ---
with tab_profil:
    st.subheader("Informasi Pribadi & Kontak")
    c1, c2 = st.columns(2)
    with c1:
        nama = st.text_input("Nama Lengkap", placeholder="Budi Santoso, S.Kom.")
        email = st.text_input("Email", placeholder="budi@email.com")
        telepon = st.text_input("Nomor Telepon/WhatsApp", placeholder="+62 812 3456 7890")
        lokasi = st.text_input("Domisili Saat Ini", placeholder="Jakarta Selatan, Indonesia")
    
    with c2:
        posisi_target = st.text_input("Posisi/Jabatan Dilamar", placeholder="Software Engineer / Data Analyst")
        linkedin = st.text_input("URL LinkedIn", placeholder="linkedin.com/in/budisantoso")
        github_portfolio = st.text_input("URL GitHub / Portofolio / Website", placeholder="github.com/budisantoso")

    st.subheader("Ringkasan Profil (Professional Summary)")
    ringkasan = st.text_area(
        "Rangkuman Singkat (3-4 kalimat)", 
        placeholder="Software Engineer dengan pengalaman 3+ tahun dalam membangun aplikasi web bertrafik tinggi. Memiliki keahlian kuat di Python dan SQL. Berhasil meningkatkan efisiensi sistem sebesar 25% di proyek sebelumnya.",
        height=120
    )

# --- TAB 2: PENGALAMAN KERJA ---
with tab_exp:
    st.subheader("Riwayat Pengalaman Kerja")
    st.caption("Urutkan dari pekerjaan paling terbaru/saat ini.")
    
    for i, exp in enumerate(st.session_state.pengalaman):
        title_label = f"Pengalaman #{i+1}: {exp['posisi']} - {exp['perusahaan']}" if exp['posisi'] else f"Pengalaman #{i+1}"
        with st.expander(title_label, expanded=True):
            c1, c2 = st.columns(2)
            exp["perusahaan"] = c1.text_input("Nama Perusahaan / Organisasi", value=exp["perusahaan"], key=f"corp_{i}")
            exp["posisi"] = c2.text_input("Jabatan / Posisi", value=exp["posisi"], key=f"pos_{i}")
            exp["periode"] = st.text_input("Periode Kerja", value=exp["periode"], key=f"per_{i}", placeholder="Jan 2022 - Sekarang")
            exp["deskripsi"] = st.text_area(
                "Pencapaian & Tugas Utama", 
                value=exp["deskripsi"], 
                key=f"desc_{i}",
                placeholder="- Mengembangkan fitur X yang meningkatkan aktivasi pengguna sebesar 15%\n- Memimpin tim berisi 4 developer dalam proyek Y",
                height=100
            )

    if st.button("➕ Tambah Pengalaman Kerja"):
        st.session_state.pengalaman.append({"perusahaan": "", "posisi": "", "periode": "", "deskripsi": ""})
        st.rerun()

# --- TAB 3: PENDIDIKAN ---
with tab_edu:
    st.subheader("Riwayat Pendidikan")
    
    for j, edu in enumerate(st.session_state.pendidikan):
        with st.expander(f"Pendidikan #{j+1}", expanded=True):
            e1, e2 = st.columns(2)
            edu["institusi"] = e1.text_input("Nama Universitas / Sekolah", value=edu["institusi"], key=f"inst_{j}")
            edu["jurusan"] = e2.text_input("Jurusan / Program Studi", value=edu["jurusan"], key=f"jur_{j}")
            edu["tahun"] = e1.text_input("Tahun Masuk - Lulus", value=edu["tahun"], key=f"thn_{j}", placeholder="2019 - 2023")
            edu["nilai"] = e2.text_input("IPK / Nilai Akhir (Opsional)", value=edu["nilai"], key=f"nil_{j}", placeholder="3.85 / 4.00")

    if st.button("➕ Tambah Pendidikan"):
        st.session_state.pendidikan.append({"institusi": "", "jurusan": "", "tahun": "", "nilai": ""})
        st.rerun()

# --- TAB 4: PROYEK & SERTIFIKASI ---
with tab_proj_cert:
    st.subheader("📌 Proyek Terkait / Portofolio")
    st.caption("Sangat direkomendasikan untuk posisi IT, Kreatif, atau jika belum banyak pengalaman kerja.")
    
    for k, proj in enumerate(st.session_state.proyek):
        with st.expander(f"Proyek #{k+1}: {proj['nama']}" if proj['nama'] else f"Proyek #{k+1}", expanded=True):
            p1, p2 = st.columns(2)
            proj["nama"] = p1.text_input("Nama Proyek", value=proj["nama"], key=f"pname_{k}")
            proj["peran"] = p2.text_input("Peran Anda", value=proj["peran"], key=f"prole_{k}", placeholder="Lead Developer / Designer")
            proj["tools"] = p1.text_input("Teknologi / Tools yang Digunakan", value=proj["tools"], key=f"ptools_{k}", placeholder="Python, Streamlit, PostgreSQL")
            proj["link"] = p2.text_input("Link Demo / Repository (Opsional)", value=proj["link"], key=f"plink_{k}", placeholder="https://github.com/...")
            proj["deskripsi"] = st.text_area("Deskripsi & Hasil Proyek", value=proj["deskripsi"], key=f"pdesc_{k}", height=80)

    if st.button("➕ Tambah Proyek"):
        st.session_state.proyek.append({"nama": "", "peran": "", "tools": "", "link": "", "deskripsi": ""})
        st.rerun()

    st.markdown("---")
    st.subheader("📜 Sertifikasi & Lisensi Profesional")
    
    for l, cert in enumerate(st.session_state.sertifikasi):
        with st.expander(f"Sertifikat #{l+1}: {cert['nama']}" if cert['nama'] else f"Sertifikat #{l+1}", expanded=True):
            s1, s2 = st.columns(2)
            cert["nama"] = s1.text_input("Nama Sertifikasi", value=cert["nama"], key=f"cname_{l}", placeholder="AWS Certified Solutions Architect")
            cert["penerbit"] = s2.text_input("Organisasi Penerbit", value=cert["penerbit"], key=f"cpub_{l}", placeholder="Amazon Web Services")
            cert["tahun"] = s1.text_input("Tahun Terbit / Masa Berlaku", value=cert["tahun"], key=f"cyear_{l}", placeholder="2023 - 2026")
            cert["link"] = s2.text_input("Link Kredensial / ID Sertifikat", value=cert["link"], key=f"clink_{l}")

    if st.button("➕ Tambah Sertifikasi"):
        st.session_state.sertifikasi.append({"nama": "", "penerbit": "", "tahun": "", "link": ""})
        st.rerun()

# --- TAB 5: SKILL, ORGANISASI & PRESTASI ---
with tab_skill_org:
    st.subheader("⚡ Keahlian (Skills)")
    sk1, sk2 = st.columns(2)
    hard_skills = sk1.text_area("Hard Skills (Pisahkan dengan koma)", placeholder="Python, SQL, HTML/CSS, Git, Data Analysis")
    soft_skills = sk2.text_area("Soft Skills (Pisahkan dengan koma)", placeholder="Problem Solving, Public Speaking, Leadership, Teamwork")
    bahasa = st.text_input("Bahasa yang Dikuasai", placeholder="Indonesia (Native), Inggris (Professional Working)")

    st.markdown("---")
    st.subheader("🏆 Pengalaman Organisasi / Relawan / Prestasi")
    
    for m, org in enumerate(st.session_state.organisasi):
        with st.expander(f"Organisasi/Prestasi #{m+1}", expanded=True):
            o1, o2 = st.columns(2)
            org["nama_org"] = o1.text_input("Nama Organisasi / Kegiatan / Kompetisi", value=org["nama_org"], key=f"oname_{m}")
            org["peran"] = o2.text_input("Peran / Juara", value=org["peran"], key=f"orole_{m}", placeholder="Ketua Himpunan / Juara 1 Hackathon")
            org["periode"] = o1.text_input("Tahun / Periode", value=org["periode"], key=f"oper_{m}", placeholder="2022")
            org["deskripsi"] = st.text_area("Deskripsi Singkat", value=org["deskripsi"], key=f"odesc_{m}", height=70)

    if st.button("➕ Tambah Organisasi/Prestasi"):
        st.session_state.organisasi.append({"nama_org": "", "peran": "", "periode": "", "deskripsi": ""})
        st.rerun()
