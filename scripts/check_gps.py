import pandas as pd

def check_gps_coordinates(file_path):
    """
    ฟังก์ชันสำหรับอ่านและตรวจสอบความถูกต้องของพิกัด GPS ในประเทศไทย
    """
    print(f"--- เริ่มต้นตรวจสอบไฟล์: {file_path} ---")
    
    try:
        # 1. อ่านไฟล์ CSV
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการเปิดไฟล์: {e}")
        return

    # 2. ตรวจสอบชื่อคอลัมน์ (ปรับชื่อตามไฟล์ของคุณได้ เช่น 'X', 'Y' หรือ 'Lat', 'Long')
    lat_col = 'Latitude'
    lon_col = 'Longitude'

    if lat_col not in df.columns or lon_col not in df.columns:
        print(f"❌ Error: ไม่พบคอลัมน์ '{lat_col}' หรือ '{lon_col}' ในไฟล์")
        return

    # 3. ตรวจสอบค่าว่าง (Missing Values)
    missing_data = df[df[lat_col].isna() | df[lon_col].isna()]
    if not missing_data.empty:
        print(f"⚠️ เตือน: พบพิกัดว่างเปล่า (NaN) จำนวน {len(missing_data)} รายการ")
    else:
        print("✅ ไม่พบข้อมูลพิกัดว่างเปล่า")

    # 4. ตรวจสอบพิกัดที่หลุดขอบเขตประเทศไทย
    # (Lat: 5.5 - 20.5, Long: 97.3 - 105.7)
    invalid_lat = (df[lat_col] < 5.5) | (df[lat_col] > 20.5)
    invalid_lon = (df[lon_col] < 97.3) | (df[lon_col] > 105.7)

    out_of_bounds = df[invalid_lat | invalid_lon]

    if not out_of_bounds.empty:
        print(f"❌ พบพิกัดหลุดนอกเขตประเทศไทย จำนวน {len(out_of_bounds)} จุด ดังนี้:")
        print(out_of_bounds[[lat_col, lon_col]])
    else:
        print("✅ พิกัดทั้งหมดถูกต้องและอยู่ในเขตประเทศไทย!")

    print("--- ตรวจสอบเสร็จสิ้น ---")

# --- ส่วนของการเรียกใช้งานสคริปต์ ---
if __name__ == "__main__":
    # ระบุพาธไฟล์ตัวอย่างพิกัดที่คุณต้องการตรวจ (เช่น ไฟล์ในโฟลเดอร์ data/)
    sample_file = "../data/gps_sample.csv" 
    check_gps_coordinates(sample_file)
