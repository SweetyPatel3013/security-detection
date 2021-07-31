$(document).ready(function () {

        var video_container = null;
        var canvas_container = null;
        var video_prediction = null;

        //var api_endpoint = "http://localhost:8888";
        var api_endpoint = "https://security-detection-api.herokuapp.com";

        var width = 640;
        var height = 480;

        function startup() {
            video_prediction = document.getElementById("prediction-result-image");
            canvas_container = document.getElementById("webcam-canvas");
            video_container = document.getElementById("prediction-video-stream");
            navigator.mediaDevices.getUserMedia({'video': true})
                .then(stream => {
                    video_container.srcObject = stream;
                    video_container.play();
                    predict_each_frame();
                })
                .catch(error => {
                    console.log("Video Processing error", error);
                })
        }

        function get_image_data_url() {
            var context = canvas_container.getContext('2d');
            var data = ''
            if (width && height) {
                canvas_container.width = width;
                canvas_container.height = height;
                context.drawImage(video_container, 0, 0, width, height);
                data = canvas_container.toDataURL('image/png');
            }
            return data;
        }

        function predict_each_frame() {
            let image_a = get_image_data_url();
            setTimeout(() => {}, 1500);
            let image_b = get_image_data_url();
            if (image_a !== '') {
                $.ajax({
                    url: api_endpoint + '/movements',
                    type: 'post',
                    data: {
                        image_a: image_a,
                        image_b: image_b
                    },
                    success: function (data) {
                        predict_each_frame();
                        data = "data:image/png;base64," + data;
                        video_prediction.setAttribute('src', data);
                    },
                    error: function (data) {
                        alert("there is some error");
                    }
                });
            }
        }

        startup();

    });
