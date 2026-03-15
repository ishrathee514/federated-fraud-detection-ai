POLICIES = {

    "no_raw_data_transfer": True,

    "model_update_signed": True,

    "audit_log_required": True

}


def check_policy(event):

    if event == "raw_data_shared" and POLICIES["no_raw_data_transfer"]:
        return False

    if event == "model_update" and not POLICIES["model_update_signed"]:
        return False

    return True


if __name__ == "__main__":

    events = [
        "transaction_processed",
        "model_update",
        "raw_data_shared"
    ]

    for e in events:

        result = check_policy(e)

        print(f"{e} → Allowed: {result}")