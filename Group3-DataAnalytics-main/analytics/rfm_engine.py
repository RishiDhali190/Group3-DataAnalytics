"""
RFM Analysis Engine for Consumer360
Calculates Recency, Frequency, Monetary scores and customer segments
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import psycopg2
from psycopg2.extras import execute_batch
import os
from dotenv import load_dotenv

load_dotenv()

class RFMEngine:
    """RFM Analysis Engine"""
    
    def __init__(self, db_config=None):
        """Initialize RFM Engine with database configuration"""
        self.db_config = db_config or {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', 5432),
            'database': os.getenv('DB_NAME', 'consumer360_db'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', '')
        }
        self.analysis_date = datetime.now()
        
    def connect_db(self):
        """Create database connection"""
        return psycopg2.connect(**self.db_config)
    
    def fetch_transaction_data(self):
        """Fetch transaction data from database"""
        query = """
        SELECT 
            c.customer_id,
            c.customer_code,
            f.transaction_timestamp,
            f.total_amount
        FROM fact_sales f
        JOIN dim_customer c ON f.customer_id = c.customer_id
        WHERE c.customer_status = 'Active'
        ORDER BY f.transaction_timestamp
        """
        
        conn = self.connect_db()
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df
    
    def calculate_rfm(self, df, analysis_date=None):
        """
        Calculate RFM metrics for each customer
        
        Parameters:
        - df: DataFrame with columns [customer_id, transaction_timestamp, total_amount]
        - analysis_date: Reference date for recency calculation (default: today)
        
        Returns:
        - DataFrame with RFM scores
        """
        if analysis_date is None:
            analysis_date = self.analysis_date
        
        # Convert transaction_timestamp to datetime
        df['transaction_timestamp'] = pd.to_datetime(df['transaction_timestamp'])
        
        # Calculate RFM metrics
        rfm = df.groupby('customer_id').agg({
            'transaction_timestamp': lambda x: (analysis_date - x.max()).days,  # Recency
            'customer_code': 'count',  # Frequency
            'total_amount': 'sum'  # Monetary
        }).reset_index()
        
        rfm.columns = ['customer_id', 'recency_days', 'frequency', 'monetary']
        
        # Calculate RFM scores (1-5 scale using quintiles)
        rfm['recency_score'] = pd.qcut(rfm['recency_days'], q=5, labels=[5, 4, 3, 2, 1], duplicates='drop')
        rfm['frequency_score'] = pd.qcut(rfm['frequency'], q=5, labels=[1, 2, 3, 4, 5], duplicates='drop')
        rfm['monetary_score'] = pd.qcut(rfm['monetary'], q=5, labels=[1, 2, 3, 4, 5], duplicates='drop')
        
        # Convert to numeric
        rfm['recency_score'] = rfm['recency_score'].astype(int)
        rfm['frequency_score'] = rfm['frequency_score'].astype(int)
        rfm['monetary_score'] = rfm['monetary_score'].astype(int)
        
        # Calculate overall RFM score (average of R, F, M)
        rfm['rfm_score'] = round((rfm['recency_score'] + rfm['frequency_score'] + rfm['monetary_score']) / 3, 2)
        
        # Assign segments based on RFM score
        rfm['segment'] = rfm['rfm_score'].apply(self.assign_segment)
        
        return rfm
    
    def assign_segment(self, rfm_score):
        """Assign customer segment based on RFM score"""
        if rfm_score >= 4.5:
            return 'Champions'
        elif rfm_score >= 4.0:
            return 'Loyal Customers'
        elif rfm_score >= 3.5:
            return 'Potential Loyalists'
        elif rfm_score >= 3.0:
            return 'New Customers'
        elif rfm_score >= 2.5:
            return 'Promising'
        elif rfm_score >= 2.0:
            return 'Hibernating'
        elif rfm_score >= 1.5:
            return 'At Risk'
        else:
            return 'Lost'
    
    def save_rfm_scores(self, rfm_df):
        """Save RFM scores to database"""
        conn = self.connect_db()
        cursor = conn.cursor()
        
        # Prepare data for insertion
        records = []
        for _, row in rfm_df.iterrows():
            records.append((
                int(row['customer_id']),
                int(row['recency_days']),
                int(row['frequency']),
                float(row['monetary']),
                int(row['recency_score']),
                int(row['frequency_score']),
                int(row['monetary_score']),
                float(row['rfm_score']),
                row['segment'],
                self.analysis_date
            ))
        
        # Insert query
        insert_query = """
        INSERT INTO rfm_scores 
        (customer_id, recency_days, frequency, monetary, recency_score, 
         frequency_score, monetary_score, rfm_score, segment, calculated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        execute_batch(cursor, insert_query, records, page_size=1000)
        conn.commit()
        
        cursor.close()
        conn.close()
        
        print(f"✅ Saved {len(records)} RFM scores to database")
    
    def get_segment_summary(self, rfm_df):
        """Generate segment summary statistics"""
        summary = rfm_df.groupby('segment').agg({
            'customer_id': 'count',
            'rfm_score': 'mean',
            'monetary': ['sum', 'mean'],
            'frequency': 'mean'
        }).reset_index()
        
        summary.columns = ['segment', 'customer_count', 'avg_rfm_score', 
                          'total_revenue', 'avg_revenue', 'avg_frequency']
        
        # Calculate revenue percentage
        summary['revenue_pct'] = (summary['total_revenue'] / summary['total_revenue'].sum() * 100).round(2)
        
        # Sort by priority
        segment_order = ['Champions', 'Loyal Customers', 'Potential Loyalists', 
                        'New Customers', 'Promising', 'Hibernating', 'At Risk', 'Lost']
        summary['segment'] = pd.Categorical(summary['segment'], categories=segment_order, ordered=True)
        summary = summary.sort_values('segment')
        
        return summary
    
    def run_analysis(self):
        """Run complete RFM analysis"""
        print("🚀 Starting RFM Analysis...")
        print(f"📅 Analysis Date: {self.analysis_date.strftime('%Y-%m-%d')}")
        
        # Fetch data
        print("📊 Fetching transaction data...")
        df = self.fetch_transaction_data()
        print(f"✅ Loaded {len(df)} transactions for {df['customer_id'].nunique()} customers")
        
        # Calculate RFM
        print("🔢 Calculating RFM scores...")
        rfm_df = self.calculate_rfm(df)
        print(f"✅ Calculated RFM scores for {len(rfm_df)} customers")
        
        # Save to database
        print("💾 Saving RFM scores to database...")
        self.save_rfm_scores(rfm_df)
        
        # Generate summary
        print("\n📈 Segment Summary:")
        summary = self.get_segment_summary(rfm_df)
        print(summary.to_string(index=False))
        
        print("\n✨ RFM Analysis Complete!")
        
        return rfm_df, summary


def main():
    """Main execution function"""
    engine = RFMEngine()
    rfm_df, summary = engine.run_analysis()
    
    # Save to CSV for reference
    rfm_df.to_csv('rfm_scores_output.csv', index=False)
    summary.to_csv('segment_summary_output.csv', index=False)
    print("\n📁 Results saved to: rfm_scores_output.csv, segment_summary_output.csv")


if __name__ == '__main__':
    main()
