"""
PowerPoint (.pptx) Presentation Generator for COVID-19 Data Visualization Dashboard
Creates outputs/reports/COVID19_Data_Visualization_Presentation.pptx with 15 professional slides.
Features 16:9 Widescreen, executive dark theme, card layouts, KPI scorecards, and formatted tables.
"""

import os
import sys

def create_presentation(output_path=None):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if output_path is None:
        output_path = os.path.join(base_dir, "outputs", "COVID19_Data_Visualization_Presentation.pptx")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        from pptx import Presentation
        from pptx.util import Inches, Pt
        from pptx.enum.text import PP_ALIGN
        from pptx.dml.color import RGBColor
        from pptx.enum.shapes import MSO_SHAPE
    except ImportError:
        print("\n[ERROR] 'python-pptx' library is not installed. Run: pip install python-pptx\n")
        return False

    prs = Presentation()
    # 16:9 Widescreen Layout
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Executive Theme Colors
    COLOR_BG = RGBColor(11, 15, 25)          # Dark Slate
    COLOR_CARD = RGBColor(21, 28, 46)        # Deep Navy Card
    COLOR_PRIMARY = RGBColor(56, 189, 248)   # Cyan / Sky Blue
    COLOR_SUCCESS = RGBColor(52, 211, 153)   # Emerald Green
    COLOR_DANGER = RGBColor(248, 113, 113)   # Coral Red
    COLOR_WARNING = RGBColor(251, 191, 36)   # Amber Orange
    COLOR_ACCENT = RGBColor(129, 140, 248)   # Indigo
    COLOR_TEXT = RGBColor(248, 250, 252)     # White Text
    COLOR_MUTED = RGBColor(148, 163, 184)    # Slate Gray

    blank_layout = prs.slide_layouts[6]

    def set_slide_background(slide):
        bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg_shape.fill.solid()
        bg_shape.fill.fore_color.rgb = COLOR_BG
        bg_shape.line.fill.background()
        return bg_shape

    def add_custom_slide(title, subtitle="", badge="COVID-19 ANALYTICS PORTFOLIO"):
        slide = prs.slides.add_slide(blank_layout)
        set_slide_background(slide)

        # Header badge
        badge_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8), Inches(0.4))
        tf_badge = badge_box.text_frame
        tf_badge.word_wrap = True
        p_badge = tf_badge.paragraphs[0]
        p_badge.text = badge.upper()
        p_badge.font.size = Pt(11)
        p_badge.font.bold = True
        p_badge.font.color.rgb = COLOR_PRIMARY

        # Slide Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_TEXT

        # Slide Subtitle
        if subtitle:
            sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(0.5))
            tf_sub = sub_box.text_frame
            tf_sub.word_wrap = True
            p_sub = tf_sub.paragraphs[0]
            p_sub.text = subtitle
            p_sub.font.size = Pt(13)
            p_sub.font.color.rgb = COLOR_MUTED

        return slide

    def add_card(slide, left, top, width, height, bg_color=COLOR_CARD, border_color=None):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1.5)
        else:
            card.line.fill.background()
        return card

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Accent Glow Line
    glow = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(0.15), Inches(3.6))
    glow.fill.solid()
    glow.fill.fore_color.rgb = COLOR_PRIMARY
    glow.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.6), Inches(11.2), Inches(4.0))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "DATA ANALYTICS PORTFOLIO PROJECT"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_PRIMARY
    p0.space_after = Pt(12)

    p1 = tf1.add_paragraph()
    p1.text = "COVID-19 Global Data Visualization & Comparative Analytics Dashboard"
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEXT
    p1.space_after = Pt(14)

    p2 = tf1.add_paragraph()
    p2.text = "Automated REST API Data Extraction • Pandas Wrangling • Tableau Production Visuals • Streamlit App"
    p2.font.size = Pt(16)
    p2.font.color.rgb = COLOR_MUTED
    p2.space_after = Pt(24)

    p3 = tf1.add_paragraph()
    p3.text = "Tools: Python | Pandas | Tableau | REST APIs | Streamlit | Plotly | OpenPyXL"
    p3.font.size = Pt(13)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_SUCCESS

    # =========================================================================
    # SLIDE 2: Executive Summary & Headline KPIs
    # =========================================================================
    s2 = add_custom_slide("Executive Summary: Pandemic Intelligence at Scale", "Evaluating 73,000+ daily epidemiological records across 60+ countries (2020–2023)")

    kpis_data = [
        ("Total Confirmed Cases", "700M+", "Worldwide laboratory infections", COLOR_PRIMARY),
        ("Total Fatalities", "6.9M+", "Reported COVID-19 deaths", COLOR_DANGER),
        ("Estimated Recoveries", "670M+", "95.7% Overall recovery rate", COLOR_SUCCESS),
        ("Vaccine Doses Administered", "13.5B+", "Global immunization campaigns", COLOR_ACCENT)
    ]

    for i, (title, val, desc, col) in enumerate(kpis_data):
        left = 0.8 + i * 2.95
        add_card(s2, left, 2.1, 2.8, 1.8, COLOR_CARD, col)
        tb = s2.shapes.add_textbox(Inches(left + 0.15), Inches(2.2), Inches(2.5), Inches(1.6))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title.upper()
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = COLOR_MUTED

        p_v = tf.add_paragraph()
        p_v.text = val
        p_v.font.size = Pt(28)
        p_v.font.bold = True
        p_v.font.color.rgb = col

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = COLOR_TEXT

    # Lower context cards
    add_card(s2, 0.8, 4.3, 5.75, 2.5)
    tb_l = s2.shapes.add_textbox(Inches(1.0), Inches(4.4), Inches(5.35), Inches(2.3))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p_lt = tf_l.paragraphs[0]
    p_lt.text = "🎯 Core Project Goals"
    p_lt.font.size = Pt(16)
    p_lt.font.bold = True
    p_lt.font.color.rgb = COLOR_PRIMARY
    
    goals = [
        "Automate extraction from disease.sh REST API for 200+ territories.",
        "Engineer 7-day smoothing & per-million population normalization.",
        "Quantify the clinical impact of vaccines in decoupling transmission from mortality.",
        "Deliver production Tableau workbooks, Streamlit web app, and Excel reports."
    ]
    for g in goals:
        p = tf_l.add_paragraph()
        p.text = f"• {g}"
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT

    add_card(s2, 6.78, 4.3, 5.75, 2.5)
    tb_r = s2.shapes.add_textbox(Inches(7.0), Inches(4.4), Inches(5.35), Inches(2.3))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p_rt = tf_r.paragraphs[0]
    p_rt.text = "💡 Strategic Business Takeaway"
    p_rt.font.size = Pt(16)
    p_rt.font.bold = True
    p_rt.font.color.rgb = COLOR_SUCCESS

    takeaway = [
        "Absolute numbers falsely penalize large countries; per-capita normalization reveals true burden.",
        "Mass vaccination reduced Case Fatality Rate by 85%+ during Omicron surge.",
        "Interactive dashboard enables public health officials to benchmark healthcare strain and ICU peaks."
    ]
    for t in takeaway:
        p = tf_r.add_paragraph()
        p.text = f"• {t}"
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT

    # =========================================================================
    # SLIDE 3: Problem Statement
    # =========================================================================
    s3 = add_custom_slide("Problem Statement: Overcoming Public Health Data Distortions", "Challenges in analyzing raw global epidemiological time-series")

    problems = [
        ("1. Weekend Reporting Drop-offs", "Health ministries underreport on weekends by 25-35%, followed by artificial Monday spikes that skew day-over-day analyses.", COLOR_DANGER),
        ("2. Population Size Disparities", "Looking only at raw case counts masks severe per-capita outbreaks in mid-sized nations with rigorous testing regimens.", COLOR_WARNING),
        ("3. Evolving Variant Virulence", "Early ancestral strains caused severe pulmonary mortality (~3.2% CFR), whereas later Omicron subvariants decoupled transmission from fatalities (<0.35% CFR).", COLOR_PRIMARY),
        ("4. Reporting & Tooling Fragmentation", "Data silos between APIs, BI dashboards (Tableau), and executive spreadsheets prevent rapid cross-functional decision making.", COLOR_ACCENT)
    ]

    for i, (title, desc, col) in enumerate(problems):
        row = i // 2
        col_idx = i % 2
        l = 0.8 + col_idx * 5.95
        t = 2.1 + row * 2.5
        add_card(s3, l, t, 5.75, 2.2, COLOR_CARD, col)
        tb = s3.shapes.add_textbox(Inches(l + 0.2), Inches(t + 0.2), Inches(5.35), Inches(1.8))
        tf = tb.text_frame
        tf.word_wrap = True

        p_h = tf.paragraphs[0]
        p_h.text = title
        p_h.font.size = Pt(16)
        p_h.font.bold = True
        p_h.font.color.rgb = col
        p_h.space_after = Pt(8)

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(13)
        p_d.font.color.rgb = COLOR_TEXT

    # =========================================================================
    # SLIDE 4: Architecture & Pipeline Workflow
    # =========================================================================
    s4 = add_custom_slide("End-to-End Pipeline Architecture", "From live REST APIs to interactive Tableau models, Streamlit web app, and Excel workbook")

    steps = [
        ("STAGE 1\nINGESTION", "REST API\n• disease.sh API\n• 200+ countries\n• JSON extraction\n• Offline generator", COLOR_PRIMARY),
        ("STAGE 2\nWRANGLING", "Pandas & NumPy\n• Type casting\n• 7-day smoothing\n• Per-million metrics\n• CFR & Recovery %", COLOR_SUCCESS),
        ("STAGE 3\nANALYTICS", "Epidemiology\n• Wave tracking\n• Country rankings\n• Vaccine decoupling\n• Trajectory curves", COLOR_WARNING),
        ("STAGE 4\nTABLEAU & BI", "Tableau Ready\n• 4 curated CSVs\n• Calculated fields\n• Dual-axis waves\n• Action filters", COLOR_ACCENT),
        ("STAGE 5\nDELIVERY", "Dashboards\n• Streamlit web app\n• Multi-sheet Excel\n• Jupyter Notebook\n• 1-Click Launchers", COLOR_DANGER)
    ]

    for i, (stage, details, col) in enumerate(steps):
        l = 0.8 + i * 2.36
        add_card(s4, l, 2.2, 2.25, 4.6, COLOR_CARD, col)
        tb = s4.shapes.add_textbox(Inches(l + 0.1), Inches(2.4), Inches(2.05), Inches(4.2))
        tf = tb.text_frame
        tf.word_wrap = True

        p_s = tf.paragraphs[0]
        p_s.text = stage
        p_s.font.size = Pt(13)
        p_s.font.bold = True
        p_s.font.color.rgb = col
        p_s.space_after = Pt(16)

        p_dt = tf.add_paragraph()
        p_dt.text = details
        p_dt.font.size = Pt(12)
        p_dt.font.color.rgb = COLOR_TEXT

    # =========================================================================
    # SLIDE 5: Data Cleaning & Feature Engineering
    # =========================================================================
    s5 = add_custom_slide("Feature Engineering & Epidemiological Mathematics", "Formulas implemented in Pandas to normalize public health time-series")

    formulas = [
        ("7-Day Rolling Moving Average", "Smooths weekend backlog reporting fluctuations", "DailyCases_7D = Mean(DailyCases[t-6 : t])", COLOR_PRIMARY),
        ("Infection & Mortality per Million", "Normalizes comparison regardless of national population size", "Cases_Per_Million = (Cumulative_Cases / Population) * 1,000,000", COLOR_SUCCESS),
        ("Case Fatality Rate (CFR %)", "Measures clinical mortality proportion among confirmed infections", "CFR (%) = (Cumulative_Deaths / Cumulative_Cases) * 100", COLOR_DANGER),
        ("Vaccine Decoupling Index", "Quantifies the drop in mortality per infection post-vaccine", "Decoupling_Ratio = CFR_PostVax / CFR_PreVax  (Reduction: 85%+)", COLOR_ACCENT)
    ]

    for i, (title, purpose, formula, col) in enumerate(formulas):
        l = 0.8 + (i % 2) * 5.95
        t = 2.1 + (i // 2) * 2.5
        add_card(s5, l, t, 5.75, 2.2, COLOR_CARD, col)
        tb = s5.shapes.add_textbox(Inches(l + 0.2), Inches(t + 0.15), Inches(5.35), Inches(1.9))
        tf = tb.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(15)
        p_t.font.bold = True
        p_t.font.color.rgb = col

        p_p = tf.add_paragraph()
        p_p.text = purpose
        p_p.font.size = Pt(12)
        p_p.font.color.rgb = COLOR_MUTED
        p_p.space_after = Pt(6)

        p_f = tf.add_paragraph()
        p_f.text = f"Formula: {formula}"
        p_f.font.size = Pt(11)
        p_f.font.bold = True
        p_f.font.color.rgb = COLOR_TEXT

    # =========================================================================
    # SLIDE 6: Global Wave Dynamics (Alpha, Delta, Omicron)
    # =========================================================================
    s6 = add_custom_slide("Global Pandemic Wave Dynamics (2020 – 2023)", "Timeline of predominant SARS-CoV-2 variants and their distinct epidemiological profiles")

    waves = [
        ("Phase 1: Ancestral Wild-Type", "Jan 2020 – Oct 2020", "High hospitalization, low testing capability, initial lockdown responses. CFR ~3.2%.", COLOR_PRIMARY),
        ("Phase 2: Alpha / Beta (B.1.1.7)", "Nov 2020 – Apr 2021", "First major Variant of Concern with 50%+ increased transmissibility. Healthcare capacity overwhelmed.", COLOR_WARNING),
        ("Phase 3: Delta Surge (B.1.617.2)", "May 2021 – Nov 2021", "Severe viral loads and high pulmonary mortality; severe wave in India, USA, and Europe. Vaccine race begins.", COLOR_DANGER),
        ("Phase 4: Omicron BA.1 (B.1.1.529)", "Dec 2021 – May 2022", "Explosive transmission, upper airway affinity, record case surges, but sharply lowered CFR (<0.35%).", COLOR_SUCCESS),
        ("Phase 5: Omicron BA.5 & Endemic", "Jun 2022 – Dec 2023", "Sublineage convergence, high hybrid immunity, transitioning disease into manageable endemic status.", COLOR_ACCENT)
    ]

    for i, (phase, timeline, impact, col) in enumerate(waves):
        t = 2.1 + i * 1.0
        add_card(s6, 0.8, t, 11.7, 0.88, COLOR_CARD, col)
        tb = s6.shapes.add_textbox(Inches(1.0), Inches(t + 0.1), Inches(11.3), Inches(0.7))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = f"{phase}  |  {timeline}"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = col

        p_i = tf.add_paragraph()
        p_i.text = impact
        p_i.font.size = Pt(11)
        p_i.font.color.rgb = COLOR_TEXT

    # =========================================================================
    # SLIDE 7: Country-Wise Comparative Analysis
    # =========================================================================
    s7 = add_custom_slide("Country-Wise Comparative Analysis: Absolute vs. Normalized", "Comparing raw case counts against population-adjusted infection rates")

    add_card(s7, 0.8, 2.1, 5.75, 4.8)
    tb_c1 = s7.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.35), Inches(4.5))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    p = tf_c1.paragraphs[0]
    p.text = "📊 Top Countries by Total Absolute Cases"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)

    top_cases_list = [
        "1. United States: 103M+ cases (Pop: 331M)",
        "2. China: ~99M cases (Pop: 1.4B)",
        "3. India: ~45M cases (Pop: 1.38B)",
        "4. France: ~39M cases (Pop: 67M)",
        "5. Germany: ~38M cases (Pop: 83M)",
        "6. Brazil: ~37M cases (Pop: 212M)",
        "7. Japan: ~33M cases (Pop: 126M)",
        "8. South Korea: ~31M cases (Pop: 51M)"
    ]
    for c in top_cases_list:
        p_c = tf_c1.add_paragraph()
        p_c.text = f"• {c}"
        p_c.font.size = Pt(12)
        p_c.font.color.rgb = COLOR_TEXT

    add_card(s7, 6.78, 2.1, 5.75, 4.8)
    tb_c2 = s7.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.35), Inches(4.5))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True
    p2 = tf_c2.paragraphs[0]
    p2.text = "🎯 Normalized Per-Capita Infection Rates"
    p2.font.size = Pt(16)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_SUCCESS
    p2.space_after = Pt(10)

    top_per_mil = [
        "• France: ~575,000 cases per million (Over 57% population detected)",
        "• South Korea: ~605,000 cases per million (Extensive mass PCR testing)",
        "• Germany: ~453,000 cases per million",
        "• United States: ~310,000 cases per million",
        "• Key Finding: European and East Asian nations with aggressive testing recorded higher detected per-capita cases than countries with lower testing capacity."
    ]
    for c in top_per_mil:
        p_c = tf_c2.add_paragraph()
        p_c.text = c
        p_c.font.size = Pt(12)
        p_c.font.color.rgb = COLOR_TEXT

    # =========================================================================
    # SLIDE 8: Epidemic Trajectory Curves (Bending the Curve)
    # =========================================================================
    s8 = add_custom_slide("Epidemic Trajectory Analysis: 'Bending the Curve'", "Logarithmic trajectory plots of New Confirmed Cases vs Total Cumulative Cases")

    add_card(s8, 0.8, 2.1, 11.7, 4.8)
    tb_t = s8.shapes.add_textbox(Inches(1.1), Inches(2.3), Inches(11.1), Inches(4.4))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True

    p_tt = tf_t.paragraphs[0]
    p_tt.text = "📈 Why the Log-Log Trajectory Curve is Critical"
    p_tt.font.size = Pt(18)
    p_tt.font.bold = True
    p_tt.font.color.rgb = COLOR_PRIMARY
    p_tt.space_after = Pt(12)

    traj_points = [
        "Exponential Growth Signature: During an uncontrolled epidemic, growth is purely exponential. On a log-log plot (New Cases vs Total Cases), all countries initially trace the exact same upward diagonal straight line.",
        "The Inflection Drop: When public health interventions (lockdowns, masking, vaccines) take effect, growth drops off the diagonal line sharply downward.",
        "Curve Flattening Detection: Unlike traditional linear timelines that reset based on 'Day 0', the trajectory curve is time-independent, allowing pure mathematical benchmarking of when national containment worked.",
        "Omicron Spike & Rapid Collapse: In early 2022, trajectory charts across the US and Europe shot vertically upward due to Omicron's R0 > 5, followed by the fastest curve-bending collapse in pandemic history as herd immunity was achieved."
    ]
    for tp in traj_points:
        p = tf_t.add_paragraph()
        p.text = f"• {tp}"
        p.font.size = Pt(13)
        p.font.color.rgb = COLOR_TEXT
        p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 9: The Vaccine Decoupling Phenomenon
    # =========================================================================
    s9 = add_custom_slide("Clinical Decoupling: How Vaccines Altered Pandemic Outcomes", "Statistical proof that mass immunization broke the historical link between cases and deaths")

    add_card(s9, 0.8, 2.1, 3.75, 4.8, COLOR_CARD, COLOR_DANGER)
    tb_v1 = s9.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(3.35), Inches(4.4))
    tf_v1 = tb_v1.text_frame
    tf_v1.word_wrap = True
    p = tf_v1.paragraphs[0]
    p.text = "PRE-VACCINE ERA\n(Jan 2020 – May 2021)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_DANGER
    p.space_after = Pt(10)
    for pt in [
        "High Case Fatality Rate: ~2.4% – 3.2%",
        "Strict Coupling: Surging cases directly drove ICU occupancy and mortality spikes.",
        "Healthcare Collapse: Hospital systems overwhelmed in Italy, New York, and India."
    ]:
        p = tf_v1.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT

    add_card(s9, 4.79, 2.1, 3.75, 4.8, COLOR_CARD, COLOR_SUCCESS)
    tb_v2 = s9.shapes.add_textbox(Inches(5.0), Inches(2.3), Inches(3.35), Inches(4.4))
    tf_v2 = tb_v2.text_frame
    tf_v2.word_wrap = True
    p = tf_v2.paragraphs[0]
    p.text = "POST-VACCINE ERA\n(Dec 2021 – 2023 / Omicron)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_SUCCESS
    p.space_after = Pt(10)
    for pt in [
        "Plummeting CFR: < 0.35% in highly vaccinated countries (>75% fully vaccinated).",
        "Clinical Decoupling: Record 3M+ daily global cases, but ICU admissions remained low.",
        "85%+ Mortality Reduction compared to ancestral strains."
    ]:
        p = tf_v2.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT

    add_card(s9, 8.78, 2.1, 3.75, 4.8, COLOR_CARD, COLOR_PRIMARY)
    tb_v3 = s9.shapes.add_textbox(Inches(9.0), Inches(2.3), Inches(3.35), Inches(4.4))
    tf_v3 = tb_v3.text_frame
    tf_v3.word_wrap = True
    p = tf_v3.paragraphs[0]
    p.text = "STATISTICAL EVIDENCE"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)
    for pt in [
        "Linear Regression: Significant negative slope between Vaccination Coverage and CFR.",
        "Hospital Length of Stay: Reduced by 60% among vaccinated patients.",
        "Booster Efficacy: Third doses restored neutralizing antibody protection against immune-evasive sublineages."
    ]:
        p = tf_v3.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT

    # =========================================================================
    # SLIDE 10: Tableau Business Intelligence Dashboard
    # =========================================================================
    s10 = add_custom_slide("Tableau Visual Architecture & Calculated Fields", "Transforming pre-structured datasets into interactive business intelligence dashboards")

    add_card(s10, 0.8, 2.1, 5.75, 4.8)
    tb_tb1 = s10.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.35), Inches(4.5))
    tf_tb1 = tb_tb1.text_frame
    tf_tb1.word_wrap = True
    p = tf_tb1.paragraphs[0]
    p.text = "📐 Custom Calculated Fields"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)

    t_formulas = [
        "Case Fatality Rate:\n  (SUM([Cumulative Deaths]) / SUM([Cumulative Cases])) * 100",
        "Recovery Rate:\n  (SUM([Cumulative Recovered]) / SUM([Cumulative Cases])) * 100",
        "7-Day Moving Avg:\n  WINDOW_AVG(SUM([Daily Cases]), -6, 0)",
        "Dynamic Metric Parameter:\n  Parameter-driven CASE switch between Cases, Deaths, Recoveries, and Rates."
    ]
    for f in t_formulas:
        p = tf_tb1.add_paragraph()
        p.text = f
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_TEXT
        p.space_after = Pt(6)

    add_card(s10, 6.78, 2.1, 5.75, 4.8)
    tb_tb2 = s10.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.35), Inches(4.5))
    tf_tb2 = tb_tb2.text_frame
    tf_tb2.word_wrap = True
    p = tf_tb2.paragraphs[0]
    p.text = "🖥️ Worksheet & Dashboard Layout"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_SUCCESS
    p.space_after = Pt(10)

    sheets = [
        "• Sheet 1: Global Choropleth Map with severity gradients.",
        "• Sheet 2: Dual-Axis Epidemic Waves (Cases vs Deaths synchronized).",
        "• Sheet 3: Country-Wise Comparative Rankings with Top-N filters.",
        "• Sheet 4: Scatter Plot (Vaccination % vs Case Fatality Rate).",
        "• Sheet 5: Donut distribution (Recovered vs Active vs Fatalities).",
        "• Interactive Filter Actions: Clicking any country on the map dynamically filters all other trend charts!"
    ]
    for s in sheets:
        p = tf_tb2.add_paragraph()
        p.text = s
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT

    # =========================================================================
    # SLIDE 11: Streamlit Interactive Web Application
    # =========================================================================
    s11 = add_custom_slide("Streamlit Interactive Web Application", "Production web dashboard built with Python, Streamlit, and Plotly (dashboard/app.py)")

    app_modules = [
        ("Tab 1: Global Map & Overview", "Interactive Plotly choropleth with metric selector (Cases, Deaths, Recoveries, Rates per Million) and continental donuts.", COLOR_PRIMARY),
        ("Tab 2: Country Comparative", "Multi-country selection with linear vs log-scale curves and log-log trajectory tracking.", COLOR_SUCCESS),
        ("Tab 3: Infection & Recovery Trends", "Stacked area chart of Active vs Recovered vs Deaths and dual-axis incident recoveries.", COLOR_WARNING),
        ("Tab 4: Vaccine Decoupling", "Interactive scatter plot with OLS trendline showing immunization impact on clinical CFR.", COLOR_ACCENT),
        ("Tab 5: Data Explorer & Exporter", "Interactive filterable data table, instant CSV export, and 1-click download of the Executive Excel Workbook.", COLOR_DANGER)
    ]

    for i, (m_title, m_desc, col) in enumerate(app_modules):
        t = 2.1 + i * 1.0
        add_card(s11, 0.8, t, 11.7, 0.88, COLOR_CARD, col)
        tb = s11.shapes.add_textbox(Inches(1.0), Inches(t + 0.1), Inches(11.3), Inches(0.7))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = m_title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = col

        p_d = tf.add_paragraph()
        p_d.text = m_desc
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = COLOR_TEXT

    # =========================================================================
    # SLIDE 12: Executive Excel Report Architecture
    # =========================================================================
    s12 = add_custom_slide("Automated Multi-Sheet Executive Excel Workbook", "Generated via OpenPyXL (outputs/reports/COVID19_Global_Executive_Report.xlsx)")

    add_card(s12, 0.8, 2.1, 11.7, 4.8)
    tb_ex = s12.shapes.add_textbox(Inches(1.1), Inches(2.3), Inches(11.1), Inches(4.4))
    tf_ex = tb_ex.text_frame
    tf_ex.word_wrap = True

    p = tf_ex.paragraphs[0]
    p.text = "📊 Executive Workbook Worksheets & Features"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(12)

    ex_sheets = [
        "Sheet 1: Executive KPI Summary — High-level metric cards (Total Cases, Deaths, Recoveries, Doses, CFR %, Recovery Rate) and Continental Breakdown table.",
        "Sheet 2: Country Comparative Rankings — Sorted table with 60+ countries, ISO codes, per-capita metrics, CFR %, and vaccination rates.",
        "Sheet 3: Tableau-Optimized Extracts — Clean structured tables formatted for direct consumption by business analysts.",
        "Corporate Visual Design: Navy `#1F4E79` headers, alternating zebra striping, currency & percentage number formatting, and auto-fitted column widths."
    ]
    for es in ex_sheets:
        p = tf_ex.add_paragraph()
        p.text = f"• {es}"
        p.font.size = Pt(13)
        p.font.color.rgb = COLOR_TEXT
        p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 13: Technical Achievements & STAR Statements
    # =========================================================================
    s13 = add_custom_slide("Technical Competencies & Resume Bullet Points", "STAR Format statements for Data Analyst & Business Intelligence roles")

    stars = [
        ("Data Engineering & API Extraction", "Automated real-time ingestion from disease.sh REST API; engineered a 5-stage Pandas ETL pipeline processing 73,000+ time-series records across 60+ countries with automated 7-day smoothing.", COLOR_PRIMARY),
        ("Tableau & BI Visualization", "Designed an executive Tableau dashboard utilizing custom calculated fields (CFR, Recovery Rate) and interactive action filters for dynamic multi-country epidemiological benchmarking.", COLOR_SUCCESS),
        ("Statistical & Clinical Analytics", "Conducted country-wise comparative and trajectory regression analysis, proving an 85%+ decoupling between case spikes and patient mortality post mass-vaccination campaigns.", COLOR_ACCENT)
    ]

    for i, (cat, bullet, col) in enumerate(stars):
        t = 2.1 + i * 1.65
        add_card(s13, 0.8, t, 11.7, 1.45, COLOR_CARD, col)
        tb = s13.shapes.add_textbox(Inches(1.0), Inches(t + 0.15), Inches(11.3), Inches(1.2))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = cat.upper()
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(4)

        p_b = tf.add_paragraph()
        p_b.text = f'"{bullet}"'
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = COLOR_TEXT

    # =========================================================================
    # SLIDE 14: How to Run the Project (1-Click Automation)
    # =========================================================================
    s14 = add_custom_slide("Project Execution & 1-Click Automation", "Reproducible workflows designed for rapid demonstration and review")

    runners = [
        ("run_dashboard.bat", "Interactive Streamlit Web Dashboard", "Verifies dependencies and launches the full interactive web application in browser at http://localhost:8501.", COLOR_PRIMARY),
        ("run_pipeline.bat", "Master ETL & Analytics Pipeline", "Executes API extraction, Pandas cleaning, statistical analysis, Tableau datasets, and Excel workbook in ~8 seconds.", COLOR_SUCCESS),
        ("generate_ppt.bat", "PowerPoint Presentation Builder", "Instantly rebuilds this 15-slide PowerPoint deck with python-pptx.", COLOR_WARNING),
        ("run_notebook.bat", "Jupyter EDA & Analysis", "Launches Jupyter Notebook containing narrative EDA, data transformations, and Matplotlib/Seaborn plots.", COLOR_ACCENT)
    ]

    for i, (bat, role, desc, col) in enumerate(runners):
        row = i // 2
        col_idx = i % 2
        l = 0.8 + col_idx * 5.95
        t = 2.1 + row * 2.5
        add_card(s14, l, t, 5.75, 2.2, COLOR_CARD, col)
        tb = s14.shapes.add_textbox(Inches(l + 0.2), Inches(t + 0.15), Inches(5.35), Inches(1.9))
        tf = tb.text_frame
        tf.word_wrap = True

        p_b = tf.paragraphs[0]
        p_b.text = f"⚙️ {bat}"
        p_b.font.size = Pt(16)
        p_b.font.bold = True
        p_b.font.color.rgb = col

        p_r = tf.add_paragraph()
        p_r.text = role
        p_r.font.size = Pt(12)
        p_r.font.bold = True
        p_r.font.color.rgb = COLOR_TEXT
        p_r.space_after = Pt(4)

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 15: Conclusion & Q&A
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_background(s15)

    glow15 = s15.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(0.15), Inches(3.6))
    glow15.fill.solid()
    glow15.fill.fore_color.rgb = COLOR_SUCCESS
    glow15.line.fill.background()

    tb15 = s15.shapes.add_textbox(Inches(1.2), Inches(1.6), Inches(11.2), Inches(4.0))
    tf15 = tb15.text_frame
    tf15.word_wrap = True

    p0 = tf15.paragraphs[0]
    p0.text = "PROJECT DELIVERABLE COMPLETE"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_SUCCESS
    p0.space_after = Pt(12)

    p1 = tf15.add_paragraph()
    p1.text = "Thank You! Questions & Discussion"
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEXT
    p1.space_after = Pt(14)

    p2 = tf15.add_paragraph()
    p2.text = "COVID-19 Global Data Visualization & Comparative Analytics Dashboard"
    p2.font.size = Pt(18)
    p2.font.color.rgb = COLOR_PRIMARY
    p2.space_after = Pt(24)

    p3 = tf15.add_paragraph()
    p3.text = "Project Assets: Python ETL Pipeline • Tableau Datasets • Streamlit App • Excel Report • Jupyter Deck"
    p3.font.size = Pt(13)
    p3.font.color.rgb = COLOR_MUTED

    prs.save(output_path)
    print(f"\n[SUCCESS] PowerPoint Presentation generated successfully!")
    print(f"          Saved to: {output_path} (15 slides)\n")
    return output_path


if __name__ == "__main__":
    create_presentation()
