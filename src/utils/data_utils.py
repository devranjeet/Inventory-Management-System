"""
Data Export and Import Utilities
"""
import pandas as pd
import os
from datetime import datetime


class DataExporter:
    @staticmethod
    def export_to_csv(data, columns, filename, output_path='reports'):
        """Export data to CSV file"""
        try:
            os.makedirs(output_path, exist_ok=True)
            
            # Convert data to list of dicts
            rows = []
            for row in data:
                row_dict = {}
                for col in columns:
                    row_dict[col] = row[col] if col in row.keys() else ''
                rows.append(row_dict)
            
            # Create DataFrame
            df = pd.DataFrame(rows)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filepath = os.path.join(output_path, f'{filename}_{timestamp}.csv')
            
            # Export to CSV
            df.to_csv(filepath, index=False)
            
            return filepath
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return None
    
    @staticmethod
    def export_to_excel(data, columns, filename, output_path='reports'):
        """Export data to Excel file"""
        try:
            os.makedirs(output_path, exist_ok=True)
            
            # Convert data to list of dicts
            rows = []
            for row in data:
                row_dict = {}
                for col in columns:
                    row_dict[col] = row[col] if col in row.keys() else ''
                rows.append(row_dict)
            
            # Create DataFrame
            df = pd.DataFrame(rows)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filepath = os.path.join(output_path, f'{filename}_{timestamp}.xlsx')
            
            # Export to Excel
            df.to_excel(filepath, index=False, engine='openpyxl')
            
            return filepath
        except Exception as e:
            print(f"Error exporting to Excel: {e}")
            return None


class DataImporter:
    @staticmethod
    def import_from_csv(filepath):
        """Import data from CSV file"""
        try:
            df = pd.read_csv(filepath)
            return df.to_dict('records')
        except Exception as e:
            print(f"Error importing from CSV: {e}")
            return None
    
    @staticmethod
    def import_from_excel(filepath):
        """Import data from Excel file"""
        try:
            df = pd.read_excel(filepath, engine='openpyxl')
            return df.to_dict('records')
        except Exception as e:
            print(f"Error importing from Excel: {e}")
            return None
    
    @staticmethod
    def validate_product_import(data):
        """Validate product import data"""
        required_fields = ['product_name', 'unit_price', 'selling_price']
        
        valid_rows = []
        errors = []
        
        for idx, row in enumerate(data):
            # Check required fields
            missing_fields = [field for field in required_fields if field not in row or not row[field]]
            
            if missing_fields:
                errors.append(f"Row {idx + 1}: Missing required fields: {', '.join(missing_fields)}")
                continue
            
            # Validate numeric fields
            try:
                row['unit_price'] = float(row['unit_price'])
                row['selling_price'] = float(row['selling_price'])
                
                if 'stock_quantity' in row and row['stock_quantity']:
                    row['stock_quantity'] = int(row['stock_quantity'])
                else:
                    row['stock_quantity'] = 0
                
                if 'min_stock_level' in row and row['min_stock_level']:
                    row['min_stock_level'] = int(row['min_stock_level'])
                else:
                    row['min_stock_level'] = 10
                
                valid_rows.append(row)
            except ValueError as e:
                errors.append(f"Row {idx + 1}: Invalid numeric value - {str(e)}")
                continue
        
        return valid_rows, errors
