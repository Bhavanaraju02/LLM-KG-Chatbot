import logging
import streamlit as st


# # Maximum number of logs to retain
# MAX_LOGS = 100

class StreamlitLogHandler(logging.Handler):
    def __init__(self, log_list):
        super().__init__()
        self.log_list = log_list

    def emit(self, record):
        log_entry = self.format(record)
        self.log_list.append(log_entry)
        # Limit the number of logs stored
#         if len(self.log_list) > MAX_LOGS:
#             self.log_list.pop(0)
#         update_logs()

# def update_logs():
#     if "log_container" in st.session_state:
#         # Displaying logs in Markdown for better formatting
#         formatted_logs = "\n\n".join([f"`{log}`" for log in st.session_state.log[-10:]])
#         st.session_state.log_container.markdown(formatted_logs)


def setup_logger():
    # Initialize the session state for logging if it doesn't exist
    if "log" not in st.session_state:
        st.session_state.log = []

    # Create a logger instance
    logger = logging.getLogger("LLM_KG_ChatbotLogger")
    logger.setLevel(logging.INFO) # higher-severity level:INFO-> INFO, WARNING, ERROR, and CRITICAL messages are logged.

    # Set up StreamlitLogHandler to capture logs in the session state
    stream_handler = StreamlitLogHandler(st.session_state.log)
    stream_handler.setLevel(logging.INFO)

    # Create and set the log format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)

    # Add the handler to the logger
    if not logger.handlers:
        logger.addHandler(stream_handler)

    return logger
