import streamlit as st

@st.dialog("Disclaimer")
def show_disclaimer_popup():

    st.write(
        """
        This chat application, 🤖 OBIS Bot, it uses data retrieved from the [OBIS REST API](https://api.obis.org/v3/), limited to 15 datasets and the first 100 occurrences per dataset and only required [eight terms](https://manual.obis.org/checklist.html), due to processing constraints of the utilized Large Language Model [GPT 4](https://platform.openai.com/docs/guides/rate-limits). Please note that while we strive for accuracy, the use of LLMs may result in occasional inaccuracies or incomplete information. Users are encouraged to verify critical information independently. Repository [here](https://github.com/gustavomarcelonunez/obis-bot/).
        """
    )
    if st.button("Close"):
         st.rerun()