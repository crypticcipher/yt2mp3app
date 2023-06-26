       // Create cookie
       function setCookie(cname, cvalue, exdays) {
        const d = new Date();
        d.setTime(d.getTime() + (exdays*24*60*60*1000));
        let expires = "expires="+ d.toUTCString();
        document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    }
    
    // Delete cookie
    function deleteCookie(cname) {
        const d = new Date();
        d.setTime(d.getTime() + (24*60*60*1000));
        let expires = "expires="+ d.toUTCString();
        document.cookie = cname + "=;" + expires + ";path=/";
    }
    
    // Read cookie
    function getCookie(cname) {
        let name = cname + "=";
        let decodedCookie = decodeURIComponent(document.cookie);
        let ca = decodedCookie.split(';');
        for(let i = 0; i <ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) == ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) == 0) {
                return c.substring(name.length, c.length);
            }
        }
        return "";
    }
    
    // Set cookie consent
    function acceptCookieConsent(){
        deleteCookie('user_cookie_consent');
        setCookie('user_cookie_consent', 1, 30);
        document.getElementById("cookieNotice").style.display = "none";
    }
    
    let cookie_consent = getCookie("user_cookie_consent");
    if(cookie_consent != ""){
        document.getElementById("cookieNotice").style.display = "none";
    }else{
        document.getElementById("cookieNotice").style.display = "block";
    }


 
    //     document.getElementById('downloadForm').addEventListener('submit', function(){
    //     // Clear form inputs after 100ms. The delay is to allow form submission before clearing.
    //     setTimeout(function(){
    //         document.getElementById('downloadForm').reset();
    //     }, 100);
    // });


    toastr.options = {
        "closeButton": true,
        "debug": false,
        "newestOnTop": false,
        "progressBar": true,
        "positionClass": "toast-top-right",
        "preventDuplicates": false,
        "onclick": null,
        "showDuration": "300",
        "hideDuration": "1000",
        "timeOut": "10000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
      }

      $(document).ready(function() {
        $('#downloadVideoButton').click(function(e) {
            e.preventDefault();
            toastr.success('Video download has started. Please be patient, it might take a few moments. Thank you!');
            
            // Reset the form
            setTimeout(function(){
                $('#downloadForm').trigger('reset');
            }, 100);
    
            // Submit the form
            $('#downloadForm').attr('action', '/downloadvid').submit();
        });
    
        $('#downloadMp3Button').click(function(e) {
            e.preventDefault();
            toastr.success('MP3 download has started. Please be patient, it might take a few moments. Thank you!');
            
            // Reset the form
            setTimeout(function(){
                $('#downloadForm').trigger('reset');
            }, 100);
    
            // Submit the form
            $('#downloadForm').attr('action', '/download').submit();
        });
    });