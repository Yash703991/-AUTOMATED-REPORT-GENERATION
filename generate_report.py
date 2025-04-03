import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import io
from datetime import datetime

def create_sales_chart(df):
    # Create a bar chart of sales by product
    plt.figure(figsize=(10, 6))
    product_sales = df.groupby('Product')['Sales'].sum()
    product_sales.plot(kind='bar')
    plt.title('Total Sales by Product')
    plt.xlabel('Product')
    plt.ylabel('Total Sales ($)')
    plt.xticks(rotation=45)
    
    # Save the plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close()
    return buf

def create_region_chart(df):
    # Create a pie chart of sales by region
    plt.figure(figsize=(8, 8))
    region_sales = df.groupby('Region')['Sales'].sum()
    plt.pie(region_sales, labels=region_sales.index, autopct='%1.1f%%')
    plt.title('Sales Distribution by Region')
    
    # Save the plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close()
    return buf

def generate_report():
    # Read the data
    df = pd.read_csv('sales_data.csv')
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        f"sales_report_{datetime.now().strftime('%Y%m%d')}.pdf",
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    heading_style = styles['Heading2']
    normal_style = styles['Normal']
    
    # Title
    elements.append(Paragraph("Sales Report", title_style))
    elements.append(Spacer(1, 12))
    
    # Executive Summary
    elements.append(Paragraph("Executive Summary", heading_style))
    elements.append(Spacer(1, 12))
    
    total_sales = df['Sales'].sum()
    avg_sales = df['Sales'].mean()
    top_product = df.groupby('Product')['Sales'].sum().idxmax()
    top_region = df.groupby('Region')['Sales'].sum().idxmax()
    
    summary_text = f"""
    This report analyzes sales data for the period {df['Date'].min()} to {df['Date'].max()}.
    Key findings include:
    • Total Sales: ${total_sales:,.2f}
    • Average Sale: ${avg_sales:,.2f}
    • Top Performing Product: {top_product}
    • Top Performing Region: {top_region}
    """
    elements.append(Paragraph(summary_text, normal_style))
    elements.append(Spacer(1, 12))
    
    # Sales by Product Chart
    elements.append(Paragraph("Sales by Product", heading_style))
    elements.append(Spacer(1, 12))
    
    sales_chart = create_sales_chart(df)
    img = Image(sales_chart, width=400, height=300)
    elements.append(img)
    elements.append(Spacer(1, 12))
    
    # Sales by Region Chart
    elements.append(Paragraph("Sales by Region", heading_style))
    elements.append(Spacer(1, 12))
    
    region_chart = create_region_chart(df)
    img = Image(region_chart, width=400, height=300)
    elements.append(img)
    elements.append(Spacer(1, 12))
    
    # Detailed Sales Table
    elements.append(Paragraph("Detailed Sales Data", heading_style))
    elements.append(Spacer(1, 12))
    
    # Prepare table data
    table_data = [['Date', 'Product', 'Sales', 'Region']]
    for _, row in df.iterrows():
        table_data.append([
            row['Date'],
            row['Product'],
            f"${row['Sales']:,.2f}",
            row['Region']
        ])
    
    # Create table
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    
    # Build the PDF
    doc.build(elements)
    print(f"Report generated successfully: sales_report_{datetime.now().strftime('%Y%m%d')}.pdf")

if __name__ == "__main__":
    generate_report() 
