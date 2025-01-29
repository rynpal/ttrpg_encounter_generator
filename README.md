# TTRPG Encounter Generator

This project is a web application that generates creative and detailed TTRPG encounters for Dungeons and Dragons Fifth Edition using OpenAI's GPT-4 model. The application allows users to specify various parameters for the encounter and generates the encounter details, stat blocks, experience award, and loot table.

## Features

- Generate encounters with customizable parameters such as number of enemies, difficulty rating, environment, enemy size, and enemy type.
- Display generated encounter details, stat blocks, experience award, and loot table.
- Simple and intuitive web interface built with Flask and Tailwind CSS.

## Requirements

- Python 3.8+
- Flask 2.3.3
- OpenAI API key
- Other dependencies listed in `requirements.txt`

## Setup

1. Clone the repository:

   ```sh
   git clone https://github.com/rynpal/ttrpg_encounter_generator.git
   cd ttrpg_encounter_generator
   ```

2. Create and activate a virtual environment:

   ```sh
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. Install the required dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your OpenAI API key and Flask secret key:

   ```properties
   FLASK_SECRET_KEY=your_secret_key
   OPENAI_API_KEY=your_openai_api_key
   ```

5. Run the application:
   ```sh
   flask run
   ```

## Usage

1. Open your web browser and navigate to `http://127.0.0.1:5000/`.
2. Fill out the form with the desired encounter parameters.
3. Click "Generate Encounter" to receive the generated encounter details.

## Deployment

To deploy the application using Gunicorn, you can use the provided `Procfile`. Ensure you have Gunicorn installed and run:

```sh
gunicorn app:app
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements

- OpenAI for providing the GPT-4 model.
- Flask for the web framework.
- Tailwind CSS for the styling framework.
