from utils.time import Time
import utils.email as email
import core.models.base as base


def print_table(data, row_length):
    content = '<table>'
    counter = 0
    for element in data:
        if counter % row_length == 0:
            content += '<tr>'
        content += '<td>%s</td>' % element
        counter += 1
        if counter % row_length == 0:
            content += '</tr>'
    if counter % row_length != 0:
        for i in range(0, row_length - counter % row_length):
            content += '<td>&nbsp;</td>'
        content += '</tr>'
    content += '</table>'

    return content


def main():
    '''This Job runs every day at noon and should give the list of stocks announcing the next day'''
    subject = 'Your Companies Earnings Announcements Tomorrow'

    # 0. get current day
    day = Time.get_time_for_delta('days', 1)
    day = Time.time_to_str_time(day)

    # 1. Get all the list of users
    users = base.managers.user_manager.get_many()

    # 2. for each user, get the list of stocks they are following
    for user in users:
        announcing_stocks = []
        stocks = user.get_stocks_for_user()

        # 3. for each stock, check if the announcement date matches the day
        for stock in stocks:
            announcement_date = stock.get('time')

            if not announcement_date:
                continue

            announcement_date = Time.time_to_str_time(announcement_date)

            if announcement_date == day:
                announcing_stocks.append(stock.get('ticker'))

        # 4. list is not empty, send user a notification email
        if len(announcing_stocks) > 0:
            print "-->user, date, stocks: %s:%s:%s" % (user.get('email'), day, announcing_stocks)
            html_content = print_table(announcing_stocks, 3)
            email.send_email(user.get('email'), None, subject, '', html_content)

if __name__ == "__main__":
    main()
