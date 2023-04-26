document.addEventListener('DOMContentLoaded', function () {
    var dateInput = document.getElementById('date');
    dateInput.addEventListener('change', function () {
        var selectedDate = dateInput.value;
        var doctorId = document.getElementById('doctor').value;
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
                    slotButton.innerText = new Date(availableTimeSlots[i]).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

                    // add a click event listener to the button
                    slotButton.addEventListener("click", function () {
                        // get the selected doctor ID and email
                        // console.log(document.getElementById("doctor"));
                        var doctorId = document.getElementById("doctor").value;
                        // var email = document.getElementById("email-input").value;

                        // get the selected time slot
                        var selectedSlot = this.innerText;
                        var selectedDateTime = new Date(selectedDate + ' ' + selectedSlot);

                        // send a POST request to book the appointment
                        var xhr = new XMLHttpRequest();
                        xhr.open("POST", "/book_appointment/");
                        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
                        xhr.onload = function () {
                            if (xhr.status === 200) {
                                var response = JSON.parse(xhr.responseText);
                                alert(response.message); // show the confirmation message
                            }
                        };
                        var data = {
                            "doctor_id": doctorId,
                            "date": selectedDate,
                            "time_slot": selectedDateTime.toISOString(),
                            "patient_email": "{{ patient_email }}",
                        };
                        xhr.send(JSON.stringify(data));
                        slotButton.style.visibility = "hidden";
                    });

                    // add the button to the container
                    slotContainer.appendChild(slotButton);
                }
            } else {
                console.log('Request failed.  Returned status of ' + xhr.status);
            }
        };
        xhr.send();
    });
});