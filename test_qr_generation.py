#!/usr/bin/env python3
"""
Test script to demonstrate enhanced QR code generation with different languages.
"""

import base64
from pathlib import Path
from database import SessionLocal
from services.provider_service import generate_enhanced_qr_code_base64

def test_qr_generation():
    """Test QR generation with multiple languages."""
    db = SessionLocal()
    
    test_cases = [
        {
            'url': 'https://nevumo.com/p/ivan-petrov',
            'business_name': 'Ремонт на климатици',
            'service_name': 'Климатичен сервис',
            'language': 'bg',
            'filename': 'test-qr-bg.png'
        },
        {
            'url': 'https://nevumo.com/p/john-smith',
            'business_name': 'AC Repair',
            'service_name': 'Air Conditioning Service',
            'language': 'en',
            'filename': 'test-qr-en.png'
        },
        {
            'url': 'https://nevumo.com/p/hans-mueller',
            'business_name': 'Klimareparatur',
            'service_name': 'Klima Service',
            'language': 'de',
            'filename': 'test-qr-de.png'
        }
    ]
    
    try:
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n🔄 Test case {i}: {test_case['language']}")
            print(f"   Business: {test_case['business_name']}")
            print(f"   Service: {test_case['service_name']}")
            
            # Generate QR code
            qr_data_uri = generate_enhanced_qr_code_base64(
                url=test_case['url'],
                business_name=test_case['business_name'],
                service_name=test_case['service_name'],
                language=test_case['language'],
                db=db
            )
            
            # Save to file
            header, encoded = qr_data_uri.split(',', 1)
            binary_data = base64.b64decode(encoded)
            
            output_path = Path(test_case['filename'])
            with open(output_path, 'wb') as f:
                f.write(binary_data)
            
            file_size = output_path.stat().st_size
            print(f"   ✅ Generated: {test_case['filename']} ({file_size:,} bytes)")
            
        print(f"\n🎉 All test cases completed successfully!")
        print("📁 QR code files saved in current directory")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    test_qr_generation()
