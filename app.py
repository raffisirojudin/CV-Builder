import streamlit as st
from jinja2 import Template
from xhtml2pdf import pisa
import io

st.set_page_config(page_title="AI & Modern CV Builder", layout="wide")

# ==========================================
# 1. INISIALISASI SESSION STATE
# ==========================================
if "pengalaman" not in st.session_state:
    st.session_state.pengalaman = [{"perusahaan": "PT Teknologi Nusantara", "posisi": "Software Engineer", "periode": "Jan 2022 - Sekarang", "deskripsi": "- Mengembangkan API menggunakan Python & FastAPI\n- Meningkatkan performa database sebesar 30%"}]

if "pendidikan" not in st.session_state:
    st.session_state.pendidikan = [{"institusi": "Universitas Indonesia", "jurusan": "Teknik Informatika", "tahun": "2018 - 2022", "nilai": "3.80 / 4.00"}]

if "proyek" not in st.session_state:
    st.session_state.proyek = [{"nama": "E-Commerce App", "peran": "Lead Developer", "tools": "Python, React, PostgreSQL", "link": "github.com/user/project", "deskripsi": "Membangun sistem pembayaran terintegrasi dengan Midtrans."}]

if "sertifikasi" not in st.session_state:
    st.session_state.sertifikasi = [{"nama": "AWS Certified Developer", "penerbit": "Amazon Web Services", "tahun": "2023", "link": ""}]

if "organisasi" not in st.session_state:
    st.session_state.organisasi = []

# ==========================================
# 2. TEMPLATE HTML & CSS (JINJA2)
# ==========================================

# TEMPLATE 1: ATS CLEAN
ATS_HTML = """
<!DOCTYPE html>
<html>
<head>
<style>
    @page { size: A4; margin: 1.2cm; }
    body { font-family: {{ font_family }}, sans-serif; font-size: 9.5pt; color: #111111; line-height: 1.35; }
    .header { text-align: center; margin-bottom: 12px; }
    .name { font-size: 18pt; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }
    .title { font-size: 11pt; font-weight: bold; color: #333333; margin-top: 2px; }
    .contact { font-size: 9pt; color: #444444; margin-top: 4px; }
    
    .section-title { 
        font-size: 10.5pt; 
        font-weight: bold; 
        text-transform: uppercase; 
        border-bottom: 1px solid #111111; 
        margin-top: 10px; 
        margin-bottom: 5px; 
        padding-bottom: 1px;
    }
    
    .item-header { font-weight: bold; font-size: 9.5pt; }
    .item-sub { font-style: italic; font-size: 9pt; color: #333333; }
    .right-text { float: right; font-weight: normal; font-style: normal; }
    .desc { margin-top: 3px; margin-bottom: 6px; white-space: pre-line; }
    .skills-table { width: 100%; border-collapse: collapse; }
    .skills-table td { vertical-align: top; padding: 2px 0; }
</style>
</head>
<body>
    <div class="header">
        <div class="name">{{ nama }}</div>
        {% if posisi_target %}<div class="title">{{ posisi_target }}</div>{% endif %}
        <div class="contact">
            {{ lokasi }} {% if lokasi and (email or telepon) %}|{% endif %}
            {{ email }} {% if email and telepon %}|{% endif %}
            {{ telepon }}
            <br>
            {% if linkedin %}{{ linkedin }}{% endif %}
            {% if linkedin and github_portfolio %} | {% endif %}
            {% if github_portfolio %}{{ github_portfolio }}{% endif %}
        </div>
    </div>

    {% if ringkasan %}
    <div class="section-title">RINGKASAN PROFIL</div>
    <div class="desc">{{ ringkasan }}</div>
    {% endif %}

    {% if pengalaman and pengalaman[0].perusahaan %}
    <div class="section-title">PENGALAMAN KERJA</div>
    {% for exp in pengalaman %}
        {% if exp.perusahaan %}
        <div class="item-header">
            {{ exp.posisi }} <span class="right-text">{{ exp.periode }}</span>
        </div>
        <div class="item-sub">{{ exp.perusahaan }}</div>
        <div class="desc">{{ exp.deskripsi }}</div>
        {% endif %}
    {% endfor %}
    {% endif %}

    {% if pendidikan and pendidikan[0].institusi %}
    <div class="section-title">PENDIDIKAN</div>
    {% for edu in pendidikan %}
        {% if edu.institusi %}
        <div class="item-header">
            {{ edu.institusi }} <span class="right-text">{{ edu.tahun }}</span>
        </div>
        <div class="item-sub">{{ edu.jurusan }} {% if edu.nilai %}(IPK: {{ edu.nilai }}){% endif %}</div>
        <br>
        {% endif %}
    {% endfor %}
    {% endif %}

    {% if proyek and proyek[0].nama %}
    <div class="section-title">PROYEK TERKAIT</div>
    {% for proj in proyek %}
        {% if proj.nama %}
        <div class="item-header">
            {{ proj.nama }} {% if proj.peran %}- <i>{{ proj.peran }}</i>{% endif %}
            {% if proj.link %}<span class="right-text">{{ proj.link }}</span>{% endif %}
        </div>
        {% if proj.tools %}<div class="item-sub">Tools: {{ proj.tools }}</div>{% endif %}
        <div class="desc">{{ proj.deskripsi }}</div>
        {% endif %}
    {% endfor %}
    {% endif %}

    {% if sertifikasi and sertifikasi[0].nama %}
    <div class="section-title">SERTIFIKASI</div>
    {% for cert in sertifikasi %}
        {% if cert.nama %}
        <div class="item-header">
            {{ cert.nama }} - <span style="font-weight:normal;">{{ cert.penerbit }}</span>
            <span class="right-text">{{ cert.tahun }}</span>
        </div>
        {% endif %}
    {% endfor %}
    {% endif %}

    {% if hard_skills or soft_skills or bahasa %}
    <div class="section-title">KEAHLIAN & LAINNYA</div>
    <table class="skills-table">
        {% if hard_skills %}<tr><td width="20%"><b>Hard Skills:</b></td><td>{{ hard_skills }}</td></tr>{% endif %}
        {% if soft_skills %}<tr><td width="20%"><b>Soft Skills:</b></td><td>{{ soft_skills }}</td></tr>{% endif %}
        {% if bahasa %}<tr><td width="20%"><b>Bahasa:</b></td><td>{{ bahasa }}</td></tr>{% endif %}
    </table>
    {% endif %}
</body>
</html>
"""

# TEMPLATE 2: MODERN EXECUTIVE
MODERN_HTML = """
<!DOCTYPE html>
<html>
<head>
<style>
    @page { size: A4; margin: 1.2cm; }
    body { font-family: {{ font_family }}, sans-serif; font-size: 9.5pt; color: #2D3748; line-height: 1.4; }
    
    .top-bar { border-top: 4px solid {{ accent_color }}; padding-top: 10px; margin-bottom: 15px; }
    .name { font-size: 20pt; font-weight: bold; color: {{ accent_color }}; text-transform: uppercase; }
    .title { font-size: 11pt; font-weight: bold; color: #4A5568; margin-top: 2px; }
    .contact { font-size: 8.5pt; color: #718096; margin-top: 6px; }
    
    .section-title { 
        font-size: 10pt; 
        font-weight: bold; 
        color: {{ accent_color }}; 
        text-transform: uppercase; 
        border-bottom: 2px solid {{ accent_color }}; 
        margin-top: 12px; 
        margin-bottom: 6px; 
        letter-spacing: 0.5px;
    }
    
    .item-header { font-weight: bold; font-size: 9.5pt; color: #1A202C; }
    .item-sub { font-weight: 600; font-size: 9pt; color: #4A5568; }
    .right-text { float: right; color: #718096; font-weight: normal; }
    .desc { margin-top: 3px; margin-bottom: 8px; white-space: pre-line; color: #2D3748; }
    
    .badge { background-color: #EDF2F7; padding: 2px 6px; font-size: 8.5pt; border-radius: 3px; color: #2B6CB0; }
</style>
</head>
<body>
    <div class="top-bar">
        <div class="name">{{ nama }}</div>
        {% if posisi_target %}<div class="title">{{ posisi_target }}</div>{% endif %}
        <div class="contact">
            📍 {{ lokasi }} &nbsp;|&nbsp; ✉️ {{ email }} &nbsp;|&nbsp; 📞 {{ telepon }}
            <br>
            {% if linkedin %}🔗 {{ linkedin }}{% endif %}
            {% if github_portfolio %} &nbsp;|&nbsp; 💻 {{ github_portfolio }}{% endif %}
        </div>
    </div>

    {% if ringkasan %}
    <div class="section-title">PROFIL PROFESIONAL</div>
    <div class="desc">{{ ringkasan }}</div>
    {% endif %}

    {% if pengalaman and pengalaman[0].perusahaan %}
    <div class="section-title">PENGALAMAN KERJA</div>
    {% for exp in pengalaman %}
        {% if exp.perusahaan %}
        <div class="item-header">
            {{ exp.posisi }} <span class="right-text">📅 {{ exp.periode }}</span>
        </div>
        <div class="item-sub">🏢 {{ exp.perusahaan }}</div>
        <div class="desc">{{ exp.deskripsi }}</div>
        {% endif %}
    {% endfor %}
    {% endif %}

    {% if pendidikan and pendidikan[0].institusi %}
    <div class="section-title">PENDIDIKAN</div>
    {% for edu in pendidikan %}
        {% if edu.institusi %}
        <div class="item-header">
            {{ edu.institusi }} <span class="right-text">📅 {{ edu.tahun }}</span>
        </div>
        <div class="item-sub">🎓 {{ edu.jurusan }} {% if edu.nilai %}(IPK: {{ edu.nilai }}){% endif %}</div>
        <br>
        {% endif %}
    {% endfor %}
    {% endif %}

    {% if proyek and proyek[0].nama %}
    <div class="section-title">PROYEK & PORTOFOLIO</div>
    {% for proj in proyek %}
        {% if proj.nama %}
        <div class="item-header">
            {{ proj.nama }} {% if proj.peran %}<span class="badge">{{ proj.peran }}</span>{% endif %}
            {% if proj.link %}<span class="right-text">{{ proj.link }}</span>{% endif %}
        </div>
        {% if proj.tools %}<div class="item-sub" style="font-size:8.5pt; color:#718096;">Stack: {{ proj.tools }}</div>{% endif %}
        <div class="desc">{{ proj.deskripsi }}</div>
        {% endif %}
    {% endfor %}
    {% endif %}

    {% if sertifikasi and sertifikasi[0].nama %}
    <div class="section-title">SERTIFIKASI PROFESIONAL</div>
    {% for cert in sertifikasi %}
        {% if cert.nama %}
        <div class="item-header">
            🏆 {{ cert.nama }} - <span style="font-weight:normal; color:#4A5568;">{{ cert.penerbit }}</span>
            <span class="right-text">{{ cert.tahun }}</span>
        </div>
        {% endif %}
    {% endfor %}
    {% endif %}

    {% if hard_skills or soft_skills or bahasa %}
    <div class="section-title">KEAHLIAN & BAHASA</div>
    <p style="margin-top: 3px;">
        {% if hard_skills %}<b>Hard Skills:</b> {{ hard_skills }}<br>{% endif %}
        {% if soft_skills %}<b>Soft Skills:</b> {{ soft_skills }}<br>{% endif %}
        {% if bahasa %}<b>Bahasa:</b> {{ bahasa }}{% endif %}
    </p>
    {% endif %}
</body>
</html>
"""

# ==========================================
# 3. FUNGSI KONVERSI PDF
# ==========================================
def generate_pdf(html_content):
    pdf_buffer = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.StringIO(html_content), dest=pdf_buffer)
    if pisa_status.err:
        return None
    return pdf_buffer.getvalue()

# ==========================================
# 4. LAYOUT UTAMA APLIKASI
# ==========================================
st.title("📄 AI & Dynamic CV Builder")

# Sidebar untuk Pengaturan Desain & Download
with st.sidebar:
    st.header("🎨 Pengaturan Template")
    selected_template = st.selectbox("Pilih Gaya CV", ["ATS Clean (ATS-Friendly)", "Modern Executive"])
    
    font_choice = st.selectbox("Font Family", ["Helvetica", "Arial", "Times-Roman", "Courier"])
    
    accent_color = "#1E3A8A" # default blue
    if selected_template == "Modern Executive":
        accent_color = st.color_picker("Warna Aksen", "#1E3A8A")

# TAB SYSTEM
tab_input, tab_preview = st.tabs(["📝 1. Isi Data CV", "👁️ 2. Live Preview & Cetak PDF"])

# --- TAB 1: FORM INPUT DATA ---
with tab_input:
    st.info("Lengkapi data Anda di bawah ini. Perubahan akan langsung terupdate di Tab Preview.")
    
    # Section Profil
    st.subheader("👤 Profil Utama")
    c1, c2 = st.columns(2)
    nama = c1.text_input("Nama Lengkap", "Budi Santoso, S.Kom.")
    posisi_target = c2.text_input("Posisi Dilamar", "Software Engineer")
    email = c1.text_input("Email", "budi.santoso@email.com")
    telepon = c2.text_input("Telepon", "+62 812 3456 7890")
    lokasi = c1.text_input("Lokasi", "Jakarta, Indonesia")
    linkedin = c2.text_input("LinkedIn", "linkedin.com/in/budisantoso")
    github_portfolio = c1.text_input("Portofolio / GitHub", "github.com/budisantoso")
    
    ringkasan = st.text_area("Ringkasan Profil", "Software Engineer dengan pengalaman 3+ tahun dalam merancang dan mengembangkan aplikasi web skala besar. Ahli dalam Python, REST API, dan arsitektur microservices.")

    # Section Pengalaman
    st.markdown("---")
    st.subheader("💼 Pengalaman Kerja")
    for i, exp in enumerate(st.session_state.pengalaman):
        with st.expander(f"Pengalaman #{i+1}: {exp['perusahaan']}", expanded=False):
            exp["perusahaan"] = st.text_input("Perusahaan", exp["perusahaan"], key=f"c_{i}")
            exp["posisi"] = st.text_input("Posisi", exp["posisi"], key=f"p_{i}")
            exp["periode"] = st.text_input("Periode", exp["periode"], key=f"per_{i}")
            exp["deskripsi"] = st.text_area("Deskripsi (Gunakan - untuk bullet point)", exp["deskripsi"], key=f"d_{i}")

    if st.button("➕ Tambah Pengalaman"):
        st.session_state.pengalaman.append({"perusahaan": "", "posisi": "", "periode": "", "deskripsi": ""})
        st.rerun()

    # Section Pendidikan
    st.markdown("---")
    st.subheader("🎓 Pendidikan")
    for j, edu in enumerate(st.session_state.pendidikan):
        with st.expander(f"Pendidikan #{j+1}: {edu['institusi']}", expanded=False):
            edu["institusi"] = st.text_input("Institusi", edu["institusi"], key=f"inst_{j}")
            edu["jurusan"] = st.text_input("Jurusan", edu["jurusan"], key=f"jur_{j}")
            edu["tahun"] = st.text_input("Tahun", edu["tahun"], key=f"thn_{j}")
            edu["nilai"] = st.text_input("IPK / Nilai", edu["nilai"], key=f"nil_{j}")

    if st.button("➕ Tambah Pendidikan"):
        st.session_state.pendidikan.append({"institusi": "", "jurusan": "", "tahun": "", "nilai": ""})
        st.rerun()

    # Section Skills
    st.markdown("---")
    st.subheader("⚡ Keahlian")
    sk1, sk2 = st.columns(2)
    hard_skills = sk1.text_area("Hard Skills", "Python, SQL, FastApi, Docker, Git, PostgreSQL")
    soft_skills = sk2.text_area("Soft Skills", "Problem Solving, Team Leadership, Communication")
    bahasa = st.text_input("Bahasa", "Indonesia (Native), Inggris (Professional)")

# --- TAB 2: LIVE PREVIEW & RENDER ---
with tab_preview:
    # 1. Pilih Template String
    raw_template = ATS_HTML if "ATS" in selected_template else MODERN_HTML
    
    # 2. Render Template dengan Jinja2
    rendered_html = Template(raw_template).render(
        nama=nama,
        posisi_target=posisi_target,
        email=email,
        telepon=telepon,
        lokasi=lokasi,
        linkedin=linkedin,
        github_portfolio=github_portfolio,
        ringkasan=ringkasan,
        pengalaman=st.session_state.pengalaman,
        pendidikan=st.session_state.pendidikan,
        proyek=st.session_state.proyek,
        sertifikasi=st.session_state.sertifikasi,
        hard_skills=hard_skills,
        soft_skills=soft_skills,
        bahasa=bahasa,
        font_family=font_choice,
        accent_color=accent_color
    )

    col_preview, col_download = st.columns([3, 1])

    with col_preview:
        st.subheader("Visual Preview")
        # Render HTML langsung di iframe Streamlit
        st.components.v1.html(rendered_html, height=800, scrolling=True)

    with col_download:
        st.subheader("📥 Export File")
        st.write("Klik tombol di bawah untuk mengunduh CV dalam format PDF siap pakai.")
        
        # Generasi File PDF Buffer
        pdf_bytes = generate_pdf(rendered_html)
        
        if pdf_bytes:
            st.download_button(
                label="📄 Download PDF",
                data=pdf_bytes,
                file_name=f"CV_{nama.replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.error("Gagal mendesain PDF. Pastikan format penulisan HTML valid.")
