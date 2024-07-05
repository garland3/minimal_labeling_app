$(document).ready(function() {
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    const image = document.getElementById('image');
    let isDrawing = false;
    let startX, startY;
    let boxes = [];
    let currentImageIndex = 0;

    image.onload = function() {
        canvas.width = image.width;
        canvas.height = image.height;
    }

    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);

    function startDrawing(e) {
        isDrawing = true;
        [startX, startY] = [e.offsetX, e.offsetY];
    }

    function draw(e) {
        if (!isDrawing) return;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawBoxes();
        ctx.strokeStyle = 'red';
        ctx.lineWidth = 2;
        ctx.strokeRect(startX, startY, e.offsetX - startX, e.offsetY - startY);
    }

    function stopDrawing(e) {
        if (!isDrawing) return;
        isDrawing = false;
        boxes.push({
            x: startX,
            y: startY,
            width: e.offsetX - startX,
            height: e.offsetY - startY
        });
        drawBoxes();
    }

    function drawBoxes() {
        boxes.forEach(box => {
            ctx.strokeStyle = 'red';
            ctx.lineWidth = 2;
            ctx.strokeRect(box.x, box.y, box.width, box.height);
        });
    }

    $('#submit').click(function() {
        $.ajax({
            url: '/submit_coordinates',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ coordinates: boxes, currentImageIndex: currentImageIndex }),
            success: function(response) {
                // alert('Coordinates submitted successfully');
                boxes = [];
                ctx.clearRect(0, 0, canvas.width, canvas.height);
            }
        });
    });

    $('#backward').click(function() {
        if (currentImageIndex > 0) {
            currentImageIndex--;
            updateImage();
        }
    });

    $('#forward').click(function() {
        currentImageIndex++;
        updateImage();
    });

    function updateImage() {
        $.ajax({
            url: `/get_image/${currentImageIndex}`,
            type: 'GET',
            success: function(response) {
                if (response.img_file_path) {
                    $('#image').attr('src', response.img_file_path);
                    boxes = [];
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                } else if (response.error) {
                    alert(response.error);
                    currentImageIndex--; // Revert the index change
                }
            }
        });
    }
});