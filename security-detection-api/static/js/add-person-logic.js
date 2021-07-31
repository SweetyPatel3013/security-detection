$(document).ready(function () {

    var swiper = new Swiper(".mySwiper", {
        slidesPerView: 3,
        centeredSlides: false,
        spaceBetween: 20,
        pagination: {
            el: ".swiper-pagination",
            type: "fraction",
        },
        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
        },
    });


    //var api_endpoint = "http://localhost:8888";
    //var api_endpoint = "https://security-detection-api.herokuapp.com";
    var api_endpoint = "";

    $("#video-div").hide();
    $("#take-photo-div").hide();
    $("#slider-div").hide();
    $("#instructions").hide();

    $("#start-webcam").click(function () {
        let name = $("#name-of-person").val();
        if (name === '' || name === null || name === undefined) {
            alert("Please enter a name before starting webcam!");
        } else {
            $.ajax({
                url: api_endpoint + '/persons',
                type: 'get',
                data: {name: name},
                success: function (data) {
                    if (data === 'FOUND') {
                        $("#name-of-person").attr('readonly', true);
                        $("#start-webcam").css("display", "none");
                        $("#take-photo-div").css("display", "block");
                        $("#video-div").css("display", "block");
                        $("#instructions").css("display", "block")
                        startup();
                    } else {
                        alert("Name Already exists");
                    }
                },
                error: function (error) {
                    alert("Error processing request: " + error.Message);
                }
            });
        }
    });

    var video_container = null;
    var canvas_container = null;
    var captured_image_counter = 0;
    var captured_images = [];

    var width = 640;
    var height = 480;

    function add_captured_image(img) {
        captured_images.push(img);
    }

    function clean_captured_images() {
        captured_images = [];
    }

    function startup() {

        canvas_container = document.getElementById("webcam-canvas");
        video_container = document.getElementById("webcam-video");
        navigator.mediaDevices.getUserMedia({'video': true})
            .then(stream => {
                video_container.srcObject = stream;
                video_container.play();
                $("#take-photo-button").css("display", "block");
            })
            .catch(error => {
                alert("Video Processing error", error);
            })
    }

    function take_photo() {
        $("#slider-div").css("display", "block");
        var context = canvas_container.getContext("2d");
        if (width && height) {
            canvas_container.width = width;
            canvas_container.height = height;

            context.drawImage(video_container, 0, 0, width, height);

            var data = canvas_container.toDataURL('image/png');
            var image_style = "top: " + 15 * captured_image_counter + "px;";
            image_style += " z-index: " + parseInt(captured_image_counter) + 1;
            var image_id = "captured-image-" + captured_image_counter;

            var attributes = {id: image_id, src: data, style: image_style, class: 'captured-image'};
            add_captured_image(attributes['src']);
//                $("#photo-div").append($("<img>", attributes));

            swiper.prependSlide(
                `<div class="swiper-slide"><img src="${data}" alt=""></div>`
            );
            captured_image_counter++;
            $("#submit-all-images-button").html("Submit <b>" + captured_image_counter + "</b> images");
        }
    }

    $("#take-photo-button").click(take_photo);

    $("#submit-all-images-button").click(function () {
        console.log("Photos : " + captured_image_counter)
        if (captured_image_counter === 0 || captured_images === undefined || captured_images.length == 0) {
            alert("You need to click some photos");
            clean_captured_images();
        } else {
            $("#spinner-div").css("display", "block");
            let images_to_be_sent = []
            let person_name = $("#name-of-person").val();
            images_to_be_sent = JSON.stringify(captured_images);
            $.ajax({
                url: api_endpoint + '/persons/photos',
                type: 'post',
                data: {
                    name: person_name,
                    images: images_to_be_sent
                },
                success: function (data) {
                    $("#spinner-div").css("display", "none");
                    clean_captured_images();
                    window.location.href = window.location.href + '/recognition';
                },
                error: function (err) {
                    alert(err.Message);
                    clean_captured_images();
                }
            });
        }
    });

    $("div#photo-div").on('click', 'img', function () {
        var id = $(this).attr('id');

        var image = document.getElementById(id);
        var modal = document.getElementById("image-modal-div");
        var modal_image = document.getElementById("image-modal-img");

        image.onclick = function () {
            modal.style.display = "block";
            modal_image.src = this.src;
            $("#delete-modal-image-button").data('id', id);
        }

        let span = document.getElementById("close-image-modal");

        span.onclick = function () {
            modal.style.display = "none";
        }
    });

    $("#delete-modal-image-button").click(function () {
        let delete_image_id = $(this).data('id');
        $("#" + delete_image_id).remove();

        var modal = document.getElementById("image-modal-div");
        modal.style.display = "none";

        var temp_counter = 0;
        $("#photo-div > img").each(function () {
            var id_element = "captured-image-" + temp_counter;
            $(this).removeAttr('style');
            $(this).css("top", 15 * temp_counter + "px");
            $(this).css("z-index", parseInt(temp_counter) + 1);
            $(this).attr('id', id_element);
            temp_counter += 1;
        });

        captured_image_counter = temp_counter;
        $("#submit-all-images-button").html("Submit <b>" + captured_image_counter + "</b> images");

    });

});
