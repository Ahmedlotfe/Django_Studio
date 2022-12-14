# Django_Studio

## Introduction

- this project is a booking application
- this application has 4 main user types (admin,studio owner,employe,customer).
- All Authentication are done via JWT
- Each owner can create a studio and assign employees to that studio
- After the employee logins he is required to choose the current working studio from a list of studios he is assigned to and create a new jwt with the extra studio id embedded in it
- Each studio has a maximum number of customers per day
- Customers can cancel their reservation if it has not passed 15mins since its creation
- Customers can see their own reservations only
- Employees can only see the current logged in studio reservations
- Studio Owners can see all the reservations from their studios
- Admin can see everything

## How to Install the Project

- Download the project from [GitHub]
- Create virtual environment and install the dependencies
- Run this command in terminal to create the virtual environment with the dependencies: `python3 -m venv venv`

  ```
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```

- Run this commands in terminal to migrate the models to the database:
  ```
  python manage.py makemigraions
  python manage.py db migrate
  ```

## How to Use the Project

- Run this command in terminal ro create admin user account: `python3 manage.py createsuperuser`
- Run this command in terminal to run the server: `python3 manage.py runserver`
- Open the browser and got to the url: `http://localhost:8000/api/register/` to register the user.
- Body of the request has to be like this :

  ```
  {
      "username": "username",
      "email": "username@mail.com",
      "type": "E",
      "password": password
  }
  type => the type of the user:
        ("S", 'studio_owner'),
        ("E", 'employee'),
        ("C", 'customer')
  ```

- Open the browser and got to the url: `http://localhost:8000/api/login/` to login to the system.
- Body of the request has to be like this :

  ```
  {
      "username": "username",
      "password": password
  }
  ```

- Open the browser and got to the url: `http://127.0.0.1:8000/api/logout/` to logout
- Open the browser and got to the url: `http://localhost:8000/studio/create/` to create studio but you have to login with studio owner to be able to create studio
- Body of the request has to be like this :

  ```
  {
    "name": "new studio"
  }
  ```

- After creating Studio owner, Employees, Customers and Studio
- Open the browser and got to the url: `http://127.0.0.1:8000/studio/add_employees/` to assign employees to studio
- Body of the request has to be like this :

  ```
  {
    "employee_ids": [1],
    "studio_id": studio_id
  }

  => You have to be the studio owner to be able to assign employees to studio
  ```

- Open the browser and got to the url: `http://127.0.0.1:8000/studio/reserve/` to create reservation
- Body of the request has to be like this :

  ```
  {
    "studio": studio_id
  }

  => You have to login with customer user to be able to make reservation
  => The studio has a maximum number of customers per day
  ```

- Open the browser and got to the url: `http://127.0.0.1:8000/studio/cancel_reservation/` to cancel reservation
- Body of the request has to be like this :

  ```
  {
    "reservation_id": 1
  }

  => You have to login with reservation owner to be able to cancel the reservation
  => You can cancel their reservation if it has not passed 15mins since its creation
  ```

- Open the browser and got to the url: `http://127.0.0.1:8000/studio/list_reservations/` to see all reservations
  ```
  => Customers can see their own reservations only
  => Employees can only see the current logged in studio reservations
  => Studio Owners can see all the reservations from their studios
  => Admin can see everything
  ```

## Prerequisite

1. asgiref==3.5.2
1. autopep8==1.7.0
1. Django==4.1.2
1. django-cors-headers==3.13.0
1. djangorestframework==3.14.0
1. pycodestyle==2.9.1
1. PyJWT==2.5.0
1. pytz==2022.4
1. sqlparse==0.4.3
1. toml==0.10.2
1. tzdata==2022.4

## Author

- (ahmedlotfe132@gmail.com)
