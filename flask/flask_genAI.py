from flask import Flask, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)

# Initialize the Google GenAI client with the API key
client = genai.Client(api_key="AIzaSyCY0pgtmhJbisYENnNgWzd0m_u5vKdiB8U")

@app.route('/generate-content', methods=['POST'])
def generate_content():
    try:
        # Get the prompt from the request body (expects JSON with a "prompt" key)
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({'error': 'Missing prompt in request body'}), 400

        prompt = data['prompt']

        print('\n----prompt')
        print(prompt)
        # Generate content using the Google GenAI client
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0)  # Disables thinking
            ),
        )
        print(response.text)
        print('\n---success')
        # Return the generated content as JSON
        return jsonify({'response': response.text})

    except Exception as e:
        print('---\nException')
        print(e)
        # Handle errors and return an error message
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8085)

    # curl -X POST -H "Content-Type: application/json" -d '{"prompt":"Explain how computer works，use chinese"}' http://localhost:8085/generate-content