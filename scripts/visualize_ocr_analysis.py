"""
OCR Analysis Visualizer - Script untuk membuat visualisasi Pattern Matching dan Feature Extraction
"""

import json
import os
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
import numpy as np

def load_report(report_path):
    """Load OCR report JSON."""
    with open(report_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def visualize_pattern_matching(report_data, output_dir):
    """Visualisasi Pattern Matching."""
    pattern_data = report_data.get("pattern_matching", {})
    
    # Buat figure dengan subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Pattern Matching Analysis', fontsize=16, fontweight='bold')
    
    # 1. Tanggal Detection
    ax1 = axes[0, 0]
    tanggal_matches = pattern_data.get("tanggal", [])
    ax1.bar(['Tanggal'], [len(tanggal_matches)], color='skyblue')
    ax1.set_title('Tanggal Detection', fontweight='bold')
    ax1.set_ylabel('Count')
    ax1.set_ylim(0, max(1, len(tanggal_matches) + 1))
    for i, v in enumerate([len(tanggal_matches)]):
        ax1.text(i, v + 0.1, str(v), ha='center', fontweight='bold')
    
    # 2. Harga Detection
    ax2 = axes[0, 1]
    harga_matches = pattern_data.get("harga", [])
    if harga_matches:
        confidences = [item.get("confidence", 0) for item in harga_matches]
        ax2.hist(confidences, bins=10, color='lightcoral', edgecolor='black')
        ax2.set_title('Harga Detection - Confidence Distribution', fontweight='bold')
        ax2.set_xlabel('Confidence Score')
        ax2.set_ylabel('Frequency')
        ax2.axvline(0.5, color='red', linestyle='--', label='Threshold 0.5')
        ax2.legend()
    else:
        ax2.text(0.5, 0.5, 'No harga matches found', ha='center', va='center', 
                transform=ax2.transAxes, fontsize=12)
        ax2.set_title('Harga Detection', fontweight='bold')
    
    # 3. Jumlah Detection
    ax3 = axes[1, 0]
    jumlah_matches = pattern_data.get("jumlah", [])
    ax3.bar(['Jumlah'], [len(jumlah_matches)], color='lightgreen')
    ax3.set_title('Jumlah Detection', fontweight='bold')
    ax3.set_ylabel('Count')
    ax3.set_ylim(0, max(1, len(jumlah_matches) + 1))
    for i, v in enumerate([len(jumlah_matches)]):
        ax3.text(i, v + 0.1, str(v), ha='center', fontweight='bold')
    
    # 4. Summary Table
    ax4 = axes[1, 1]
    ax4.axis('off')
    summary_data = [
        ['Pattern Type', 'Matches Found'],
        ['Tanggal', len(tanggal_matches)],
        ['Harga', len(harga_matches)],
        ['Jumlah', len(jumlah_matches)]
    ]
    table = ax4.table(cellText=summary_data, cellLoc='center', loc='center',
                     colWidths=[0.6, 0.4])
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 2)
    # Style header
    for i in range(2):
        table[(0, i)].set_facecolor('#4CAF50')
        table[(0, i)].set_text_props(weight='bold', color='white')
    ax4.set_title('Pattern Matching Summary', fontweight='bold')
    
    plt.tight_layout()
    output_path = os.path.join(output_dir, "pattern_matching_visualization.png")
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    return output_path

def visualize_feature_extraction(report_data, output_dir):
    """Visualisasi Feature Extraction."""
    feature_data = report_data.get("feature_extraction", {})
    
    # Buat figure dengan subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Feature Extraction Analysis', fontsize=16, fontweight='bold')
    
    # 1. Spatial Distribution
    ax1 = axes[0, 0]
    spatial = feature_data.get("spatial_distribution", {})
    x_range = spatial.get("x_range", [0, 100])
    y_range = spatial.get("y_range", [0, 100])
    x_center = spatial.get("x_center", 50)
    y_center = spatial.get("y_center", 50)
    
    # Gambar bounding box
    rect = Rectangle((x_range[0], y_range[0]), 
                    x_range[1] - x_range[0], 
                    y_range[1] - y_range[0],
                    linewidth=2, edgecolor='blue', facecolor='none', label='Text Region')
    ax1.add_patch(rect)
    
    # Gambar center point
    ax1.plot(x_center, y_center, 'ro', markersize=10, label='Center Point')
    
    ax1.set_xlim(0, max(x_range[1] + 50, 100))
    ax1.set_ylim(0, max(y_range[1] + 50, 100))
    ax1.set_xlabel('X Position')
    ax1.set_ylabel('Y Position')
    ax1.set_title('Spatial Distribution', fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Text Density
    ax2 = axes[0, 1]
    density = feature_data.get("text_density", {})
    total_regions = density.get("total_text_regions", 0)
    regions_per_line = density.get("regions_per_line", 0)
    
    categories = ['Total Regions', 'Regions per Line']
    values = [total_regions, regions_per_line]
    colors = ['orange', 'purple']
    
    ax2.bar(categories, values, color=colors)
    ax2.set_title('Text Density', fontweight='bold')
    ax2.set_ylabel('Count')
    for i, v in enumerate(values):
        ax2.text(i, v + max(values)*0.02, str(v), ha='center', fontweight='bold')
    
    # 3. Confidence Distribution
    ax3 = axes[1, 0]
    conf_dist = feature_data.get("confidence_distribution", {})
    min_conf = conf_dist.get("min_confidence", 0)
    max_conf = conf_dist.get("max_confidence", 1)
    avg_conf = conf_dist.get("avg_confidence", 0)
    
    metrics = ['Min Confidence', 'Max Confidence', 'Avg Confidence']
    values = [min_conf, max_conf, avg_conf]
    colors = ['red', 'green', 'blue']
    
    ax3.bar(metrics, values, color=colors)
    ax3.set_title('Confidence Distribution', fontweight='bold')
    ax3.set_ylabel('Confidence Score')
    ax3.set_ylim(0, 1)
    ax3.axhline(0.5, color='red', linestyle='--', label='Threshold 0.5')
    ax3.legend()
    for i, v in enumerate(values):
        ax3.text(i, v + 0.02, f'{v:.3f}', ha='center', fontweight='bold')
    
    # 4. Feature Summary
    ax4 = axes[1, 1]
    ax4.axis('off')
    summary_data = [
        ['Feature', 'Value'],
        ['X Range', f'{x_range[0]:.1f} - {x_range[1]:.1f}'],
        ['Y Range', f'{y_range[0]:.1f} - {y_range[1]:.1f}'],
        ['Center Point', f'({x_center:.1f}, {y_center:.1f})'],
        ['Total Regions', str(total_regions)],
        ['Regions per Line', str(regions_per_line)],
        ['Avg Confidence', f'{avg_conf:.3f}']
    ]
    table = ax4.table(cellText=summary_data, cellLoc='center', loc='center',
                     colWidths=[0.5, 0.5])
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 1.8)
    # Style header
    for i in range(2):
        table[(0, i)].set_facecolor('#2196F3')
        table[(0, i)].set_text_props(weight='bold', color='white')
    ax4.set_title('Feature Extraction Summary', fontweight='bold')
    
    plt.tight_layout()
    output_path = os.path.join(output_dir, "feature_extraction_visualization.png")
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    return output_path

def visualize_combined_analysis(report_data, output_dir):
    """Visualisasi gabungan Pattern Matching dan Feature Extraction."""
    pattern_data = report_data.get("pattern_matching", {})
    feature_data = report_data.get("feature_extraction", {})
    
    # Buat figure besar
    fig = plt.figure(figsize=(16, 12))
    fig.suptitle('OCR Analysis: Pattern Matching & Feature Extraction', 
                 fontsize=18, fontweight='bold')
    
    # Grid layout
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # 1. Pattern Counts (Top Left)
    ax1 = fig.add_subplot(gs[0, 0])
    pattern_counts = [
        len(pattern_data.get("tanggal", [])),
        len(pattern_data.get("harga", [])),
        len(pattern_data.get("jumlah", []))
    ]
    pattern_labels = ['Tanggal', 'Harga', 'Jumlah']
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    ax1.pie(pattern_counts, labels=pattern_labels, colors=colors, autopct='%1.1f%%',
            startangle=90)
    ax1.set_title('Pattern Detection Distribution', fontweight='bold')
    
    # 2. Confidence Histogram (Top Middle)
    ax2 = fig.add_subplot(gs[0, 1])
    harga_matches = pattern_data.get("harga", [])
    if harga_matches:
        confidences = [item.get("confidence", 0) for item in harga_matches]
        ax2.hist(confidences, bins=15, color='lightcoral', edgecolor='black', alpha=0.7)
        ax2.axvline(0.5, color='red', linestyle='--', linewidth=2, label='Threshold 0.5')
        ax2.set_title('Harga Confidence Distribution', fontweight='bold')
        ax2.set_xlabel('Confidence Score')
        ax2.set_ylabel('Frequency')
        ax2.legend()
    else:
        ax2.text(0.5, 0.5, 'No data', ha='center', va='center', fontsize=14)
        ax2.set_title('Harga Confidence Distribution', fontweight='bold')
    
    # 3. Spatial Plot (Top Right)
    ax3 = fig.add_subplot(gs[0, 2])
    spatial = feature_data.get("spatial_distribution", {})
    x_range = spatial.get("x_range", [0, 100])
    y_range = spatial.get("y_range", [0, 100])
    x_center = spatial.get("x_center", 50)
    y_center = spatial.get("y_center", 50)
    
    rect = Rectangle((x_range[0], y_range[0]), 
                    x_range[1] - x_range[0], 
                    y_range[1] - y_range[0],
                    linewidth=2, edgecolor='blue', facecolor='lightblue', alpha=0.5)
    ax3.add_patch(rect)
    ax3.plot(x_center, y_center, 'ro', markersize=12, label='Center')
    ax3.set_xlim(0, max(x_range[1] + 50, 100))
    ax3.set_ylim(0, max(y_range[1] + 50, 100))
    ax3.set_title('Spatial Distribution', fontweight='bold')
    ax3.set_xlabel('X')
    ax3.set_ylabel('Y')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. Text Metrics (Middle Left)
    ax4 = fig.add_subplot(gs[1, 0])
    density = feature_data.get("text_density", {})
    total = density.get("total_text_regions", 0)
    per_line = density.get("regions_per_line", 0)
    
    metrics = ['Total\nRegions', 'Regions\nper Line']
    values = [total, per_line]
    ax4.bar(metrics, values, color=['#FFA07A', '#98D8C8'])
    ax4.set_title('Text Density Metrics', fontweight='bold')
    for i, v in enumerate(values):
        ax4.text(i, v + max(values)*0.02, str(v), ha='center', fontweight='bold', fontsize=12)
    
    # 5. Confidence Metrics (Middle Middle)
    ax5 = fig.add_subplot(gs[1, 1])
    conf_dist = feature_data.get("confidence_distribution", {})
    conf_metrics = ['Min', 'Max', 'Avg']
    conf_values = [
        conf_dist.get("min_confidence", 0),
        conf_dist.get("max_confidence", 1),
        conf_dist.get("avg_confidence", 0)
    ]
    colors_conf = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    ax5.bar(conf_metrics, conf_values, color=colors_conf)
    ax5.set_title('Confidence Metrics', fontweight='bold')
    ax5.set_ylim(0, 1)
    ax5.axhline(0.5, color='red', linestyle='--', alpha=0.7)
    for i, v in enumerate(conf_values):
        ax5.text(i, v + 0.02, f'{v:.3f}', ha='center', fontweight='bold')
    
    # 6. Pattern Summary Table (Middle Right)
    ax6 = fig.add_subplot(gs[1, 2])
    ax6.axis('off')
    pattern_summary = [
        ['Pattern', 'Count', 'Avg Conf'],
        ['Tanggal', len(pattern_data.get("tanggal", [])), 'N/A'],
        ['Harga', len(pattern_data.get("harga", [])), 
         f'{np.mean([h.get("confidence",0) for h in pattern_data.get("harga", [])]):.3f}' if pattern_data.get("harga") else 'N/A'],
        ['Jumlah', len(pattern_data.get("jumlah", [])), 'N/A']
    ]
    table = ax6.table(cellText=pattern_summary, cellLoc='center', loc='center',
                     colWidths=[0.3, 0.3, 0.4])
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2)
    for i in range(3):
        table[(0, i)].set_facecolor('#9B59B6')
        table[(0, i)].set_text_props(weight='bold', color='white')
    ax6.set_title('Pattern Summary', fontweight='bold')
    
    # 7. Feature Summary Table (Bottom - spans all columns)
    ax7 = fig.add_subplot(gs[2, :])
    ax7.axis('off')
    feature_summary = [
        ['Feature', 'Value'],
        ['X Range', f'{x_range[0]:.1f} - {x_range[1]:.1f}'],
        ['Y Range', f'{y_range[0]:.1f} - {y_range[1]:.1f}'],
        ['Center Point', f'({x_center:.1f}, {y_center:.1f})'],
        ['Total Text Regions', str(total)],
        ['Regions per Line', str(per_line)],
        ['Min Confidence', f'{conf_dist.get("min_confidence", 0):.4f}'],
        ['Max Confidence', f'{conf_dist.get("max_confidence", 1):.4f}'],
        ['Avg Confidence', f'{conf_dist.get("avg_confidence", 0):.4f}']
    ]
    table = ax7.table(cellText=feature_summary, cellLoc='center', loc='center',
                     colWidths=[0.3, 0.7])
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 1.5)
    for i in range(2):
        table[(0, i)].set_facecolor('#3498DB')
        table[(0, i)].set_text_props(weight='bold', color='white')
    ax7.set_title('Complete Feature Summary', fontweight='bold', fontsize=14)
    
    output_path = os.path.join(output_dir, "combined_analysis_visualization.png")
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    return output_path

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Visualize OCR Analysis Data')
    parser.add_argument('report_path', help='Path to ocr_report.json')
    parser.add_argument('--output', '-o', help='Output directory for visualizations')
    
    args = parser.parse_args()
    
    # Load report
    report_data = load_report(args.report_path)
    
    # Determine output directory
    if args.output:
        output_dir = args.output
    else:
        report_dir = os.path.dirname(args.report_path)
        output_dir = os.path.join(report_dir, "04_analysis_visualization")
    
    os.makedirs(output_dir, exist_ok=True)
    
    print("Generating visualizations...")
    
    # Generate visualizations
    pattern_path = visualize_pattern_matching(report_data, output_dir)
    print(f"✓ Pattern matching visualization: {pattern_path}")
    
    feature_path = visualize_feature_extraction(report_data, output_dir)
    print(f"✓ Feature extraction visualization: {feature_path}")
    
    combined_path = visualize_combined_analysis(report_data, output_dir)
    print(f"✓ Combined analysis visualization: {combined_path}")
    
    print(f"\nAll visualizations saved to: {output_dir}")

if __name__ == "__main__":
    main()
