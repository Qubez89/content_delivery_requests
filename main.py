import streamlit as st
from datetime import datetime, date
from utils import get_mongodb_collection, convert_date


collection = get_mongodb_collection()
# Initialize session state
def init_session_state():
    if "items" not in st.session_state:
        st.session_state.items = []
    if "name" not in st.session_state:
        st.session_state.name = ""
    # Add other session state variables as needed

init_session_state()

def main():
    init_session_state()


# UI Title
st.title("📄 Content Delivery Request Form")

# Step navigation
step = st.radio("Step", ["📝 Requestor Details", "📅 Request Dates", "📂 Items"])

# Step 1: Requestor Details
if step == "📝 Requestor Details":
    st.header("📝 Requestor Details")
    st.session_state["name"] = st.text_input("Requestor Name", value=st.session_state.get("name", ""))
    st.session_state["organization"] = st.text_input("Organization Name", value=st.session_state.get("organization", ""))
    st.session_state["email"] = st.text_input("Email", value=st.session_state.get("email", ""))
    st.session_state["country"] = st.text_input("Country", value=st.session_state.get("country", ""))
    st.session_state["request type"] = st.selectbox("Request Type", ["internal", "external"])

# Step 2: Request Dates
elif step == "📅 Request Dates":
    st.header("📅 Request Dates")
    st.session_state["received_in_QNL"] = st.date_input("Received in QNL", value=st.session_state.get("received_in_QNL", datetime.today()))
    st.session_state["received_in_DCD"] = st.date_input("Received in DCD", value=st.session_state.get("received_in_DCD", datetime.today()))
    st.session_state["sent_to_patron"] = st.date_input("Sent to Patron", value=st.session_state.get("sent_to_patron", datetime.today()))

# Step 3: Items
elif step == "📂 Items":
    st.header("📂 Items")

    st.subheader("➕ Add New Item")
    with st.form("item_form"):
        item_type = st.selectbox("Item Type", ["Manuscript", "Book", "Article"])
        number_of_images = st.number_input("Number of Images", min_value=1, step=1)
        file_format = st.selectbox("File Format", ["PDF", "JPEG", "TIFF"])
        status = st.selectbox("Status", ["Approved", "Pending", "Rejected"])
        platform = st.selectbox("Platform", ["Manara", "QDL", "Other"])
        collections = st.text_area("Collections (comma-separated)").split(",")

        url = st.text_input("URL")
        ark_pid_id = st.text_input("ARK ID / PID")
        shelfmark_record_no = st.text_input("Shelfmark Record No.")

        comments = st.text_area("Comments")
        copyright_info = st.text_area("Copyright Info")
        purpose_of_reuse = st.text_input("Purpose of Reuse")

        published_or_displayed = st.checkbox("Published or Displayed?")
        received_pdf_copy = st.checkbox("Received PDF Copy?")

        submitted = st.form_submit_button("✅ Save Item")
        if submitted:
            new_item = {
                "item_type": item_type,
                "number_of_images": number_of_images,
                "file_format": file_format,
                "status": status,
                "platform": platform,
                "collections": collections,
                "identifiers": {
                    "url": url,
                    "ark_pid_id": ark_pid_id,
                    "shelfmark_record_no": shelfmark_record_no,
                },
                "notes": {
                    "comments": comments,
                    "copyright": copyright_info,
                    "purpose_of_reuse": purpose_of_reuse,
                    "published_or_displayed": published_or_displayed,
                    "received_pdf_copy": received_pdf_copy,
                }
            }
            st.session_state["items"].append(new_item)
            st.success(f"✅ Item {len(st.session_state['items'])} added!")

# Final submit button (always visible)
st.markdown("---")
if st.button("📤 Submit Request"):
    request_data = {
        "requests": {
            "name": st.session_state.get("name", ""),
            "organization_name": st.session_state.get("organization", ""),
            "email": st.session_state.get("email", ""),
            "country": st.session_state.get("country", ""),
            "request type": st.session_state.get("request type", "")
        },
        "request_dates": {
            "received_in_QNL": convert_date(st.session_state.get("received_in_QNL")),
            "received_in_DCD": convert_date(st.session_state.get("received_in_DCD")),
            "sent_to_patron": convert_date(st.session_state.get("sent_to_patron")),
        },
        "items": st.session_state["items"]
    }

    try:
        collection.insert_one(request_data)
        st.success("✅ Request saved successfully!")
        st.session_state["items"] = []
    except Exception as e:
        st.error(f"Error saving request: {e}")

if __name__ == "__main__":
    main()
