from groq import Groq

# Initialize Groq client with your API key
client = Groq(api_key="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")

# Function to ask a question
def ask_groq(question, model="gemma2-9b-it"):  # You can change to any model just by selecting in Groq
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant,but dont use any emoji."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

# Example usage
question = "What is the capital of France?"
answer = ask_groq(question)
print("Answer:", answer)
