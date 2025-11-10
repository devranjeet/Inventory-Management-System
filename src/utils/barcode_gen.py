"""
Barcode Utility Module
"""
import barcode
from barcode.writer import ImageWriter
import os


class BarcodeGenerator:
    @staticmethod
    def generate_barcode(data, barcode_type='code128', output_path='reports/barcodes'):
        """
        Generate barcode image
        barcode_type: code128, code39, ean13, etc.
        """
        try:
            os.makedirs(output_path, exist_ok=True)
            
            # Get barcode class
            barcode_class = barcode.get_barcode_class(barcode_type)
            
            # Generate barcode
            barcode_instance = barcode_class(data, writer=ImageWriter())
            
            # Save barcode
            filename = os.path.join(output_path, f'{data}')
            filepath = barcode_instance.save(filename)
            
            return filepath
        except Exception as e:
            print(f"Error generating barcode: {e}")
            return None
    
    @staticmethod
    def generate_product_barcode(product_sku):
        """Generate barcode for a product using its SKU"""
        return BarcodeGenerator.generate_barcode(product_sku)
