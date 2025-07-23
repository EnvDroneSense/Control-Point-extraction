# GCP Control Point Filter

A Python GUI application for filtering Ground Control Point (GCP) data based on control points. This tool helps process drone survey data by matching real-world coordinates between GCP data files and control point lists.

## Features

- **Simple GUI Interface**: Easy-to-use tkinter-based interface with file pickers
- **Coordinate Matching**: Filters GCP data by matching X, Y, Z coordinates with configurable tolerance
- **File Format Support**: Handles tab-delimited files with CRS headers
- **Statistics Display**: Shows detailed statistics including pictures per control point
- **Error Handling**: Robust error handling for file operations and data processing

## Requirements

- Python 3.6 or higher
- tkinter (usually included with Python)
- Standard library modules: os, typing, collections

## Usage

1. **Run the application**:
   ```bash
   python gcp_filter.py
   ```

2. **Select input files**:
   - **GCP Data File**: Contains GCP data with real-world coordinates, pixel coordinates, and image filenames
   - **Control Points File**: Lists control points to filter by (X, Y, Z coordinates)

3. **Configure settings**:
   - Set coordinate tolerance (default: 0.001 meters)
   - Choose output file location

4. **Run the filter**: Click "Run Filter" to process the files

## File Formats

### GCP Data File (e.g., marker_40m_converted.txt)
```
+proj=sterea +lat_0=52.1561605555556 +lon_0=5.38763888888889 +k=0.9999079 +x_0=155000 +y_0=463000 +ellps=bessel +units=m +no_defs +type=crs
72432.195670000	451442.083300000	3.309333333	4643.098140	1133.228880	DJI_20250717132308_0057_D.JPG
72432.195670000	451442.083300000	3.309333333	4588.871580	2346.470460	DJI_20250717132310_0058_D.JPG
...
```

### Control Points File (e.g., CP_data.txt)
```
+proj=sterea +lat_0=52.1561605555556 +lon_0=5.38763888888889 +k=0.9999079 +x_0=155000 +y_0=463000 +ellps=bessel +units=m +no_defs +type=crs
72432.195670000	451442.083300000	3.309333333	gcp1
72366.773670000	451500.445000000	7.224000000	gcp2
...
```

### Output File
The output file contains only the rows from the GCP data file where coordinates match the control points, preserving the original CRS header and format.

## Features Explained

### Coordinate Matching
- Compares X, Y, Z coordinates between files
- Uses configurable tolerance (default ±0.001m) to handle floating-point precision
- Matches coordinates within the specified tolerance range

### Statistics
The application provides detailed statistics including:
- Number of matched control points vs. total requested
- Pictures per control point (minimum, maximum, average)
- Detailed breakdown showing coordinates and picture count for each matched control point

### Error Handling
- Validates file existence and readability
- Handles invalid coordinate data gracefully
- Provides clear error messages and warnings
- Logs all operations for debugging

## Example Output
```
✅ Filter completed successfully!
Matched 42 rows from 100 total GCP data rows
Matched data saved to: marker_CP.txt

--- STATISTICS ---
Control Points matched: 15/20
Pictures per control point:
  • Minimum: 1
  • Maximum: 8
  • Average: 2.8

Detailed breakdown:
  CP1 (72432.196, 451442.083, 3.309): 4 pictures
  CP2 (72366.774, 451500.445, 7.224): 3 pictures
  ...
```

## Troubleshooting

### Common Issues

1. **File format errors**: Ensure files are tab-delimited with proper CRS headers
2. **Coordinate parsing errors**: Check that coordinate columns contain valid numeric data
3. **No matches found**: Verify coordinate values and increase tolerance if needed
4. **Memory issues**: For very large files, consider splitting the data

### File Format Requirements

- Files must be tab-delimited (not space or comma-delimited)
- First line must contain the CRS header
- Coordinate columns must contain valid floating-point numbers
- At least 3 columns required for X, Y, Z coordinates

## License

This project is open source and available under the MIT License.
