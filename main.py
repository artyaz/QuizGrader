from flask import Flask, request, render_template
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the uploaded file
        file = request.files['file']

        # Load the HTML file into BeautifulSoup
        soup = BeautifulSoup(file, 'html.parser')

        # Define colors for correct and incorrect answers
        GREEN_COLOR = "green"
        RED_COLOR = "red"

        # Loop through each question div and extract the question name, checked radio button, and score
        results = []
        for div in soup.find_all('div', class_='que'):
            # Extract the question name
            question_name = div.find('div', class_='qtext').text.strip()

            # Extract the checked radio button
            checked_radio = div.find('input', {'checked': 'checked'})
            if checked_radio:
                answer = checked_radio.parent.text.strip()

            # Extract the score
            score_div = div.find('div', class_='grade')
            if score_div:
                score = score_div.text.strip()
                is_correct = float(score.split()[1].replace(',', '.')) >= 1

            # Format the answer text with the appropriate color and prefix
            if is_correct:
                answer_text = f"`{answer} ({GREEN_COLOR})`"
                prefix = "✅"
            else:
                answer_text = f"`! {answer} ({RED_COLOR})`"
                prefix = "❌"

            # Format the output text for this question
            output_text = f"<br>### {question_name}<br>{prefix} {answer_text}"

            results.append(output_text)

        return render_template('results.html', results=results)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
