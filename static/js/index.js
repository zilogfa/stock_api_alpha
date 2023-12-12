$(document).ready(function(){
    $('#stockForm').submit(function(e){
        e.preventDefault();  // Prevent default form submission
        console.log('Form submitted'); 

        $.ajax({
            url: '/get-stock-data',
            type: 'post',
            data: $('#stockForm').serialize(),
            success: function(data) {
                console.log('AJAX request succeeded');
                $('#result').empty(); // clearing 
                
                if (data.plot_urls) { 
                    if (data.stats) {
                        //appending stats
                        $('#result').append(`  
                            <div class="static">
                                <p><span>Mean:</span> <span>${data.stats.mean}</span></p>
                                <p><span>Max:</span> <span>${data.stats.max}</span></p>
                                <p><span>Min:</span> <span>${data.stats.min}</span></p>
                                <p><span>std_dev:</span> <span>${data.stats.std_dev}</span></p>
                                <p><span>Latest:</span> <span>${data.stats.latest}</span></p>
                            <div>`);
                    }
                    //appending images
                    data.plot_urls.forEach(url => { 
                        $('#result').append(`<img src="${url}" alt="Stock Chart" style="margin-top: 20px;"/>`);
                    });
                    
                } else {
                    $('#result').append(`<p>Error: ${data.error}</p>`);
                }
            },
            //debuging
            error: function(xhr, status, errorThrown) {
                console.log('AJAX error status:', status); 
                console.log('Thrown Error:', errorThrown);
                console.log('Response:', xhr.responseText);
                $('#result').html(`<p>Error: ${xhr.responseText || 'Unknown error'}</p>`);
            }
        });
    });
});
