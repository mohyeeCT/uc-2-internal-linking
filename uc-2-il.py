import streamlit as st
import pandas as pd
import numpy as np
import re
import io
import time

st.set_page_config(
    page_title="UC2 — Internal Linking",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}

/* ── Page background ── */
.stApp {
    background-color: #0d1117;
    color: #e6edf3;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #161b22;
    border-right: 1px solid #21262d;
}
[data-testid="stSidebar"] * {
    color: #c9d1d9 !important;
}
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stTextInput label,
[data-testid="stSidebar"] .stCheckbox label,
[data-testid="stSidebar"] .stNumberInput label {
    color: #8b949e !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div {
    background-color: #0d1117;
    border: 1px solid #30363d;
    color: #e6edf3;
}
[data-testid="stSidebar"] .stTextInput > div > div > input {
    background-color: #0d1117;
    border: 1px solid #30363d;
    color: #e6edf3;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem;
}

/* ── Main headings ── */
h1 { 
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-weight: 600 !important;
    color: #e6edf3 !important;
    letter-spacing: -0.02em !important;
}
h2, h3 {
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-weight: 500 !important;
    color: #c9d1d9 !important;
}

/* ── Upload areas ── */
[data-testid="stFileUploader"] {
    background-color: #161b22;
    border: 1px dashed #30363d;
    border-radius: 6px;
    padding: 12px;
}
[data-testid="stFileUploader"]:hover {
    border-color: #1f6feb;
}
[data-testid="stFileUploader"] label {
    color: #8b949e !important;
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}

/* ── Buttons ── */
.stButton > button {
    background-color: #1f6feb !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    padding: 0.5rem 1.25rem !important;
    transition: background-color 0.15s ease !important;
}
.stButton > button:hover {
    background-color: #388bfd !important;
}
.stDownloadButton > button {
    background-color: #238636 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-weight: 500 !important;
}
.stDownloadButton > button:hover {
    background-color: #2ea043 !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background-color: #161b22;
    border: 1px solid #21262d;
    border-radius: 8px;
    padding: 16px 20px;
}
[data-testid="stMetricLabel"] {
    color: #8b949e !important;
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}
[data-testid="stMetricValue"] {
    color: #e6edf3 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 1.6rem !important;
    font-weight: 600 !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid #21262d;
    border-radius: 6px;
}

/* ── Alerts / info boxes ── */
.stAlert {
    border-radius: 6px !important;
    border-left-width: 3px !important;
}
[data-testid="stInfo"] {
    background-color: #0d2234 !important;
    border-left-color: #1f6feb !important;
    color: #79c0ff !important;
}
[data-testid="stSuccess"] {
    background-color: #0a2217 !important;
    border-left-color: #238636 !important;
    color: #3fb950 !important;
}
[data-testid="stWarning"] {
    background-color: #231c00 !important;
    border-left-color: #e3b341 !important;
    color: #e3b341 !important;
}
[data-testid="stError"] {
    background-color: #280d11 !important;
    border-left-color: #da3633 !important;
    color: #f85149 !important;
}

/* ── Dividers ── */
hr { border-color: #21262d; }

/* ── Expanders ── */
.streamlit-expanderHeader {
    background-color: #161b22 !important;
    border: 1px solid #21262d !important;
    border-radius: 6px !important;
    color: #c9d1d9 !important;
    font-size: 0.85rem !important;
}
.streamlit-expanderContent {
    background-color: #0d1117 !important;
    border: 1px solid #21262d !important;
    border-top: none !important;
}

/* ── Code blocks ── */
code {
    font-family: 'IBM Plex Mono', monospace !important;
    background-color: #161b22 !important;
    color: #79c0ff !important;
    padding: 2px 6px !important;
    border-radius: 3px !important;
    font-size: 0.82em !important;
}

/* ── Tag pills ── */
.tag {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    font-family: 'IBM Plex Mono', monospace;
    letter-spacing: 0.03em;
    margin: 1px;
}
.tag-blog { background: #0d2234; color: #79c0ff; border: 1px solid #1f6feb; }
.tag-product { background: #0a2217; color: #3fb950; border: 1px solid #238636; }
.tag-service { background: #231c00; color: #e3b341; border: 1px solid #9e6a03; }
.tag-other { background: #1c1c1c; color: #8b949e; border: 1px solid #30363d; }

/* ── Section title bar ── */
.section-bar {
    background: linear-gradient(90deg, #1f6feb22, transparent);
    border-left: 3px solid #1f6feb;
    padding: 8px 16px;
    border-radius: 0 6px 6px 0;
    margin: 20px 0 12px 0;
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #79c0ff;
}

/* ── Progress ── */
.stProgress > div > div {
    background-color: #1f6feb !important;
}

/* ── Slider ── */
.stSlider > div > div > div {
    color: #1f6feb !important;
}
</style>
""", unsafe_allow_html=True)


# ─── HELPERS ────────────────────────────────────────────────────────

def norm_url(url):
    if not isinstance(url, str): return ''
    return re.sub(r'[?#].*$', '', url.strip().lower().rstrip('/'))

def load_file(f):
    if f is None: return None
    try:
        name = f.name.lower()
        if name.endswith(('.xlsx', '.xls')):
            return pd.read_excel(f)
        return pd.read_csv(f)
    except Exception as e:
        st.error(f"Could not read file: {e}")
        return None

def detect_emb_col(df):
    for col in df.columns:
        if col.lower() in ['embedding', 'embeddings']:
            return col
    for col in df.columns:
        if col == 'Address': continue
        sample = df[col].dropna()
        if len(sample) > 0 and isinstance(sample.iloc[0], str) and sample.iloc[0].count(',') > 50:
            return col
    return None

def parse_vec(s):
    try:
        arr = np.array([float(x) for x in str(s).strip().strip('[]').split(',')], dtype=np.float32)
        return arr if arr.ndim == 1 and len(arr) > 0 else None
    except:
        return None

def filter_uniform_vecs(df, vec_col='_vec'):
    """Drop rows whose vector length differs from the most common length."""
    lengths = df[vec_col].apply(lambda v: len(v) if v is not None else 0)
    if lengths.nunique() <= 1:
        return df
    modal_len = lengths.mode()[0]
    bad = (lengths != modal_len).sum()
    if bad > 0:
        st.warning(f"Dropped {bad} rows with inconsistent vector dimensions (expected {modal_len})")
    return df[lengths == modal_len].reset_index(drop=True)

def section(title):
    st.markdown(f'<div class="section-bar">{title}</div>', unsafe_allow_html=True)


# ─── SIDEBAR ────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.markdown("---")

    provider = st.selectbox("Embedding Provider", ["Gemini", "OpenAI"],
        help="Must match the provider used in your Screaming Frog crawl")

    st.markdown("**Similarity Range**")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        min_sim = st.number_input("Min", value=0.70, min_value=0.50, max_value=0.90, step=0.05, format="%.2f")
    with col_s2:
        max_sim = st.number_input("Max", value=0.95, min_value=0.85, max_value=0.99, step=0.01, format="%.2f")

    top_k = st.slider("Max suggestions per page", 1, 10, 5)
    skip_linked = st.checkbox("Skip already-linked pairs", value=True)

    st.markdown("---")
    st.markdown("**Intent URL Patterns**")
    st.caption("Format: `/fragment/:label` — comma separated")
    intent_raw = st.text_area("Patterns", value="/blog/:blog, /product/:product, /service/:service, /solution/:solution, /case-stud/:case_study, /about/:about, /location/:location", height=120)

    st.markdown("---")
    st.markdown("**Viability Weights**")
    st.caption("Set 0 to exclude a direction entirely")
    w_blog_product = st.slider("Blog → Product", 0.0, 1.0, 1.00, 0.05)
    w_blog_service = st.slider("Blog → Service/Solution", 0.0, 1.0, 0.80, 0.05)
    w_case_product = st.slider("Case Study → Product", 0.0, 1.0, 0.90, 0.05)
    w_service_product = st.slider("Service → Product", 0.0, 1.0, 0.85, 0.05)
    w_default = st.slider("Default (other pairs)", 0.0, 1.0, 0.40, 0.05)
    w_about = st.slider("About → Anything", 0.0, 1.0, 0.00, 0.05)


# ─── MAIN ───────────────────────────────────────────────────────────

st.markdown("# 🔗 Internal Linking Opportunities")
st.markdown("Finds semantically relevant link opportunities across your site, scored by topical similarity and business priority.")
st.markdown("---")

# ── FILE UPLOADS ────────────────────────────────────────────────────
section("01 — Upload Files")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Embeddings Export** `required`")
    st.caption("Screaming Frog → Bulk Export → Content → Embeddings Export")
    emb_file = st.file_uploader("Drop SF embeddings file", type=["csv", "xlsx", "xls"], key="emb", label_visibility="collapsed")

    st.markdown("**Internal Links Export** `optional`")
    st.caption("Screaming Frog → Bulk Export → Links → All Internal Links")
    links_file = st.file_uploader("Drop internal links file", type=["csv", "xlsx", "xls"], key="links", label_visibility="collapsed")

with col2:
    st.markdown("**GA4 Sessions Export** `optional`")
    st.caption("Adds traffic demand to opportunity scoring")
    ga_file = st.file_uploader("Drop GA4 export", type=["csv", "xlsx", "xls"], key="ga", label_visibility="collapsed")

    st.markdown("**Ahrefs / Semrush Export** `optional`")
    st.caption("Referring domains — adds authority signal to scoring")
    ahrefs_file = st.file_uploader("Drop Ahrefs/Semrush export", type=["csv", "xlsx", "xls"], key="ahrefs", label_visibility="collapsed")


# ── FILE STATUS ──────────────────────────────────────────────────────
emb_df = load_file(emb_file)
links_df = load_file(links_file)
ga_df = load_file(ga_file)
ahrefs_df = load_file(ahrefs_file)

status_cols = st.columns(4)
files_status = [
    ("Embeddings", emb_df, True),
    ("Internal Links", links_df, False),
    ("GA4 Data", ga_df, False),
    ("Ahrefs Data", ahrefs_df, False),
]
for i, (label, df, required) in enumerate(files_status):
    with status_cols[i]:
        if df is not None:
            st.success(f"✓ {label} — {len(df):,} rows")
        elif required:
            st.error(f"✗ {label} — required")
        else:
            st.info(f"○ {label} — optional")


# ── VALIDATE EMBEDDINGS ──────────────────────────────────────────────
emb_col = None
if emb_df is not None:
    if 'Address' not in emb_df.columns:
        st.error("No 'Address' column in embeddings file. Check your export.")
    else:
        emb_col = detect_emb_col(emb_df)
        if emb_col is None:
            st.error("Could not detect the embedding vector column. Ensure you exported the AI tab from Screaming Frog.")
        else:
            emb_df['_url_norm'] = emb_df['Address'].apply(norm_url)


# ── RUN ──────────────────────────────────────────────────────────────
section("02 — Run Analysis")
run_btn = st.button("▶  Run Analysis", disabled=(emb_df is None or emb_col is None))

if run_btn:
    # Parse intent patterns
    intent_map = {}
    for chunk in intent_raw.split(','):
        chunk = chunk.strip()
        if ':' in chunk:
            parts = chunk.split(':')
            intent_map[parts[0].strip()] = parts[1].strip()

    def classify_intent(url):
        u = (url or '').lower()
        for pattern, label in intent_map.items():
            if pattern.lower() in u:
                return label
        return 'other'

    viability_rules = {
        ('blog', 'product'): w_blog_product,
        ('blog', 'service'): w_blog_service,
        ('blog', 'solution'): w_blog_service,
        ('case_study', 'product'): w_case_product,
        ('case_study', 'service'): w_case_product * 0.85,
        ('service', 'product'): w_service_product,
        ('solution', 'product'): w_service_product,
        ('location', 'service'): 0.75,
        ('location', 'product'): 0.75,
        ('product', 'blog'): 0.55,
        ('about', 'product'): w_about,
        ('about', 'service'): w_about,
        ('about', 'blog'): w_about,
    }

    with st.spinner("Parsing embedding vectors..."):
        emb_df['_vec'] = emb_df[emb_col].apply(parse_vec)
        bad = emb_df['_vec'].isna().sum()
        emb_df = emb_df[emb_df['_vec'].notna()].reset_index(drop=True)
        emb_df = filter_uniform_vecs(emb_df)
        emb_df['_intent'] = emb_df['Address'].apply(classify_intent)
        if bad > 0:
            st.warning(f"Dropped {bad} rows with unparseable embeddings")

    with st.spinner(f"Computing cosine similarity for {len(emb_df):,} pages..."):
        vecs = np.stack(emb_df['_vec'].values)
        norms_ = np.linalg.norm(vecs, axis=1, keepdims=True)
        norms_[norms_ == 0] = 1.0
        unit = vecs / norms_
        sim_matrix = unit @ unit.T

    # Internal links
    linked_pairs = set()
    if links_df is not None:
        src_col = next((c for c in links_df.columns if 'source' in c.lower()), None)
        dst_col = next((c for c in links_df.columns if 'destination' in c.lower() or 'target' in c.lower()), None)
        if src_col and dst_col:
            linked_pairs = set(zip(links_df[src_col].apply(norm_url), links_df[dst_col].apply(norm_url)))

    # Need scores
    need_scores = {}
    if ga_df is not None or ahrefs_df is not None:
        inlink_counts = {}
        if links_df is not None and dst_col:
            for _, row in links_df.iterrows():
                d = norm_url(row.get(dst_col, ''))
                inlink_counts[d] = inlink_counts.get(d, 0) + 1
        max_il = max(inlink_counts.values()) if inlink_counts else 1

        ref_domains = {}
        max_rd = 1
        if ahrefs_df is not None:
            url_c = next((c for c in ahrefs_df.columns if 'url' in c.lower() or 'page' in c.lower()), ahrefs_df.columns[0])
            ref_c = next((c for c in ahrefs_df.columns if 'refer' in c.lower() or 'domain' in c.lower() or 'rd' == c.lower()), None)
            if ref_c:
                for _, row in ahrefs_df.iterrows():
                    ref_domains[norm_url(str(row[url_c]))] = float(row[ref_c]) if pd.notna(row[ref_c]) else 0
                max_rd = max(ref_domains.values()) if ref_domains else 1

        ga_demand = {}
        if ga_df is not None:
            ga_url_c = next((c for c in ga_df.columns if 'page' in c.lower() or 'url' in c.lower() or 'path' in c.lower()), ga_df.columns[0])
            eng_c = next((c for c in ga_df.columns if 'engaged' in c.lower()), None)
            rate_c = next((c for c in ga_df.columns if 'rate' in c.lower()), None)
            max_eng = pd.to_numeric(ga_df[eng_c], errors='coerce').max() if eng_c else 1
            for _, row in ga_df.iterrows():
                u = norm_url(str(row[ga_url_c]))
                eng = float(row[eng_c]) / max_eng if eng_c and max_eng > 0 and pd.notna(row[eng_c]) else 0
                rate = float(row[rate_c]) if rate_c and pd.notna(row[rate_c]) else 0.5
                ga_demand[u] = eng * rate

        for url_norm in emb_df['_url_norm']:
            il = inlink_counts.get(url_norm, 0)
            int_need = 1 - (il / max_il)
            rd = ref_domains.get(url_norm, 0)
            ext_need = 1 - min(rd / max_rd, 1)
            demand = ga_demand.get(url_norm, 0)
            need_scores[url_norm] = 0.50 * int_need + 0.20 * ext_need + 0.30 * demand

    urls = emb_df['Address'].tolist()
    urls_norm = emb_df['_url_norm'].tolist()
    intents = emb_df['_intent'].tolist()
    n = len(urls)
    use_need = len(need_scores) > 0

    with st.spinner("Generating link suggestions..."):
        rows = []
        prog = st.progress(0)
        for i in range(n):
            prog.progress((i + 1) / n)
            kept = 0
            idx_sorted = np.argsort(-sim_matrix[i])
            for j in idx_sorted:
                if j == i: continue
                score = float(sim_matrix[i, j])
                if score > max_sim: continue
                if score < min_sim: break
                src_int = intents[i]
                tgt_int = intents[j]
                weight = viability_rules.get((src_int, tgt_int), w_default)
                if weight <= 0: continue
                already = (urls_norm[i], urls_norm[j]) in linked_pairs
                if skip_linked and already: continue
                need = need_scores.get(urls_norm[j], 0.5) if use_need else 0.5
                viab = weight * score
                opp = viab * need if use_need else viab
                rows.append({
                    'Source URL': urls[i],
                    'Source Intent': src_int,
                    'Target URL': urls[j],
                    'Target Intent': tgt_int,
                    'Cosine Similarity': round(score, 4),
                    'Viability Weight': round(weight, 2),
                    'Viability Score': round(viab, 4),
                    'Target Need Score': round(need, 4) if use_need else 'N/A',
                    'Opportunity Score': round(opp, 4),
                    'Already Linked': already,
                })
                kept += 1
                if kept >= top_k: break
        prog.empty()

    if not rows:
        st.warning("No results found. Try lowering the minimum similarity or checking your intent patterns.")
    else:
        out_df = (pd.DataFrame(rows)
                  .sort_values(['Source URL', 'Opportunity Score'], ascending=[True, False])
                  .reset_index(drop=True))
        st.session_state['uc2_results'] = out_df


# ── RESULTS ──────────────────────────────────────────────────────────
if 'uc2_results' in st.session_state:
    out_df = st.session_state['uc2_results']
    section("03 — Results")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Link Opportunities", f"{len(out_df):,}")
    m2.metric("Source Pages", f"{out_df['Source URL'].nunique():,}")
    m3.metric("Top Opportunity Score", f"{out_df['Opportunity Score'].max():.3f}")
    m4.metric("Avg Similarity", f"{out_df['Cosine Similarity'].mean():.3f}")

    st.markdown("")

    # Intent distribution
    with st.expander("📊 Intent Breakdown", expanded=False):
        ic = out_df.groupby(['Source Intent', 'Target Intent']).size().reset_index(name='Count')
        ic = ic.sort_values('Count', ascending=False).head(15)
        st.dataframe(ic, use_container_width=True, hide_index=True)

    # Top results
    display_cols = ['Source URL', 'Source Intent', 'Target URL', 'Target Intent',
                    'Cosine Similarity', 'Opportunity Score', 'Already Linked']
    st.dataframe(
        out_df[display_cols].head(200),
        use_container_width=True,
        hide_index=True,
        column_config={
            'Cosine Similarity': st.column_config.ProgressColumn(min_value=0, max_value=1, format="%.3f"),
            'Opportunity Score': st.column_config.ProgressColumn(min_value=0, max_value=1, format="%.3f"),
        }
    )

    section("04 — Export")
    csv = out_df.to_csv(index=False).encode()
    st.download_button(
        "⬇  Download internal_link_opportunities.csv",
        data=csv,
        file_name="internal_link_opportunities.csv",
        mime="text/csv",
    )
    st.caption("Sort by **Opportunity Score** descending to start with the highest-impact links. Filter **Already Linked = False** to focus on gaps.")
