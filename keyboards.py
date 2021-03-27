import json


def home_keyboard():
    return json.dumps(
        {"one_time_keyboard":True,"resize_keyboard": True, "keyboard":
            [
                [
                    {"text": "⛅ Узнать погоду 🌧", "data": "F"}
                ],
                [
                    {"text": "Создать цитату"}
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


