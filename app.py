import streamlit as st
from datetime import date, timedelta

# ==========================================================
# Influencer WorkMate
# เว็บไซต์ช่วยจัดการงานและกำหนดส่งของอินฟลูเอ็นเซอร์
# ใช้ Python + Streamlit
# ==========================================================

st.set_page_config(
    page_title="Influencer WorkMate",
    page_icon="🎬",
    layout="wide"
)

# สถานะที่ผู้ใช้สามารถเลือกให้แต่ละงานได้
STATUSES = ["รอเริ่มงาน", "กำลังทำ", "รอแบรนด์อนุมัติ", "เสร็จแล้ว"]
PLATFORMS = ["TikTok", "Instagram", "YouTube", "Facebook", "อื่น ๆ"]

# เริ่มต้นข้อมูลใน session_state เมื่อเปิดแอปครั้งแรก
# ข้อมูลจะอยู่ระหว่างเซสชัน ไม่ใช่ฐานข้อมูลถาวร
if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {
            "id": 1,
            "brand": "Glow Skin",
            "title": "รีวิวเซรั่ม",
            "platform": "TikTok",
            "due_date": date.today() + timedelta(days=1),
            "fee": 3500.0,
            "status": "กำลังทำ",
            "notes": "ถ่ายคลิปและใส่คำบรรยาย"
        },
        {
            "id": 2,
            "brand": "Cafe Bloom",
            "title": "รีวิวคาเฟ่",
            "platform": "Instagram",
            "due_date": date.today() + timedelta(days=4),
            "fee": 2500.0,
            "status": "รอแบรนด์อนุมัติ",
            "notes": "รอแบรนด์ตรวจร่างโพสต์"
        },
        {
            "id": 3,
            "brand": "Daily Bag",
            "title": "ถ่ายวิดีโอสินค้า",
            "platform": "YouTube",
            "due_date": date.today() - timedelta(days=1),
            "fee": 5000.0,
            "status": "รอเริ่มงาน",
            "notes": "ติดต่อแบรนด์เพื่อยืนยันรายละเอียด"
        },
    ]

if "next_id" not in st.session_state:
    st.session_state.next_id = 4

# รูปแบบสีและการ์ดของเว็บไซต์
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #f8f6ff 0%, #ffffff 55%, #f7f5ff 100%);
}
.hero {
    background: linear-gradient(120deg, #e7ddff, #f8e8ff);
    border: 1px solid #ded0ff;
    padding: 1.4rem 1.6rem;
    border-radius: 22px;
    margin-bottom: 1rem;
}
.hero h1 { color: #39226d; margin: 0; }
.hero p { color: #67558c; margin: .35rem 0 0 0; }
div.stButton > button {
    border-radius: 11px;
    min-height: 2.6rem;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🎬 Influencer WorkMate</h1>
    <p>Creator Task & Deadline Manager — จัดการงานให้ทันทุกเดดไลน์</p>
</div>
""", unsafe_allow_html=True)

st.write("รวมงานจากทุกแบรนด์ไว้ในที่เดียว พร้อมตรวจสอบงานใกล้ส่งและงานที่เลยกำหนด")

# ----------------------------------------------------------
# ฟังก์ชันช่วยคำนวณสถานะกำหนดส่ง
# ----------------------------------------------------------
def get_deadline_label(task, today):
    """คืนข้อความสถานะกำหนดส่งจากวันครบกำหนดและสถานะงาน"""
    if task["status"] == "เสร็จแล้ว":
        return "เสร็จแล้ว"
    days_left = (task["due_date"] - today).days
    if days_left < 0:
        return "เลยกำหนด"
    elif days_left == 0:
        return "ครบกำหนดวันนี้"
    elif days_left <= 2:
        return "ใกล้ส่ง"
    else:
        return "ยังมีเวลา"

def format_deadline(task, today):
    """แสดงข้อความกำหนดส่งให้อ่านง่าย"""
    if task["status"] == "เสร็จแล้ว":
        return f"กำหนดส่ง {task['due_date'].strftime('%d/%m/%Y')} · ปิดงานแล้ว"
    days_left = (task["due_date"] - today).days
    if days_left < 0:
        return f"เลยกำหนดมาแล้ว {abs(days_left)} วัน"
    elif days_left == 0:
        return "ครบกำหนดวันนี้"
    elif days_left == 1:
        return "เหลืออีก 1 วัน"
    else:
        return f"เหลืออีก {days_left} วัน"

today = date.today()

# ----------------------------------------------------------
# แถบเพิ่มงาน
# ----------------------------------------------------------
with st.expander("➕ เพิ่มงานจากแบรนด์", expanded=False):
    with st.form("add_task_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            brand = st.text_input("ชื่อแบรนด์ *", placeholder="เช่น Brand A")
            task_title = st.text_input("ชื่องาน *", placeholder="เช่น รีวิวครีมกันแดด")
            platform = st.selectbox("แพลตฟอร์ม", PLATFORMS)
        with col2:
            due_date = st.date_input("วันกำหนดส่ง", value=today + timedelta(days=3))
            fee = st.number_input("ค่าจ้าง (บาท)", min_value=0.0, value=0.0, step=500.0)
            status = st.selectbox("สถานะงาน", STATUSES)
        notes = st.text_area("หมายเหตุ (ไม่บังคับ)", placeholder="เช่น ต้องส่งร่างให้แบรนด์ตรวจ")
        submitted = st.form_submit_button("บันทึกงาน", use_container_width=True)

        if submitted:
            if not brand.strip() or not task_title.strip():
                st.error("กรุณากรอกชื่อแบรนด์และชื่องานก่อนบันทึก")
            else:
                new_task = {
                    "id": st.session_state.next_id,
                    "brand": brand.strip(),
                    "title": task_title.strip(),
                    "platform": platform,
                    "due_date": due_date,
                    "fee": float(fee),
                    "status": status,
                    "notes": notes.strip()
                }
                st.session_state.tasks.append(new_task)
                st.session_state.next_id += 1
                st.success("เพิ่มงานเรียบร้อยแล้ว")
                st.rerun()

# ----------------------------------------------------------
# Dashboard: สรุปตัวเลข
# ----------------------------------------------------------
tasks = st.session_state.tasks
active_tasks = [task for task in tasks if task["status"] != "เสร็จแล้ว"]
completed_tasks = [task for task in tasks if task["status"] == "เสร็จแล้ว"]
urgent_tasks = [
    task for task in active_tasks
    if (task["due_date"] - today).days <= 2
]
overdue_tasks = [
    task for task in active_tasks
    if (task["due_date"] - today).days < 0
]

st.subheader("📊 ภาพรวมงานของคุณ")
m1, m2, m3, m4 = st.columns(4)
m1.metric("งานทั้งหมด", len(tasks))
m2.metric("งานที่ยังไม่เสร็จ", len(active_tasks))
m3.metric("ใกล้ส่ง / เลยกำหนด", len(urgent_tasks))
m4.metric("งานเสร็จแล้ว", len(completed_tasks))

# แจ้งเตือนกำหนดส่ง
if overdue_tasks:
    st.error(f"🚨 มีงานเลยกำหนด {len(overdue_tasks)} งาน โปรดตรวจสอบรายการด้านล่าง")
elif urgent_tasks:
    st.warning(f"⏰ มีงานที่ใกล้ถึงกำหนด {len(urgent_tasks)} งาน อย่าลืมจัดลำดับความสำคัญ")
else:
    st.success("✨ ตอนนี้ไม่มีงานที่ใกล้ถึงกำหนดใน 2 วัน")

# ----------------------------------------------------------
# ตัวกรองและรายการงาน
# ----------------------------------------------------------
st.divider()
st.subheader("🗂️ รายการงานทั้งหมด")

filter_col1, filter_col2 = st.columns(2)
with filter_col1:
    status_filter = st.selectbox("กรองตามสถานะงาน", ["ทั้งหมด"] + STATUSES)
with filter_col2:
    deadline_filter = st.selectbox(
        "กรองตามกำหนดส่ง",
        ["ทั้งหมด", "ใกล้ส่ง (ภายใน 2 วัน)", "เลยกำหนด", "เสร็จแล้ว"]
    )

filtered_tasks = tasks[:]

if status_filter != "ทั้งหมด":
    filtered_tasks = [t for t in filtered_tasks if t["status"] == status_filter]

if deadline_filter == "ใกล้ส่ง (ภายใน 2 วัน)":
    filtered_tasks = [
        t for t in filtered_tasks
        if t["status"] != "เสร็จแล้ว" and 0 <= (t["due_date"] - today).days <= 2
    ]
elif deadline_filter == "เลยกำหนด":
    filtered_tasks = [
        t for t in filtered_tasks
        if t["status"] != "เสร็จแล้ว" and (t["due_date"] - today).days < 0
    ]
elif deadline_filter == "เสร็จแล้ว":
    filtered_tasks = [t for t in filtered_tasks if t["status"] == "เสร็จแล้ว"]

# เรียงงานที่ยังไม่เสร็จและมีกำหนดใกล้ที่สุดไว้ก่อน
filtered_tasks.sort(key=lambda t: (t["status"] == "เสร็จแล้ว", t["due_date"]))

if not filtered_tasks:
    st.info("ไม่พบงานตามตัวกรองที่เลือก ลองเปลี่ยนตัวกรองหรือเพิ่มงานใหม่")
else:
    for task in filtered_tasks:
        label = get_deadline_label(task, today)
        with st.container(border=True):
            title_col, status_col = st.columns([3, 1])
            with title_col:
                st.markdown(f"### {task['title']}")
                st.caption(f"🏷️ {task['brand']} · 📱 {task['platform']}")
            with status_col:
                if label == "เลยกำหนด":
                    st.error(label)
                elif label in ["ใกล้ส่ง", "ครบกำหนดวันนี้"]:
                    st.warning(label)
                elif label == "เสร็จแล้ว":
                    st.success(label)
                else:
                    st.info(label)

            detail1, detail2, detail3 = st.columns(3)
            detail1.write(f"📅 {task['due_date'].strftime('%d/%m/%Y')}")
            detail2.write(f"💰 {task['fee']:,.0f} บาท")
            detail3.write(f"📌 {task['status']}")
            st.caption(f"⏳ {format_deadline(task, today)}")
            if task["notes"]:
                st.write(f"หมายเหตุ: {task['notes']}")

            action1, action2 = st.columns([2, 1])
            status_key = f"status_{task['id']}"
            with action1:
                new_status = st.selectbox(
                    "เปลี่ยนสถานะงาน",
                    STATUSES,
                    index=STATUSES.index(task["status"]),
                    key=status_key
                )
                if st.button("อัปเดตสถานะ", key=f"update_{task['id']}", use_container_width=True):
                    for saved_task in st.session_state.tasks:
                        if saved_task["id"] == task["id"]:
                            saved_task["status"] = new_status
                            break
                    st.success("อัปเดตสถานะแล้ว")
                    st.rerun()
            with action2:
                st.write("")
                st.write("")
                if st.button("🗑️ ลบงาน", key=f"delete_{task['id']}", use_container_width=True):
                    st.session_state.tasks = [
                        saved_task for saved_task in st.session_state.tasks
                        if saved_task["id"] != task["id"]
                    ]
                    st.rerun()

# ----------------------------------------------------------
# สรุปและคำอธิบายโปรแกรม
# ----------------------------------------------------------
st.divider()
st.subheader("💡 สรุปการทำงาน")
total_fee = sum(task["fee"] for task in tasks)
st.write(f"- งานทั้งหมดในระบบ: **{len(tasks)} งาน**")
st.write(f"- งานที่ยังไม่เสร็จ: **{len(active_tasks)} งาน**")
st.write(f"- งานที่เสร็จแล้ว: **{len(completed_tasks)} งาน**")
st.write(f"- มูลค่าค่าจ้างรวมของงานที่บันทึก: **{total_fee:,.0f} บาท**")

with st.expander("เกี่ยวกับโปรเจกต์และข้อจำกัด"):
    st.write(
        "Influencer WorkMate เป็นโปรเจกต์เพื่อการเรียนรู้ ใช้ if-else ตรวจสอบกำหนดส่ง, "
        "for loop วนแสดงรายการงาน, functions ช่วยแยกการทำงาน และ list/dictionary เก็บข้อมูล"
    )
    st.write(
        "ข้อมูลเริ่มต้นเป็นข้อมูลตัวอย่าง และข้อมูลที่เพิ่มจะอยู่ใน session state ระหว่างใช้งาน "
        "หากเริ่มเซสชันใหม่ ข้อมูลอาจกลับไปเป็นข้อมูลตัวอย่าง ยังไม่ได้เชื่อมฐานข้อมูลถาวร "
        "หรือส่งการแจ้งเตือนออกนอกเว็บไซต์"
    )
