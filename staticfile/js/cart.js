function plusCart(event) {
    event.preventDefault();
    var cartId = $(event.currentTarget).attr('href');

    // Создаем AJAX-запрос
    $.ajax({
        type: 'GET',
        url: cartId,
        success: function (response) {
            // Обновляем содержимое корзины или другие необходимые действия
            // Например, обновление количества и общей стоимости
            var cartQuantity = $(event.currentTarget).siblings('input');
            var cartTotalPrice = $(event.currentTarget).closest('td').next('td').find('p');

            cartQuantity.val(response.quantity); // Обновляем значение количества
            cartTotalPrice.text('$' + response.total_price); // Обновляем значение общей стоимости
        },
        error: function (error) {
            console.log(error);
        }
    });
}

function minusCart(event) {
    event.preventDefault();
    var cartId = $(event.currentTarget).attr('href');

    // Создаем AJAX-запрос
    $.ajax({
        type: 'GET',
        url: cartId,
        success: function (response) {
            // Обновляем содержимое корзины или другие необходимые действия
            // Например, обновление количества и общей стоимости
            var cartQuantity = $(event.currentTarget).siblings('input');
            var cartTotalPrice = $(event.currentTarget).closest('td').next('td').find('p');

            cartQuantity.val(response.quantity); // Обновляем значение количества
            cartTotalPrice.text('$' + response.total_price); // Обновляем значение общей стоимости
        },
        error: function (error) {
            console.log(error);
        }
    });
}
