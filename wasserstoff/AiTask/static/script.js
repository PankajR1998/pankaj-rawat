$(document).ready(function() {
    $('#userInput').keypress(function(event) {
        // Check if the Enter key was pressed
        if (event.which === 13) {
            // Prevent the default action (form submission)
            event.preventDefault();
            // Trigger a click event on the send button
            $('#send-btn').click();
        }
    });

    $('#send-btn').on('click', function() {
        var userQuery = $('#userInput').val().trim();
        $('<div class="message"><strong>User: </strong>' + userQuery + '</div>').appendTo('.message-display');
        // $('.message-display').scrollTop($('.message-display')[0].scrollHeight);
            // Clear the input area
        $('#userInput').val('');
        
        if (userQuery) {
            $.ajax({
                url: '/send',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ 'user_input': userQuery }),
                success: function(response) {
                    $('#userInput').val('');

                    $('<p><strong>' + response.sender + ': </strong>' + response.content + '</p>').appendTo('.message-display');
                    $('.message-display').scrollTop($('.message-display')[0].scrollHeight);
                },
                error: function(err) {
                    console.error('Error fetching response:', err);
                }
            });

        }
    });


    // Attach click event handler to the send button
    // $('#send-btn').on('click', sendMessage);
});