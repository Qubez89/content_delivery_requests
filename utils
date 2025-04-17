from datetime import datetime, date
import pymongo
import streamlit as st

def get_mongodb_collection():
    client = pymongo.MongoClient(st.secrets["MONGO_URI"])
    return client["content_delivery_requests"]["requests"]

def convert_date(date_obj):
    if isinstance(date_obj, (datetime, date)):
        return datetime.combine(date_obj, datetime.min.time()).isoformat() + "Z"
    return None
