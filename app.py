from flask import Flask, render_template, request, redirect, url_for, flash
import openai
from markupsafe import escape
from dotenv import load_dotenv
import os
import markdown
from markupsafe import Markup
import logging
import re

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')  # Load secret key from .env file

# Configure OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')  # Load OpenAI API key from .env file

# Configure logging
logging.basicConfig(level=logging.DEBUG)

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
            max_tokens=2000
        )

        # Log the full response from OpenAI
        # logging.debug(f"OpenAI response: {response}")

        encounter_text = response.choices[0].message.content.strip()

        # Use regular expressions to extract sections
        encounter_details_match = re.search(r'### Encounter Details\s*(.*?)\s*(?=###|$)', encounter_text, re.DOTALL)
        stat_blocks_match = re.search(r'### Stat Blocks\s*(.*?)\s*(?=###|$)', encounter_text, re.DOTALL)
        experience_award_match = re.search(r'### Experience Award\s*(.*?)\s*(?=###|$)', encounter_text, re.DOTALL)
        loot_table_match = re.search(r'### Loot Table\s*(.*?)\s*(?=###|$)', encounter_text, re.DOTALL)

        encounter_details = encounter_details_match.group(1).strip() if encounter_details_match else "No encounter details provided."
        stat_blocks = stat_blocks_match.group(1).strip() if stat_blocks_match else "No stat blocks provided."
        experience_award = experience_award_match.group(1).strip() if experience_award_match else "No experience award provided."
        loot_table = loot_table_match.group(1).strip() if loot_table_match else "No loot table provided."

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
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0",debug=False)
