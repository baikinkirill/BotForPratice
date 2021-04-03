import json


def home_keyboard():
    return json.dumps(
        {"one_time_keyboard": True, "resize_keyboard": True, "keyboard":
            [
                [
                    {"text": "⛅ Узнать погоду 🌧", "data": "F"}
                ],
                [
                    {"text": "✍ Создать цитату 💬"}
                ],
                [
                    {"text": "🔢 КаЛьКуЛяТоР 🔢"}
                ],

            ]
         }
    )


def cancel():
    return json.dumps(
        {
            "inline_keyboard": [
                [
                    {"text": "Отмена", "callback_data": "cancel"},
                ]
            ]
        }
    )





def calc():
    return json.dumps(
        {
            "inline_keyboard": [
                [
                    {"text": "1", "callback_data": "c1"}, {"text": "2", "callback_data": "c2"},
                    {"text": "3", "callback_data": "c3"},{"text": "+", "callback_data": "c+"}
                ],
                [
                    {"text": "4", "callback_data": "c4"}, {"text": "5", "callback_data": "c5"},
                    {"text": "6", "callback_data": "c6"}, {"text": "-", "callback_data": "c-"}
                ],
                [
                    {"text": "7", "callback_data": "c7"}, {"text": "8", "callback_data": "c8"},
                    {"text": "9", "callback_data": "c9"}, {"text": "*", "callback_data": "c*"}
                ],
                [
                    {"text": "Ce", "callback_data": "cC"}, {"text": "0", "callback_data": "c0"},
                    {"text": "=", "callback_data": "c="}, {"text": "/", "callback_data": "c/"}
                ],
                [
                    {"text": "(", "callback_data": "c("}, {"text": ")", "callback_data": "c)"},
                ],

            ]
        }
    )
