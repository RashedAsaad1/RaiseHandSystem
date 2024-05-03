# Raise Hand System

![GitHub License](https://img.shields.io/github/license/RashedAsaad1/RaiseHandSystem)

<!-- PROJECT LOGO -->
<p align="center">
  <a href="https://github.com/RashedAsaad1/RaiseHandSystem">
    <img src="assets/images/logo.webp" alt="Logo" width="80" height="80">
  </a>
</p>

## Table of Contents

- [About the Project](#about-the-project)
- [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Usage](#usage)
- [License](#license)
- [Contact](#contact)

## About the Project

The "Raise Hand System" is designed to facilitate interaction in both physical and virtual learning environments. It enables students to digitally signal their need for assistance, thereby improving communication between students and instructors. This system is particularly useful in large classrooms or during online sessions where it can be challenging for instructors to manage participation effectively.

**Key Features:**
- **Hand Raising Functionality:** Students can easily indicate their need to ask questions or request help, whether in a physical classroom or a virtual setting.
- **Participant Management:** Instructors can view and manage hand raises in real-time, helping them prioritize and address student queries in an orderly manner.

**Motivation:**
This system was developed to enhance the educational experience by improving student engagement and interaction, making classroom management more efficient for instructors, particularly during exercises or when direct interaction is needed.

[Back to top](#table-of-contents)

## Built With

- ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=flat-square&logo=django&logoColor=white) - [Django](https://www.djangoproject.com)
- ![Channels](https://img.shields.io/badge/django_channels-9cf.svg?style=flat-square&logo=django) - [Django Channels](https://channels.readthedocs.io)
- ![Daphne](https://img.shields.io/badge/daphne-9cf.svg?style=flat-square&logo=django) - [Daphne](https://github.com/django/daphne)
- ![Channels Redis](https://img.shields.io/badge/channels_redis-9cf.svg?style=flat-square&logo=redis) - [Channels Redis](https://github.com/django/channels_redis)

[Back to top](#table-of-contents)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/RashedAsaad1/RaiseHandSystem.git
   ```
2. Navigate to the project directory:
   ```bash
   cd RaiseHandSystem
   ```
3. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Set up the database:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
6. Run the server:
   ```bash
   python manage.py runserver
   ```

Now, you should be able to access the application locally at `http://localhost:8000`.

[Back to top](#table-of-contents)

### Usage

The Raise Hand System can be used in both virtual and physical classroom settings as follows:

1. **Create an Account:** Administrators and teachers set up their accounts to manage classes.
2. **Student Participation:** Students log in to raise their hands during the class when they need help.
3. **Manage Hand Raises:** Instructors can see the order of raised hands and address the students’ queries accordingly.
4. **Direct Communication:** The system facilitates direct communication between students and instructors if needed.

[Back to top](#table-of-contents)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

[Back to top](#table-of-contents)

## Contact

Rashed Asaad - [@Fargosoc](https://twitter.com/Fargosoc) - [rashed@fargo.solutions](rashed@fargo.solutions)

Project Link: [https://github.com/RashedAsaad1/RaiseHandSystem](https://github.com/RashedAsaad1/RaiseHandSystem)

[Back to top](#table-of-contents)
