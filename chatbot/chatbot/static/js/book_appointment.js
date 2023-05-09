document.addEventListener('DOMContentLoaded', function () {
    var dateInput = document.getElementById('date');
    var doctorSelect = document.getElementById('doctor');
    var specialitySelect = document.getElementById('speciality');
    var confirmButton = document.getElementById('confirm-button');
    var cancelButton = document.getElementById('cancel-button');

    $('#speciality').change(function () {
        var selectedSpeciality = specialitySelect.value;
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/get_doctors/?speciality=' + selectedSpeciality);
        xhr.onload = function () {
            if (xhr.status === 200) {
                // Update the page with the available time slots
                var response = JSON.parse(xhr.responseText);
                var availableDoctors = response.doctors;
                var doctorSelect = document.getElementById('doctor');
                doctorSelect.innerHTML = '';
                for (var i = 0; i < availableDoctors.length; i++) {
                    // create the button element  
                    var doctorOption = document.createElement("option");
                    doctorOption.value = availableDoctors[i].id;
                    doctorOption.innerText = availableDoctors[i].name;
                    doctorSelect.appendChild(doctorOption);
                }
            }
        };
        xhr.send();
    });

    // Add event listener for date input change
    $('#doctor, #date').change(function () {
        var selectedDate = dateInput.value;
        var doctorId = doctorSelect.value;
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/check_availability/?doctor=' + doctorId + '&date=' + selectedDate);
        xhr.onload = function () {
            if (xhr.status === 200) {
                // Update the page with the available time slots
                var response = JSON.parse(xhr.responseText);
                var availableTimeSlots = response.available_time_slots;
                var timeSlotsList = document.getElementById('available-time-slots');
                timeSlotsList.innerHTML = '';
                var slotContainer = document.getElementById("available-time-slots");

                for (var i = 0; i < availableTimeSlots.length; i++) {
                    // create the button element
                    var slotButton = document.createElement("button");
                    slotButton.classList.add("time-slot");
                    slotButton.innerText = "Book " + new Date(availableTimeSlots[i]).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

                    slotButton.addEventListener("click", function () {
                        // slotButton.disabled = true;
                        const confirmationMessage = document.getElementById("confirmation-message");
                        // confirmationMessage.style.display = "block";

                        var doctorName = doctorSelect.options[doctorSelect.selectedIndex].text;
                        var selectedTime = this.innerText;
                        var confirmationData = document.getElementById("confirmation-data");
                        confirmationData.innerHTML = "Patient: " + patientEmail + "<br>Doctor: " + doctorName + "<br>Date: " + selectedDate + "<br>Time: " + selectedTime.substr(5);
                        submitAppointment(doctorId, doctorName, selectedDate, selectedTime, confirmationData, confirmButton);
                        this.style.visibility = "hidden";
                    });
                    slotContainer.appendChild(slotButton);
                }
            }
        };
        xhr.send();
    });
});
function submitAppointment(doctorId, doctorName, selectedDate, selectedTime, confirmationData, confirmButton) {
    const selectedDateTime = new Date(`${selectedDate} ${selectedTime.substr(5)}`);
    const xhr = new XMLHttpRequest();
    xhr.open('POST', window.location.href);
    xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
    xhr.setRequestHeader('X-CSRFToken', document.getElementsByName('csrfmiddlewaretoken')[0].value);
    xhr.onload = function () {
        if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            if (!response.error) {
                document.getElementById('confirmation-message').style.display = 'block';
                confirmationData.innerHTML = `<h2>Appointment ID #${response.appointment_id}</h2>${confirmationData.innerHTML}`;
                confirmButton.addEventListener('click', function () {
                    document.getElementById('confirmation-message').style.display = 'none';
                    window.location.href = '/chat';
                });
            }
            else {
                alert(response.error);
            }
        }
    };
    xhr.send(JSON.stringify({
        doctor_id: doctorId,
        date: selectedDate,
        time_slot: selectedDateTime.toISOString(),
        patient_email: patientEmail,
    }));
}