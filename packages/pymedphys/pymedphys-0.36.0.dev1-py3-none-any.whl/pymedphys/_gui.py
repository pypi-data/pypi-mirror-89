# Copyright (C) 2019 Simon Biggs
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# pylint: disable = protected-access

import pathlib
import shutil

from pymedphys._imports import streamlit as st

HERE = pathlib.Path(__file__).parent.resolve()
STREAMLIT_CONTENT_DIR = HERE.joinpath("_streamlit")


def fill_streamlit_credentials():
    streamlit_config_dir = pathlib.Path.home().joinpath(".streamlit")
    streamlit_config_dir.mkdir(exist_ok=True)

    template_streamlit_credentials_file = STREAMLIT_CONTENT_DIR.joinpath(
        "credentials.toml"
    )
    new_credential_file = streamlit_config_dir.joinpath("credentials.toml")

    try:
        shutil.copy2(template_streamlit_credentials_file, new_credential_file)
    except FileExistsError:
        pass


def main(_):
    """Boot up the pymedphys GUI

    """
    fill_streamlit_credentials()

    streamlit_script_path = str(HERE.joinpath("_app.py"))

    # This direct private call is undergone so as to guarantee that the
    # same Python that called ``pymedphys gui`` is the same Python that
    # is used to run streamlit.

    # Unfortunately streamlit does not as of yet support
    # ``python -m streamlit``. See <https://github.com/streamlit/streamlit/pull/2351>
    # for more details.
    st._is_running_with_streamlit = True
    st.bootstrap.run(streamlit_script_path, "", [])
