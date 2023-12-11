$(document).ready(function(){
    $('#stockForm').submit(function(e){
        e.preventDefault();  // Prevent default form submission
        console.log('Form submitted'); // Debugging line

        $.ajax({
            url: '/get-stock-data',
            type: 'post',
            data: $('#stockForm').serialize(),
            success: function(data) {
                console.log('AJAX request succeeded'); // Debugging line
                $('#result').empty(); // Clear previous results
                if (data.plot_url) {
                    if (data.stats) {
                        $('#result').append(`<p>Mean: ${data.stats.mean}</p>
                                             <p>Max: ${data.stats.max}</p>
                                             <p>Min: ${data.stats.min}</p>`);
                        // Append other stats as needed
                    }
                    $('#result').append(`<img src="${data.plot_url}" alt="Stock Data"/>`);
                    
                } else {
                    $('#result').append(`<p>Error: ${data.error}</p>`);
                }
            },
            error: function() {
                console.log('AJAX request failed'); // Debugging line
                $('#result').html('<p>An error occurred while processing your request.</p>');
            }
        });
    });
});