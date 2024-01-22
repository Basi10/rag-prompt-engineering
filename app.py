# Import necessary libraries
from flask import Flask, request, jsonify
import openai
from src.database.database import WeaviatePDFManager
from src.evaluation.evaluation import Evaluation
from src.promptgeneration.generateprompt import ChatBot

# Initialize Flask app
app = Flask(__name__)

# Set your OpenAI API key
import os
weaviate_url = "https://my-pdf-cluster-wi4uylnj.weaviate.network"
weaviate_api_key = os.environ['WEAVIATE_URL']
openai_api_key = os.environ['OPENAI_API_KEY']

# Define a route to handle user requests for prompt generation
@app.route('/generate_prompt', methods=['POST'])
def generate_prompt():
    try:
        # Get data from the request
        data = request.get_json()

        # Extract user input from the request
        user_input = data.get('user_input')
        num_test_output = data.get('num_test_output')
        pdf_uploader = WeaviatePDFManager(weaviate_url, weaviate_api_key, openai_api_key)
        # Perform necessary steps (You can modify this part based on your requirements)
        query_result = pdf_uploader.query_data('PDF1', query_text=user_input,limit=2)
        text_values = [item["text"] for item in query_result["data"]["Get"]["PDF1"]]
        chatbot = Evaluation(openai_api_key)
        context = "\n".join(text_values)
        classification = chatbot.main(user_message=user_input, context=context)
        if classification == "false":
            return jsonify({'Sorry. The context provided is not sufficient to answer your question.'})

        # Generate the prompt
        chatbot = ChatBot(client=openai_api_key)
        prompt = chatbot.generate_prompt(context=context, num_test_output=num_test_output)


        # Send the response back to the frontend
        return jsonify({'generated_prompt': prompt})

    except Exception as e:
        return jsonify({'error': str(e)})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
