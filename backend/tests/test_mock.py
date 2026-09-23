from unittest.mock import Mock


def notify_maintenance(send_email, equipment_name):
    send_email(equipment_name)

    return "Notification completed"


def test_notify_maintenance():
    fake_email = Mock()

    result = notify_maintenance(fake_email, "MRI Machine")

    assert result == "Notification completed"
    fake_email.assert_called_once_with("MRI Machine")
def send_maintenance_alert(equipment_name, email_service):
    message = f"{equipment_name} requires maintenance"
    email_service(message)

    return message


def test_send_maintenance_alert():
    fake_email_service = Mock()

    result = send_maintenance_alert(
        "MRI Machine",
        fake_email_service
    )

    assert result == "MRI Machine requires maintenance"

    fake_email_service.assert_called_once_with(
        "MRI Machine requires maintenance"
    )