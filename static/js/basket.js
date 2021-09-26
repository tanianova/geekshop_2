window.onload = function () {
    $('.basket_list').on('click', 'input[type="number"]', function (evt) {
        let t_href = evt.target;
        $.ajax({
            url: "/baskets/edit/" + t_href.name + "/" + t_href.value + "/",
            success: function (data) {
                $('.basket_list').html(data.result);
            }
        });
        evt.preventDefault();
    });
}