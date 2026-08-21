import streamlit as st
from jinja2 import Template
from xhtml2pdf import pisa
import io
import base64

st.set_page_config(page_title="AI & Dynamic CV Builder", layout="wide")

# ==========================================
# 1. HELPER: KONVERSI GAMBAR KE BASE64
# ==========================================
def get_base64_image(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        base64_str = base64.b64encode(bytes_data).decode('utf-8')
        mime_type = uploaded_file.type
        return f"data:{mime_type};base64,{base64_str}"
    return None

# ==========================================
# 2. INISIALISASI SESSION STATE
# ==========================================
if "pengalaman" not in st.session_state:
    st.session_state.pengalaman = [{"perusahaan": "PT Teknologi Nusantara", "posisi": "Software Engineer", "periode": "Jan 2022 - Sekarang", "deskripsi": "- Mengembangkan API menggunakan Python & FastAPI\n- Meningkatkan performa database sebesar 30%"}]

if "pendidikan" not in st.session_state:
    st.session_state.pendidikan = [{"institusi": "Universitas Indonesia", "jurusan": "Teknik Informatika", "tahun": "2018 - 2022", "nilai": "3.80 / 4.00"}]

# ==========================================
# 3. MAPPING FONT
# ==========================================
FONT_MAPPING = {
    "Arial (Clean Sans)": {"css": "Arial, Helvetica, sans-serif", "pdf": "Helvetica"},
    "Times New Roman (Serif)": {"css": "'Times New Roman', Times, serif", "pdf": "Times-Roman"},
    "Courier (Monospace)": {"css": "'Courier New', Courier, monospace", "pdf": "Courier"}
}

# ==========================================
# 4. TEMPLATES HTML & CSS (DENGAN SUPPORT FOTO)
# ==========================================

# --- TEMPLATE 1: CREATIVE TWO-COLUMN (SANGAT COCOK DENGAN FOTO) ---
CREATIVE_HTML = """
<!DOCTYPE html>
<html>
<head>
<style>
    @page { size: a4 portrait; margin: 0; }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    html { background-color: #2b2b2b; padding: 15px; }
    body { 
        background-color: #ffffff !important; color: #2d3748 !important; 
        font-family: {{ font_family }}; font-size: 8.5pt; line-height: 1.25;
        width: 210mm; min-height: 297mm; margin: 0 auto;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
    }
    .cv-table { width: 100%; border-collapse: collapse; }
    .left-col { 
        background-color: #2D3748 !important; color: #FFFFFF !important; 
        padding: 10mm 7mm; vertical-align: top; text-align: center;
    }
    .right-col { background-color: #FFFFFF !important; padding: 10mm 9mm; vertical-align: top; text-align: left; }
    
    .profile-img {
        width: 105px; height: 105px; border-radius: 50%;
        border: 2pt solid {{ accent_color }}; margin-bottom: 10pt;
        object-fit: cover;
    }

    .sidebar-title { font-size: 14pt; font-weight: bold; color: #FFFFFF; text-transform: uppercase; line-height: 1.1; text-align: center; }
    .sidebar-sub { font-size: 8.5pt; color: #CBD5E0; margin-bottom: 12pt; text-transform: uppercase; letter-spacing: 0.5pt; margin-top: 2pt; text-align: center; }
    .sidebar-sec { font-size: 9pt; font-weight: bold; color: {{ accent_color }}; text-transform: uppercase; border-bottom: 1pt solid #4A5568; margin-top: 12pt; margin-bottom: 5pt; padding-bottom: 1pt; text-align: left; }
    .sidebar-text { font-size: 8pt; color: #E2E8F0; margin-bottom: 3pt; word-break: break-all; text-align: left; }
    
    .main-sec { font-size: 10pt; font-weight: bold; color: #1A202C; text-transform: uppercase; border-bottom: 1.5pt solid {{ accent_color }}; margin-top: 10pt; margin-bottom: 6pt; padding-bottom: 1pt; }
    .item-header { font-weight: bold; font-size: 9pt; color: #1A202C; margin-top: 3pt; }
    .item-sub { font-size: 8pt; color: #4A5568; font-style: italic; margin-bottom: 2pt; }
    .right-text { float: right; color: #718096; font-weight: normal; font-size: 8pt; }
    .desc { margin-top: 2pt; margin-bottom: 6pt; white-space: pre-line; color: #2D3748; font-size: 8.5pt; }
</style>
</head>
<body>
    <table class="cv-table">
        <tr>
            <!-- LEFT SIDEBAR -->
            <td class="left-col" width="32%" valign="top">
                {% if foto_base64 %}
                <img src="{{ foto_base64 }}" class="profile-img" />
                {% endif %}
                <div class="sidebar-title">{{ nama }}</div>
                <div class="sidebar-sub">{{ posisi_target }}</div>
                
                <div class="sidebar-sec" style="color: #63B3ED;">KONTAK</div>
                <div class="sidebar-text">📍 {{ lokasi }}</div>
                <div class="sidebar-text">✉️ {{ email }}</div>
                <div class="sidebar-text">📞 {{ telepon }}</div>
                {% if linkedin %}<div class="sidebar-text">🔗 {{ linkedin }}</div>{% endif %}
                {% if github_portfolio %}<div class="sidebar-text">💻 {{ github_portfolio }}</div>{% endif %}

                {% if hard_skills %}
                <div class="sidebar-sec" style="color: #63B3ED;">HARD SKILLS</div>
                <div class="sidebar-text">{{ hard_skills }}</div>
                {% endif %}

                {% if soft_skills %}
                <div class="sidebar-sec" style="color: #63B3ED;">SOFT SKILLS</div>
                <div class="sidebar-text">{{ soft_skills }}</div>
                {% endif %}

                {% if bahasa %}
                <div class="sidebar-sec" style="color: #63B3ED;">BAHASA</div>
                <div class="sidebar-text">{{ bahasa }}</div>
                {% endif %}
            </td>

            <!-- RIGHT MAIN CONTENT -->
            <td class="right-col" width="68%" valign="top">
                {% if ringkasan %}
                <div class="main-sec">TENTANG SAYA</div>
                <div class="desc">{{ ringkasan }}</div>
                {% endif %}

                {% if pengalaman and pengalaman[0].perusahaan %}
                <div class="main-sec">PENGALAMAN KERJA</div>
                {% for exp in pengalaman %}{% if exp.perusahaan %}
                    <div class="item-header">{{ exp.posisi }} <span class="right-text">{{ exp.periode }}</span></div>
                    <div class="item-sub">{{ exp.perusahaan }}</div>
                    <div class="desc">{{ exp.deskripsi }}</div>
                {% endif %}{% endfor %}{% endif %}

                {% if pendidikan and pendidikan[0].institusi %}
                <div class="main-sec">PENDIDIKAN</div>
                {% for edu in pendidikan %}{% if edu.institusi %}
                    <div class="item-header">{{ edu.institusi }} <span class="right-text">{{ edu.tahun }}</span></div>
                    <div class="item-sub">{{ edu.jurusan }} {% if edu.nilai %}(IPK: {{ edu.nilai }}){% endif %}</div>
                {% endif %}{% endfor %}{% endif %}
            </td>
        </tr>
    </table>
</body>
</html>
"""

# --- TEMPLATE 2: MODERN EXECUTIVE (HEADER DENGAN FOTO) ---
MODERN_HTML = """
<!DOCTYPE html>
<html>
<head>
<style>
    @page { size: a4 portrait; margin: 12mm; }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    html { background-color: #2b2b2b; padding: 15px; }
    body { 
        background-color: #ffffff !important; color: #2d3748 !important; 
        font-family: {{ font_family }}; font-size: 9.5pt; line-height: 1.3;
        width: 210mm; min-height: 297mm; margin: 0 auto; padding: 12mm;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
    }
    .top-bar { border-top: 4pt solid {{ accent_color }}; padding-top: 8pt; margin-bottom: 10pt; }
    .header-table { width: 100%; border-collapse: collapse; }
    .profile-img-header {
        width: 85px; height: 85px; border-radius: 8px;
        border: 1.5pt solid {{ accent_color }}; object-fit: cover;
    }
    .name { font-size: 19pt; font-weight: bold; color: {{ accent_color }}; text-transform: uppercase; line-height: 1.1; }
    .title { font-size: 10.5pt; font-weight: bold; color: #4a5568; margin-top: 2pt; }
    .contact { font-size: 8.5pt; color: #718096; margin-top: 4pt; }
    .section-title { 
        font-size: 10pt; font-weight: bold; color: {{ accent_color }}; text-transform: uppercase; 
        border-bottom: 1.5pt solid {{ accent_color }}; margin-top: 10pt; margin-bottom: 6pt; padding-bottom: 2pt;
    }
    .item-header { font-weight: bold; font-size: 9.5pt; color: #1a202c; margin-top: 4pt; }
    .item-sub { font-weight: 600; font-size: 8.5pt; color: #4a5568; }
    .right-text { float: right; color: #718096; font-weight: normal; }
    .desc { margin-top: 2pt; margin-bottom: 5pt; white-space: pre-line; color: #2d3748; font-size: 8.5pt; }
</style>
</head>
<body>
    <div class="top-bar">
        <table class="header-table">
            <tr>
                {% if foto_base64 %}
                <td width="18%" valign="top">
                    <img src="{{ foto_base64 }}" class="profile-img-header" />
                </td>
                {% endif %}
                <td valign="top">
                    <div class="name">{{ nama }}</div>
                    {% if posisi_target %}<div class="title">{{ posisi_target }}</div>{% endif %}
                    <div class="contact">
                        📍 {{ lokasi }} &nbsp;|&nbsp; ✉️ {{ email }} &nbsp;|&nbsp; 📞 {{ telepon }}
                        <br>{% if linkedin %}🔗 {{ linkedin }}{% endif %} {% if github_portfolio %}&nbsp;|&nbsp; 💻 {{ github_portfolio }}{% endif %}
                    </div>
                </td>
            </tr>
        </table>
    </div>
    {% if ringkasan %}<div class="section-title">PROFIL PROFESIONAL</div><div class="desc">{{ ringkasan }}</div>{% endif %}
    {% if pengalaman and pengalaman[0].perusahaan %}
    <div class="section-title">PENGALAMAN KERJA</div>
    {% for exp in pengalaman %}{% if exp.perusahaan %}
        <div class="item-header">{{ exp.posisi }} <span class="right-text">📅 {{ exp.periode }}</span></div>
        <div class="item-sub">🏢 {{ exp.perusahaan }}</div>
        <div class="desc">{{ exp.deskripsi }}</div>
    {% endif %}{% endfor %}{% endif %}
    {% if pendidikan and pendidikan[0].institusi %}
    <div class="section-title">PENDIDIKAN</div>
    {% for edu in pendidikan %}{% if edu.institusi %}
        <div class="item-header">{{ edu.institusi }} <span class="right-text">📅 {{ edu.tahun }}</span></div>
        <div class="item-sub">🎓 {{ edu.jurusan }} {% if edu.nilai %}(IPK: {{ edu.nilai }}){% endif %}</div>
    {% endif %}{% endfor %}{% endif %}
</body>
</html>
"""

# ==========================================
# 5. FUNGSI GENERATE PDF
# ==========================================
def generate_pdf(html_content):
    pdf_buffer = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.StringIO(html_content), dest=pdf_buffer)
    if pisa_status.err:
        return None
    return pdf_buffer.getvalue()

# ==========================================
# 6. LAYOUT UTAMA & SIDEBAR
# ==========================================
st.title("📄 AI & Dynamic CV Builder")

with st.sidebar:
    st.header("🎨 Pengaturan Template")
    selected_template = st.selectbox(
        "Pilih Gaya CV", 
        ["Creative Two-Column", "Modern Executive"]
    )
    
    font_label = st.selectbox("Font Family", list(FONT_MAPPING.keys()))
    selected_css_font = FONT_MAPPING[font_label]["css"]
    selected_pdf_font = FONT_MAPPING[font_label]["pdf"]

    accent_color = st.color_picker("Warna Aksen", "#2563EB")

# TABS
tab_input, tab_preview = st.tabs(["📝 1. Isi Data CV", "👁️ 2. Live Preview & Cetak PDF"])

# --- TAB 1: FORM INPUT DATA ---
with tab_input:
    st.info("Lengkapi data Anda di bawah ini.")
    
    st.subheader("🖼️ Foto Profil (Opsional)")
    foto_file = st.file_uploader("Upload Foto Profil (PNG / JPG / JPEG)", type=["png", "jpg", "jpeg"])
    foto_base64 = get_base64_image(foto_file)

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

    st.markdown("---")
    st.subheader("⚡ Keahlian & Lainnya")
    sk1, sk2 = st.columns(2)
    hard_skills = sk1.text_area("Hard Skills", "Python, SQL, FastApi, Docker, Git, PostgreSQL")
    soft_skills = sk2.text_area("Soft Skills", "Problem Solving, Team Leadership, Communication")
    bahasa = st.text_input("Bahasa", "Indonesia (Native), Inggris (Professional)")

# --- TAB 2: LIVE PREVIEW & DOWNLOAD ---
with tab_preview:
    if "Creative" in selected_template:
        raw_template = CREATIVE_HTML
    else:
        raw_template = MODERN_HTML
    
    # Render HTML Preview (Web)
    rendered_html_preview = Template(raw_template).render(
        foto_base64=foto_base64,
        nama=nama, posisi_target=posisi_target, email=email, telepon=telepon, lokasi=lokasi,
        linkedin=linkedin, github_portfolio=github_portfolio, ringkasan=ringkasan,
        pengalaman=st.session_state.pengalaman, pendidikan=st.session_state.pendidikan,
        hard_skills=hard_skills, soft_skills=soft_skills, bahasa=bahasa,
        font_family=selected_css_font, accent_color=accent_color
    )

    # Render HTML Engine (PDF)
    rendered_html_pdf = Template(raw_template).render(
        foto_base64=foto_base64,
        nama=nama, posisi_target=posisi_target, email=email, telepon=telepon, lokasi=lokasi,
        linkedin=linkedin, github_portfolio=github_portfolio, ringkasan=ringkasan,
        pengalaman=st.session_state.pengalaman, pendidikan=st.session_state.pendidikan,
        hard_skills=hard_skills, soft_skills=soft_skills, bahasa=bahasa,
        font_family=selected_pdf_font, accent_color=accent_color
    )

    col_preview, col_download = st.columns([3, 1])

    with col_preview:
        st.subheader("Visual Preview (Presisi A4)")
        st.components.v1.html(rendered_html_preview, height=850, scrolling=True)

    with col_download:
        st.subheader("📥 Export File")
        pdf_bytes = generate_pdf(rendered_html_pdf)
        
        if pdf_bytes:
            st.download_button(
                label="📄 Download PDF",
                data=pdf_bytes,
                file_name=f"CV_{nama.replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.error("Gagal mendesain PDF.")
