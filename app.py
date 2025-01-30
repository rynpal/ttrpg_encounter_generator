from flask import Flask, render_template, request, redirect, url_for, flash
import openai
from markupsafe import escape
from dotenv import load_dotenv
import os
from markupsafe import Markup
import logging
import re
import markdown2

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
            f"Please format the STR, DEX, CON, INT, WIS, and CHA stats as rows.\n"
            f"Include the following sections, delimited by '###':\n"
            f"### Encounter Details\n"
            f"### Stat Blocks\n"
            f"### Experience Award\n"
            f"### Loot Table"
            f"Do not include any pithy summaries at the end of the response.    "
        )

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates TTRPG encounters."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000
        )

        # Log the full response from OpenAI
        # logging.debug(f"OpenAI response: {response}")

        encounter_text = response.choices[0].message.content.strip()

        # Convert the entire encounter text to HTML
        encounter_html = markdown2.markdown(encounter_text, extras=["tables"])

        # Use regular expressions to extract sections from the HTML
        encounter_details_match = re.search(r'<h3>Encounter Details</h3>\s*(.*?)\s*(?=<h3>|$)', encounter_html, re.DOTALL)
        stat_blocks_match = re.search(r'<h3>Stat Blocks</h3>\s*(.*?)\s*(?=<h3>|$)', encounter_html, re.DOTALL)
        experience_award_match = re.search(r'<h3>Experience Award</h3>\s*(.*?)\s*(?=<h3>|$)', encounter_html, re.DOTALL)
        loot_table_match = re.search(r'<h3>Loot Table</h3>\s*(.*?)\s*(?=<h3>|$)', encounter_html, re.DOTALL)

        encounter_details = encounter_details_match.group(1).strip() if encounter_details_match else "No encounter details provided."
        stat_blocks = stat_blocks_match.group(1).strip() if stat_blocks_match else "No stat blocks provided."
        experience_award = experience_award_match.group(1).strip() if experience_award_match else "No experience award provided."
        loot_table = loot_table_match.group(1).strip() if loot_table_match else "No loot table provided."

        return render_template('result.html', encounter=Markup(encounter_details), stat_blocks=Markup(stat_blocks), experience_award=Markup(experience_award), loot_table=Markup(loot_table))
    except Exception as e:
        # logging.error("An error occurred: %s", str(e))
        # logging.error("Stack trace: %s", traceback.format_exc())
        flash(f"An error occurred: {str(e)}")
        return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    if os.getenv('FLASK_ENV') == 'development':
        app.run(host="0.0.0.0", port=port, debug=True)
    else:
        app.run(host="0.0.0.0", port=port, debug=False)
