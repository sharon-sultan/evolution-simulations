# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

add_footer="""
<style>

footer{
    visibility:visible;
}
footer:after{
    content: 'Efrat Herbst, Dr. Ofer Mokady, and Prof. Zohar Yakhini';
    display:block;
    position:relative;
    color:grey;
    # padding:5px;
    top:3px;
}

</style>
"""

def run():
    st.set_page_config(
        page_title="Evolution Simulator",
        page_icon=':earth_americas:',
    )
    st.markdown(add_footer, unsafe_allow_html=True)

    st.write("# Welcome to the Evolution Simulator!")
    st.sidebar.success("Select a simulation above.")

    st.markdown(
        """
        This app is desined to demonstrate some of the concepts underlying the complex process of Evolution, as research understand it to date.
        
        **👈 Select a simulation from the sidebar** to watch these concepts in action.
        ### Want to learn more?
        - Check out [a link to evolution...](https://streamlit.io)
        ### This app is provided by...
        - Reichman university [some website?](https://github.com/streamlit/demo-self-driving)
        - Israel learning.... [some website?](https://github.com/streamlit/demo-uber-nyc-pickups)
    """
    )


if __name__ == "__main__":
    run()
