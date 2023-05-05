$(document).ready(function () {
    // Initialize the chat log with a welcome message
    $('#chat-log').append('<div><p class="bot">Hello! How can I assist you today?</p></div>');

    // Listen for form submission
    $('#chat-form').submit(function (event) {
        event.preventDefault();

        // Get the user's input
        var userInput = $('#chat-input').val();

        // Add the user's message to the chat log
        $('#chat-log').append('<div class= "message" ><p class="user">' + userInput + '</p></div>');
        $.ajax({
            url: '/chatbot/',
            type: 'POST',
            data: {
                'user_input': userInput,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            dataType: 'json',
            success: function (response) {  
                response.bot_response = response.bot_response.replace(/(?:\r\n|\r|\n)/g, '<br>');
                // Add the bot's response to the chat log
                if (response.link) {
                    // If the response includes a link, redirect to the link automatically
                    botResponse = '<p class="bot">' + response.bot_response + '</p></div>';
                    setTimeout(function () {
                        window.location.href = response.link;
                    }, 2000);
                } else {
                    // Otherwise, display the bot response as usual
                    botResponse = '<p class="bot">' + response.bot_response + '</p></div>';
                }
                $('#chat-log').append(botResponse);
                // Clear the input field
                $('#chat-input').val('');
            }
        });
    });
});