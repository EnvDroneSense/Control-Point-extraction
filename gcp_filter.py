#!/usr/bin/env python3
"""
GCP Control Point Filter

A GUI application to filter Ground Control Point (GCP) data based on control points.
Matches real-world coordinates (X, Y, Z) from two input files with floating-point tolerance.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
from typing import List, Tuple, Dict, Set
from collections import defaultdict


class GCPFilter:
    def __init__(self, root):
        self.root = root
        self.root.title("GCP Control Point Filter")
        self.root.geometry("800x600")
        
        # Variables for file paths
        self.file1_path = tk.StringVar()
        self.file2_path = tk.StringVar()
        self.output_path = tk.StringVar()
        
        # Tolerance for coordinate matching (in meters)
        self.tolerance = tk.DoubleVar(value=0.001)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # File selection section
        ttk.Label(main_frame, text="File Selection", font=("Arial", 12, "bold")).grid(
            row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 10)
        )
        
        # File 1 (GCP data)
        ttk.Label(main_frame, text="GCP Data File:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(main_frame, textvariable=self.file1_path, width=60).grid(
            row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=2
        )
        ttk.Button(main_frame, text="Browse", command=self.browse_file1).grid(
            row=1, column=2, pady=2
        )
        
        # File 2 (Control points)
        ttk.Label(main_frame, text="Control Points File:").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(main_frame, textvariable=self.file2_path, width=60).grid(
            row=2, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=2
        )
        ttk.Button(main_frame, text="Browse", command=self.browse_file2).grid(
            row=2, column=2, pady=2
        )
        
        # Output file
        ttk.Label(main_frame, text="Output File:").grid(row=3, column=0, sticky=tk.W, pady=2)
        ttk.Entry(main_frame, textvariable=self.output_path, width=60).grid(
            row=3, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=2
        )
        ttk.Button(main_frame, text="Browse", command=self.browse_output).grid(
            row=3, column=2, pady=2
        )
        
        # Tolerance setting
        ttk.Label(main_frame, text="Coordinate Tolerance (m):").grid(row=4, column=0, sticky=tk.W, pady=(10, 2))
        tolerance_frame = ttk.Frame(main_frame)
        tolerance_frame.grid(row=4, column=1, sticky=tk.W, padx=(5, 5), pady=(10, 2))
        ttk.Entry(tolerance_frame, textvariable=self.tolerance, width=10).pack(side=tk.LEFT)
        ttk.Label(tolerance_frame, text="meters").pack(side=tk.LEFT, padx=(5, 0))
        
        # Run button
        ttk.Button(main_frame, text="Run Filter", command=self.run_filter, 
                  style="Accent.TButton").grid(
            row=5, column=1, pady=(20, 10), sticky=tk.W
        )
        
        # Status and results section
        ttk.Label(main_frame, text="Status & Results", font=("Arial", 12, "bold")).grid(
            row=6, column=0, columnspan=3, sticky=tk.W, pady=(20, 10)
        )
        
        # Status log
        self.status_log = scrolledtext.ScrolledText(main_frame, height=15, width=80)
        self.status_log.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Configure grid weights for resizing
        main_frame.rowconfigure(7, weight=1)
        
        # Initialize status log
        self.log_message("Ready to process GCP data files.")
        
    def browse_file1(self):
        """Browse for GCP data file"""
        filename = filedialog.askopenfilename(
            title="Select GCP Data File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.file1_path.set(filename)
            self.log_message(f"Selected GCP data file: {os.path.basename(filename)}")
            
    def browse_file2(self):
        """Browse for control points file"""
        filename = filedialog.askopenfilename(
            title="Select Control Points File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.file2_path.set(filename)
            self.log_message(f"Selected control points file: {os.path.basename(filename)}")
            
    def browse_output(self):
        """Browse for output file location"""
        filename = filedialog.asksaveasfilename(
            title="Save Filtered Data As",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.output_path.set(filename)
            self.log_message(f"Output will be saved to: {os.path.basename(filename)}")
            
    def log_message(self, message: str):
        """Add a message to the status log"""
        self.status_log.insert(tk.END, f"{message}\n")
        self.status_log.see(tk.END)
        self.root.update_idletasks()
        
    def read_file_with_crs(self, filepath: str) -> Tuple[str, List[List[str]]]:
        """
        Read a tab-delimited file with CRS header
        Returns: (crs_header, data_rows)
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            if not lines:
                raise ValueError("File is empty")
                
            # First line is CRS header
            crs_header = lines[0].strip()
            
            # Parse data rows (skip empty lines)
            data_rows = []
            for line in lines[1:]:
                line = line.strip()
                if line:
                    data_rows.append(line.split('\t'))
                    
            return crs_header, data_rows
            
        except Exception as e:
            raise Exception(f"Error reading file {filepath}: {str(e)}")
            
    def coordinates_match(self, coord1: Tuple[float, float, float], 
                         coord2: Tuple[float, float, float]) -> bool:
        """
        Check if two coordinate tuples match within tolerance
        """
        tolerance = self.tolerance.get()
        return (abs(coord1[0] - coord2[0]) <= tolerance and
                abs(coord1[1] - coord2[1]) <= tolerance and
                abs(coord1[2] - coord2[2]) <= tolerance)
                
    def parse_coordinates(self, row: List[str], coord_indices: Tuple[int, int, int]) -> Tuple[float, float, float]:
        """
        Parse coordinates from a data row
        """
        try:
            x = float(row[coord_indices[0]])
            y = float(row[coord_indices[1]])
            z = float(row[coord_indices[2]])
            return (x, y, z)
        except (ValueError, IndexError) as e:
            raise ValueError(f"Error parsing coordinates: {str(e)}")
            
    def run_filter(self):
        """Main filtering process"""
        try:
            # Validate input files
            if not self.file1_path.get() or not os.path.exists(self.file1_path.get()):
                messagebox.showerror("Error", "Please select a valid GCP data file")
                return
                
            if not self.file2_path.get() or not os.path.exists(self.file2_path.get()):
                messagebox.showerror("Error", "Please select a valid control points file")
                return
                
            if not self.output_path.get():
                messagebox.showerror("Error", "Please specify an output file path")
                return
                
            self.log_message("Starting filter process...")
            
            # Read input files
            self.log_message("Reading GCP data file...")
            crs_header1, gcp_data = self.read_file_with_crs(self.file1_path.get())
            self.log_message(f"Loaded {len(gcp_data)} GCP data rows")
            
            self.log_message("Reading control points file...")
            crs_header2, cp_data = self.read_file_with_crs(self.file2_path.get())
            self.log_message(f"Loaded {len(cp_data)} control point rows")
            
            # Parse control points coordinates (assume first 3 columns are X, Y, Z)
            control_points = set()
            for row in cp_data:
                if len(row) >= 3:
                    try:
                        coords = self.parse_coordinates(row, (0, 1, 2))
                        control_points.add(coords)
                    except ValueError as e:
                        self.log_message(f"Warning: Skipping invalid control point row: {e}")
                        
            self.log_message(f"Parsed {len(control_points)} unique control points")
            
            # Filter GCP data
            self.log_message("Filtering GCP data...")
            matched_rows = []
            match_stats = defaultdict(list)  # For statistics
            
            for row in gcp_data:
                if len(row) >= 3:
                    try:
                        # Assume first 3 columns are X, Y, Z coordinates
                        gcp_coords = self.parse_coordinates(row, (0, 1, 2))
                        
                        # Check if this GCP matches any control point
                        for cp_coords in control_points:
                            if self.coordinates_match(gcp_coords, cp_coords):
                                matched_rows.append(row)
                                # Track statistics
                                if len(row) >= 6:  # Assuming image filename is in column 5 (0-indexed)
                                    image_name = row[5] if len(row) > 5 else "unknown"
                                    match_stats[cp_coords].append(image_name)
                                break
                    except ValueError as e:
                        self.log_message(f"Warning: Skipping invalid GCP row: {e}")
                        
            # Write output file
            self.log_message("Writing output file...")
            with open(self.output_path.get(), 'w', encoding='utf-8') as f:
                f.write(crs_header1 + '\n')
                for row in matched_rows:
                    f.write('\t'.join(row) + '\n')
                    
            # Display results and statistics
            self.log_message(f"✅ Filter completed successfully!")
            self.log_message(f"Matched {len(matched_rows)} rows from {len(gcp_data)} total GCP data rows")
            self.log_message(f"Matched data saved to: {self.output_path.get()}")
            
            # Display detailed statistics
            self.log_message("\n--- STATISTICS ---")
            if match_stats:
                total_matched_cps = len(match_stats)
                total_requested_cps = len(control_points)
                
                self.log_message(f"Control Points matched: {total_matched_cps}/{total_requested_cps}")
                
                # Pictures per control point statistics
                pics_per_cp = [len(images) for images in match_stats.values()]
                if pics_per_cp:
                    min_pics = min(pics_per_cp)
                    max_pics = max(pics_per_cp)
                    avg_pics = sum(pics_per_cp) / len(pics_per_cp)
                    
                    self.log_message(f"Pictures per control point:")
                    self.log_message(f"  • Minimum: {min_pics}")
                    self.log_message(f"  • Maximum: {max_pics}")
                    self.log_message(f"  • Average: {avg_pics:.1f}")
                    
                    # Detailed breakdown
                    self.log_message("\nDetailed breakdown:")
                    for i, (cp_coords, images) in enumerate(match_stats.items(), 1):
                        self.log_message(f"  CP{i} ({cp_coords[0]:.3f}, {cp_coords[1]:.3f}, {cp_coords[2]:.3f}): {len(images)} pictures")
            else:
                self.log_message("No control points were matched!")
                
            messagebox.showinfo("Success", f"Filter completed!\nMatched {len(matched_rows)} rows.\nSaved to: {os.path.basename(self.output_path.get())}")
            
        except Exception as e:
            error_msg = f"Error during filtering: {str(e)}"
            self.log_message(f"❌ {error_msg}")
            messagebox.showerror("Error", error_msg)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = GCPFilter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
