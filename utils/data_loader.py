"""
Data Loading Utilities
SIH PS1 - Cybersecurity Threat Detector
"""
import json
import csv
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional

class DataLoader:
    """Data loading and management utilities"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"
        
        # Create directories if they don't exist
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
    
    def load_json(self, filename: str, from_raw: bool = True) -> Optional[Dict]:
        """Load JSON data"""
        try:
            data_path = self.raw_dir if from_raw else self.processed_dir
            file_path = data_path / filename
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"File not found: {filename}")
            return None
        except json.JSONDecodeError:
            print(f"Invalid JSON format: {filename}")
            return None
    
    def save_json(self, data: Dict, filename: str, to_processed: bool = True) -> bool:
        """Save data as JSON"""
        try:
            data_path = self.processed_dir if to_processed else self.raw_dir
            file_path = data_path / filename
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving JSON: {e}")
            return False
    
    def load_csv(self, filename: str, from_raw: bool = True) -> Optional[pd.DataFrame]:
        """Load CSV data as pandas DataFrame"""
        try:
            data_path = self.raw_dir if from_raw else self.processed_dir
            file_path = data_path / filename
            
            return pd.read_csv(file_path)
        except FileNotFoundError:
            print(f"File not found: {filename}")
            return None
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return None
    
    def save_csv(self, df: pd.DataFrame, filename: str, to_processed: bool = True) -> bool:
        """Save DataFrame as CSV"""
        try:
            data_path = self.processed_dir if to_processed else self.raw_dir
            file_path = data_path / filename
            
            df.to_csv(file_path, index=False)
            return True
        except Exception as e:
            print(f"Error saving CSV: {e}")
            return False
    
    def load_sample_data(self) -> Dict:
        """Load sample threat data"""
        sample_data = self.load_json("sample_threats.json")
        
        if sample_data is None:
            # Create default sample data
            sample_data = {
                "phishing_samples": [
                    {
                        "text": "URGENT: Your account will be suspended! Click here to verify immediately.",
                        "label": "phishing",
                        "risk_score": 0.9
                    },
                    {
                        "text": "Thank you for your purchase. Your order will arrive soon.",
                        "label": "safe",
                        "risk_score": 0.1
                    }
                ],
                "url_samples": [
                    {
                        "url": "http://192.168.1.1/login",
                        "label": "suspicious",
                        "risk_score": 0.7
                    },
                    {
                        "url": "https://amazon.com/orders",
                        "label": "safe",
                        "risk_score": 0.05
                    }
                ]
            }
            
            # Save default data
            self.save_json(sample_data, "sample_threats.json", to_processed=False)
        
        return sample_data
    
    def get_training_data(self) -> Optional[pd.DataFrame]:
        """Get training data for model development"""
        # Try to load existing training data
        df = self.load_csv("training_data.csv")
        
        if df is None:
            # Create training data from samples
            sample_data = self.load_sample_data()
            
            training_records = []
            
            # Add text samples
            for sample in sample_data.get("phishing_samples", []):
                training_records.append({
                    'content': sample['text'],
                    'type': 'text',
                    'label': sample['label'],
                    'risk_score': sample['risk_score']
                })
            
            # Add URL samples
            for sample in sample_data.get("url_samples", []):
                training_records.append({
                    'content': sample['url'],
                    'type': 'url',
                    'label': sample['label'],
                    'risk_score': sample['risk_score']
                })
            
            df = pd.DataFrame(training_records)
            
            # Save training data
            self.save_csv(df, "training_data.csv")
        
        return df
    
    def add_training_sample(self, content: str, content_type: str, 
                          label: str, risk_score: float) -> bool:
        """Add new training sample"""
        try:
            df = self.get_training_data()
            
            new_sample = pd.DataFrame([{
                'content': content,
                'type': content_type,
                'label': label,
                'risk_score': risk_score
            }])
            
            df = pd.concat([df, new_sample], ignore_index=True)
            
            return self.save_csv(df, "training_data.csv")
        except Exception as e:
            print(f"Error adding training sample: {e}")
            return False
    
    def get_data_stats(self) -> Dict:
        """Get statistics about loaded data"""
        df = self.get_training_data()
        
        if df is None:
            return {"error": "No data available"}
        
        return {
            "total_samples": len(df),
            "text_samples": len(df[df['type'] == 'text']),
            "url_samples": len(df[df['type'] == 'url']),
            "phishing_samples": len(df[df['label'] == 'phishing']),
            "safe_samples": len(df[df['label'] == 'safe']),
            "suspicious_samples": len(df[df['label'] == 'suspicious']),
            "avg_risk_score": df['risk_score'].mean()
        }
