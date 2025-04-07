import streamlit as st
from logger import setup_logger
logger=setup_logger()

MODEL_API_KEY = st.secrets["MODEL_API_KEY"]
MODEL_END_POINT = st.secrets["MODEL_END_POINT"]

if not MODEL_API_KEY or not MODEL_END_POINT or MODEL_API_KEY=="MODEL_API_KEY" or MODEL_END_POINT=="MODEL_END_POINT":
    logger.warning("Please add MODEL_API_KEY and MODEL_END_POINT before running the UI ")
    st.error("Configuration Error: Please add MODEL_API_KEY and MODEL_END_POINT in secrets.toml")
    st.stop()

logger.info("API key and endpoint successfully loaded.")
