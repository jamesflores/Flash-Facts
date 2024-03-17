# Flash Facts

Flash Facts is a Django-based web application that displays a random fact on any particular day. 
It uses the Numbers API provided by [Rapid API](https://rapidapi.com/divad12/api/numbers-1/) and stock images from [Pexels](https://pexels.com)


## Installation

1. Clone the repository: `git clone https://github.com/jamesflores/Flash-Facts.git`
2. Navigate to the project directory
3. Install the requirements: `pip install -r requirements.txt`
4. Configure your environment variables (create a Rapid API account, Pexels account and generate your own SECRET_KEY for Django):
```
export FF_RAPID_API_KEY=
export FF_RAPID_API_HOST=numbersapi.p.rapidapi.com
export FF_RAPID_API_URL=https://numbersapi.p.rapidapi.com
export FF_SECRET_KEY=
export PEXELS_API_KEY=
```
5. Run the server: `python manage.py runserver`

## Usage

Open your web browser and navigate to `http://localhost:8000`.
Demo: https://facts.jamesf.xyz
