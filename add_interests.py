import core.models.base as base
from core.models.interest import Interest


def main():
    interest_list = [
        "Technology",
        "Energy",
        "Financials",
        "Health",
        "Industrials",
        "Materials",
        "Communications",
        "Utilities",
        "Consumer"
    ]

    for interest in interest_list:
        interest = Interest(name=interest, image_url="/static/images/%s.png" % interest)
        base.managers.interest_manager.add_one(interest)

if __name__ == "__main__":
    main()
