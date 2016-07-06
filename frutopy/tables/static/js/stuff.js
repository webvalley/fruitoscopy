$(document).ready (function(){
            $("#success-alert").hide();
            $("#please").click(function showAlert() {
                $("#success-alert").alert();
                $("#success-alert").fadeTo(2000, 500).slideUp(500, function(){
               $("#success-alert").alert('close');
                });
            });
 });
