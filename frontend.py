import streamlit as st
import requests
import json

# Backend API URL
API_URL = "http://127.0.0.1:8000"

st.title("Chatbot")

user_id = 1


if "access_token" not in st.session_state:
    st.session_state.access_token = None

if st.session_state.access_token:
    if "history" not in st.session_state:
        st.session_state.history = []

    # Function to fetch messages
    def fetch_messages(user_id):
        try:
            response = requests.get(f"{API_URL}/messages/{user_id}")
            if response.status_code == 200:
                messages = response.json()
                for message in messages:
                    if message["message_type"] == 0:
                        st.markdown(
                            f'<div style="background-color: #ddd; padding: 10px; border-radius: 10px; margin: 5px 0;">'
                            f'<span style="color: black;">You:</span> {message["message_content"]}'
                            "</div>",
                            unsafe_allow_html=True,
                        )
                    elif message["message_type"] == 1:
                        st.markdown(
                            f'<div style="background-color: #007bff; color: white; padding: 10px; border-radius: 10px; margin: 5px 0;">'
                            f'<span style="color: white;">Chatbot:</span> {message["message_content"]}'
                            "</div>",
                            unsafe_allow_html=True,
                        )
            else:
                st.error(
                    f"Failed to fetch messages. Status code: {response.status_code}"
                )
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching messages: {e}")

    # Fetch messages for the current user
    fetch_messages(user_id)

    # User input
    user_input = st.text_input("You: ", "")

    if user_input:
        st.session_state.history.append(user_input)

        headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
        request_payload = {"text": user_input}

        # Log the request payload
        st.write("Request Payload:", json.dumps(request_payload, indent=2))

        response = requests.post(
            f"{API_URL}/generate/", json=request_payload, headers=headers
        )

        try:
            response_data = response.json()
            st.write("Response Status Code:", response.status_code)
            st.write("Response Payload:", response_data)

            st.session_state.history.append(response_data["response"])

            # new message
            if len(st.session_state.history) % 2 == 1:
                st.markdown(
                    f'<div style="background-color: #ddd; padding: 10px; border-radius: 10px; margin: 5px 0;">'
                    f'<span style="color: black;">You:</span> {st.session_state.history[-2]}'
                    "</div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div style="background-color: #007bff; color: white; padding: 10px; border-radius: 10px; margin: 5px 0;">'
                    f'<span style="color: white;">Chatbot:</span> {st.session_state.history[-1]}'
                    "</div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div style="background-color: #007bff; color: white; padding: 10px; border-radius: 10px; margin: 5px 0;">'
                    f'<span style="color: white;">Chatbot:</span> {st.session_state.history[-1]}'
                    "</div>",
                    unsafe_allow_html=True,
                )

        except json.JSONDecodeError:
            st.error(
                "Failed to decode JSON response from server. Status code:",
                response.status_code,
            )

else:
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        login_payload = {"username": username, "password": password}

        st.write("Login Request Payload:", json.dumps(login_payload, indent=2))

        response = requests.post(f"{API_URL}/token", data=login_payload)

        if response.status_code == 200:
            try:
                response_data = response.json()
                st.session_state.access_token = response_data["access_token"]
                st.experimental_rerun()
            except json.JSONDecodeError:
                st.error(
                    "Failed to decode JSON response from server. Status code:",
                    response.status_code,
                )
        else:
            st.error("Invalid username or password")
