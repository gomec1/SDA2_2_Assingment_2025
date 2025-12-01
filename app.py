import io
from typing import List
from PIL import Image
import streamlit as st

from core.text_core import TextProcessingCore


@st.cache_resource
def get_core() -> TextProcessingCore:
    """
    Create and cache the core instance with created plugins.
    Using cache_resource so it is only constructed once per session.
    """
    return TextProcessingCore.from_discovery()

# Front end :)
def main() -> None:
    st.set_page_config(page_title="Microkernel Text Tool", layout="wide")
    col1, col2 = st.columns([1, 6])

    with col1:
        logo = Image.open("assets/logoSDA2.png") # I cannot really defend myself here
        st.image(logo, width=150)

    with col2:
        st.title("Microkernel Text Processing Tool")
        st.caption(
            "Made by: Barcikowska Anna, Stähli Thomas, Gomez Pereanez Carlos Andres, Stettler Gil Colin, Kallioinen Jimi Eemil. "
        )

    core = get_core()
    plugins = core.list_plugins()

    # Sidebar
    st.sidebar.header("Available plugins")
    if not plugins:
        st.sidebar.warning("No plugins found.")
    else:
        for p in plugins:
            with st.sidebar.expander(p.name, expanded=False):
                st.write(p.description or "_No description_")
    # main
    st.subheader("1. Upload input text file")
    uploaded = st.file_uploader("Choose a .txt file", type=["txt"])

    input_text: str = ""
    if uploaded is not None:
        input_bytes = uploaded.read()
        input_text = core.read_text_from_bytes(input_bytes)
        st.text_area("Original text", value=input_text, height=200)

    st.subheader("2. Select plugins to apply")
    plugin_names: List[str] = [p.name for p in plugins]
    selected_names: List[str] = st.multiselect(
        "Plugins will be applied in the order shown below.",
        options=plugin_names,
        default=plugin_names, 
    ) 

    # Find & Replace plugin
    ###############################################################################
    find_replace = next((p for p in plugins if p.name == "Find & Replace"), None)

    if find_replace is not None and find_replace.name in selected_names:
        with st.expander("Find & Replace settings", expanded=False):
            pattern = st.text_input(
                "Find",
                value=getattr(find_replace, "pattern", ""),
                help="Text (or regex if 'Use regex' is checked)"
            )
            replacement = st.text_input(
                "Replace with",
                value=getattr(find_replace, "replacement", ""),
            )
            use_regex = st.checkbox(
                "Use regex",
                value=getattr(find_replace, "use_regex", False),
            )

        find_replace.pattern = pattern
        find_replace.replacement = replacement
        find_replace.use_regex = use_regex
    ###############################################################################

         # Translating Plugin settings with DeepL
    ###############################################################################
    deepL_plugin = next(
        (p for p in plugins if p.name == "Translating Plugin with DeepL"), None
    )

    if deepL_plugin is not None and deepL_plugin.name in selected_names:
        # Get supported language names and DeepL codes
        language_labels = list(getattr(deepL_plugin, "SUPPORTED_TARGET_LANGS", {}).keys())
        code_map = getattr(deepL_plugin, "SUPPORTED_TARGET_LANGS", {})

        if not language_labels:
            language_labels = ["English"]
            code_map = {"English": "EN"}

        # Determine current language index for default selection
        current_code = getattr(deepL_plugin, "target_lang", "EN")
        try:
            current_label_index = list(code_map.values()).index(current_code)
        except ValueError:
            current_label_index = 0

        with st.expander("Translation Settings", expanded=False):
            selected_label = st.selectbox(
                "Select target language:",
                options=language_labels,
                index=current_label_index,
                help="Choose the language you want the text to be translated into."
            )

        # Update plugin configuration
        deepL_plugin.target_lang = code_map[selected_label]
    ###############################################################################



    st.subheader("3. Process text")
    process_button = st.button("Run processing", disabled=(uploaded is None))

    processed_text: str | None = None

    if process_button and uploaded is not None:
        with st.spinner("Processing text..."):
            processed_text = core.apply_plugins(input_text, selected_names)

        st.success("Processing complete.")
        st.text_area("Processed text", value=processed_text, height=200)

        # Download button
        download_name = f"processed_{uploaded.name}"
        st.download_button(
            label="Download your new file",
            data=core.write_text_to_bytes(processed_text),
            file_name=download_name,
            mime="text/plain",
        )


if __name__ == "__main__":
    main()
