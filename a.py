import os
import shutil
import base64
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from PIL import Image
from io import BytesIO
import time

@st.cache_resource(show_spinner=False)
def get_logpath():
    return os.path.join(os.getcwd(), 'selenium.log')

@st.cache_resource(show_spinner=False)
def get_chromedriver_path():
    return shutil.which('chromedriver')

@st.cache_resource(show_spinner=False)
def get_webdriver_options():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-features=NetworkService")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-features=VizDisplayCompositor")
    return options

def get_webdriver_service(logpath):
    service = Service(
        executable_path=get_chromedriver_path(),
        log_output=logpath,
    )
    return service

def delete_selenium_log(logpath):
    if os.path.exists(logpath):
        os.remove(logpath)

def show_selenium_log(logpath):
    if os.path.exists(logpath):
        with open(logpath) as f:
            content = f.read()
            st.code(body=content, language='log', line_numbers=True)
    else:
        st.warning('No log file found!')

def run_selenium(logpath):
    screenshot_path = "screenshot.png"  # Temporary path to save the screenshot

    with webdriver.Chrome(options=get_webdriver_options(), service=get_webdriver_service(logpath=logpath)) as driver:
        url = "https://bawuat1.dfveriflow.com/ProcessPortal/login.jsp"
        driver.get(url)
        time.sleep(10)
        
        # Capture screenshot and save it
        screenshot = driver.get_screenshot_as_png()

        # making download link
        buf = BytesIO()
        screenshot.save(buf, format="JPEG")
        byte_im = buf.getvalue()

        btn = col.download_button(label="Download Image",data=byte_im,file_name="screenshot.png",mime="screenshot/jpeg",)
        
        # Display the screenshot on Streamlit
        st.image(Image.open(BytesIO(screenshot)), caption="Screenshot", use_column_width=True)

        # Wait for the element to be rendered:
        element = driver.find_element(By.ID, "user_id")
        element_1 = element.text

    return href, element_1


if __name__ == "__main__":
    logpath=get_logpath()
    delete_selenium_log(logpath=logpath)
    st.set_page_config(page_title="Selenium Test", page_icon='✅',
        initial_sidebar_state='collapsed')
    st.title('🔨 Selenium on Streamlit Cloud')
    st.markdown('''This app is only a very simple test for **Selenium** running on **Streamlit Cloud** runtime.<br>
        The suggestion for this demo app came from a post on the Streamlit Community Forum.<br>
        <https://discuss.streamlit.io/t/issue-with-selenium-on-a-streamlit-app/11563><br><br>
        This is just a very very simple example and more a proof of concept.<br>
        A link is called and waited for the existence of a specific class to read a specific property.
        If there is no error message, the action was successful.
        Afterwards the log file of chromium is read and displayed.
        ''', unsafe_allow_html=True)
    st.markdown('---')

    # st.balloons()
    if st.button('Start Selenium run'):
        st.warning('Selenium is running, please wait...')
        result = run_selenium(logpath=logpath)
        st.info(f'Result -> {result}')
        # st.info('Successful finished. Selenium log file is shown below...')
        # show_selenium_log(logpath=logpath)
