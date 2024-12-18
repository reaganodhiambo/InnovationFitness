# Fitness Assessment Project

## Description
The Fitness Assessment project is a Django web application designed to help users assess their fitness levels through various tests and provide personalized feedback. The application includes features for user registration, login, and assessment results.

## Installation
To set up the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/reaganodhiambo/FitnessAssessment.git
   cd FitnessAssessment
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

6. Access the application at `http://127.0.0.1:8000/`.

## Usage
- Register a new account to access the fitness assessment features.
- Log in to view your assessment results and update your profile.

## Features
- User registration and authentication
- Various fitness assessment tests
- Personalized feedback based on assessment results
- User profile management

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push to your branch and create a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
