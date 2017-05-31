function dupa() {


    alert('dupa');

    $("#start_game").submit(function (e) {
        alert('dupa');
        e.preventDefault();
        alert('dupa');
        var left_column = $("#left_column");
        left_column.show();

        var start_game_form = $("#start_game");
        start_game_form.hide();

        var play_again_button = $("#play_again");
        play_again_button.show();
    });

    $("#play_again").click(function () {

        var left_column = $("#left_column");
        left_column.hide();

        var start_game_form = $("#start_game");
        start_game_form.show();


        var play_again_button = $("#play_again");
        play_again_button.hide();
    });

}