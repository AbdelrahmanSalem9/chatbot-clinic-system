<b><h1 align="center">Clinic Reservation Website with Chatbot</h1></b>

This is a Django-based web application for a clinic reservation system that provides a chatbot to facilitate the reservation process.

## **Project Overview**
The clinic reservation website is designed to help patients easily book appointments with different doctors with different specialties. The web application includes a chatbot that provides users with an intuitive way to communicate with the system and book appointments.

## **Features**
- Appointment booking: Patients can search and book valid appointments with doctors of different specializations. The system ensures that no two appointments for the same doctor can exist.
- Appointment modification: Patients can modify existing appointments with the same or different doctors of the same specialization.
- Appointment cancellation: Patients can cancel their appointments by verifying the correct information about the appointment, including the appointment ID, patient email, and doctor information.
- Available specializations: Patients can discover all specializations and associated doctors
- Doctor information: Patients can query doctor information, including working days and hours, appointment pricing, specialization, medical experience, and history in the field.


## **Architecture**
As django uses client-server typical architecture,I have used layered architecture (MVC) for the server side processing, where the `views.py` module is considered as the endpoint for the users to send requests and receive responses based on the program logic. The `query_handler.py` and `actions.py` modules are responsible for parsing and understanding the semantic of the requests and accessing the database through the `models.py` module. Finally, the server responses logic is constructed by these modules in the controller layer and returned back to the client-side.

## **Notes**
for the sake of simplicity, I have assumed that each appointment time is 30 min, so the patients can book appointments in more convinent way.  

##  **Future Work**
- Replace the trivial bot model by some Natural language machine learning model to understand the semantic of the user input text.
- Generalize the appointment duration and remove the 30 min duration for all appointments
- Add more authentication and authorization checks

## **Technologies Used**
- Django
- SQLite
- Natural Language Toolkit (NLTK)
- HTML/CSS/JavaScript
- JQuery
- Bootstrap

## **Credits**
This project was created by Abdelrahman Salem