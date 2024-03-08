import streamlit as st
import openai

# openai.api_key = "YOUR_API_KEY_HERE"
openai.api_key = "YOUR_API_KEY_HERE"

st.set_page_config(page_title = "text-to-image-generator", layout = "centered")

# To customize background-colour
background_color_style = """
    <style>
    .stApp {
        background-image: url("https://www.hdwallpapers.in/download/light_blue_mountain_during_morning_4k_hd_light_blue-1600x900.jpg");
        background-size: cover;
    }
    </style>
    """
st.markdown(background_color_style, unsafe_allow_html=True)

# To customize header and subheader
header_style = "color: #333333; font-family: Book Antiqua;"
subheader_style = "color: #333333; font-family: Book Antiqua;"

st.markdown(f"<center><h1 style='{header_style}'>Text-To-Image Generator</h1></center>", 
            unsafe_allow_html=True)
st.markdown(f"<center><h2 style='{subheader_style}'>Enter descriptive words to generate an image...!!!</h2></center>", 
            unsafe_allow_html=True)

# To customize text-input
text_input_style = """
        <style>
        .stTextInput label {
            color: #333333;
        }            
        div[data-baseweb="base-input"]{
            background-color: #F5F5F5;
            border: 2px solid #0E4A7B;
            border-radius: 8px;
        }
        input[class]{
            color: #333333;
            font-family: Trebuchet MS, sans-serif;
            font-size: 130%;
        }
        </style>
        """
st.markdown(text_input_style, unsafe_allow_html=True)

user_input = st.text_input("Enter your words (comma-seperated):")

# To customize the "Generate Image" button
button_style = """
    <style>
    .stButton button {
        background-color: #2AABE2;
        color: #0E4A7B;
        border: 2px solid #0E4A7B;
        border-radius: 11px;
        height: auto;
        padding-top: 3px;
        padding-bottom: 3px;
    }
    </style>
    """
st.markdown(button_style, unsafe_allow_html=True)


if st.button("Generate Image"):

    words_list = [word.strip() for word in user_input.split(",")]

    if not user_input.strip():
        st.warning("Please enter at least one descriptive word...!!!")

    elif len(words_list) > 3:
        st.warning("Please enter a maximum of three descriptive words only...!!!")

    else:
        narrative = "Imagine a real and vivid image with the words {} and describe it in two or three short and concise sentences.".format(
            ", ".join(words_list)
        )

        chatgpt_prompt = narrative

        # To call "gpt-3.5-turbo" to create prompt
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role" : "system", "content" : "You are a micro-storyteller, painting vivid pictures with a few well-chosen words."},
                {"role" : "user", "content" : chatgpt_prompt}
            ]
        )
        dalle_prompt = response["choices"][0]["message"]["content"]

        # To generate image with the prompt created
        response = openai.Image.create(
            prompt=dalle_prompt,
            n=2,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']

        # To customize the expander 
        expander_style = """
                <style>
                .streamlit-expander {
                    border: 1px hidden #E0E0E0;
                    border-radius: 20px;
                }
                .streamlit-expanderHeader {
                    background-color: #2AABE2;
                    color: #0E4A7B;
                    padding: 10px;
                    border: 2px solid #0E4A7B;
                    border-radius: 20px 20px 20px 20px;
                }
                .streamlit-expanderContent {
                    background-color: #F5F5F5;
                    color: #333333;
                    padding: 10px;
                    border: 2px solid #0E4A7B;
                    border-radius: 15px 15px 20px 20px;
                    border-top: 0;
                }
                div[data-testid="stExpander"] div[role="button"] p {
                    font-family: Trebuchet MS, sans-serif;
                    font-size: 150%;
                }
                div[data-testid="stExpander"] div[role="button"] + div p {
                    font-family: Trebuchet MS, sans-serif;
                    font-style: italic;
                    font-size: 130%;
                }
                </style>
                """
        st.markdown(expander_style, unsafe_allow_html=True)

        # Display of the created prompt and generated image
        if len(words_list) == 1:
            with st.expander("Generated Prompt and Image with the word '{}'.".format(user_input)):
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Generated Prompt:")
                    st.write(dalle_prompt)
                with col2:
                    st.subheader("Generated Image:")
                    st.image(image_url)
        else:
            with st.expander("Generated Prompt and Image with the words '{}'.".format(user_input)):
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Generated Prompt:")
                    st.write(dalle_prompt)
                with col2:
                    st.subheader("Generated Image:")
                    st.image(image_url)
