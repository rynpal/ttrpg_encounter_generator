from flask import Flask, render_template, request, redirect, url_for, flash
import openai
from markupsafe import escape
from dotenv import load_dotenv
import os
import markdown
from markupsafe import Markup

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')  # Load secret key from .env file

# Configure OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')  # Load OpenAI API key from .env file

@app.route('/')
def index():
    return render_template('index.html')

def strip_heading(text, heading):
    return text.replace(heading, '').strip()

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Get form data
        num_enemies = escape(request.form['num_enemies'])
        difficulty = escape(request.form['difficulty'])
        environment = escape(request.form['environment'])
        enemy_size = escape(request.form['enemy_size'])
        enemy_type = escape(request.form['enemy_type'])
        additional_details = escape(request.form['additional_details'])

        # Call OpenAI API to generate encounter
        prompt = (
            f"Generate a creative and detailed TTRPG encounter for Dungeons and Dragons Fifth Edition with the following details:\n"
            f"Number of Enemies: {num_enemies}\n"
            f"Difficulty Rating: {difficulty}\n"
            f"Environment: {environment}\n"
            f"Enemy Size: {enemy_size}\n"
            f"Enemy Type: {enemy_type}\n"
            f"Additional Details: {additional_details}\n"
            f"Possibly include a group of enemies with a leader who has an interesting name and title, but this is not required.\n"
            f"Ensure the encounter details, stat blocks, experience award, and loot table are in line with Dungeons and Dragons Fifth Edition rules.\n"
            f"Include the following sections, delimited by '###':\n"
            f"### Encounter Details\n"
            f"### Stat Blocks\n"
            f"### Experience Award\n"
            f"### Loot Table"
        )

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates TTRPG encounters."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )

        encounter_text = response.choices[0].message.content.strip()

        # Split the response into different sections
        sections = encounter_text.split("###")
        encounter_details = sections[1].strip() if len(sections) > 1 else "No encounter details provided."
        stat_blocks = sections[2].strip() if len(sections) > 2 else "No stat blocks provided."
        experience_award = sections[3].strip() if len(sections) > 3 else "No experience award provided."
        loot_table = sections[4].strip() if len(sections) > 4 else "No loot table provided."

        # Strip headings
        encounter_details = strip_heading(encounter_details, "Encounter Details")
        stat_blocks = strip_heading(stat_blocks, "Stat Blocks")
        experience_award = strip_heading(experience_award, "Experience Award")
        loot_table = strip_heading(loot_table, "Loot Table")

        # Convert Markdown to HTML and sanitize
        encounter_details_html = Markup(markdown.markdown(encounter_details))
        stat_blocks_html = Markup(markdown.markdown(stat_blocks))
        experience_award_html = Markup(markdown.markdown(experience_award))
        loot_table_html = Markup(markdown.markdown(loot_table))

        return render_template('result.html', encounter=encounter_details_html, stat_blocks=stat_blocks_html, experience_award=experience_award_html, loot_table=loot_table_html)
    except Exception as e:
        flash(f"An error occurred: {str(e)}")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
