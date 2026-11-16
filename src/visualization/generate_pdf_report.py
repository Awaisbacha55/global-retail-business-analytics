"""
Professional PDF Report Generator using ReportLab.
Compiles executive summaries, KPI scorecards, visual analytics,
SQL methodology, machine learning benchmarks, and recommendations
into a publication-quality final PDF document.
"""

from pathlib import Path
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically inject running headers, footers, and page numbers.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            # Suppress headers and footers on the cover page
            return

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))

        # Running Header
        self.drawString(54, 750, "Global Retail Business Analytics & Decision Intelligence | Devixo Solutions")
        self.drawRightString(558, 750, "Task 04 Final Report")
        self.setStrokeColor(colors.HexColor("#CCCCCC"))
        self.setLineWidth(0.5)
        self.line(54, 744, 558, 744)

        # Running Footer
        self.line(54, 45, 558, 45)
        self.drawString(54, 32, "Author: Muhammad Awais Bacha | Data Science Internship")
        self.drawRightString(558, 32, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def build_final_pdf_report(output_pdf_path: Path, figures_dir: Path) -> Path:
    logger.info(f"Initiating PDF report generation at: {output_pdf_path}")
    output_pdf_path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(output_pdf_path),
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=26,
        leading=32,
        textColor=colors.HexColor("#0D3B66"),
        alignment=1,
        spaceAfter=15
    )
    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=13,
        leading=18,
        textColor=colors.HexColor("#4A5568"),
        alignment=1,
        spaceAfter=30
    )
    h1_style = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0D3B66"),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        "Heading2_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#1F77B4"),
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        "Body_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#2D3748"),
        spaceAfter=6
    )
    bullet_style = ParagraphStyle(
        "Bullet_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#2D3748"),
        leftIndent=15,
        spaceAfter=4
    )
    caption_style = ParagraphStyle(
        "Caption_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#666666"),
        alignment=1,
        spaceAfter=10
    )

    story = []

    # =========================================================================
    # 1. COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 1.2 * inch))
    story.append(Paragraph("DEVIXO SOLUTIONS DATA SCIENCE INTERNSHIP", ParagraphStyle("MetaHeader", fontName="Helvetica-Bold", fontSize=12, leading=14, alignment=1, textColor=colors.HexColor("#EE6C4D"))))
    story.append(Spacer(1, 15))
    story.append(Paragraph("Global Retail Business Analytics & Decision Intelligence", title_style))
    story.append(Paragraph("End-to-End Enterprise Analytics, SQL Architecture, Power BI Modeling & Machine Learning", subtitle_style))
    story.append(Spacer(1, 0.5 * inch))

    # Metadata Box
    meta_data = [
        [Paragraph("<b>Candidate Name:</b>", body_style), Paragraph("Muhammad Awais Bacha", body_style)],
        [Paragraph("<b>Internship Organization:</b>", body_style), Paragraph("Devixo Solutions", body_style)],
        [Paragraph("<b>Project Task:</b>", body_style), Paragraph("Task 04 — Complete Business Analytics Project", body_style)],
        [Paragraph("<b>Dataset:</b>", body_style), Paragraph("Global Superstore Enterprise (51,290 Records)", body_style)],
        [Paragraph("<b>Repository:</b>", body_style), Paragraph("global-retail-business-analytics", body_style)],
        [Paragraph("<b>Date of Submission:</b>", body_style), Paragraph(datetime.date.today().strftime("%B %d, %Y"), body_style)]
    ]
    meta_table = Table(meta_data, colWidths=[160, 280])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 0.8 * inch))

    # Executive Highlights Card
    card_data = [
        [Paragraph("<b>Revenue:</b> $12.64M", body_style), Paragraph("<b>Net Profit:</b> $1.47M", body_style), Paragraph("<b>Orders:</b> 25,035", body_style)],
        [Paragraph("<b>AOV:</b> $504.99", body_style), Paragraph("<b>Margin:</b> 11.61%", body_style), Paragraph("<b>CAGR:</b> +23.9%", body_style)]
    ]
    card_table = Table(card_data, colWidths=[145, 145, 150])
    card_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93C5FD")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#BFDBFE")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(card_table)
    story.append(PageBreak())

    # =========================================================================
    # 2. EXECUTIVE SUMMARY & PROBLEM CONTEXT
    # =========================================================================
    story.append(Paragraph("1. Executive Summary & Problem Context", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0D3B66"), spaceAfter=10))
    story.append(Paragraph(
        "Between January 2011 and December 2014, the Global Superstore enterprise fulfilled 51,290 retail and commercial order lines across 147 countries, generating $12,642,501.91 in gross revenue and $1,467,457.29 in net cumulative profit. "
        "While top-line revenue expanded aggressively at a 4-year Compound Annual Growth Rate (CAGR) of 23.9%, underlying profitability varies dramatically across regional markets, customer tiers, and product categories.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Core Business Questions Addressed:</b><br/>"
        "1. <i>Catalog Profitability:</i> Which product categories drive operating profits, and which act as financial drains?<br/>"
        "2. <i>Discount Optimization:</i> How do price promotions impact profit margins across fulfillment modes?<br/>"
        "3. <i>Customer Segmentation:</i> How is enterprise revenue distributed across commercial and consumer accounts?<br/>"
        "4. <i>Predictive Replenishment:</i> Can future monthly sales be reliably forecasted to prevent Q4 stockouts?",
        body_style
    ))
    story.append(Spacer(1, 8))

    # Core KPI Summary Table
    story.append(Paragraph("Audited Executive KPI Scorecard", h2_style))
    kpi_rows = [
        [Paragraph("<b>Metric Name</b>", body_style), Paragraph("<b>Mathematical Formula</b>", body_style), Paragraph("<b>Audited Value</b>", body_style)],
        ["Total Revenue", "SUM(Sales)", "$12,642,501.91"],
        ["Total Profit", "SUM(Profit)", "$1,467,457.29"],
        ["Total Distinct Orders", "COUNT(DISTINCT Order ID)", "25,035 Orders"],
        ["Average Order Value (AOV)", "Total Revenue / Total Orders", "$504.99 per Order"],
        ["Net Profit Margin %", "(Total Profit / Total Revenue) * 100", "11.61%"],
        ["Total Active Customers", "COUNT(DISTINCT Customer ID)", "1,590 Accounts"],
        ["Annual Sales Growth (CAGR)", "((Rev_2014 / Rev_2011)^(1/3) - 1) * 100", "+23.93% per Annum"]
    ]
    kpi_table = Table(kpi_rows, colWidths=[140, 200, 140])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0D3B66")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 10))

    # Embed Fig 2 & 3
    if (figures_dir / "02_monthly_sales_trend.png").exists():
        story.append(Image(str(figures_dir / "02_monthly_sales_trend.png"), width=6.2*inch, height=2.6*inch))
        story.append(Paragraph("Figure 1: 48-Month Historical Sales Trend (2011–2014) displaying Q4 holiday demand acceleration.", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # 3. DATA QUALITY, CLEANING & FEATURE ENGINEERING
    # =========================================================================
    story.append(Paragraph("2. Data Preparation, Quality Audit & Feature Engineering", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0D3B66"), spaceAfter=10))
    story.append(Paragraph(
        "The raw dataset contained 51,290 records across 24 columns. A rigorous data quality audit was conducted in Python: "
        "<br/>• <b>Missing Value Treatment:</b> 41,296 unpopulated `Postal Code` entries (80.5%) were evaluated. Cross-tabulation proved postal codes exist strictly for US domestic orders; non-US records do not carry US-style ZIP codes. Dropping these rows would have deleted 80% of global operations. They were safely categorized as 'Unknown', preserving full data integrity."
        "<br/>• <b>Deduplication:</b> Zero exact duplicates existed in the raw dataset."
        "<br/>• <b>Feature Enrichment:</b> 21 new attributes were engineered, including calendar dimensions (`order_year`, `order_month`, `order_quarter`), operational transit duration (`shipping_duration_days`), financial metrics (`profit_margin_pct`, `unit_price`, `unit_cost`), and customer RFM lifetime statistics.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # Embed Fig 1 & Fig 17
    fig_col = []
    if (figures_dir / "01_overall_sales_distribution.png").exists():
        story.append(Image(str(figures_dir / "01_overall_sales_distribution.png"), width=6.0*inch, height=2.5*inch))
        story.append(Paragraph("Figure 2: Order Line Sales Distribution showing core density under $250 with positive skew.", caption_style))

    if (figures_dir / "17_sales_growth_analysis.png").exists():
        story.append(Image(str(figures_dir / "17_sales_growth_analysis.png"), width=6.0*inch, height=2.5*inch))
        story.append(Paragraph("Figure 3: Year-over-Year Revenue Growth Rate (%) demonstrating sustained double-digit expansion.", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # 4. EXPLORATORY DATA ANALYSIS: CATEGORY & PRODUCT DYNAMICS
    # =========================================================================
    story.append(Paragraph("3. Product Catalog & Category Performance", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0D3B66"), spaceAfter=10))
    story.append(Paragraph(
        "Evaluation across the 3 product categories and 17 subcategories reveals stark profitability divergences: "
        "<br/>• <b>Technology:</b> Drives $4,744,557.50 in revenue and $663,778.73 in net profit at an industry-leading 13.99% margin. Copiers alone delivered $258,609.91 in profit (17.13% margin)."
        "<br/>• <b>Office Supplies:</b> Highly consistent cash flow generator ($3,787,070.22 sales, $518,473.83 profit, 13.69% margin)."
        "<br/>• <b>Furniture:</b> Generated $4,110,874.19 in sales but achieved only $285,204.72 in profit (6.94% margin). This underperformance is directly caused by the <b>Tables</b> subcategory, which lost <b>-$64,083.39</b> due to severe shipping freight costs and unmanaged discounting.",
        body_style
    ))
    story.append(Spacer(1, 6))

    if (figures_dir / "04_sales_by_product_category.png").exists():
        story.append(Image(str(figures_dir / "04_sales_by_product_category.png"), width=6.0*inch, height=2.4*inch))
        story.append(Paragraph("Figure 4: Total Revenue contribution by major product category.", caption_style))

    if (figures_dir / "05_sales_by_subcategory.png").exists():
        story.append(Image(str(figures_dir / "05_sales_by_subcategory.png"), width=6.0*inch, height=2.7*inch))
        story.append(Paragraph("Figure 5: Total Sales ranking across all 17 subcategories.", caption_style))

    story.append(PageBreak())

    # Embed Fig 6 & 7
    story.append(Paragraph("Top and Bottom Product Revenue Generators", h2_style))
    if (figures_dir / "06_top_10_products_by_sales.png").exists():
        story.append(Image(str(figures_dir / "06_top_10_products_by_sales.png"), width=6.0*inch, height=2.6*inch))
        story.append(Paragraph("Figure 6: Top 10 Revenue-Generating Products led by commercial copiers and smart phones.", caption_style))

    if (figures_dir / "07_bottom_10_products_by_sales.png").exists():
        story.append(Image(str(figures_dir / "07_bottom_10_products_by_sales.png"), width=6.0*inch, height=2.6*inch))
        story.append(Paragraph("Figure 7: Bottom 10 Revenue-Generating Products representing slow-moving inventory candidates.", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # 5. REGIONAL & GEOGRAPHIC PERFORMANCE
    # =========================================================================
    story.append(Paragraph("4. Geographic Markets & Regional Analytics", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0D3B66"), spaceAfter=10))
    story.append(Paragraph(
        "Global Superstore operates across 7 continental markets and 13 geographic regions. International operations now account for over 80% of global transactions. "
        "<br/>• <b>Asia-Pacific (APAC):</b> Largest overall market ($3,585,744.80 sales, $436,045.26 profit, 12.16% margin)."
        "<br/>• <b>Europe (EU):</b> Second largest market ($2,938,205.85 sales, $372,829.74 profit, 12.69% margin)."
        "<br/>• <b>United States (US):</b> Foundation market ($2,297,200.86 sales, $286,397.02 profit, 12.47% margin)."
        "<br/>• <b>EMEA & Africa:</b> Lagging margin efficiency. EMEA achieved only 5.44% net margin ($806.2K sales, $43.9K profit), hampered by fragmented courier delivery networks and customs fees.",
        body_style
    ))
    story.append(Spacer(1, 6))

    if (figures_dir / "09_regional_sales_performance.png").exists():
        story.append(Image(str(figures_dir / "09_regional_sales_performance.png"), width=6.0*inch, height=2.5*inch))
        story.append(Paragraph("Figure 8: Regional Sales Performance across all 13 operating regions.", caption_style))

    if (figures_dir / "10_profit_by_region.png").exists():
        story.append(Image(str(figures_dir / "10_profit_by_region.png"), width=6.0*inch, height=2.5*inch))
        story.append(Paragraph("Figure 9: Cumulative Profit by Region highlighting profitability disparities.", caption_style))

    story.append(PageBreak())

    # Embed Fig 19 & 20
    story.append(Paragraph("Geographic Concentration and Category Heatmap", h2_style))
    if (figures_dir / "19_top_15_countries_sales.png").exists():
        story.append(Image(str(figures_dir / "19_top_15_countries_sales.png"), width=6.0*inch, height=2.6*inch))
        story.append(Paragraph("Figure 10: Top 15 Revenue Contributing Countries led by United States, Australia, and France.", caption_style))

    if (figures_dir / "20_category_market_profit_heatmap.png").exists():
        story.append(Image(str(figures_dir / "20_category_market_profit_heatmap.png"), width=6.0*inch, height=2.6*inch))
        story.append(Paragraph("Figure 11: Profitability Heatmap: Category vs Market ($ in Thousands).", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # 6. PROFITABILITY, DISCOUNTING & FULFILLMENT LOGISTICS
    # =========================================================================
    story.append(Paragraph("5. Profitability Drivers & Discount Exposure", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0D3B66"), spaceAfter=10))
    story.append(Paragraph(
        "A critical finding of this analytics engagement is the devastating impact of unmanaged promotional discounting. "
        "<br/>• Over <b>12,544 transaction lines (24.46%) produced negative net profit</b>, inflicting an aggregate gross loss exceeding $380,000."
        "<br/>• Transactions with 0% discount average <b>+$31.00 net profit</b>. When discounts exceed 20%, average transaction profit collapses into steep negative territory (-$35 to -$88 per item)."
        "<br/>• Standard Class fulfillment represents 59.9% of shipments (avg 5.0 days) with an 11.6% margin. Same Day delivery delivered an identical 11.4% margin, showing that expedited surcharges fail to capture an urgency premium.",
        body_style
    ))
    story.append(Spacer(1, 6))

    if (figures_dir / "13_discount_vs_profit_relationship.png").exists():
        story.append(Image(str(figures_dir / "13_discount_vs_profit_relationship.png"), width=6.0*inch, height=2.5*inch))
        story.append(Paragraph("Figure 12: Severe profit collapse when promotional discounts exceed 20%.", caption_style))

    if (figures_dir / "18_shipping_mode_analysis.png").exists():
        story.append(Image(str(figures_dir / "18_shipping_mode_analysis.png"), width=6.0*inch, height=2.5*inch))
        story.append(Paragraph("Figure 13: Order fulfillment distribution and volume by Shipping Mode.", caption_style))

    story.append(PageBreak())

    # Embed Fig 12 & 16
    story.append(Paragraph("Sales-to-Profit Correlation & Monthly Profit Velocity", h2_style))
    if (figures_dir / "12_sales_vs_profit_relationship.png").exists():
        story.append(Image(str(figures_dir / "12_sales_vs_profit_relationship.png"), width=6.0*inch, height=2.6*inch))
        story.append(Paragraph("Figure 14: Sales vs Profit Scatter Matrix showing negative-margin outlier transactions.", caption_style))

    if (figures_dir / "16_monthly_profit_trend.png").exists():
        story.append(Image(str(figures_dir / "16_monthly_profit_trend.png"), width=6.0*inch, height=2.6*inch))
        story.append(Paragraph("Figure 15: 48-Month Historical Profit Velocity showing strong Q4 surges.", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # 7. CUSTOMER BEHAVIOR & MACHINE LEARNING MODELS
    # =========================================================================
    story.append(Paragraph("6. Customer Intelligence & Machine Learning Models", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0D3B66"), spaceAfter=10))
    story.append(Paragraph(
        "Two enterprise machine learning solutions were developed and evaluated: "
        "<br/>• <b>Model A: Time-Series Sales Forecasting (Random Forest):</b> A monthly demand predictor evaluated on 2014 hold-out validation data achieved an outstanding <b>16.95% MAPE</b> (MAE: $68,184.35 | RMSE: $85,070.62), decisively outperforming 3-Month Moving Average (24.85% MAPE) and Naive baselines (27.71% MAPE)."
        "<br/>• <b>Model B: Customer RFM Segmentation (K-Means Clustering):</b> Clustered 1,590 customer accounts into 4 operational tiers (Silhouette Score: 0.392). The top two segments (Champions and Core Growth, 806 accounts) generate <b>87.4% ($11.05M) of total revenue</b>.",
        body_style
    ))
    story.append(Spacer(1, 6))

    if (Path("models/sales_forecasting/forecast_validation_plot.png")).exists():
        story.append(Image("models/sales_forecasting/forecast_validation_plot.png", width=6.0*inch, height=2.6*inch))
        story.append(Paragraph("Figure 16: Sales Demand Forecasting: Actual vs Predicted (2014 Validation).", caption_style))

    if (Path("models/customer_segmentation/customer_segments_scatter.png")).exists():
        story.append(Image("models/customer_segmentation/customer_segments_scatter.png", width=6.0*inch, height=2.6*inch))
        story.append(Paragraph("Figure 17: Customer RFM Segmentation Matrix (k=4).", caption_style))

    story.append(PageBreak())

    # Embed Fig 8 & 14
    story.append(Paragraph("Customer Concentration and Segment Share", h2_style))
    if (figures_dir / "08_top_10_customers_by_revenue.png").exists():
        story.append(Image(str(figures_dir / "08_top_10_customers_by_revenue.png"), width=6.0*inch, height=2.6*inch))
        story.append(Paragraph("Figure 18: Top 10 Customers by Cumulative Lifetime Spend.", caption_style))

    if (figures_dir / "14_order_distribution_by_segment.png").exists():
        story.append(Image(str(figures_dir / "14_order_distribution_by_segment.png"), width=5.5*inch, height=2.6*inch))
        story.append(Paragraph("Figure 19: Order Distribution by Customer Segment.", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # 8. STRATEGIC RECOMMENDATIONS & CONCLUSION
    # =========================================================================
    story.append(Paragraph("7. Strategic Business Recommendations", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0D3B66"), spaceAfter=10))
    story.append(Paragraph(
        "Based on rigorous analytical evidence, leadership is advised to implement the following high-impact initiatives:",
        body_style
    ))

    rec_table_data = [
        [Paragraph("<b>#</b>", body_style), Paragraph("<b>Strategic Initiative</b>", body_style), Paragraph("<b>Target Benefit</b>", body_style), Paragraph("<b>Priority</b>", body_style)],
        ["1", "Cap Discounts >20% in Order System", "Recover $150K–$220K in lost annual margin", "HIGH"],
        ["2", "Restructure Tables Subcategory Catalog", "Reverse -$64.1K loss into break-even/profit", "HIGH"],
        ["3", "VIP Key Account Retention for Champions", "Protect $11M in core recurring revenue", "HIGH"],
        ["4", "Embed ML Forecast in Inventory Replenishment", "Cut Q4 stockouts by 30% and rush freight by $45K", "MEDIUM"],
        ["5", "Establish Centralized EMEA Logistics Hub", "Elevate EMEA margin from 5.4% toward 10.0%", "MEDIUM"],
        ["6", "Rebalance Same-Day Delivery Surcharges", "Capture ~$30K incremental net courier profit", "MEDIUM"],
        ["7", "Bundle High-Margin Technology & Copiers", "Expand store AOV by $35–$50 and margin by 1.0%", "MEDIUM"],
        ["8", "Implement Minimum Order Quantities on Fasteners", "Cut small-parts warehouse pick/pack labor 40%", "LOW"],
        ["9", "Automated Win-Back for At-Risk Customers", "Reactivate 15% of lapsed accounts (~$115K sales)", "MEDIUM"],
        ["10", "Deploy Power BI 6-Page Interactive Dashboard", "Accelerate executive decision SLA to real-time", "HIGH"]
    ]
    rec_table = Table(rec_table_data, colWidths=[20, 210, 180, 70])
    rec_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0D3B66")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('ALIGN', (3,1), (3,-1), 'CENTER')
    ]))
    story.append(rec_table)
    story.append(Spacer(1, 14))

    story.append(Paragraph("8. Project Limitations & Attribution", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0D3B66"), spaceAfter=10))
    story.append(Paragraph(
        "<b>Technical Limitations:</b><br/>"
        "• <i>Geographic Resolution:</i> Postal codes are only recorded for US orders. International spatial analytics are bounded at City/State/Country level.<br/>"
        "• <i>Cost Disaggregation:</i> Raw data provides aggregated Sales and Profit; detailed breakdown of COGS, marketing, and tariffs is estimated via unit cost modeling.<br/>"
        "• <i>Power BI Desktop:</i> Native `.pbix` automation was not accessible in the current Windows headless CLI; comprehensive Star Schema models, verified DAX measures, and manual build guides have been fully generated in `dashboard/`.",
        body_style
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<b>Dataset Attribution:</b><br/>"
        "Global Superstore 2011–2014 dataset. Sourced from authentic public business intelligence benchmark distributions (Tableau / Kaggle). Utilized under educational and professional portfolio license.",
        body_style
    ))

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    logger.info(f"PDF successfully built: {output_pdf_path} ({output_pdf_path.stat().st_size:,} bytes)")
    return output_pdf_path


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parents[2]
    out_pdf = base_dir / "reports" / "final_project_report.pdf"
    figs = base_dir / "reports" / "figures"
    build_final_pdf_report(out_pdf, figs)
