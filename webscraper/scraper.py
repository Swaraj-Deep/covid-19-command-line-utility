from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt

url = "https://www.mohfw.gov.in/"


def get_url() -> str:
    return url


def get_response(url) -> "response":
    return requests.get(url, timeout=10)


def return_content() -> "html":
    return BeautifulSoup(get_response(get_url()).content, "html.parser")


content = return_content()


def get_content() -> "html":
    return content


def get_helpline_numbers() -> "list":
    helpline_numbers = []
    content = get_content()
    for helpline in content.findAll('div', attrs={"class": "progress-block-area"}):
        number_text = helpline.find('p', attrs={"class": "mblock"}).get_text(
            strip=True, separator='|').split('|')
        for numbers in number_text:
            if numbers.find(":") != -1:
                helpline_numbers.append(numbers[numbers.find(":") + 1:])
            else:
                helpline_numbers.append(numbers)
    return helpline_numbers


def get_summary() -> "list":
    label_data = []
    summary_data = []
    summary_content = get_content()
    summary = summary_content.findAll(
        'div', attrs={"class": "information_block"})
    for data in summary:
        label_data = data.findAll('div', attrs={"class": "iblock_text"})
    for text in label_data:
        a = text.find('div')
        b = text.find('span')
        summary_data.append(a.get_text() + ': ' + b.get_text() + ', ')
    return summary_data


def get_state_wise_data() -> "list":
    p_content = get_content()
    state_list = []
    state_wise_data = p_content.findAll('div', attrs={"id": "cases"})
    for l_p in state_wise_data:
        para = l_p.find('p')
    state_list.append(para.get_text())
    for l_data in state_wise_data:
        table = l_data.find('table')
    title = []
    for l_title in table.find_all('th'):
        for l_title_ind in l_title:
            title.append(l_title_ind.get_text())
    state_list.append(title)
    state_data = []
    for l_row in table.find_all('tr')[:-1]:
        temp = []
        l_row_data = l_row.find_all('td')
        for l_ind_data in l_row_data:
            temp_data = ""
            if l_ind_data.get_text().endswith("#") or l_ind_data.get_text().endswith("*"):
                temp_data = l_ind_data.get_text()[:-1]
                temp.append(temp_data)
            else:
                temp.append(l_ind_data.get_text())
        if len(temp) != 0:
            state_data.append(temp)
    state_list.append(state_data)
    state_data_frame = pd.DataFrame(state_list[2])
    state_data_frame.columns = state_list[1]
    return_data = []
    return_data.append(state_list[0])
    return_data.append(state_data_frame)
    return return_data


if __name__ == '__main__':
    print("Welcome to covid-19 command line utility")
    print("Press 1: For getting helpline numbers")
    print("Press 2: For getting summary")
    print("Press 3: For getting state wise report")
    print("Press 4: For getting state wise report(graphical format)")
    print("Press 5: For a list of state wise Helpline numbers")
    print("Press 6: For Helpline number of a state")
    a = 0
    while(a != -1):
        a = int(input("Enter Your Choice: "))
        if a == 1:
            helpline_numbers = get_helpline_numbers()
            print("First Number: " + helpline_numbers[0])
            print("Second Number: " + helpline_numbers[1])
            print("All the numbers are Toll Free")
        if a == 2:
            m_summary_data = get_summary()
            m_summary = ' '.join(m_summary_data)
            print(m_summary)
        if a == 3 or a == 4:
            m_state_wise_data = get_state_wise_data()
            print(m_state_wise_data[0])
            m_state_data_frame = m_state_wise_data[1][:-1]
            states = list(m_state_data_frame['Name of State / UT'])
            plot_data = {}
            plot_data['Total Confirmed cases (Indian National)'] = list(
                pd.to_numeric(m_state_data_frame['Total Confirmed cases (Indian National)'], downcast="float"))
            plot_data['Total Confirmed cases (Foreign National)'] = list(
                pd.to_numeric(m_state_data_frame['Total Confirmed cases ( Foreign National )'], downcast="float"))
            plot_data['Cured / Discharged / Migrated'] = list(
                pd.to_numeric(m_state_data_frame['Cured/Discharged/Migrated'], downcast="float"))
            plot_data['Death'] = list(pd.to_numeric(
                m_state_data_frame['Death'], downcast="float"))
            plot_data_frame = pd.DataFrame(plot_data, index=states)
            if a == 4:
                ax = plot_data_frame.plot.bar(figsize=(20, 30), width=1)
                plt.show()
            else:
                new_title = ['Infected (Indian)',
                             'Infected (Foreigners)', 'Cured', 'Deaths']
                plot_data_frame.columns = new_title
                print(plot_data_frame)
        if a == 5:
            with open('statewise_helpline_number.txt') as f:
                read_data = f.read()
            print(read_data)
        if a == 6:
            state_name = input("Enter the state name: ")
            state_name.lower()
            f = open('statewise_helpline_number.txt')
            print('')
            flag = False
            for line in f:
                match = line.lower()
                if state_name in match:
                    print(line)
                    flag = True
            if flag == False:
                print("Sorry! We Cannot find any match with these keywords.\nTry again with other keyword")
            else:
                print("Above is the list of possible matches")
    print("Thanks for using our service.\nPlease Stay at Home until situation gets under control.")
