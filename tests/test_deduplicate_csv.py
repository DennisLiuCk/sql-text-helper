import unittest
import os
import tempfile
import pandas as pd
from deduplicate_csv import deduplicate_csv

class TestDeduplicateCsv(unittest.TestCase):
    def setUp(self):
        # Create temporary directories for test files
        self.test_dir = tempfile.mkdtemp()
        self.output_dir = os.path.join(self.test_dir, "output")
        os.makedirs(self.output_dir, exist_ok=True)
    
    def tearDown(self):
        # Clean up temporary files and directories
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.test_dir)
    
    def create_test_csv(self, content):
        """Helper method to create test CSV files"""
        filepath = os.path.join(self.test_dir, "test.csv")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filepath
    
    def test_basic_deduplication(self):
        """Test basic deduplication of rows"""
        csv_content = """STORE_SKU_ID,PRODUCT_CAT_CODE,ONLINE_STATUS
C0001,AA123,ONLINE
C0001,AA123,ONLINE
C0002,BB456,ONLINE
C0002,BB456,ONLINE"""
        
        input_file = self.create_test_csv(csv_content)
        output_file = deduplicate_csv(input_file, self.output_dir)
        
        # Read the output file
        df = pd.read_csv(output_file)
        
        # Verify results
        self.assertEqual(len(df), 2)  # Should have 2 unique rows
        self.assertEqual(df['STORE_SKU_ID'].tolist(), ['C0001', 'C0002'])
    
    def test_no_duplicates(self):
        """Test behavior when there are no duplicates"""
        csv_content = """STORE_SKU_ID,PRODUCT_CAT_CODE,ONLINE_STATUS
C0001,AA123,ONLINE
C0002,BB456,ONLINE"""
        
        input_file = self.create_test_csv(csv_content)
        output_file = deduplicate_csv(input_file, self.output_dir)
        
        # Read the output file
        df = pd.read_csv(output_file)
        
        # Verify results
        self.assertEqual(len(df), 2)  # Should still have 2 rows
        self.assertEqual(df['STORE_SKU_ID'].tolist(), ['C0001', 'C0002'])
    
    def test_empty_file(self):
        """Test behavior with empty file (only header)"""
        csv_content = "STORE_SKU_ID,PRODUCT_CAT_CODE,ONLINE_STATUS"
        
        input_file = self.create_test_csv(csv_content)
        output_file = deduplicate_csv(input_file, self.output_dir)
        
        # Read the output file
        df = pd.read_csv(output_file)
        
        # Verify results
        self.assertEqual(len(df), 0)  # Should have no data rows
    
    def test_multiple_duplicates(self):
        """Test with multiple duplicate rows"""
        csv_content = """STORE_SKU_ID,PRODUCT_CAT_CODE,ONLINE_STATUS
C0001,AA123,ONLINE
C0001,AA123,ONLINE
C0001,AA123,ONLINE
C0002,BB456,ONLINE
C0002,BB456,ONLINE"""
        
        input_file = self.create_test_csv(csv_content)
        output_file = deduplicate_csv(input_file, self.output_dir)
        
        # Read the output file
        df = pd.read_csv(output_file)
        
        # Verify results
        self.assertEqual(len(df), 2)  # Should have 2 unique rows
        self.assertEqual(df['STORE_SKU_ID'].tolist(), ['C0001', 'C0002'])
    
    def test_output_directory_creation(self):
        """Test that output directory is created if it doesn't exist"""
        csv_content = """STORE_SKU_ID,PRODUCT_CAT_CODE,ONLINE_STATUS
C0001,AA123,ONLINE"""
        
        input_file = self.create_test_csv(csv_content)
        new_output_dir = os.path.join(self.test_dir, "new_output")
        
        # Verify directory doesn't exist
        self.assertFalse(os.path.exists(new_output_dir))
        
        # Run deduplication
        output_file = deduplicate_csv(input_file, new_output_dir)
        
        # Verify directory was created
        self.assertTrue(os.path.exists(new_output_dir))
        self.assertTrue(os.path.exists(output_file))

if __name__ == '__main__':
    unittest.main()
