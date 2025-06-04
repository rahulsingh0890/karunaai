# KarunaAi 🤖✨🪷
KarunaAi is an AI-powered voice companion designed to provide compassionate check-ins and support for elderly care. The system uses natural language processing and voice technology to engage in meaningful conversations, monitor well-being, and provide timely updates to caregivers.

## Features 🌟
- **Voice Check-ins**: Automated voice calls with natural conversation flow
- **Caregiver Updates**: Email summaries of conversations and well-being status
- **Sentiment Analysis**: Mood tracking and notable observations
- **Customizable Interactions**: Personalized conversation flows based on user preferences

## Project Structure 📁
```
KarunaAi/
├── app/
│   ├── conversation_flow.py    # Main conversation logic
│   ├── fetch_call_logs.py      # Call log retrieval
│   ├── summarize_call_logs.py  # Conversation summarization
│   ├── send_summaries_email.py # Caregiver email updates
├── config/
│   └── users.json             # User and caregiver configurations
├── tests/                     # Test suite
├── requirements.txt           # Python dependencies
└── server.py                  # API server
```

## Prerequisites 🎯
Before setting up KarunaAi, you'll need:
1. **Vapi.ai Account**
   - Sign up at [Vapi.ai](https://vapi.ai)
   - Set up a new phone number
   - Configure assistant settings
   - Get your API key

2. **Mistral & Ollama**
   - Install [Ollama](https://ollama.ai)
   - Pull the Mistral model: `ollama pull mistral`
   - Ensure Ollama is running locally

3. **Gmail Account**
   - Create a Gmail account or use existing one
   - Enable 2-factor authentication
   - Generate an App Password for the application

## Setup 🛠️

1. Clone the repository:
   ```bash
   git clone https://github.com/rahulsingh0890/karunaai.git
   cd KarunaAi
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory with the following:
   ```
   # Vapi.ai Configuration
   VAPI_API_KEY=your_vapi_api_key
   VAPI_PHONE_NUMBER=your_vapi_phone_number
   VAPI_ASSISTANT_ID=your_vapi_assistant_id

   # Email Configuration
   EMAIL_SENDER=your_gmail_address
   EMAIL_PASSWORD=your_gmail_app_password

   # Ollama Configuration
   OLLAMA_BASE_URL=http://localhost:11434
   ```

5. Configure User Details:
   Update `config/users.json` with:
   ```json
   {
     "users": [
       {
         "client_name": "Client Name",
         "phone_number": "+1XXXXXXXXXX",
         "caregiver_name": "Caregiver Name",
         "caregiver_email": "caregiver@email.com"
       }
     ]
   }
   ```

## Usage 📱

1. Start the server:
   ```bash
   python server.py
   ```

2. Initiate a check-in call:
   ```bash
   python app/conversation_flow.py
   ```

3. Generate summaries:
   ```bash
   python app/summarize_call_logs.py
   ```

4. Send caregiver updates:
   ```bash
   python app/send_summaries_email.py
   ```

## Configuration ⚙️
- Update `config/users.json` with client and caregiver information
- Modify conversation flows in `app/conversation_flow.py`
- Adjust email templates in `app/send_summaries_email.py`

## Contributing 🤝
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License 📄
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments 🙏
- Built with 💛 for elderly care
- Powered by advanced AI and voice technology
- Designed to make a difference in people's lives

## Contact & Resources 📧
- **Email**: karunaaiupdates@gmail.com
- **Website**: [Karuna - Gentle Conversations](https://karuna-gentle-conversations.lovable.app/)
- **GitHub Issues**: For technical support, please open an issue in the repository 