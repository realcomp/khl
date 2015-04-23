$(document).ready(function(){
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    var htmlString = "<div id=\"dropzone-container\"><div class=\"fileinput-label\">Перетащите файлы сюда<br><span>или</span></div><button class=\"fileinput-button\">Выберите файлы</button></div><div class=\"m-t-20\"><div class=\"ui teal progress\" id=\"progress-bar\" style=\"opacity: 0;\"><div id=\"progress\" class=\"bar\"></div></div></div><div class=\"table table-striped\" class=\"files m-t-20\" id=\"previews\"><div id=\"template\" class=\"file-row\"></div></div>";

    $(".filerFile").append(htmlString);

    $("button.fileinput-button").on("click", function(event) {
        event.preventDefault();
        return false;
    });

    var previewNode = document.querySelector("#template");
    if (previewNode) {
        previewNode.id = "";
        var previewTemplate = previewNode.parentNode.innerHTML;
        previewNode.parentNode.removeChild(previewNode);
        var myDropzone = new Dropzone("div#dropzone-container", { // Make the whole body a dropzone
            url: "/api/hockey/admin/fiu/", // Set the url
            uploadMultiple: false,
            createImageThumbnails: false,
            paramName: "file",
            method: "PUT",
            addRemoveLinks: false,
            enqueueForUpload: false,
            thumbnailWidth: 80,
            thumbnailHeight: 80,
            parallelUploads: 1,
            previewTemplate: previewTemplate,
            autoQueue: true, // Make sure the files aren't queued until manually added
            previewsContainer: "#previews", // Define the container to display the previews
            clickable: ".fileinput-button", // Define the element that should be used as click trigger to select files.
            sending: function(file, xhr, formData) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                var data = window.location.pathname.split('/hockeyapp/')[1].split('/');
                var model_name = data[0];
                var id = data[1];
                formData.append("model_name", model_name);
                formData.append("id", id);
            },
        });

        myDropzone.on("success", function(file, response, event) {
            $(".filerFile > span#id_photo_description_txt").html(response.name);
            $(".filerFile > a").attr("href", response.url);
            $(".filerFile > a#lookup_id_photo").attr("href", response.folder_url+"?_to_field=file_ptr");
            $(".filerFile > a > img#id_photo_thumbnail_img").attr("src", response.icon);
            $(".filerFile > a > img#id_photo_thumbnail_img").attr("alt", response.name);
            $(".filerFile > input#id_photo").val(response.pk);
        });

    };

    /*
    myDropzone.on("addedfile", function(file) {
        // Hookup the start button
        file.status = Dropzone.ADDED;
        // file.previewElement.querySelector(".start").onclick = function() { myDropzone.enqueueFile(file); };
    });

    // Update the total progress bar
    myDropzone.on("totaluploadprogress", function(progress) {
        document.querySelector("#progress-bar #progress").style.width = progress + '%';
    });

    myDropzone.on("sending", function(file) {
        // Show the total progress bar when upload starts
        document.querySelector("#progress-bar").style.opacity = "1";
        // And disable the start button
    });

    // Hide the total progress bar when nothing's uploading anymore
    myDropzone.on("queuecomplete", function(progress) {
        document.querySelector("#progress-bar").style.opacity = "0";
    });

    // Setup the buttons for all transfers
    // The "add files" button doesn't need to be setup because the config
    // `clickable` has already been specified.
    document.querySelector(".start").onclick = function() {
        myDropzone.enqueueFiles(myDropzone.getFilesWithStatus(Dropzone.ADDED));
    };
    document.querySelector(".cancel").onclick = function() {
        myDropzone.removeAllFiles(true);
    };
    */
});