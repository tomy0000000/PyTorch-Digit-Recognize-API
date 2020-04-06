let uploaded_counter = 1;

function insertResult(filename, canvas) {
    return new Promise((resolve, reject) => {
        $("<li>").attr("class", "media my-4").append(canvas.attr("class", "mr-3"), $("<div>").attr("class", "media-body").text("Context").prepend($("<h5>").attr({
            id: `result-${uploaded_counter}`,
            class: "mt-0 mb-1"
        }))).prependTo("ul");
        resolve(filename);
    });
}

function resizeImage(filename, canvas) {
    return new Promise((resolve, reject) => {
        let reader = new FileReader();
        reader.onload = (readerEvent) => {
            let image = new Image();
            image.onload = (imageEvent) => {
                // Resize the image
                let max_size = 28,
                    width = image.width,
                    height = image.height;
                if (width > height) {
                    if (width > max_size) {
                        height *= max_size / width;
                        width = max_size;
                    }
                } else {
                    if (height > max_size) {
                        width *= max_size / height;
                        height = max_size;
                    }
                }
                let canvas = document.getElementById(`uploaded-image-${uploaded_counter}`);
                canvas.width = width;
                canvas.height = height;
                canvas.getContext('2d').drawImage(image, 0, 0, width, height);
                canvas.toBlob(resolve, "image/jpeg");
            };
            image.src = readerEvent.target.result;
        };
        reader.readAsDataURL(filename); // convert to base64 string
    });
}

function queryAPI(img_blob) {
    console.log("query called");
    console.log(img_blob);
    let formData = new FormData();
    formData.append("image", img_blob);
    $.ajax({
        type: "POST",
        url: $("#main-form").data('api-endpoint'),
        data: formData,
        processData: false,
        contentType: false
    }).done((data) => {
        $(`#result-${uploaded_counter}`).text(`Is This ${data.result}?`);
        uploaded_counter += 1;
    }).fail((data) => {
        alert("Oops, somthing went wrong...");
        console.log(data);
        location.reload();
    });
}
$('#inputfile').bind('change', function() {
    let fileSize = this.files[0].size / 1024 / 1024; // this gives in MB
    if (fileSize > 1) {
        $("#inputfile").val(null);
        alert('file is too big. images more than 1MB are not allowed');
        return;
    }
    let filename = this.files[0];
    let canvas = $("<canvas>").attr("id", `uploaded-image-${uploaded_counter}`);
    insertResult(filename, canvas).then(resizeImage).then(queryAPI).then();
});
